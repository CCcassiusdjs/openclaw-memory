// File System Sphere Viewer - OpenGL/GLX (no external deps beyond OpenGL and X11)
// Compile: gcc -O3 -o fs_viewer fs_viewer_glx.c -lGL -lGLU -lX11 -lm

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glx.h>
#include <X11/Xlib.h>
#include <X11/keysym.h>

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
    float r, g, b;
} Node;

Node *nodes = NULL;
int node_count = 0;

// Camera
double cam_dist = 500.0;
double cam_rot_x = 0.3;
double cam_rot_y = 0.0;
double cam_target_x = 0.0;
double cam_target_y = 0.0;
double cam_target_z = 0.0;

// View
int max_level = 5;
int show_files = 1;

// X11/GLX
Display *dpy;
Window win;
GLXContext ctx;
int win_width = 1920;
int win_height = 1080;

// Fibonacci sphere for uniform distribution
void fibonacci_sphere(int level, int index, int total, double *x, double *y, double *z) {
    double radius = level * 12.0 + 8.0;
    double golden_ratio = (1.0 + sqrt(5.0)) / 2.0;
    double theta = 2.0 * M_PI * index / golden_ratio;
    double phi = acos(1.0 - 2.0 * (index + 0.5) / total);
    
    *x = radius * cos(theta) * sin(phi);
    *y = radius * sin(theta) * sin(phi);
    *z = radius * cos(phi);
}

// Load data from files
int load_data(const char *dirs_file, const char *files_file) {
    FILE *f;
    char line[MAX_PATH_LEN];
    int level_counts[25] = {0};
    
    nodes = malloc(MAX_NODES * sizeof(Node));
    if (!nodes) {
        printf("Error: Cannot allocate memory\n");
        return 0;
    }
    
    // Load directories
    printf("Loading directories...\n");
    f = fopen(dirs_file, "r");
    if (!f) { printf("Error: Cannot open %s\n", dirs_file); return 0; }
    
    while (fgets(line, sizeof(line), f) && node_count < MAX_NODES) {
        line[strcspn(line, "\n")] = 0;
        if (strlen(line) < 2) continue;
        
        Node *n = &nodes[node_count];
        strncpy(n->id, line, MAX_PATH_LEN - 1);
        
        const char *last_slash = strrchr(line, '/');
        strncpy(n->name, last_slash ? last_slash + 1 : line, MAX_NAME_LEN - 1);
        
        n->type = 0;
        n->level = 1;
        for (char *p = line; *p; p++) if (*p == '/') n->level++;
        
        n->r = 0.0f; n->g = 1.0f; n->b = 1.0f;  // cyan for dirs
        n->size = 4.0;
        
        node_count++;
    }
    fclose(f);
    printf("Loaded %d directories\n", node_count);
    
    // Load files (sampled)
    printf("Loading files (5%% sample)...\n");
    int sample_idx = 0;
    f = fopen(files_file, "r");
    if (!f) { printf("Error: Cannot open %s\n", files_file); return 0; }
    
    while (fgets(line, sizeof(line), f) && node_count < MAX_NODES) {
        line[strcspn(line, "\n")] = 0;
        if (strlen(line) < 2) continue;
        
        sample_idx++;
        if (sample_idx % 20 != 0) continue;  // 5% sample
        
        Node *n = &nodes[node_count];
        strncpy(n->id, line, MAX_PATH_LEN - 1);
        
        const char *last_slash = strrchr(line, '/');
        strncpy(n->name, last_slash ? last_slash + 1 : line, MAX_NAME_LEN - 1);
        
        n->type = 1;
        n->level = 1;
        for (char *p = line; *p; p++) if (*p == '/') n->level++;
        
        if (n->level > 24) continue;
        
        n->r = 1.0f; n->g = 0.4f; n->b = 0.0f;  // orange for files
        n->size = 2.0;
        
        node_count++;
    }
    fclose(f);
    printf("Total nodes: %d\n", node_count);
    
    return 1;
}

// Calculate positions using Fibonacci sphere per level
void calculate_positions() {
    printf("Calculating positions...\n");
    
    // Count nodes per level
    int level_counts[25] = {0};
    int level_current[25] = {0};
    
    for (int i = 0; i < node_count; i++) {
        level_counts[nodes[i].level]++;
    }
    
    for (int i = 0; i < node_count; i++) {
        Node *n = &nodes[i];
        int level = n->level;
        int idx = level_current[level]++;
        int total = level_counts[level];
        
        fibonacci_sphere(level, idx, total, &n->x, &n->y, &n->z);
    }
    
    printf("Positions calculated\n");
}

// Render scene
void render() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glLoadIdentity();
    
    // Camera position
    gluLookAt(
        cam_target_x + cam_dist * sin(cam_rot_y) * cos(cam_rot_x),
        cam_target_y + cam_dist * sin(cam_rot_x),
        cam_target_z + cam_dist * cos(cam_rot_y) * cos(cam_rot_x),
        cam_target_x, cam_target_y, cam_target_z,
        0, 1, 0
    );
    
    // Draw nodes as points
    glBegin(GL_POINTS);
    for (int i = 0; i < node_count; i++) {
        Node *n = &nodes[i];
        
        if (n->level > max_level) continue;
        if (!show_files && n->type == 1) continue;
        
        glColor4f(n->r, n->g, n->b, 0.85f);
        glVertex3f(n->x, n->y, n->z);
    }
    glEnd();
    
    // Draw level indicators (spheres)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
    for (int l = 1; l <= max_level; l++) {
        double radius = l * 12.0 + 8.0;
        glColor4f(0.3f, 0.3f, 0.5f, 0.2f);
        
        // Draw wireframe sphere
        gluSphere(gluNewQuadric(), radius, 16, 8);
    }
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
    
    glXSwapBuffers(dpy, win);
}

// Handle keyboard input
void handle_key(KeySym key) {
    switch (key) {
        case XK_Escape:
            exit(0);
        case XK_Up:
            if (max_level < 24) max_level++;
            printf("Level: %d\n", max_level);
            break;
        case XK_Down:
            if (max_level > 1) max_level--;
            printf("Level: %d\n", max_level);
            break;
        case XK_f:
            show_files = !show_files;
            printf("Show files: %s\n", show_files ? "ON" : "OFF");
            break;
        case XK_r:
            cam_dist = 500.0;
            cam_rot_x = 0.3;
            cam_rot_y = 0.0;
            printf("View reset\n");
            break;
    }
}

// Handle mouse motion for rotation
void handle_motion(int dx, int dy, int button) {
    if (button == 1) {  // Left button = rotate
        cam_rot_y += dx * 0.005;
        cam_rot_x += dy * 0.005;
        if (cam_rot_x > 1.5) cam_rot_x = 1.5;
        if (cam_rot_x < -1.5) cam_rot_x = -1.5;
    }
}

// Main loop
int main(int argc, char **argv) {
    printf("=== File System Sphere Viewer (GLX) ===\n\n");
    
    // Load data
    if (!load_data("fs_index/dirs.txt", "fs_index/files.txt")) {
        return 1;
    }
    
    // Calculate positions
    calculate_positions();
    
    // Open X display
    dpy = XOpenDisplay(NULL);
    if (!dpy) {
        printf("Error: Cannot open X display\n");
        return 1;
    }
    
    // Choose visual
    int attr[] = {
        GLX_RGBA,
        GLX_DEPTH_SIZE, 24,
        GLX_DOUBLEBUFFER,
        None
    };
    XVisualInfo *vi = glXChooseVisual(dpy, DefaultScreen(dpy), attr);
    if (!vi) {
        printf("Error: Cannot choose visual\n");
        return 1;
    }
    
    // Create window
    Window root = RootWindow(dpy, vi->screen);
    XSetWindowAttributes swa;
    swa.colormap = XCreateColormap(dpy, root, vi->visual, AllocNone);
    swa.border_pixel = 0;
    swa.event_mask = ExposureMask | KeyPressMask | ButtonPressMask | ButtonMotionMask;
    
    win = XCreateWindow(dpy, root, 0, 0, win_width, win_height, 0,
        vi->depth, InputOutput, vi->visual, CWColormap | CWBorderPixel | CWEventMask, &swa);
    
    XMapWindow(dpy, win);
    XStoreName(dpy, win, "File System Sphere Viewer");
    
    // Create GLX context
    ctx = glXCreateContext(dpy, vi, NULL, True);
    glXMakeCurrent(dpy, win, ctx);
    
    // OpenGL setup
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glClearColor(0.0f, 0.02f, 0.04f, 1.0f);
    glPointSize(3.0f);
    
    // Perspective
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(60.0, (double)win_width / win_height, 1.0, 10000.0);
    glMatrixMode(GL_MODELVIEW);
    
    // Print controls
    printf("\n=== Controls ===\n");
    printf("  Mouse drag: Rotate\n");
    printf("  Scroll: Zoom (not implemented in this version)\n");
    printf("  UP/DOWN: Change visible levels (current: %d)\n", max_level);
    printf("  F: Toggle files\n");
    printf("  R: Reset view\n");
    printf("  ESC: Exit\n\n");
    
    // Event loop
    XEvent event;
    int button_pressed = 0;
    int last_x = 0, last_y = 0;
    
    while (1) {
        while (XPending(dpy)) {
            XNextEvent(dpy, &event);
            
            switch (event.type) {
                case Expose:
                    render();
                    break;
                case KeyPress: {
                    KeySym key = XLookupKeysym(&event.xkey, 0);
                    handle_key(key);
                    break;
                }
                case ButtonPress:
                    button_pressed = event.xbutton.button;
                    last_x = event.xbutton.x;
                    last_y = event.xbutton.y;
                    break;
                case MotionNotify:
                    if (button_pressed == 1) {
                        int dx = event.xmotion.x - last_x;
                        int dy = event.xmotion.y - last_y;
                        handle_motion(dx, dy, button_pressed);
                        last_x = event.xmotion.x;
                        last_y = event.xmotion.y;
                    }
                    break;
            }
        }
        
        render();
    }
    
    return 0;
}
