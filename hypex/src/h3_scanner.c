/*
 * h3_scanner.c - File System Scanner
 * 
 * Scans file system and builds tree structure for H3 layout.
 * Uses recursive directory traversal with depth limiting.
 */

#define _GNU_SOURCE
#define _POSIX_C_SOURCE 200809L

#include "hyperbolic.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <errno.h>
#include <fnmatch.h>

// Default hemisphere radius (must match h3_layout.c)
#ifndef H3_BASE_RADIUS
#define H3_BASE_RADIUS 0.1
#endif

/* ============================================================================
 * Node Creation
 * ============================================================================ */

H3Node *h3_create_node(const char *path, H3Node *parent) {
    H3Node *node = calloc(1, sizeof(H3Node));
    if (!node) return NULL;
    
    // Copy path
    node->path = strdup(path);
    if (!node->path) {
        free(node);
        return NULL;
    }
    
    // Extract name from path
    const char *name = strrchr(path, '/');
    node->name = name ? strdup(name + 1) : strdup(path);
    node->name_len = strlen(node->name);
    
    // Parent
    node->parent = parent;
    node->depth = parent ? parent->depth + 1 : 0;
    
    // Get file info
    struct stat st;
    if (lstat(path, &st) == 0) {
        node->size = st.st_size;
        node->mtime = st.st_mtime;
        node->atime = st.st_atime;
        node->mode = st.st_mode;
        
        // Determine type
        if (S_ISDIR(st.st_mode)) {
            node->type = H3_NODE_DIR;
        } else if (S_ISLNK(st.st_mode)) {
            node->type = H3_NODE_SYMLINK;
        } else if (S_ISREG(st.st_mode)) {
            node->type = H3_NODE_FILE;
        } else {
            node->type = H3_NODE_SPECIAL;
        }
    } else {
        node->size = 0;
        node->mtime = 0;
        node->type = H3_NODE_FILE;
    }
    
    // Initialize layout state
    node->position = (H3Point){0, 0, 0, 1};
    node->hemisphere_radius = H3_BASE_RADIUS;
    
    // Default color (will be set by layout)
    node->color[0] = 0.8f;
    node->color[1] = 0.8f;
    node->color[2] = 0.8f;
    node->color[3] = 1.0f;
    
    node->projected_size = 1.0f;
    node->visible = true;
    node->selected = false;
    node->highlighted = false;
    
    return node;
}

/* ============================================================================
 * Node Cleanup
 * ============================================================================ */

void h3_destroy_node(H3Node *node) {
    if (!node) return;
    
    // Free children
    for (uint32_t i = 0; i < node->child_count; i++) {
        h3_destroy_node(node->children[i]);
    }
    free(node->children);
    
    // Free self
    free(node->path);
    free(node->name);
    free(node);
}

/* ============================================================================
 * Tree Management
 * ============================================================================ */

H3Tree *h3_tree_create(void) {
    H3Tree *tree = calloc(1, sizeof(H3Tree));
    if (!tree) return NULL;
    
    tree->node_capacity = H3_INITIAL_CAPACITY;
    tree->nodes = malloc(tree->node_capacity * sizeof(H3Node*));
    tree->id_to_index = malloc(tree->node_capacity * sizeof(uint64_t));
    
    if (!tree->nodes || !tree->id_to_index) {
        free(tree->nodes);
        free(tree->id_to_index);
        free(tree);
        return NULL;
    }
    
    tree->node_count = 0;
    tree->next_id = 0;
    tree->zoom = 1.0f;
    tree->target_zoom = 1.0f;
    
    pthread_mutex_init(&tree->lock, NULL);
    
    return tree;
}

void h3_tree_destroy(H3Tree *tree) {
    if (!tree) return;
    
    pthread_mutex_lock(&tree->lock);
    
    // Free all nodes
    if (tree->root) {
        h3_destroy_node(tree->root);
    }
    
    free(tree->nodes);
    free(tree->id_to_index);
    
    pthread_mutex_unlock(&tree->lock);
    pthread_mutex_destroy(&tree->lock);
    
    free(tree);
}

int h3_tree_add_node(H3Tree *tree, H3Node *node) {
    if (!tree || !node) return -1;
    
    pthread_mutex_lock(&tree->lock);
    
    // Expand capacity if needed
    if (tree->node_count >= tree->node_capacity) {
        uint64_t new_capacity = tree->node_capacity * 2;
        H3Node **new_nodes = realloc(tree->nodes, new_capacity * sizeof(H3Node*));
        uint64_t *new_ids = realloc(tree->id_to_index, new_capacity * sizeof(uint64_t));
        
        if (!new_nodes || !new_ids) {
            pthread_mutex_unlock(&tree->lock);
            return -1;
        }
        
        tree->nodes = new_nodes;
        tree->id_to_index = new_ids;
        tree->node_capacity = new_capacity;
    }
    
    // Add node
    node->id = tree->next_id++;
    tree->nodes[tree->node_count] = node;
    tree->id_to_index[tree->node_count] = node->id;
    tree->node_count++;
    
    pthread_mutex_unlock(&tree->lock);
    return 0;
}

H3Node *h3_tree_find_node(H3Tree *tree, const char *path) {
    if (!tree || !path) return NULL;
    
    uint64_t hash = h3_hash_path(path);
    
    for (uint64_t i = 0; i < tree->node_count; i++) {
        H3Node *node = tree->nodes[i];
        if (node->hash == hash && strcmp(node->path, path) == 0) {
            return node;
        }
    }
    
    return NULL;
}

H3Node *h3_tree_find_by_id(H3Tree *tree, uint64_t id) {
    if (!tree) return NULL;
    
    for (uint64_t i = 0; i < tree->node_count; i++) {
        if (tree->nodes[i]->id == id) {
            return tree->nodes[i];
        }
    }
    
    return NULL;
}

void h3_tree_remove_node(H3Tree *tree, H3Node *node) {
    if (!tree || !node) return;
    
    pthread_mutex_lock(&tree->lock);
    
    // Find and remove from array
    for (uint64_t i = 0; i < tree->node_count; i++) {
        if (tree->nodes[i] == node) {
            // Shift remaining nodes
            for (uint64_t j = i; j < tree->node_count - 1; j++) {
                tree->nodes[j] = tree->nodes[j + 1];
                tree->id_to_index[j] = tree->id_to_index[j + 1];
            }
            tree->node_count--;
            break;
        }
    }
    
    // Remove from parent's children
    if (node->parent) {
        for (uint32_t i = 0; i < node->parent->child_count; i++) {
            if (node->parent->children[i] == node) {
                // Shift remaining children
                for (uint32_t j = i; j < node->parent->child_count - 1; j++) {
                    node->parent->children[j] = node->parent->children[j + 1];
                }
                node->parent->child_count--;
                break;
            }
        }
    }
    
    pthread_mutex_unlock(&tree->lock);
    
    // Free node
    h3_destroy_node(node);
}

/* ============================================================================
 * Add Child to Node
 * ============================================================================ */

static int add_child(H3Node *parent, H3Node *child) {
    if (!parent || !child) return -1;
    
    // Expand capacity if needed
    if (parent->child_count >= parent->child_capacity) {
        uint32_t new_capacity = parent->child_capacity == 0 ? 8 : parent->child_capacity * 2;
        H3Node **new_children = realloc(parent->children, new_capacity * sizeof(H3Node*));
        
        if (!new_children) return -1;
        
        parent->children = new_children;
        parent->child_capacity = new_capacity;
    }
    
    parent->children[parent->child_count++] = child;
    child->parent = parent;
    child->depth = parent->depth + 1;
    
    return 0;
}

/* ============================================================================
 * Exclude Patterns
 * ============================================================================ */

static bool should_exclude(const char *name, H3Config *config) {
    if (!config->exclude_patterns) return false;
    
    for (uint32_t i = 0; i < config->exclude_count; i++) {
        if (fnmatch(config->exclude_patterns[i], name, 0) == 0) {
            return true;
        }
    }
    
    // Default excludes
    const char *default_excludes[] = {
        ".git", ".svn", ".hg", ".bzr",        // Version control
        "node_modules", "bower_components",   // Dependencies
        "__pycache__", "*.pyc",                // Python cache
        ".cache", ".local", "tmp",             // Cache/temp
        NULL
    };
    
    for (int i = 0; default_excludes[i]; i++) {
        if (fnmatch(default_excludes[i], name, 0) == 0) {
            return true;
        }
    }
    
    return false;
}

/* ============================================================================
 * Recursive Directory Scan
 * ============================================================================ */

static int scan_directory(H3Node *parent, H3Tree *tree, H3Config *config, uint32_t depth) {
    if (!parent || !tree || !config) return -1;
    
    // Depth limit
    if (depth > config->max_depth) return 0;
    
    // File count limit
    if (config->max_files > 0 && tree->node_count >= config->max_files) return 0;
    
    DIR *dir = opendir(parent->path);
    if (!dir) {
        log_debug("Cannot open directory: %s (%s)", parent->path, strerror(errno));
        return 0;
    }
    
    struct dirent *entry;
    int result = 0;
    
    while ((entry = readdir(dir)) != NULL) {
        // Skip . and ..
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
            continue;
        }
        
        // Check exclude patterns
        if (should_exclude(entry->d_name, config)) {
            continue;
        }
        
        // Build full path
        char child_path[H3_MAX_PATH];
        snprintf(child_path, sizeof(child_path), "%s/%s", parent->path, entry->d_name);
        
        // Create child node
        H3Node *child = h3_create_node(child_path, parent);
        if (!child) {
            log_debug("Failed to create node: %s", child_path);
            continue;
        }
        
        // Add to tree
        if (h3_tree_add_node(tree, child) != 0) {
            h3_destroy_node(child);
            continue;
        }
        
        // Add to parent
        if (add_child(parent, child) != 0) {
            continue;
        }
        
        // Recurse if directory
        if (child->type == H3_NODE_DIR) {
            result = scan_directory(child, tree, config, depth + 1);
            if (result != 0) break;
        }
        
        // Progress indicator for large scans
        if (tree->node_count % 10000 == 0) {
            log_info("Scanned %lu nodes...", tree->node_count);
        }
    }
    
    closedir(dir);
    return result;
}

/* ============================================================================
 * Update Statistics (Bottom-up)
 * ============================================================================ */

void h3_update_node_stats(H3Node *node) {
    if (!node) return;
    
    // Reset counters
    node->file_count = 0;
    node->dir_count = 0;
    node->descendant_count = 0;
    node->total_size = node->size;
    
    // Accumulate from children
    for (uint32_t i = 0; i < node->child_count; i++) {
        H3Node *child = node->children[i];
        h3_update_node_stats(child);
        
        node->file_count += child->file_count;
        node->dir_count += child->dir_count;
        node->descendant_count += child->descendant_count + 1;
        node->total_size += child->total_size;
    }
    
    // Self
    if (node->type == H3_NODE_FILE) {
        node->file_count = 1;
    } else if (node->type == H3_NODE_DIR) {
        node->dir_count = 1;
    }
}

/* ============================================================================
 * Main Scan Function
 * ============================================================================ */

int h3_scan_filesystem(const char *root_path, H3Tree *tree, H3Config *config) {
    if (!root_path || !tree || !config) return -1;
    
    log_info("Scanning file system: %s", root_path);
    
    // Create root node
    H3Node *root = h3_create_node(root_path, NULL);
    if (!root) {
        log_error("Failed to create root node");
        return -1;
    }
    
    // Set as tree root
    tree->root = root;
    if (h3_tree_add_node(tree, root) != 0) {
        h3_destroy_node(root);
        return -1;
    }
    
    // Recursive scan
    int result = scan_directory(root, tree, config, 0);
    if (result != 0) {
        log_error("Scan failed: %d", result);
        return result;
    }
    
    // Update statistics (bottom-up)
    log_info("Updating statistics...");
    h3_update_node_stats(root);
    
    // Update tree stats
    tree->total_files = root->file_count;
    tree->total_dirs = root->dir_count;
    tree->total_size = root->total_size;
    
    log_info("Scan complete: %lu files, %lu directories, %.2f GB",
             tree->total_files, 
             tree->total_dirs,
             (double)tree->total_size / (1024.0 * 1024.0 * 1024.0));
    
    return 0;
}

/* ============================================================================
 * Incremental Update (Apply Event)
 * ============================================================================ */

int h3_apply_event(H3Tree *tree, H3Event *event) {
    if (!tree || !event) return -1;
    
    pthread_mutex_lock(&tree->lock);
    
    switch (event->type) {
        case H3_EVENT_CREATE: {
            // Find parent
            char *parent_path = strdup(event->path);
            char *last_slash = strrchr(parent_path, '/');
            if (last_slash) *last_slash = '\0';
            
            H3Node *parent = h3_tree_find_node(tree, parent_path);
            free(parent_path);
            
            if (parent) {
                // Create new node
                H3Node *node = h3_create_node(event->path, parent);
                if (node) {
                    h3_tree_add_node(tree, node);
                    add_child(parent, node);
                    h3_update_node_stats(parent);
                }
            }
            break;
        }
        
        case H3_EVENT_DELETE: {
            H3Node *node = h3_tree_find_node(tree, event->path);
            if (node) {
                h3_tree_remove_node(tree, node);
            }
            break;
        }
        
        case H3_EVENT_MODIFY: {
            H3Node *node = h3_tree_find_node(tree, event->path);
            if (node) {
                struct stat st;
                if (stat(event->path, &st) == 0) {
                    node->size = st.st_size;
                    node->mtime = st.st_mtime;
                    // Update parent stats
                    if (node->parent) {
                        h3_update_node_stats(node->parent);
                    }
                }
            }
            break;
        }
        
        case H3_EVENT_MOVE: {
            // Delete old, create new
            if (event->old_path) {
                H3Node *node = h3_tree_find_node(tree, event->old_path);
                if (node) {
                    h3_tree_remove_node(tree, node);
                }
            }
            // Create new (same as CREATE)
            // ...
            break;
        }
        
        default:
            break;
    }
    
    pthread_mutex_unlock(&tree->lock);
    
    // Re-run layout
    h3_layout_tree(tree);
    
    return 0;
}