/*
 * main.c - HypEx: Hyperbolic File Explorer
 * 
 * Entry point and main loop for the 3D hyperbolic file system visualizer.
 * Based on H3 algorithm by Tamara Munzner (Stanford, 1998)
 */

#define _GNU_SOURCE
#define _POSIX_C_SOURCE 200809L

#include "hyperbolic.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdarg.h>
#include <getopt.h>
#include <signal.h>
#include <time.h>

// OpenGL includes (platform-specific)
#ifdef __APPLE__
    #define GL_SILENCE_DEPRECATION
    #include <OpenGL/gl3.h>
    #include <GLFW/glfw3.h>
#else
    #define GL_GLEXT_PROTOTYPES
    #include <GL/gl.h>
    #include <GL/glext.h>
    #include <GLFW/glfw3.h>
#endif

/* ============================================================================
 * Global State
 * ============================================================================ */

static volatile bool g_running = true;
static H3Tree *g_tree = NULL;
static H3Config g_config;
static H3RenderContext g_render_ctx;
static H3InputState g_input;
static GLFWwindow *g_window = NULL;

// Window dimensions
static int g_window_width = 1920;
static int g_window_height = 1080;

/* ============================================================================
 * Utility Functions
 * ============================================================================ */

uint64_t get_time_us(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec * 1000000ULL + ts.tv_nsec / 1000ULL;
}

void log_info(const char *fmt, ...) {
    va_list args;
    va_start(args, fmt);
    fprintf(stdout, "[INFO] ");
    vfprintf(stdout, fmt, args);
    fprintf(stdout, "\n");
    va_end(args);
}

void log_error(const char *fmt, ...) {
    va_list args;
    va_start(args, fmt);
    fprintf(stderr, "[ERROR] ");
    vfprintf(stderr, fmt, args);
    fprintf(stderr, "\n");
    va_end(args);
}

void log_debug(const char *fmt, ...) {
#ifdef DEBUG
    va_list args;
    va_start(args, fmt);
    fprintf(stdout, "[DEBUG] ");
    vfprintf(stdout, fmt, args);
    fprintf(stdout, "\n");
    va_end(args);
#else
    (void)fmt;
#endif
}

/* ============================================================================
 * OpenGL Shaders
 * ============================================================================ */

static const char *vertex_shader_source =
    "#version 330 core\n"
    "layout(location = 0) in vec3 aPos;\n"
    "layout(location = 1) in vec3 aColor;\n"
    "layout(location = 2) in float aSize;\n"
    "layout(location = 3) in float aType;\n"  // Changed to float
    "\n"
    "uniform mat4 uView;\n"
    "uniform mat4 uProjection;\n"
    "uniform vec3 uFocus;\n"
    "uniform float uZoom;\n"
    "uniform float uTime;\n"
    "\n"
    "out vec3 vColor;\n"
    "out float vSize;\n"
    "out float vDist;\n"
    "out float vType;\n"  // Changed to float
    "\n"
    "// Klein to Poincaré disk model conversion\n"
    "vec3 klein_to_poincare(vec3 k) {\n"
    "    float r = length(k);\n"
    "    if (r >= 1.0) return vec3(0.0);  // Clamp to unit ball\n"
    "    return k / (1.0 + sqrt(1.0 - r * r));\n"
    "}\n"
    "\n"
    "void main() {\n"
    "    // Convert from Klein to Poincaré model\n"
    "    vec3 poincare = klein_to_poincare(aPos);\n"
    "    \n"
    "    // Apply view transform\n"
    "    vec4 viewPos = uView * vec4(poincare, 1.0);\n"
    "    gl_Position = uProjection * viewPos;\n"
    "    \n"
    "    // Calculate distance from focus for size attenuation\n"
    "    vDist = length(viewPos.xyz - uFocus);\n"
    "    \n"
    "    // Point size with zoom and distance attenuation\n"
    "    float baseSize = aSize * uZoom;\n"
    "    float attenuation = 1.0 / (1.0 + vDist * 0.5);\n"
    "    gl_PointSize = baseSize * attenuation * 100.0 / gl_Position.w;\n"
    "    gl_PointSize = clamp(gl_PointSize, 2.0, 64.0);\n"
    "    \n"
    "    vColor = aColor;\n"
    "    vSize = aSize;\n"
    "    vType = aType;\n"
    "}\n";

static const char *fragment_shader_source =
    "#version 330 core\n"
    "in vec3 vColor;\n"
    "in float vSize;\n"
    "in float vDist;\n"
    "in float vType;\n"  // Changed to float
    "\n"
    "out vec4 FragColor;\n"
    "\n"
    "uniform float uTime;\n"
    "\n"
    "void main() {\n"
    "    // Circular point sprite\n"
    "    vec2 coord = gl_PointCoord - vec2(0.5);\n"
    "    float dist = length(coord);\n"
    "    if (dist > 0.5) discard;  // Circular mask\n"
    "    \n"
    "    // Glow effect\n"
    "    float glow = 1.0 - smoothstep(0.0, 0.5, dist);\n"
    "    \n"
    "    // Color based on type\n"
    "    vec3 color = vColor;\n"
    "    \n"
    "    // Directories have a slight glow (type 1.0)\n"
    "    if (vType > 0.5 && vType < 1.5) {\n"
    "        color *= 1.0 + 0.2 * glow;\n"
    "    }\n"
    "    \n"
    "    // Distance-based fade\n"
    "    float fade = 1.0 / (1.0 + vDist * 0.3);\n"
    "    \n"
    "    // Final color\n"
    "    FragColor = vec4(color * fade, glow * fade);\n"
    "}\n";

static GLuint g_shader_program = 0;
static GLuint g_vao = 0;
static GLuint g_vbo_vertices = 0;
static GLuint g_vbo_colors = 0;
static GLuint g_vbo_sizes = 0;
static GLuint g_vbo_types = 0;

/* ============================================================================
 * Shader Compilation
 * ============================================================================ */

static GLuint compile_shader(GLenum type, const char *source) {
    GLuint shader = glCreateShader(type);
    glShaderSource(shader, 1, &source, NULL);
    glCompileShader(shader);
    
    GLint success;
    glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
    if (!success) {
        char log[512];
        glGetShaderInfoLog(shader, 512, NULL, log);
        log_error("Shader compilation error: %s", log);
        return 0;
    }
    
    return shader;
}

static int init_shaders(void) {
    GLuint vs = compile_shader(GL_VERTEX_SHADER, vertex_shader_source);
    GLuint fs = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_source);
    
    if (!vs || !fs) {
        return -1;
    }
    
    g_shader_program = glCreateProgram();
    glAttachShader(g_shader_program, vs);
    glAttachShader(g_shader_program, fs);
    glLinkProgram(g_shader_program);
    
    GLint success;
    glGetProgramiv(g_shader_program, GL_LINK_STATUS, &success);
    if (!success) {
        char log[512];
        glGetProgramInfoLog(g_shader_program, 512, NULL, log);
        log_error("Shader linking error: %s", log);
        return -1;
    }
    
    glDeleteShader(vs);
    glDeleteShader(fs);
    
    return 0;
}

/* ============================================================================
 * OpenGL Initialization
 * ============================================================================ */

static int init_opengl(void) {
    // Initialize GLFW
    if (!glfwInit()) {
        log_error("Failed to initialize GLFW");
        return -1;
    }
    
    // Configure GLFW
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    glfwWindowHint(GLFW_SAMPLES, 4);  // MSAA
    glfwWindowHint(GLFW_DOUBLEBUFFER, GLFW_TRUE);
    
#ifdef __APPLE__
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
    glfwWindowHint(GLFW_COCOA_RETINA_FRAMEBUFFER, GLFW_TRUE);
#endif
    
    // Create window
    g_window = glfwCreateWindow(g_window_width, g_window_height, 
                                "HypEx - Hyperbolic File Explorer", 
                                NULL, NULL);
    if (!g_window) {
        log_error("Failed to create GLFW window");
        glfwTerminate();
        return -1;
    }
    
    glfwMakeContextCurrent(g_window);
    glfwSwapInterval(1);  // VSync
    
    // Initialize GLEW (optional, for extensions)
    // glewExperimental = GL_TRUE;
    // if (glewInit() != GLEW_OK) { ... }
    
    // Enable features
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glEnable(GL_POINT_SMOOTH);
    glEnable(GL_MULTISAMPLE);
    
    // Initialize shaders
    if (init_shaders() != 0) {
        log_error("Failed to initialize shaders");
        return -1;
    }
    
    // Create VAO and VBOs
    glGenVertexArrays(1, &g_vao);
    glBindVertexArray(g_vao);
    
    glGenBuffers(1, &g_vbo_vertices);
    glGenBuffers(1, &g_vbo_colors);
    glGenBuffers(1, &g_vbo_sizes);
    glGenBuffers(1, &g_vbo_types);
    
    glBindVertexArray(0);
    
    log_info("OpenGL initialized successfully");
    return 0;
}

/* ============================================================================
 * Rendering
 * ============================================================================ */

static void render_tree(void) {
    if (g_tree == NULL || g_tree->node_count == 0) return;
    
    uint64_t frame_start = get_time_us();
    
    glUseProgram(g_shader_program);
    glBindVertexArray(g_vao);
    
    // Build view/projection matrices
    float view[16], proj[16];
    
    // Perspective projection
    float fov = 45.0f;
    float aspect = (float)g_window_width / g_window_height;
    float near = 0.01f;
    float far = 100.0f;
    
    // Build projection matrix (standard perspective)
    float f = 1.0f / tanf(fov * 0.5f * 3.14159f / 180.0f);
    proj[0] = f / aspect; proj[4] = 0;     proj[8] = 0;                     proj[12] = 0;
    proj[1] = 0;          proj[5] = f;     proj[9] = 0;                     proj[13] = 0;
    proj[2] = 0;          proj[6] = 0;     proj[10] = (far + near) / (near - far); proj[14] = 2 * far * near / (near - far);
    proj[3] = 0;          proj[7] = 0;     proj[11] = -1;                   proj[15] = 0;
    
    // Build view matrix (look at focus point)
    // Simplified: identity with zoom
    memset(view, 0, sizeof(view));
    view[0] = g_tree->zoom;
    view[5] = g_tree->zoom;
    view[10] = g_tree->zoom;
    view[15] = 1.0f;
    
    // Set uniforms
    GLint uView = glGetUniformLocation(g_shader_program, "uView");
    GLint uProjection = glGetUniformLocation(g_shader_program, "uProjection");
    GLint uFocus = glGetUniformLocation(g_shader_program, "uFocus");
    GLint uZoom = glGetUniformLocation(g_shader_program, "uZoom");
    GLint uTime = glGetUniformLocation(g_shader_program, "uTime");
    
    glUniformMatrix4fv(uView, 1, GL_FALSE, view);
    glUniformMatrix4fv(uProjection, 1, GL_FALSE, proj);
    glUniform3f(uFocus, g_tree->focus.x, g_tree->focus.y, g_tree->focus.z);
    glUniform1f(uZoom, g_tree->zoom);
    glUniform1f(uTime, glfwGetTime());
    
    // Collect visible nodes and upload to GPU
    // For now, upload all nodes (optimization: frustum culling)
    uint64_t max_nodes = g_tree->node_count < H3_MAX_VISIBLE ? g_tree->node_count : H3_MAX_VISIBLE;
    
    float *vertices = malloc(max_nodes * 3 * sizeof(float));
    float *colors = malloc(max_nodes * 3 * sizeof(float));
    float *sizes = malloc(max_nodes * sizeof(float));
    float *types = malloc(max_nodes * sizeof(float));  // Changed to float
    
    uint64_t drawn = 0;
    for (uint64_t i = 0; i < max_nodes && drawn < H3_MAX_VISIBLE; i++) {
        H3Node *node = g_tree->nodes[i];
        
        // Time budget check
        if (get_time_us() - frame_start > g_render_ctx.frame_budget_us) break;
        
        // Check visibility (inside unit ball)
        if (!h3_inside_unit_ball(&node->position)) continue;
        
        vertices[drawn * 3] = (float)node->position.x;
        vertices[drawn * 3 + 1] = (float)node->position.y;
        vertices[drawn * 3 + 2] = (float)node->position.z;
        
        colors[drawn * 3] = node->color[0];
        colors[drawn * 3 + 1] = node->color[1];
        colors[drawn * 3 + 2] = node->color[2];
        
        sizes[drawn] = node->projected_size;
        types[drawn] = (float)node->type;  // Convert to float
        
        drawn++;
    }
    
    if (drawn == 0) {
        free(vertices);
        free(colors);
        free(sizes);
        free(types);
        return;
    }
    
    // Upload vertices
    glBindBuffer(GL_ARRAY_BUFFER, g_vbo_vertices);
    glBufferData(GL_ARRAY_BUFFER, drawn * 3 * sizeof(float), vertices, GL_DYNAMIC_DRAW);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, NULL);
    glEnableVertexAttribArray(0);
    
    // Upload colors
    glBindBuffer(GL_ARRAY_BUFFER, g_vbo_colors);
    glBufferData(GL_ARRAY_BUFFER, drawn * 3 * sizeof(float), colors, GL_DYNAMIC_DRAW);
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, NULL);
    glEnableVertexAttribArray(1);
    
    // Upload sizes
    glBindBuffer(GL_ARRAY_BUFFER, g_vbo_sizes);
    glBufferData(GL_ARRAY_BUFFER, drawn * sizeof(float), sizes, GL_DYNAMIC_DRAW);
    glVertexAttribPointer(2, 1, GL_FLOAT, GL_FALSE, 0, NULL);
    glEnableVertexAttribArray(2);
    
    // Upload types (now float)
    glBindBuffer(GL_ARRAY_BUFFER, g_vbo_types);
    glBufferData(GL_ARRAY_BUFFER, drawn * sizeof(float), types, GL_DYNAMIC_DRAW);
    glVertexAttribPointer(3, 1, GL_FLOAT, GL_FALSE, 0, NULL);
    glEnableVertexAttribArray(3);
    
    // Draw points
    glDrawArrays(GL_POINTS, 0, drawn);
    
    // Cleanup
    free(vertices);
    free(colors);
    free(sizes);
    free(types);
    
    g_render_ctx.nodes_drawn = drawn;
    g_render_ctx.nodes_visible = g_tree->node_count;
}

/* ============================================================================
 * Input Handling
 * ============================================================================ */

static void key_callback(GLFWwindow *window, int key, int scancode, int action, int mods) {
    (void)window;  // Unused parameter
    (void)scancode;  // Unused parameter
    (void)mods;  // Unused parameter
    
    if (action == GLFW_PRESS) {
        g_input.keys[key] = 1;
        g_input.keys_pressed[key] = 1;
        
        // Special keys
        if (key == GLFW_KEY_ESCAPE) {
            g_running = false;
        }
        if (key == GLFW_KEY_Q && (mods & GLFW_MOD_CONTROL)) {
            g_running = false;
        }
    }
    else if (action == GLFW_RELEASE) {
        g_input.keys[key] = 0;
        g_input.keys_released[key] = 1;
    }
}

static void mouse_button_callback(GLFWwindow *window, int button, int action, int mods) {
    (void)window;
    (void)mods;
    
    if (action == GLFW_PRESS) {
        g_input.mouse_buttons |= (1 << button);
    }
    else if (action == GLFW_RELEASE) {
        g_input.mouse_buttons &= ~(1 << button);
    }
}

static void cursor_pos_callback(GLFWwindow *window, double xpos, double ypos) {
    (void)window;
    
    g_input.last_mouse_x = g_input.mouse_x;
    g_input.last_mouse_y = g_input.mouse_y;
    g_input.mouse_x = xpos;
    g_input.mouse_y = ypos;
}

static void scroll_callback(GLFWwindow *window, double xoffset, double yoffset) {
    (void)window;
    (void)xoffset;
    
    // Zoom
    g_tree->target_zoom *= (1.0 + yoffset * 0.1);
    g_tree->target_zoom = fmax(0.1, fmin(10.0, g_tree->target_zoom));
}

static void window_size_callback(GLFWwindow *window, int width, int height) {
    (void)window;
    g_window_width = width;
    g_window_height = height;
    glViewport(0, 0, width, height);
}

static void init_input(void) {
    memset(&g_input, 0, sizeof(g_input));
    glfwSetKeyCallback(g_window, key_callback);
    glfwSetMouseButtonCallback(g_window, mouse_button_callback);
    glfwSetCursorPosCallback(g_window, cursor_pos_callback);
    glfwSetScrollCallback(g_window, scroll_callback);
    glfwSetFramebufferSizeCallback(g_window, window_size_callback);
}

static void update_input(void) {
    // Navigation: WASD + QE for rotation
    double pan_speed = 0.02 * g_config.pan_speed;
    double rot_speed = 0.02 * g_config.rotation_speed;
    
    if (g_input.keys[GLFW_KEY_W]) {
        g_tree->target_focus.z += pan_speed;
    }
    if (g_input.keys[GLFW_KEY_S]) {
        g_tree->target_focus.z -= pan_speed;
    }
    if (g_input.keys[GLFW_KEY_A]) {
        g_tree->target_focus.x -= pan_speed;
    }
    if (g_input.keys[GLFW_KEY_D]) {
        g_tree->target_focus.x += pan_speed;
    }
    if (g_input.keys[GLFW_KEY_R]) {
        g_tree->target_focus.y += pan_speed;
    }
    if (g_input.keys[GLFW_KEY_F]) {
        g_tree->target_focus.y -= pan_speed;
    }
    
    // Rotation: Arrow keys
    if (g_input.keys[GLFW_KEY_LEFT]) {
        g_input.rotation_angle -= rot_speed;
    }
    if (g_input.keys[GLFW_KEY_RIGHT]) {
        g_input.rotation_angle += rot_speed;
    }
    
    // Zoom: +/-
    if (g_input.keys[GLFW_KEY_EQUAL] || g_input.keys[GLFW_KEY_KP_ADD]) {
        g_tree->target_zoom *= 1.05;
    }
    if (g_input.keys[GLFW_KEY_MINUS] || g_input.keys[GLFW_KEY_KP_SUBTRACT]) {
        g_tree->target_zoom *= 0.95;
    }
    
    // Reset: Home
    if (g_input.keys[GLFW_KEY_HOME]) {
        g_tree->target_focus = g_tree->root->position;
        g_tree->target_zoom = 1.0;
    }
    
    // Mouse drag for rotation
    if (g_input.mouse_buttons & GLFW_MOUSE_BUTTON_LEFT) {
        double dx = g_input.mouse_x - g_input.last_mouse_x;
        (void)dx;  // Used for rotation
        g_input.rotation_angle += dx * 0.005;
    }
    
    // Smooth interpolation
    g_tree->focus.x = h3_lerp(g_tree->focus.x, g_tree->target_focus.x, 0.1);
    g_tree->focus.y = h3_lerp(g_tree->focus.y, g_tree->target_focus.y, 0.1);
    g_tree->focus.z = h3_lerp(g_tree->focus.z, g_tree->target_focus.z, 0.1);
    g_tree->zoom = h3_lerp(g_tree->zoom, g_tree->target_zoom, 0.1);
    
    // Clamp zoom
    g_tree->zoom = fmax(0.1, fmin(10.0, g_tree->zoom));
    
    // Clamp focus to unit ball
    h3_normalize(&g_tree->focus);
    
    // Clear per-frame state
    memset(g_input.keys_pressed, 0, sizeof(g_input.keys_pressed));
    memset(g_input.keys_released, 0, sizeof(g_input.keys_released));
}

/* ============================================================================
 * Main Loop
 * ============================================================================ */

static void main_loop(void) {
    log_info("Entering main loop...");
    
    while (g_running && !glfwWindowShouldClose(g_window)) {
        uint64_t frame_start = get_time_us();
        
        // Clear
        glClearColor(0.05f, 0.05f, 0.1f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        
        // Update input
        update_input();
        
        // Render
        render_tree();
        
        // Swap buffers
        glfwSwapBuffers(g_window);
        glfwPollEvents();
        
        // FPS calculation
        uint64_t frame_time = get_time_us() - frame_start;
        g_render_ctx.frame_time_us = frame_time;
        g_render_ctx.fps = 1000000.0f / frame_time;
        
        // Update window title with stats
        char title[256];
        snprintf(title, sizeof(title), 
                 "HypEx - %lu nodes | %.1f FPS | %.3f zoom",
                 g_tree ? g_tree->node_count : 0,
                 g_render_ctx.fps,
                 g_tree ? g_tree->zoom : 1.0f);
        glfwSetWindowTitle(g_window, title);
    }
}

/* ============================================================================
 * Cleanup
 * ============================================================================ */

static void cleanup(void) {
    log_info("Cleaning up...");
    
    if (g_vao) glDeleteVertexArrays(1, &g_vao);
    if (g_vbo_vertices) glDeleteBuffers(1, &g_vbo_vertices);
    if (g_vbo_colors) glDeleteBuffers(1, &g_vbo_colors);
    if (g_vbo_sizes) glDeleteBuffers(1, &g_vbo_sizes);
    if (g_vbo_types) glDeleteBuffers(1, &g_vbo_types);
    if (g_shader_program) glDeleteProgram(g_shader_program);
    
    if (g_window) glfwDestroyWindow(g_window);
    glfwTerminate();
    
    if (g_tree) {
        // h3_tree_destroy(g_tree);
        free(g_tree);
    }
    
    log_info("Cleanup complete");
}

/* ============================================================================
 * Signal Handler
 * ============================================================================ */

static void signal_handler(int sig) {
    (void)sig;
    g_running = false;
}

/* ============================================================================
 * Configuration Defaults
 * ============================================================================ */

static void config_defaults(H3Config *config) {
    memset(config, 0, sizeof(H3Config));
    
    // Layout
    config->base_node_size = 1.0;
    config->size_scale_factor = 1.5;
    config->depth_scale_factor = 0.95;
    config->use_file_size_for_size = true;
    
    // Rendering
    config->target_fps = 20;
    config->max_visible_nodes = H3_MAX_VISIBLE;
    config->node_size_min = 0.5f;
    config->node_size_max = 20.0f;
    config->draw_edges = false;
    config->draw_labels = false;
    config->use_point_sprites = true;
    
    // Colors
    config->color_dir[0] = 0.3f; config->color_dir[1] = 0.5f; config->color_dir[2] = 1.0f; config->color_dir[3] = 1.0f;
    config->color_file[0] = 0.8f; config->color_file[1] = 0.8f; config->color_file[2] = 0.8f; config->color_file[3] = 1.0f;
    
    // Navigation
    config->pan_speed = 1.0;
    config->zoom_speed = 1.0;
    config->rotation_speed = 1.0;
    config->invert_y_axis = false;
    
    // File system
    config->root_path = getenv("HOME");
    if (!config->root_path) config->root_path = "/";
    config->max_depth = 100;
    config->max_files = 0;  // Unlimited
    
    // Database
    config->poll_interval_ms = 100;
}

/* ============================================================================
 * Usage
 * ============================================================================ */

static void print_usage(const char *prog) {
    printf("HypEx - Hyperbolic File Explorer\n");
    printf("\n");
    printf("Usage: %s [OPTIONS]\n", prog);
    printf("\n");
    printf("Options:\n");
    printf("  -r, --root PATH    Root directory to visualize (default: $HOME)\n");
    printf("  -w, --width WIDTH  Window width (default: 1920)\n");
    printf("  -h, --height HEIGHT Window height (default: 1080)\n");
    printf("  -f, --fps FPS      Target frame rate (default: 20)\n");
    printf("  -d, --db PATH      Database path (default: ~/.hypex/data.db)\n");
    printf("  -v, --verbose      Enable verbose output\n");
    printf("  --help             Show this help\n");
    printf("\n");
    printf("Navigation:\n");
    printf("  WASD               Pan\n");
    printf("  RF                 Pan up/down\n");
    printf("  Arrow keys         Rotate\n");
    printf("  +/-                Zoom\n");
    printf("  Home               Reset view\n");
    printf("  ESC/Q              Exit\n");
    printf("\n");
    printf("Based on H3 algorithm by Tamara Munzner (Stanford, 1998)\n");
}

/* ============================================================================
 * Main Entry Point
 * ============================================================================ */

int main(int argc, char **argv) {
    // Parse command line
    config_defaults(&g_config);
    
    static struct option long_options[] = {
        {"root",   required_argument, 0, 'r'},
        {"width",  required_argument, 0, 'w'},
        {"height", required_argument, 0, 'H'},
        {"fps",    required_argument, 0, 'f'},
        {"db",     required_argument, 0, 'd'},
        {"verbose", no_argument,      0, 'v'},
        {"help",   no_argument,       0, '?'},
        {0, 0, 0, 0}
    };
    
    int opt;
    while ((opt = getopt_long(argc, argv, "r:w:H:f:d:v?", long_options, NULL)) != -1) {
        switch (opt) {
            case 'r':
                g_config.root_path = optarg;
                break;
            case 'w':
                g_window_width = atoi(optarg);
                break;
            case 'H':
                g_window_height = atoi(optarg);
                break;
            case 'f':
                g_config.target_fps = atoi(optarg);
                break;
            case 'd':
                g_config.db_path = optarg;
                break;
            case 'v':
                // Enable verbose logging
                break;
            case '?':
                print_usage(argv[0]);
                return 0;
            default:
                print_usage(argv[0]);
                return 1;
        }
    }
    
    log_info("HypEx - Hyperbolic File Explorer");
    log_info("Root: %s", g_config.root_path);
    
    // Setup signal handlers
    signal(SIGINT, signal_handler);
    signal(SIGTERM, signal_handler);
    
    // Initialize OpenGL
    if (init_opengl() != 0) {
        log_error("Failed to initialize OpenGL");
        return 1;
    }
    
    // Initialize input
    init_input();
    
    // Initialize render context
    memset(&g_render_ctx, 0, sizeof(g_render_ctx));
    g_render_ctx.frame_budget_us = 1000000 / g_config.target_fps;
    
    // Scan file system
    log_info("Scanning file system from: %s", g_config.root_path);
    g_tree = h3_tree_create();
    if (!g_tree) {
        log_error("Failed to create tree");
        cleanup();
        return 1;
    }
    
    if (h3_scan_filesystem(g_config.root_path, g_tree, &g_config) != 0) {
        log_error("Failed to scan file system");
        cleanup();
        return 1;
    }
    
    log_info("Found %lu nodes", g_tree->node_count);
    
    // Layout tree
    log_info("Computing H3 layout...");
    h3_layout_tree(g_tree);
    h3_layout_assign_colors(g_tree);
    
    log_info("Layout complete: %u max depth", g_tree->max_depth);
    
    // Main loop
    main_loop();
    
    // Cleanup
    cleanup();
    
    return 0;
}