/*
 * h3_layout.c - H3 Layout Algorithm Implementation
 * 
 * Based on "Exploring Large Graphs in 3D Hyperbolic Space" by Tamara Munzner
 * Stanford University, 1998
 * 
 * The H3 layout algorithm uses hemispherical packing to arrange nodes
 * in 3D hyperbolic space, providing exponential room for tree growth.
 */

#include "hyperbolic.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>

/* ============================================================================
 * Internal Constants
 * ============================================================================ */

#define H3_BASE_RADIUS    0.1     // Minimum hemisphere radius
#define H3_RADIUS_SCALE    1.5     // Scale factor for child hemispheres
#define H3_BAND_GROWTH     1.618   // Golden ratio for band spacing

/* ============================================================================
 * Internal Helper Functions
 * ============================================================================ */

// Calculate hemisphere area for given radius
static double compute_hemisphere_area(double radius) {
    return h3_sphere_area(radius);
}

// Calculate radius from hemisphere area
static double compute_radius_from_area(double area) {
    if (area <= 0) return H3_BASE_RADIUS;
    return h3_radius_from_area(area);
}

// Estimate subtree size (files + dirs)
// Subtree size is computed directly from node->file_count + node->dir_count
// static inline uint64_t estimate_subtree_size(H3Node *node) {
//     return node->file_count + node->dir_count;
// }

// Compare nodes by descendant count (descending order)
static int compare_by_descendants(const void *a, const void *b) {
    H3Node *na = *(H3Node**)a;
    H3Node *nb = *(H3Node**)b;
    uint64_t da = na->descendant_count;
    uint64_t db = nb->descendant_count;
    
    // Sort descending (largest first)
    if (db > da) return 1;
    if (db < da) return -1;
    return 0;
}

/* ============================================================================
 * Bottom-Up Pass: Compute Hemisphere Radii
 * ============================================================================ */

void h3_layout_compute_radii(H3Node *node) {
    if (node == NULL) return;
    
    // Leaf node: minimum hemisphere
    if (node->child_count == 0) {
        node->hemisphere_radius = H3_BASE_RADIUS;
        node->descendant_count = 0;
        node->file_count = (node->type == H3_NODE_FILE) ? 1 : 0;
        node->dir_count = (node->type == H3_NODE_DIR) ? 1 : 0;
        node->total_size = node->size;
        return;
    }
    
    // Recursively compute children first (bottom-up)
    node->descendant_count = 0;
    node->file_count = 0;
    node->dir_count = (node->type == H3_NODE_DIR) ? 1 : 0;
    node->total_size = node->size;
    
    for (uint32_t i = 0; i < node->child_count; i++) {
        h3_layout_compute_radii(node->children[i]);
        
        // Accumulate statistics
        node->descendant_count += node->children[i]->descendant_count + 1;
        node->file_count += node->children[i]->file_count;
        node->dir_count += node->children[i]->dir_count;
        node->total_size += node->children[i]->total_size;
    }
    
    // Calculate total area needed to contain all children
    // Children are arranged in concentric bands on the hemisphere
    
    // Sort children by descendant count (largest first for better packing)
    qsort(node->children, node->child_count, sizeof(H3Node*), compare_by_descendants);
    
    // Compute total area needed
    double total_area = 0.0;
    for (uint32_t i = 0; i < node->child_count; i++) {
        double child_radius = node->children[i]->hemisphere_radius;
        double child_area = compute_hemisphere_area(child_radius);
        
        // Scale by importance (descendant count)
        double importance = 1.0 + 0.1 * log1p(node->children[i]->descendant_count);
        child_area *= importance;
        
        total_area += child_area;
    }
    
    // Add spacing between bands
    double spacing_factor = 1.0 + 0.05 * sqrt(node->child_count);
    total_area *= spacing_factor;
    
    // Calculate parent hemisphere radius
    node->hemisphere_radius = compute_radius_from_area(total_area);
    
    // Ensure minimum radius
    if (node->hemisphere_radius < H3_BASE_RADIUS) {
        node->hemisphere_radius = H3_BASE_RADIUS;
    }
}

/* ============================================================================
 * Circle Packing: Arrange Children on Hemisphere
 * ============================================================================ */

void h3_layout_pack_children(H3Node *parent) {
    if (parent == NULL || parent->child_count == 0) return;
    
    // Children are already sorted by descendant count (largest first)
    // Place largest at the pole, others in concentric bands
    
    double R = parent->hemisphere_radius;
    double current_band_radius = 0.0;
    uint32_t band_start = 0;
    uint32_t band_index = 0;
    double band_circumference = 0.0;
    
    for (uint32_t i = 0; i < parent->child_count; i++) {
        H3Node *child = parent->children[i];
        double child_r = child->hemisphere_radius;
        
        // First child at pole, others in bands
        if (i == 0) {
            band_index = 0;
            band_start = 0;
            current_band_radius = child_r;
        } else {
            // Calculate required spacing
            double required_spacing = 2.0 * child_r * H3_RADIUS_SCALE;
            double next_band_radius = current_band_radius + required_spacing;
            
            // Check if next band still fits within parent hemisphere
            if (next_band_radius + child_r < R) {
                // Start new band?
                if (band_index == 0 || 
                    current_band_radius + required_spacing > R * 0.9) {
                    // Start new band
                    band_index++;
                    band_start = i;
                    current_band_radius = next_band_radius;
                    band_circumference = 0.0;
                }
            } else {
                // Clamp to fit
                current_band_radius = (current_band_radius + child_r < R * 0.95) 
                    ? current_band_radius : R * 0.9;
            }
        }
        
        // Calculate angular position - distribute nodes in bands
        uint32_t nodes_in_band = (band_index == 0) ? 1 : (i - band_start + 1);
        double angle_spacing = (2.0 * H3_PI) / nodes_in_band;
        double angle = angle_spacing * (i - band_start);
        
        // Position on hemisphere surface (Klein model)
        // For Klein model, we project onto unit ball
        double radial_dist = current_band_radius / R;  // Normalized distance from pole
        
        child->position.x = radial_dist * cos(angle);
        child->position.y = radial_dist * sin(angle);
        child->position.z = sqrt(1.0 - radial_dist * radial_dist);  // Height on hemisphere
        
        // Record layout state
        child->band_index = band_index;
        child->band_position = i - band_start;
        child->angular_position = angle;
        
        // Update band state
        band_circumference += 2.0 * child_r;
        
        // Clamp to stay inside unit ball
        h3_normalize(&child->position);
    }
}

/* ============================================================================
 * Top-Down Pass: Position Children in Hyperbolic Space
 * ============================================================================ */

void h3_layout_position_children(H3Node *node, H3Point parent_pos) {
    if (node == NULL) return;
    
    // Combine parent position with local position
    // In hyperbolic space, we translate from parent origin
    
    if (node->parent != NULL) {
        // This node's position is relative to parent
        // Apply hyperbolic translation from parent to this position
        
        // For now, use simple addition (approximation for small distances)
        // In full implementation, use hyperbolic translation formula
        
        // Convert local position on hemisphere to absolute position
        // The hemisphere is centered at parent position
        
        // Scale by parent's hemisphere radius
        double scale = node->parent->hemisphere_radius;
        
        node->position.x = parent_pos.x + node->position.x * scale;
        node->position.y = parent_pos.y + node->position.y * scale;
        node->position.z = parent_pos.z + node->position.z * scale;
        
        // Normalize to stay inside unit ball
        h3_normalize(&node->position);
        
        // Record depth
        node->depth = node->parent->depth + 1;
    } else {
        // Root node at origin
        node->position = (H3Point){0, 0, 0, 1};
        node->depth = 0;
    }
    
    // Pack children on this node's hemisphere
    h3_layout_pack_children(node);
    
    // Recursively position children
    for (uint32_t i = 0; i < node->child_count; i++) {
        h3_layout_position_children(node->children[i], node->position);
    }
}

/* ============================================================================
 * Main Layout Function
 * ============================================================================ */

void h3_layout_tree(H3Tree *tree) {
    if (tree == NULL || tree->root == NULL) return;
    
    log_info("Starting H3 layout for %lu nodes...", tree->node_count);
    
    // Step 1: Compute hemisphere radii (bottom-up)
    log_debug("Phase 1: Computing hemisphere radii...");
    h3_layout_compute_radii(tree->root);
    
    // Step 2: Position root at origin
    log_debug("Phase 2: Positioning root...");
    tree->root->position = (H3Point){0, 0, 0, 1};
    tree->root->depth = 0;
    
    // Step 3: Position children on hemisphere (top-down)
    log_debug("Phase 3: Packing children...");
    h3_layout_pack_children(tree->root);
    
    // Step 4: Recursively layout all nodes
    log_debug("Phase 4: Recursive positioning...");
    for (uint32_t i = 0; i < tree->root->child_count; i++) {
        h3_layout_position_children(tree->root->children[i], tree->root->position);
    }
    
    // Step 5: Initialize focus point
    tree->focus = tree->root->position;
    tree->target_focus = tree->root->position;
    tree->zoom = 1.0;
    tree->target_zoom = 1.0;
    
    // Step 6: Update statistics
    tree->total_files = tree->root->file_count;
    tree->total_dirs = tree->root->dir_count;
    tree->total_size = tree->root->total_size;
    
    // Calculate max depth
    uint32_t max_depth = 0;
    for (uint64_t i = 0; i < tree->node_count; i++) {
        if (tree->nodes[i]->depth > max_depth) {
            max_depth = tree->nodes[i]->depth;
        }
    }
    tree->max_depth = max_depth;
    
    log_info("H3 layout complete: %lu files, %lu dirs, max depth %u",
             tree->total_files, tree->total_dirs, max_depth);
}

/* ============================================================================
 * Incremental Update (for real-time changes)
 * ============================================================================ */

void h3_layout_update(H3Tree *tree, H3Node *changed_node) {
    if (tree == NULL || changed_node == NULL) return;
    
    // Find the highest ancestor that needs radius recomputation
    H3Node *update_root = changed_node;
    while (update_root->parent != NULL) {
        update_root = update_root->parent;
        
        // Check if radius would change significantly
        // For now, just update all ancestors
        (void)update_root;  // Suppress unused warning
    }
    
    // Re-compute from the root (could be optimized)
    h3_layout_compute_radii(tree->root);
    
    // Re-position children
    h3_layout_pack_children(tree->root);
    for (uint32_t i = 0; i < tree->root->child_count; i++) {
        h3_layout_position_children(tree->root->children[i], tree->root->position);
    }
}

/* ============================================================================
 * Utility: Find node by screen position
 * ============================================================================ */

H3Node *h3_layout_find_node_at(H3Tree *tree, double screen_x, double screen_y,
                                H3RenderContext *ctx) {
    (void)ctx;  // Parameter reserved for future use (frustum culling)
    if (tree == NULL) return NULL;
    
    // Find closest node to screen position
    H3Node *closest = NULL;
    double min_dist = INFINITY;
    
    for (uint64_t i = 0; i < tree->node_count; i++) {
        H3Node *node = tree->nodes[i];
        
        // Check if visible and close to screen position
        if (node->visible) {
            double dx = node->screen_x - screen_x;
            double dy = node->screen_y - screen_y;
            double dist = sqrt(dx * dx + dy * dy);
            
            // Account for node size
            double hit_radius = node->projected_size / 2.0;
            
            if (dist < hit_radius && dist < min_dist) {
                min_dist = dist;
                closest = node;
            }
        }
    }
    
    return closest;
}

/* ============================================================================
 * Color assignment based on file type and depth
 * ============================================================================ */

void h3_layout_assign_colors(H3Tree *tree) {
    if (tree == NULL || tree->root == NULL) return;
    
    for (uint64_t i = 0; i < tree->node_count; i++) {
        H3Node *node = tree->nodes[i];
        
        // Base color by type
        switch (node->type) {
            case H3_NODE_DIR:
                node->color[0] = 0.3f;
                node->color[1] = 0.5f;
                node->color[2] = 1.0f;
                break;
            case H3_NODE_FILE:
                node->color[0] = 0.8f;
                node->color[1] = 0.8f;
                node->color[2] = 0.8f;
                break;
            case H3_NODE_SYMLINK:
                node->color[0] = 0.5f;
                node->color[1] = 0.8f;
                node->color[2] = 0.3f;
                break;
            default:
                node->color[0] = 0.5f;
                node->color[1] = 0.5f;
                node->color[2] = 0.5f;
                break;
        }
        node->color[3] = 1.0f;
        
        // Adjust by depth (darker with depth)
        float depth_factor = 1.0f - 0.05f * node->depth;
        depth_factor = h3_clamp(depth_factor, 0.3f, 1.0f);
        
        node->color[0] *= depth_factor;
        node->color[1] *= depth_factor;
        node->color[2] *= depth_factor;
        
        // Size based on file size (log scale)
        if (node->type == H3_NODE_FILE && node->size > 0) {
            double log_size = log10((double)node->size);
            node->projected_size = 1.0f + 0.5f * log_size;
        } else if (node->type == H3_NODE_DIR) {
            // Size based on child count
            node->projected_size = 2.0f + 0.1f * sqrt((double)node->descendant_count);
        } else {
            node->projected_size = 1.0f;
        }
        
        // Clamp size
        node->projected_size = h3_clamp(node->projected_size, 0.5f, 20.0f);
    }
}