# HypEx - Hyperbolic File Explorer

Explorador de arquivos de próxima geração usando árvore 3D hiperbólica.

## Por Que Hiperbólico?

### O Problema
- **3.2M arquivos, 365K diretórios**
- Árvores tradicionais sofrem de **clutter exponencial**
- Binary tree: nível n tem 2^n nós
- File systems têm branching factor muito maior

### A Solução: Espaço Hiperbólico

| Propriedade | Euclidiano | Hiperbólico |
|-------------|------------|-------------|
| Área do círculo | πr² | 2π(cosh(r)-1) ≈ πe^r |
| Crescimento | Polinomial | Exponencial |
| Espaço para filhos | Limitado | Quase infinito |

**Insight crítico:** Em espaço hiperbólico, cada nó filho tem quase tanto espaço quanto o pai para seus próprios filhos. Isso resolve o problema do clutter exponencial.

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    HYPERBOLIC FILE EXPLORER                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   FS Monitor │    │   H3 Layout  │    │  OpenGL     │     │
│  │   (daemon)   │───▶│   Algorithm  │───▶│  Renderer   │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│         │                   │                   │           │
│         ▼                   ▼                   ▼           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   SQLite    │    │   Klein     │    │   Shaders   │     │
│  │   Database  │    │   Model     │    │   GLSL      │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│         │                   │                   │           │
│         ▼                   ▼                   ▼           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Event     │    │   Hyperbolic│    │   User      │     │
│  │   Queue     │    │   Transform  │    │   Interaction│     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Componentes Principais

### 1. FS Monitor (Existente)
- `fs-monitor-daemon.py` - Monitoramento em tempo real
- `fs-monitor.db` - SQLite com todos os eventos
- Já implementado ✅

### 2. H3 Layout Algorithm (Novo)
Baseado no trabalho de Tamara Munzner (Stanford, 1998)

#### Passos do Layout:
1. **Bottom-up pass**: Calcular raio de cada hemisphere para acomodar filhos
2. **Top-down pass**: Posicionar cada filho na superfície do hemisphere pai
3. **Circle packing**: Filhos em bandas concêntricas ao redor do polo

#### Fórmulas:
- Hemispherical layout: nós em superfície 2D (hemisphere)
- Não volume 3D (evita oclusão)
- Área do hemisphere: A = 2π(cosh(r) - 1)

### 3. Klein Model (Escolha)
Por que Klein e não Poincaré?

| Modelo | Vantagem | Desvantagem |
|--------|----------|-------------|
| **Poincaré** | Geodésicas são arcos | Transformações complexas |
| **Klein** | Geodésicas são retas | Ângulos distorcidos |
| **Escolha** | **Matrizes 4x4 padrão** | Distortion aceitável |

**Klein model** permite usar matrizes de transformação padrão do OpenGL.

### 4. Adaptive Drawing
Garantir frame rate interativo:
- Só desenhar nós visíveis (projetam > 1 pixel)
- Pool de candidatos baseado em estrutura do grafo
- Frame rate target: 20 FPS mínimo

## Estruturas de Dados (C)

```c
// hyperbolic.h - Core structures

#ifndef HYPERBOLIC_H
#define HYPERBOLIC_H

#include <stdint.h>
#include <math.h>
#include <stdbool.h>

// Hyperbolic space uses Minkowski metric
// Points in Klein model are inside unit ball

typedef struct {
    double x, y, z, w;  // Homogeneous coordinates
} H4Point;

typedef struct {
    double m[4][4];  // Transformation matrix
} H4Transform;

// Node in the file tree
typedef struct FSNode {
    uint64_t id;
    char *path;
    char *name;
    uint64_t parent_id;
    uint64_t *children_ids;
    uint32_t child_count;
    uint32_t child_capacity;
    
    // File info
    uint64_t size;
    uint64_t mtime;
    uint8_t type;  // file, dir, symlink
    
    // Layout state
    H4Point position;      // Position in hyperbolic space
    double hemisphere_radius;  // Radius needed for children
    double angular_position;   // Position on parent's hemisphere
    uint32_t descendant_count; // Total descendants
    
    // Rendering state
    float color[4];
    float projected_size;
    bool visible;
    uint8_t depth;
    
    struct FSNode *parent;
    struct FSNode **children;
} FSNode;

// The entire tree
typedef struct {
    FSNode *root;
    FSNode **nodes;          // Flat array for iteration
    uint64_t *id_to_index;   // Hash map: id -> index
    uint64_t node_count;
    uint64_t node_capacity;
    
    // View state
    H4Point focus;          // Current focus point
    H4Transform view;       // Current view transform
    float zoom;
    
    // Stats
    uint64_t total_files;
    uint64_t total_dirs;
    uint64_t total_size;
} FSTree;

// Circle packing state
typedef struct {
    double *band_radii;      // Radius of each band
    uint32_t *band_counts;   // Nodes in each band
    uint32_t band_count;
} CirclePacking;

// Rendering context
typedef struct {
    // Frame rate control
    uint64_t frame_start;
    uint64_t frame_budget;   // Microseconds for 20 FPS
    uint64_t nodes_drawn;
    
    // View parameters
    H4Point center;
    double scale;
    
    // Culling
    double near_plane;
    double far_plane;
    
    // Statistics
    uint64_t total_visible;
    uint64_t total_drawn;
} RenderContext;

// Event from FS monitor
typedef struct {
    uint64_t timestamp;
    char *path;
    uint8_t event_type;  // CREATE, DELETE, MODIFY, etc.
    uint64_t size;
} FSEvent;

// Database connection
typedef struct {
    sqlite3 *db;
    sqlite3_stmt *stmt_events;
    sqlite3_stmt *stmt_baseline;
    sqlite3_stmt *stmt_stats;
} FSDatabase;

#endif // HYPERBOLIC_H
```

## Algoritmos Principais

### H3 Layout (h3_layout.c)

```c
#include "hyperbolic.h"
#include <math.h>
#include <string.h>

// Hyperbolic math constants
#define H3_PI 3.14159265358979323846
#define H3_E  2.71828182845904523536

// sinh and cosh for hemisphere area
static double h3_sinh(double x) { return sinh(x); }
static double h3_cosh(double x) { return cosh(x); }

// Hemisphere surface area: A = 2π(cosh(r) - 1)
static double hemisphere_area(double radius) {
    return 2.0 * H3_PI * (h3_cosh(radius) - 1.0);
}

// Inverse: radius from area
static double radius_from_area(double area) {
    // Solve: area = 2π(cosh(r) - 1)
    // cosh(r) = area/(2π) + 1
    // r = acosh(area/(2π) + 1)
    return acosh(area / (2.0 * H3_PI) + 1.0);
}

// Bottom-up pass: compute hemisphere radii
void h3_compute_radii(FSNode *node) {
    if (node->child_count == 0) {
        // Leaf node: minimal hemisphere
        node->hemisphere_radius = 0.1;  // Base unit
        node->descendant_count = 0;
        return;
    }
    
    // Recursively compute children first
    uint64_t total_descendants = 0;
    for (uint32_t i = 0; i < node->child_count; i++) {
        h3_compute_radii(node->children[i]);
        total_descendants += node->children[i]->descendant_count + 1;
    }
    node->descendant_count = total_descendants;
    
    // Compute total area needed
    double total_area = 0.0;
    for (uint32_t i = 0; i < node->child_count; i++) {
        double child_area = hemisphere_area(node->children[i]->hemisphere_radius);
        total_area += child_area;
    }
    
    // Radius that can contain all children
    node->hemisphere_radius = radius_from_area(total_area);
}

// Circle packing: arrange children on hemisphere
void h3_pack_children(FSNode *parent) {
    if (parent->child_count == 0) return;
    
    // Sort children by descendant count (largest first)
    // This puts complex subtrees near the pole
    for (uint32_t i = 0; i < parent->child_count - 1; i++) {
        for (uint32_t j = i + 1; j < parent->child_count; j++) {
            if (parent->children[j]->descendant_count > 
                parent->children[i]->descendant_count) {
                FSNode *tmp = parent->children[i];
                parent->children[i] = parent->children[j];
                parent->children[j] = tmp;
            }
        }
    }
    
    // Arrange in concentric bands around the pole
    double current_radius = 0.0;
    uint32_t band_index = 0;
    uint32_t nodes_in_band = 0;
    uint32_t band_start = 0;
    
    for (uint32_t i = 0; i < parent->child_count; i++) {
        FSNode *child = parent->children[i];
        double child_radius = child->hemisphere_radius;
        
        // Check if fits in current band
        if (current_radius + child_radius > parent->hemisphere_radius) {
            // Start new band
            band_start = i;
            nodes_in_band = 1;
            current_radius = child_radius;
        } else {
            nodes_in_band++;
        }
        
        // Angular position on band
        double angle = (2.0 * H3_PI * (i - band_start)) / nodes_in_band;
        
        // Position on hemisphere surface (in parent's tangent space)
        // Convert to 3D point on hemisphere
        double r = current_radius;  // Distance from pole
        child->angular_position = angle;
        
        // Point on hemisphere (local coordinates)
        // x = r * cos(angle)
        // y = r * sin(angle)
        // z = sqrt(R² - r²) where R is parent radius
        double R = parent->hemisphere_radius;
        child->position.x = r * cos(angle);
        child->position.y = r * sin(angle);
        child->position.z = sqrt(R * R - r * r);
        child->position.w = 1.0;  // Homogeneous coordinate
        
        current_radius += 2.0 * child_radius;  // Spacing
    }
}

// Top-down pass: position children on hemisphere surfaces
void h3_layout_tree(FSNode *node, H4Point parent_position) {
    if (node == NULL) return;
    
    // Apply parent transform to get final position
    node->position = h4_transform_point(&node->position, &parent_position);
    
    // Position children on hemisphere
    h3_pack_children(node);
    
    // Recursively layout children
    for (uint32_t i = 0; i < node->child_count; i++) {
        h3_layout_tree(node->children[i], node->position);
    }
}

// Main layout function
void h3_layout(FSTree *tree) {
    if (tree->root == NULL) return;
    
    // Step 1: Compute hemisphere radii (bottom-up)
    h3_compute_radii(tree->root);
    
    // Step 2: Position root at origin
    tree->root->position = (H4Point){0, 0, 0, 1};
    
    // Step 3: Layout children (top-down)
    h3_layout_tree(tree->root, tree->root->position);
    
    // Step 4: Update statistics
    tree->total_files = 0;
    tree->total_dirs = 0;
    tree->total_size = 0;
    // ... count files and dirs
}
```

### Hyperbolic Transforms (h3_transform.c)

```c
#include "hyperbolic.h"
#include <math.h>
#include <string.h>

// Minkowski inner product for hyperbolic geometry
// <u, v> = -u0*v0 + u1*v1 + u2*v2 + u3*v3
static double minkowski_dot(H4Point *u, H4Point *v) {
    return -u->w * v->w + u->x * v->x + u->y * v->y + u->z * v->z;
}

// Distance in hyperbolic space
double h3_distance(H4Point *p1, H4Point *p2) {
    double dot = minkowski_dot(p1, p2);
    return acosh(-dot);  // Note: negative because we use signature (-+++)
}

// Create identity transform
H4Transform h3_identity(void) {
    H4Transform t;
    memset(&t, 0, sizeof(t));
    t.m[0][0] = t.m[1][1] = t.m[2][2] = t.m[3][3] = 1.0;
    return t;
}

// Translation in hyperbolic space (along direction d by distance dist)
// In Klein model, this is a projective transformation
H4Transform h3_translation(H4Point *direction, double distance) {
    // Lorentz boost in direction
    double cosh_d = cosh(distance);
    double sinh_d = sinh(distance);
    
    // Normalize direction (in Euclidean sense for Klein model)
    double len = sqrt(direction->x * direction->x + 
                       direction->y * direction->y + 
                       direction->z * direction->z);
    if (len < 1e-10) return h3_identity();
    
    double nx = direction->x / len;
    double ny = direction->y / len;
    double nz = direction->z / len;
    
    H4Transform t;
    // Lorentz boost matrix
    t.m[0][0] = cosh_d;      t.m[0][1] = sinh_d * nx;  t.m[0][2] = 0;           t.m[0][3] = 0;
    t.m[1][0] = sinh_d * nx; t.m[1][1] = cosh_d;       t.m[1][2] = 0;           t.m[1][3] = 0;
    t.m[2][0] = sinh_d * ny; t.m[2][1] = 0;            t.m[2][2] = cosh_d;      t.m[2][3] = 0;
    t.m[3][0] = sinh_d * nz; t.m[3][1] = 0;            t.m[3][2] = 0;           t.m[3][3] = cosh_d;
    
    return t;
}

// Rotation around origin (works same in hyperbolic)
H4Transform h3_rotation(double angle_x, double angle_y, double angle_z) {
    H4Transform t = h3_identity();
    
    double cx = cos(angle_x), sx = sin(angle_x);
    double cy = cos(angle_y), sy = sin(angle_y);
    double cz = cos(angle_z), sz = sin(angle_z);
    
    // Combined rotation matrix (standard Euler angles)
    t.m[0][0] = cy * cz;
    t.m[0][1] = cy * sz;
    t.m[0][2] = -sy;
    t.m[1][0] = sx * sy * cz - cx * sz;
    t.m[1][1] = sx * sy * sz + cx * cz;
    t.m[1][2] = sx * cy;
    t.m[2][0] = cx * sy * cz + sx * sz;
    t.m[2][1] = cx * sy * sz - sx * cz;
    t.m[2][2] = cx * cy;
    
    return t;
}

// Apply transform to point
H4Point h4_transform_point(H4Point *p, H4Point *origin) {
    // In Klein model, we add the origin offset
    // This is a projective transformation
    H4Point result;
    
    // Translation in hyperbolic space
    // We use the hyperbolic translation formula
    double dot = minkowski_dot(p, origin);
    double dist = acosh(-dot);
    
    // Direction from origin to point
    double dx = p->x - origin->x;
    double dy = p->y - origin->y;
    double dz = p->z - origin->z;
    
    // Project back to Klein model (stay within unit ball)
    result.x = dx;
    result.y = dy;
    result.z = dz;
    result.w = 1.0;
    
    // Normalize to stay within unit ball
    double len = sqrt(result.x * result.x + result.y * result.y + result.z * result.z);
    if (len > 0.999) {
        result.x /= len * 1.001;
        result.y /= len * 1.001;
        result.z /= len * 1.001;
    }
    
    return result;
}

// Transform composition
H4Transform h4_compose(H4Transform *a, H4Transform *b) {
    H4Transform result;
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            result.m[i][j] = 0;
            for (int k = 0; k < 4; k++) {
                result.m[i][j] += a->m[i][k] * b->m[k][j];
            }
        }
    }
    return result;
}
```

### OpenGL Renderer (gl_renderer.c)

```c
#include "hyperbolic.h"
#include <GL/gl.h>
#include <GL/glu.h>
#include <stdio.h>

// Shader for hyperbolic projection
static const char *vertex_shader_src = 
    "#version 330 core\n"
    "layout(location = 0) in vec3 aPos;\n"
    "layout(location = 1) in vec3 aColor;\n"
    "layout(location = 2) in float aSize;\n"
    "\n"
    "uniform mat4 uView;\n"
    "uniform mat4 uProjection;\n"
    "uniform vec3 uFocus;\n"
    "\n"
    "out vec3 vColor;\n"
    "out float vSize;\n"
    "\n"
    "// Klein to Poincaré disk model\n"
    "vec3 klein_to_poincare(vec3 k) {\n"
    "    float r = length(k);\n"
    "    if (r >= 1.0) return vec3(0.0);  // Clamp\n"
    "    return k / (1.0 + sqrt(1.0 - r * r));\n"
    "}\n"
    "\n"
    "void main() {\n"
    "    vec3 poincare = klein_to_poincare(aPos);\n"
    "    gl_Position = uProjection * uView * vec4(poincare, 1.0);\n"
    "    gl_PointSize = aSize * 10.0 / gl_Position.w;  // Size attenuation\n"
    "    vColor = aColor;\n"
    "    vSize = aSize;\n"
    "}\n";

static const char *fragment_shader_src =
    "#version 330 core\n"
    "in vec3 vColor;\n"
    "in float vSize;\n"
    "out vec4 FragColor;\n"
    "\n"
    "void main() {\n"
    "    vec2 coord = gl_PointCoord - vec2(0.5);\n"
    "    float dist = length(coord);\n"
    "    if (dist > 0.5) discard;  // Circular points\n"
    "\n"
    "    // Glow effect based on distance from center\n"
    "    float glow = 1.0 - smoothstep(0.0, 0.5, dist);\n"
    "    FragColor = vec4(vColor * glow, glow);\n"
    "}\n";

typedef struct {
    GLuint program;
    GLuint vao;
    GLuint vbo_vertices;
    GLuint vbo_colors;
    GLuint vbo_sizes;
    GLuint ibo;
    
    // Uniforms
    GLint uView;
    GLint uProjection;
    GLint uFocus;
    
    // Stats
    uint64_t nodes_drawn;
    uint64_t nodes_visible;
} GLRenderer;

// Compile shader
static GLuint compile_shader(GLenum type, const char *src) {
    GLuint shader = glCreateShader(type);
    glShaderSource(shader, 1, &src, NULL);
    glCompileShader(shader);
    
    GLint success;
    glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
    if (!success) {
        char log[512];
        glGetShaderInfoLog(shader, 512, NULL, log);
        fprintf(stderr, "Shader error: %s\n", log);
    }
    
    return shader;
}

// Initialize renderer
int gl_init(GLRenderer *r) {
    // Compile shaders
    GLuint vs = compile_shader(GL_VERTEX_SHADER, vertex_shader_src);
    GLuint fs = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_src);
    
    r->program = glCreateProgram();
    glAttachShader(r->program, vs);
    glAttachShader(r->program, fs);
    glLinkProgram(r->program);
    
    glDeleteShader(vs);
    glDeleteShader(fs);
    
    // Get uniform locations
    r->uView = glGetUniformLocation(r->program, "uView");
    r->uProjection = glGetUniformLocation(r->program, "uProjection");
    r->uFocus = glGetUniformLocation(r->program, "uFocus");
    
    // Create VAO and VBOs
    glGenVertexArrays(1, &r->vao);
    glGenBuffers(1, &r->vbo_vertices);
    glGenBuffers(1, &r->vbo_colors);
    glGenBuffers(1, &r->vbo_sizes);
    glGenBuffers(1, &r->ibo);
    
    return 0;
}

// Check if node is visible (within viewing frustum)
static bool is_visible(FSNode *node, H4Point *focus, double threshold) {
    double dist = h3_distance(&node->position, focus);
    // Nodes too far from focus are clipped
    return dist < threshold;
}

// Render tree with adaptive LOD
void gl_render_tree(GLRenderer *r, FSTree *tree, RenderContext *ctx) {
    glUseProgram(r->program);
    
    // Build view/projection matrices
    float view[16], proj[16];
    // ... build matrices from tree->view and ctx
    
    glUniformMatrix4fv(r->uView, 1, GL_FALSE, view);
    glUniformMatrix4fv(r->uProjection, 1, GL_FALSE, proj);
    glUniform3f(r->uFocus, tree->focus.x, tree->focus.y, tree->focus.z);
    
    // Collect visible nodes
    uint64_t frame_budget = ctx->frame_budget;
    uint64_t frame_start = get_time_us();
    
    // Priority queue: draw nodes closest to focus first
    FSNode **draw_queue = malloc(tree->node_count * sizeof(FSNode*));
    uint64_t queue_size = 0;
    
    // BFS from focus
    FSNode *focus_node = find_nearest_node(tree, &tree->focus);
    if (focus_node) {
        // Priority: ancestors, siblings, descendants
        collect_visible_nodes(focus_node, draw_queue, &queue_size, ctx->near_plane);
    }
    
    // Upload to GPU
    float *vertices = malloc(queue_size * 3 * sizeof(float));
    float *colors = malloc(queue_size * 3 * sizeof(float));
    float *sizes = malloc(queue_size * sizeof(float));
    
    uint64_t drawn = 0;
    for (uint64_t i = 0; i < queue_size && drawn < 100000; i++) {
        FSNode *node = draw_queue[i];
        
        // Time budget check
        if (get_time_us() - frame_start > frame_budget) break;
        
        // Upload node data
        vertices[drawn * 3] = node->position.x;
        vertices[drawn * 3 + 1] = node->position.y;
        vertices[drawn * 3 + 2] = node->position.z;
        
        // Color based on type
        if (node->type == 1) {  // Directory
            colors[drawn * 3] = 0.3f;
            colors[drawn * 3 + 1] = 0.5f;
            colors[drawn * 3 + 2] = 1.0f;
        } else {  // File
            colors[drawn * 3] = 0.8f;
            colors[drawn * 3 + 1] = 0.8f;
            colors[drawn * 3 + 2] = 0.8f;
        }
        
        sizes[drawn] = node->projected_size;
        drawn++;
    }
    
    // Upload to GPU
    glBindVertexArray(r->vao);
    
    glBindBuffer(GL_ARRAY_BUFFER, r->vbo_vertices);
    glBufferData(GL_ARRAY_BUFFER, drawn * 3 * sizeof(float), vertices, GL_DYNAMIC_DRAW);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, NULL);
    glEnableVertexAttribArray(0);
    
    glBindBuffer(GL_ARRAY_BUFFER, r->vbo_colors);
    glBufferData(GL_ARRAY_BUFFER, drawn * 3 * sizeof(float), colors, GL_DYNAMIC_DRAW);
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, NULL);
    glEnableVertexAttribArray(1);
    
    glBindBuffer(GL_ARRAY_BUFFER, r->vbo_sizes);
    glBufferData(GL_ARRAY_BUFFER, drawn * sizeof(float), sizes, GL_DYNAMIC_DRAW);
    glVertexAttribPointer(2, 1, GL_FLOAT, GL_FALSE, 0, NULL);
    glEnableVertexAttribArray(2);
    
    // Draw
    glDrawArrays(GL_POINTS, 0, drawn);
    
    // Cleanup
    free(vertices);
    free(colors);
    free(sizes);
    free(draw_queue);
    
    r->nodes_drawn = drawn;
    r->nodes_visible = queue_size;
    ctx->total_drawn = drawn;
    ctx->total_visible = queue_size;
}
```

### File System Scanner (fs_scanner.c)

```c
#include "hyperbolic.h"
#include <dirent.h>
#include <sys/stat.h>
#include <string.h>

// Scan file system and build tree
int fs_scan(const char *root_path, FSTree *tree) {
    // Initialize tree
    tree->node_count = 0;
    tree->node_capacity = 65536;  // Start with 64K
    tree->nodes = malloc(tree->node_capacity * sizeof(FSNode*));
    tree->id_to_index = malloc(tree->node_capacity * sizeof(uint64_t));
    
    // Create root
    FSNode *root = fs_create_node(root_path, NULL);
    if (!root) return -1;
    
    tree->root = root;
    fs_add_node(tree, root);
    
    // Recursive scan
    fs_scan_recursive(root, tree);
    
    // Build parent/child links
    fs_build_links(tree);
    
    // Compute layout
    h3_layout(tree);
    
    return 0;
}

// Recursive scan
static void fs_scan_recursive(FSNode *node, FSTree *tree) {
    DIR *dir = opendir(node->path);
    if (!dir) return;
    
    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        // Skip . and ..
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
            continue;
        
        // Build full path
        char child_path[PATH_MAX];
        snprintf(child_path, sizeof(child_path), "%s/%s", node->path, entry->d_name);
        
        // Create child node
        FSNode *child = fs_create_node(child_path, node);
        if (!child) continue;
        
        // Add to tree
        fs_add_node(tree, child);
        
        // Recurse if directory
        if (child->type == 1) {  // Directory
            fs_scan_recursive(child, tree);
        }
    }
    
    closedir(dir);
}

// Create node from path
FSNode *fs_create_node(const char *path, FSNode *parent) {
    FSNode *node = malloc(sizeof(FSNode));
    if (!node) return NULL;
    
    node->path = strdup(path);
    node->name = strrchr(path, '/');
    node->name = node->name ? node->name + 1 : node->path;
    node->parent = parent;
    node->children = NULL;
    node->child_count = 0;
    node->child_capacity = 0;
    
    // Get file info
    struct stat st;
    if (lstat(path, &st) == 0) {
        node->size = st.st_size;
        node->mtime = st.st_mtime;
        node->type = S_ISDIR(st.st_mode) ? 1 : (S_ISLNK(st.st_mode) ? 2 : 0);
    } else {
        node->size = 0;
        node->mtime = 0;
        node->type = 0;
    }
    
    // Default color
    node->color[0] = node->type == 1 ? 0.3f : 0.8f;
    node->color[1] = node->type == 1 ? 0.5f : 0.8f;
    node->color[2] = node->type == 1 ? 1.0f : 0.8f;
    node->color[3] = 1.0f;
    
    return node;
}

// Add node to tree
void fs_add_node(FSTree *tree, FSNode *node) {
    if (tree->node_count >= tree->node_capacity) {
        tree->node_capacity *= 2;
        tree->nodes = realloc(tree->nodes, tree->node_capacity * sizeof(FSNode*));
        tree->id_to_index = realloc(tree->id_to_index, tree->node_capacity * sizeof(uint64_t));
    }
    
    node->id = tree->node_count;
    tree->nodes[tree->node_count] = node;
    tree->id_to_index[tree->node_count] = node->id;
    tree->node_count++;
}

// Build parent/child links after scan
void fs_build_links(FSTree *tree) {
    for (uint64_t i = 0; i < tree->node_count; i++) {
        FSNode *node = tree->nodes[i];
        if (node->parent) {
            // Add to parent's children
            if (node->parent->child_count >= node->parent->child_capacity) {
                node->parent->child_capacity = node->parent->child_capacity == 0 ? 8 : node->parent->child_capacity * 2;
                node->parent->children = realloc(node->parent->children, node->parent->child_capacity * sizeof(FSNode*));
            }
            node->parent->children[node->parent->child_count++] = node;
        }
    }
}
```

## Makefile

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -O3 -fPIC
LDFLAGS = -lglfw -lGL -lm -lsqlite3 -lpthread

# Source files
SRCS = main.c h3_layout.c h3_transform.c gl_renderer.c fs_scanner.c
OBJS = $(SRCS:.c=.o)

# Target
TARGET = hypex

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

%.o: %.c hyperbolic.h
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

# Dependencies
main.o: hyperbolic.h
h3_layout.o: hyperbolic.h
h3_transform.o: hyperbolic.h
gl_renderer.o: hyperbolic.h
fs_scanner.o: hyperbolic.h

.PHONY: all clean
```

## Estrutura do Projeto

```
hypex/
├── src/
│   ├── main.c              # Entry point, main loop
│   ├── hyperbolic.h        # Core structures and declarations
│   ├── h3_layout.c         # H3 layout algorithm
│   ├── h3_transform.c      # Hyperbolic transformations
│   ├── gl_renderer.c       # OpenGL rendering
│   ├── fs_scanner.c        # File system scanner
│   ├── fs_monitor.c        # Real-time updates
│   └── ui_input.c          # User interaction
├── shaders/
│   ├── hyperbolic.vert     # Vertex shader
│   └── hyperbolic.frag     # Fragment shader
├── Makefile
├── README.md
└── design.md              # Este documento
```

## Performance Targets

| Métrica | Target |
|---------|--------|
| **Nós renderizados** | 100,000+ |
| **Frame rate** | 20 FPS mínimo |
| **Latência interação** | < 50ms |
| **Memória** | < 2GB para 3M nós |
| **Startup** | < 5 segundos |

## Próximos Passos

1. **Implementar h3_layout.c** - Layout algorithm completo
2. **Implementar h3_transform.c** - Transformações hiperbólicas
3. **Implementar gl_renderer.c** - OpenGL com shaders
4. **Integrar com fs-monitor** - Updates em tempo real
5. **Adicionar UI** - Mouse/keyboard navigation
6. **Otimizar** - Frustum culling, LOD, GPU instancing

## Referências

1. **Munzner, T. (1998).** "Exploring Large Graphs in 3D Hyperbolic Space" - Stanford
2. **Lamping, J., Rao, R. (1995).** "A Focus+Context Technique Based on Hyperbolic Geometry" - Xerox PARC
3. **Munzner, T. (1997).** "H3: Laying Out Large Directed Graphs in 3D Hyperbolic Space" - InfoVis
4. **Phillips, M., Gunn, C. (1992).** "Visualizing Hyperbolic Space: Unusual Uses of 4x4 Matrices"
5. **Wikipedia:** Hyperbolic Tree, Poincaré Disk Model, Klein Model