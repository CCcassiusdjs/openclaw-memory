/*
 * hyperbolic.h - Core structures for Hyperbolic File Explorer
 * 
 * Based on H3 algorithm by Tamara Munzner (Stanford, 1998)
 * Uses Klein model for fast matrix transformations
 */

#ifndef HYPERBOLIC_H
#define HYPERBOLIC_H

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <math.h>
#include <pthread.h>

/* ============================================================================
 * Constants
 * ============================================================================ */

#define H3_PI       3.14159265358979323846
#define H3_E        2.71828182845904523536
#define H3_EPSILON  1e-10

// File system
#define H3_MAX_PATH       4096
#define H3_MAX_NAME       256
#define H3_INITIAL_CAPACITY 65536

// Rendering
#define H3_FRAME_BUDGET_US   50000   // 50ms = 20 FPS
#define H3_MAX_VISIBLE       100000  // Max nodes to draw per frame
#define H3_NEAR_PLANE        0.001
#define H3_FAR_PLANE         100.0

// Colors
#define H3_COLOR_DIR         0.3f, 0.5f, 1.0f, 1.0f
#define H3_COLOR_FILE        0.8f, 0.8f, 0.8f, 1.0f
#define H3_COLOR_SYMLINK     0.5f, 0.8f, 0.3f, 1.0f
#define H3_COLOR_HIDDEN      0.5f, 0.5f, 0.5f, 1.0f

/* ============================================================================
 * Hyperbolic Math - Minkowski Space (Klein Model)
 * ============================================================================ */

// Points in 3D hyperbolic space (Klein model)
// All points lie within the unit ball: x² + y² + z² < 1
// We use homogeneous coordinates (w=1) for projective transformations
typedef struct {
    double x, y, z, w;  // w is homogeneous coordinate (usually 1.0)
} H3Point;

// 4x4 transformation matrix for hyperbolic transformations
// These are Lorentz boosts + rotations
typedef struct {
    double m[4][4];
} H3Transform;

// Minkowski inner product for hyperbolic geometry
// Signature (-+++) for the Klein model
// <u,v> = -u0*v0 + u1*v1 + u2*v2 + u3*v3
static inline double h3_minkowski_dot(const H3Point *u, const H3Point *v) {
    return -u->w * v->w + u->x * v->x + u->y * v->y + u->z * v->z;
}

// Distance in hyperbolic space
static inline double h3_distance(const H3Point *p1, const H3Point *p2) {
    double dot = h3_minkowski_dot(p1, p2);
    // Clamp for numerical stability
    if (dot >= -1.0) return 0.0;
    return acosh(-dot);
}

// Normalize to unit ball (Klein model constraint)
static inline void h3_normalize(H3Point *p) {
    double len = sqrt(p->x * p->x + p->y * p->y + p->z * p->z);
    if (len > 0.9999) {
        p->x /= len * 1.001;
        p->y /= len * 1.001;
        p->z /= len * 1.001;
    }
    p->w = 1.0;
}

// Sphere surface area in hyperbolic space
// A = 2π(cosh(r) - 1)
static inline double h3_sphere_area(double radius) {
    return 2.0 * H3_PI * (cosh(radius) - 1.0);
}

// Radius from sphere area
// r = acosh(A/(2π) + 1)
static inline double h3_radius_from_area(double area) {
    return acosh(area / (2.0 * H3_PI) + 1.0);
}

// Hyperbolic trigonometric functions
static inline double h3_sinh(double x) { return sinh(x); }
static inline double h3_cosh(double x) { return cosh(x); }
static inline double h3_tanh(double x) { return tanh(x); }

/* ============================================================================
 * File System Tree
 * ============================================================================ */

// Node types
typedef enum {
    H3_NODE_FILE = 0,
    H3_NODE_DIR = 1,
    H3_NODE_SYMLINK = 2,
    H3_NODE_SPECIAL = 3  // Devices, pipes, sockets
} H3NodeType;

// Node in the file tree
typedef struct H3Node {
    // Identification
    uint64_t id;
    uint64_t hash;          // Hash of path for quick lookup
    
    // Path info
    char *path;              // Full path
    char *name;              // File/dir name
    uint32_t name_len;
    uint32_t depth;          // Depth in tree
    
    // Hierarchy
    struct H3Node *parent;
    struct H3Node **children;
    uint32_t child_count;
    uint32_t child_capacity;
    
    // File info
    uint64_t size;           // File size (bytes)
    uint64_t mtime;          // Modification time (unix timestamp)
    uint64_t atime;           // Access time
    uint32_t mode;           // File permissions
    H3NodeType type;
    
    // H3 Layout state
    H3Point position;        // Position in hyperbolic space
    double hemisphere_radius; // Radius needed for children
    double angular_position; // Position on parent's hemisphere
    uint32_t band_index;     // Which concentric band
    uint32_t band_position;  // Position within band
    uint64_t descendant_count; // Total descendants
    
    // Rendering state
    float color[4];          // RGBA color
    float projected_size;    // Size on screen
    float screen_x, screen_y; // Projected coordinates
    bool visible;            // Currently visible?
    bool selected;           // User selected?
    bool highlighted;        // Hover/highlight state?
    
    // Statistics
    uint32_t file_count;     // Number of files in subtree
    uint32_t dir_count;      // Number of dirs in subtree
    uint64_t total_size;     // Total size of subtree
    
} H3Node;

// The entire file system tree
typedef struct {
    H3Node *root;
    H3Node **nodes;          // Flat array for fast iteration
    uint64_t *id_to_index;   // Hash map: id -> index
    uint64_t node_count;
    uint64_t node_capacity;
    uint64_t next_id;
    
    // View state
    H3Point focus;           // Current focus point
    H3Point target_focus;    // Target for smooth animation
    H3Transform view;        // Current view transform
    float zoom;
    float target_zoom;
    
    // Statistics
    uint64_t total_files;
    uint64_t total_dirs;
    uint64_t total_size;
    uint32_t max_depth;
    
    // Threading
    pthread_mutex_t lock;
    
} H3Tree;

/* ============================================================================
 * Rendering Context
 * ============================================================================ */

typedef struct {
    // Frame rate control
    uint64_t frame_start_us;
    uint64_t frame_budget_us;
    uint64_t frame_time_us;
    
    // View parameters
    H3Point center;
    double scale;
    float fov;
    
    // Culling
    double near_plane;
    double far_plane;
    
    // Statistics
    uint64_t nodes_drawn;
    uint64_t nodes_visible;
    uint64_t nodes_culled;
    float fps;
    
} H3RenderContext;

/* ============================================================================
 * Events and Updates
 * ============================================================================ */

// Event types from FS monitor
typedef enum {
    H3_EVENT_CREATE = 0,
    H3_EVENT_DELETE = 1,
    H3_EVENT_MODIFY = 2,
    H3_EVENT_MOVE = 3,
    H3_EVENT_ATTR_CHANGE = 4
} H3EventType;

// Event from file system monitor
typedef struct {
    uint64_t timestamp;
    char *path;
    char *old_path;          // For move events
    H3EventType type;
    uint64_t size;
    uint32_t mode;
    uint32_t flags;
} H3Event;

// Event queue (thread-safe)
typedef struct {
    H3Event *events;
    uint64_t capacity;
    uint64_t head;
    uint64_t tail;
    pthread_mutex_t lock;
    pthread_cond_t cond;
} H3EventQueue;

/* ============================================================================
 * Database Interface
 * ============================================================================ */

typedef struct sqlite3 sqlite3;
typedef struct sqlite3_stmt sqlite3_stmt;

typedef struct {
    sqlite3 *db;
    sqlite3_stmt *stmt_insert_event;
    sqlite3_stmt *stmt_get_events;
    sqlite3_stmt *stmt_get_baseline;
    sqlite3_stmt *stmt_get_stats;
    char *db_path;
} H3Database;

/* ============================================================================
 * User Interaction
 * ============================================================================ */

typedef struct {
    double mouse_x, mouse_y;
    double last_mouse_x, last_mouse_y;
    int mouse_buttons;        // Bitmask of pressed buttons
    int mouse_modifiers;      // Shift, Ctrl, etc.
    
    // Keyboard state
    int keys[512];            // Current key state (GLFW key codes go up to ~350)
    int keys_pressed[512];    // Key press events this frame
    int keys_released[512];   // Key release events this frame
    
    // Navigation state
    H3Point focus_target;     // Where we're navigating to
    double navigation_speed;
    bool auto_rotate;
    double rotation_angle;
    
    // Selection
    H3Node *hovered_node;
    H3Node *selected_node;
    H3Node *path[64];         // Path from root to selected node
    uint32_t path_len;
    
} H3InputState;

/* ============================================================================
 * Configuration
 * ============================================================================ */

typedef struct {
    // Layout
    double base_node_size;
    double size_scale_factor;
    double depth_scale_factor;
    bool use_file_size_for_size;
    
    // Rendering
    uint32_t target_fps;
    uint32_t max_visible_nodes;
    float node_size_min;
    float node_size_max;
    bool draw_edges;
    bool draw_labels;
    bool use_point_sprites;
    
    // Colors
    float color_dir[4];
    float color_file[4];
    float color_symlink[4];
    float color_hidden[4];
    float color_selected[4];
    float color_highlighted[4];
    
    // Navigation
    double pan_speed;
    double zoom_speed;
    double rotation_speed;
    bool invert_y_axis;
    
    // File system
    char *root_path;
    char **exclude_patterns;
    uint32_t exclude_count;
    uint32_t max_depth;
    uint64_t max_files;
    
    // Database
    char *db_path;
    uint32_t poll_interval_ms;
    
} H3Config;

/* ============================================================================
 * API Functions
 * ============================================================================ */

// h3_tree.c - Tree management
H3Tree *h3_tree_create(void);
void h3_tree_destroy(H3Tree *tree);
int h3_tree_add_node(H3Tree *tree, H3Node *node);
H3Node *h3_tree_find_node(H3Tree *tree, const char *path);
H3Node *h3_tree_find_by_id(H3Tree *tree, uint64_t id);
void h3_tree_remove_node(H3Tree *tree, H3Node *node);

// h3_layout.c - H3 Layout algorithm
void h3_layout_compute_radii(H3Node *node);
void h3_layout_pack_children(H3Node *parent);
void h3_layout_position_children(H3Node *node, H3Point parent_pos);
void h3_layout_tree(H3Tree *tree);
void h3_layout_update(H3Tree *tree, H3Node *changed_node);
void h3_layout_assign_colors(H3Tree *tree);

// h3_transform.c - Hyperbolic transformations
H3Transform h3_transform_identity(void);
H3Transform h3_transform_translation(H3Point *direction, double distance);
H3Transform h3_transform_rotation(double rx, double ry, double rz);
H3Transform h3_transform_compose(H3Transform *a, H3Transform *b);
H3Point h3_transform_apply(H3Transform *t, H3Point *p);

// Klein model <-> Poincaré model conversions
H3Point h3_klein_to_poincare(H3Point *k);
H3Point h3_poincare_to_klein(H3Point *p);

// h3_render.c - OpenGL rendering
int h3_render_init(void);
void h3_render_cleanup(void);
void h3_render_begin(H3RenderContext *ctx);
void h3_render_tree(H3Tree *tree, H3RenderContext *ctx);
void h3_render_end(H3RenderContext *ctx);
void h3_render_node(H3Node *node, H3RenderContext *ctx);
void h3_render_edges(H3Tree *tree, H3Node *from, H3Node *to, H3RenderContext *ctx);

// h3_input.c - User interaction
void h3_input_init(H3InputState *input);
void h3_input_update(H3InputState *input, H3Tree *tree, H3RenderContext *ctx);
void h3_input_mouse_move(H3InputState *input, double x, double y);
void h3_input_mouse_button(H3InputState *input, int button, int action);
void h3_input_key(H3InputState *input, int key, int action);
H3Node *h3_input_pick_node(H3InputState *input, H3Tree *tree, double x, double y);

// h3_scanner.c - File system scanning
int h3_scan_filesystem(const char *root_path, H3Tree *tree, H3Config *config);
void h3_scan_directory(H3Node *parent, H3Tree *tree, H3Config *config);
H3Node *h3_create_node(const char *path, H3Node *parent);
void h3_update_node_stats(H3Node *node);

// h3_monitor.c - Real-time updates
int h3_monitor_start(H3Tree *tree, H3Config *config);
void h3_monitor_stop(void);
int h3_monitor_poll(H3EventQueue *queue, uint32_t timeout_ms);
int h3_apply_event(H3Tree *tree, H3Event *event);

// h3_database.c - Persistence
int h3_database_open(H3Database *db, const char *path);
void h3_database_close(H3Database *db);
int h3_database_insert_event(H3Database *db, H3Event *event);
int h3_database_get_events(H3Database *db, uint64_t since, H3Event **events, uint64_t *count);
int h3_database_get_baseline(H3Database *db, const char *path, H3Node *node);

// h3_config.c - Configuration
int h3_config_load(H3Config *config, const char *path);
int h3_config_save(H3Config *config, const char *path);
void h3_config_defaults(H3Config *config);

// main.c - Utility functions
uint64_t get_time_us(void);
void log_info(const char *fmt, ...);
void log_error(const char *fmt, ...);
void log_debug(const char *fmt, ...);

/* ============================================================================
 * Inline Utility Functions
 * ============================================================================ */

// Hash function for paths
static inline uint64_t h3_hash_path(const char *path) {
    uint64_t hash = 5381;
    int c;
    while ((c = *path++)) {
        hash = ((hash << 5) + hash) + c;
    }
    return hash;
}

// Compare nodes by descendant count (for sorting)
static inline int h3_compare_descendants(const void *a, const void *b) {
    H3Node *na = *(H3Node**)a;
    H3Node *nb = *(H3Node**)b;
    return (int)(nb->descendant_count - na->descendant_count);
}

// Check if point is inside unit ball
static inline bool h3_inside_unit_ball(const H3Point *p) {
    double len2 = p->x * p->x + p->y * p->y + p->z * p->z;
    return len2 < 1.0;
}

// Linear interpolation
static inline double h3_lerp(double a, double b, double t) {
    return a + (b - a) * t;
}

// Clamp value
static inline double h3_clamp(double x, double min, double max) {
    if (x < min) return min;
    if (x > max) return max;
    return x;
}

#endif // HYPERBOLIC_H