#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <GLFW/glfw3.h>

#define MAX_NODES 4000000
#define MAX_NAME_LEN 256
#define MAX_PATH_LEN 4096

typedef struct {
    char id[MAX_PATH_LEN];
    char name[MAX_NAME_LEN];
    int type;  // 0 = dir, 1 = file
    int level;
    double x, y, z;
    double size;
    unsigned int color;
    int parent_idx;
} Node;

Node *nodes;
int node_count = 0;
int nodes_by_level[25] = {0};

// Camera
double cam_dist = 500.0;
double cam_rot_x = 0.0;
double cam_rot_y = 0.0;
double cam_target_x = 0.0;
double cam_target_y = 0.0;
double cam_target_z = 0.0;

// Mouse
double last_mouse_x = 0.0;
double last_mouse_y = 0.0;
int mouse_pressed = 0;

// Selection
int selected_node = -1;
int hovered_node = -1;

// View settings
int max_level_view = 5;
int show_labels = 0;
int show_files = 1;

// Fibonacci sphere for uniform distribution
void fibonacci_sphere(int level, int index, int total, double *x, double *y, double *z) {
    double radius = level * 15.0 + 10.0;
    double golden_ratio = (1.0 + sqrt(5.0)) / 2.0;
    double theta = 2.0 * M_PI * index / golden_ratio;
    double phi = acos(1.0 - 2.0 * (index + 0.5) / total);
    
    *x = radius * cos(theta) * sin(phi);
    *y = radius * sin(theta) * sin(phi);
    *z = radius * cos(phi);
}

// Parse line from files
int parse_line(const char *line, char *path, char *name, int *level) {
    if (!line || strlen(line) < 2) return 0;
    
    // Copy path
    strncpy(path, line, MAX_PATH_LEN - 1);
    path[MAX_PATH_LEN - 1] = '\0';
    
    // Extract name
    const char *last_slash = strrchr(line, '/');
    if (last_slash) {
        strncpy(name, last_slash + 1, MAX_NAME_LEN - 1);
    } else {
        strncpy(name, line, MAX_NAME_LEN - 1);
    }
    name[MAX_NAME_LEN - 1] = '\0';
    
    // Calculate level
    *level = 1;
    for (const char *p = line; *p; p++) {
        if (*p == '/') (*level)++;
    }
    
    return 1;
}

// Load data
int load_data(const char *dirs_file, const char *files_file) {
    printf("Loading directories...\n");
    
    FILE *f = fopen(dirs_file, "r");
    if (!f) {
        printf("Error: Cannot open %s\n", dirs_file);
        return 0;
    }
    
    char line[MAX_PATH_LEN];
    while (fgets(line, sizeof(line), f) && node_count < MAX_NODES) {
        line[strcspn(line, "\n")] = 0;
        if (strlen(line) < 2) continue;
        
        int level = 1;
        for (char *p = line; *p; p++) {
            if (*p == '/') level++;
        }
        
        Node *n = &nodes[node_count];
        strncpy(n->id, line, MAX_PATH_LEN - 1);
        const char *last_slash = strrchr(line, '/');
        strncpy(n->name, last_slash ? last_slash + 1 : line, MAX_NAME_LEN - 1);
        n->type = 0;  // directory
        n->level = level;
        n->color = 0x00FFFF00;  // cyan
        n->size = 4.0;
        n->parent_idx = -1;
        
        nodes_by_level[level]++;
        node_count++;
    }
    fclose(f);
    
    printf("Loaded %d directories\n", node_count);
    printf("Loading files (sampling 5%%)...\n");
    
    f = fopen(files_file, "r");
    if (!f) {
        printf("Error: Cannot open %s\n", files_file);
        return 0;
    }
    
    int file_count = 0;
    int sample_rate = 20;  // 1 in 20 = 5%
    int sample_idx = 0;
    
    while (fgets(line, sizeof(line), f) && node_count < MAX_NODES) {
        line[strcspn(line, "\n")] = 0;
        if (strlen(line) < 2) continue;
        
        sample_idx++;
        if (sample_idx % sample_rate != 0) continue;
        
        int level = 1;
        for (char *p = line; *p; p++) {
            if (*p == '/') level++;
        }
        
        if (level > 24) continue;  // Skip very deep files
        
        Node *n = &nodes[node_count];
        strncpy(n->id, line, MAX_PATH_LEN - 1);
        const char *last_slash = strrchr(line, '/');
        strncpy(n->name, last_slash ? last_slash + 1 : line, MAX_NAME_LEN - 1);
        n->type = 1;  // file
        n->level = level;
        n->color = 0xFF660000;  // orange
        n->size = 2.0;
        n->parent_idx = -1;
        
        nodes_by_level[level]++;
        node_count++;
        file_count++;
    }
    fclose(f);
    
    printf("Loaded %d files (sampled)\n", file_count);
    printf("Total nodes: %d\n", node_count);
    
    return 1;
}

// Calculate positions
void calculate_positions() {
    printf("Calculating positions...\n");
    
    // Track index per level for fibonacci distribution
    int *level_counts = calloc(25, sizeof(int));
    int *level_totals = calloc(25, sizeof(int));
    
    // Count nodes per level
    for (int i = 0; i < node_count; i++) {
        level_totals[nodes[i].level]++;
    }
    
    // Assign positions
    for (int i = 0; i < node_count; i++) {
        Node *n = &nodes[i];
        int level = n->level;
        
        // Fibonacci sphere distribution within level sphere
        int idx = level_counts[level];
        int total = level_totals[level];
        
        fibonacci_sphere(level, idx, total, &n->x, &n->y, &n->z);
        
        level_counts[level]++;
    }
    
    free(level_counts);
    free(level_totals);
    
    printf("Positions calculated\n");
}

// Draw text
void draw_text(float x, float y, const char *text, float r, float g, float b) {
    glColor3f(r, g, b);
    glRasterPos2f(x, y);
    for (const char *c = text; *c; c++) {
        // glutBitmapCharacter(GLUT_BITMAP_8_BY_13, *c);
    }
}

// Render scene
void render() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glLoadIdentity();
    
    // Camera
    gluLookAt(
        cam_target_x + cam_dist * sin(cam_rot_y) * cos(cam_rot_x),
        cam_target_y + cam_dist * sin(cam_rot_x),
        cam_target_z + cam_dist * cos(cam_rot_y) * cos(cam_rot_x),
        cam_target_x, cam_target_y, cam_target_z,
        0, 1, 0
    );
    
    // Draw nodes
    glBegin(GL_POINTS);
    for (int i = 0; i < node_count; i++) {
        Node *n = &nodes[i];
        
        // Filter by level
        if (n->level > max_level_view) continue;
        
        // Filter by type
        if (!show_files && n->type == 1) continue;
        
        // Color
        unsigned int c = n->color;
        float r = ((c >> 24) & 0xFF) / 255.0f;
        float g = ((c >> 16) & 0xFF) / 255.0f;
        float b = ((c >> 8) & 0xFF) / 255.0f;
        
        // Highlight hovered
        if (i == hovered_node) {
            r = 1.0f; g = 1.0f; b = 1.0f;
        }
        
        glColor4f(r, g, b, 0.8f);
        glVertex3f(n->x, n->y, n->z);
    }
    glEnd();
    
    // Draw connections for visible nodes
    glLineWidth(0.5f);
    glColor4f(0.3f, 0.3f, 0.5f, 0.3f);
    glBegin(GL_LINES);
    // Draw parent-child links for first few levels only
    // (too many otherwise)
    glEnd();
}

// Mouse callback
void mouse_button(GLFWwindow *win, int button, int action, int mods) {
    if (button == GLFW_MOUSE_BUTTON_LEFT) {
        if (action == GLFW_PRESS) {
            mouse_pressed = 1;
            glfwGetCursorPos(win, &last_mouse_x, &last_mouse_y);
        } else {
            mouse_pressed = 0;
        }
    }
}

// Mouse motion
void mouse_motion(GLFWwindow *win, double x, double y) {
    if (mouse_pressed) {
        double dx = x - last_mouse_x;
        double dy = y - last_mouse_y;
        
        cam_rot_y += dx * 0.005;
        cam_rot_x += dy * 0.005;
        
        if (cam_rot_x > 1.5) cam_rot_x = 1.5;
        if (cam_rot_x < -1.5) cam_rot_x = -1.5;
        
        last_mouse_x = x;
        last_mouse_y = y;
    }
}

// Scroll callback
void scroll(GLFWwindow *win, double xoffset, double yoffset) {
    cam_dist *= (1.0 - yoffset * 0.1);
    if (cam_dist < 10.0) cam_dist = 10.0;
    if (cam_dist > 2000.0) cam_dist = 2000.0;
}

// Keyboard callback
void keyboard(GLFWwindow *win, int key, int scancode, int action, int mods) {
    if (action == GLFW_PRESS) {
        switch (key) {
            case GLFW_KEY_ESCAPE:
                glfwSetWindowShouldClose(win, 1);
                break;
            case GLFW_KEY_L:
                show_labels = !show_labels;
                break;
            case GLFW_KEY_F:
                show_files = !show_files;
                break;
            case GLFW_KEY_UP:
                if (max_level_view < 24) max_level_view++;
                printf("Showing levels 1-%d\n", max_level_view);
                break;
            case GLFW_KEY_DOWN:
                if (max_level_view > 1) max_level_view--;
                printf("Showing levels 1-%d\n", max_level_view);
                break;
            case GLFW_KEY_R:
                cam_dist = 500.0;
                cam_rot_x = 0.0;
                cam_rot_y = 0.0;
                break;
        }
    }
}

// Resize callback
void reshape(GLFWwindow *win, int w, int h) {
    glViewport(0, 0, w, h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(60.0, (double)w / h, 1.0, 10000.0);
    glMatrixMode(GL_MODELVIEW);
}

int main(int argc, char **argv) {
    printf("=== File System Sphere Viewer ===\n\n");
    
    // Allocate
    nodes = malloc(MAX_NODES * sizeof(Node));
    if (!nodes) {
        printf("Error: Cannot allocate memory\n");
        return 1;
    }
    
    // Load data
    if (!load_data("fs_index/dirs.txt", "fs_index/files.txt")) {
        free(nodes);
        return 1;
    }
    
    // Calculate positions
    calculate_positions();
    
    // Init GLFW
    if (!glfwInit()) {
        printf("Error: Cannot initialize GLFW\n");
        free(nodes);
        return 1;
    }
    
    // Create window
    GLFWwindow *win = glfwCreateWindow(1920, 1080, "File System Sphere Viewer", NULL, NULL);
    if (!win) {
        printf("Error: Cannot create window\n");
        glfwTerminate();
        free(nodes);
        return 1;
    }
    
    glfwMakeContextCurrent(win);
    glfwSetMouseButtonCallback(win, mouse_button);
    glfwSetCursorPosCallback(win, mouse_motion);
    glfwSetScrollCallback(win, scroll);
    glfwSetKeyCallback(win, keyboard);
    glfwSetFramebufferSizeCallback(win, reshape);
    
    // OpenGL setup
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glClearColor(0.0, 0.02, 0.04, 1.0);
    
    // Point size
    glPointSize(3.0f);
    
    // Print controls
    printf("\nControls:\n");
    printf("  Mouse drag: Rotate\n");
    printf("  Scroll: Zoom\n");
    printf("  UP/DOWN: Change level visibility\n");
    printf("  F: Toggle files\n");
    printf("  L: Toggle labels\n");
    printf("  R: Reset view\n");
    printf("  ESC: Exit\n");
    
    // Main loop
    while (!glfwWindowShouldClose(win)) {
        render();
        glfwSwapBuffers(win);
        glfwPollEvents();
    }
    
    // Cleanup
    glfwDestroyWindow(win);
    glfwTerminate();
    free(nodes);
    
    return 0;
}
