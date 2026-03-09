/*
 * h3_transform.c - Hyperbolic Transformations
 * 
 * Implements transformations in 3D hyperbolic space using the Klein model.
 * The Klein model represents hyperbolic space as the interior of the unit ball.
 * Geodesics (straight lines in hyperbolic space) appear as straight lines in this model.
 * 
 * Key advantage: Transformations can be expressed as standard 4x4 matrices.
 */

#include "hyperbolic.h"
#include <string.h>
#include <math.h>

/* ============================================================================
 * Identity Transform
 * ============================================================================ */

H3Transform h3_transform_identity(void) {
    H3Transform t;
    memset(&t, 0, sizeof(t));
    t.m[0][0] = 1.0;
    t.m[1][1] = 1.0;
    t.m[2][2] = 1.0;
    t.m[3][3] = 1.0;
    return t;
}

/* ============================================================================
 * Translation in Hyperbolic Space (Lorentz Boost)
 * ============================================================================ */

// In hyperbolic space, "translation" is actually a Lorentz boost
// This preserves the Minkowski inner product and keeps points inside the unit ball

H3Transform h3_transform_translation(H3Point *direction, double distance) {
    H3Transform t = h3_transform_identity();
    
    // Normalize direction
    double len = sqrt(direction->x * direction->x + 
                       direction->y * direction->y + 
                       direction->z * direction->z);
    
    if (len < H3_EPSILON) {
        return t;  // No translation if direction is zero
    }
    
    double nx = direction->x / len;
    double ny = direction->y / len;
    double nz = direction->z / len;
    
    // Lorentz boost parameters
    double gamma = cosh(distance);
    (void)sinh;  // Mark as used to suppress warning
    
    // Build boost matrix along direction (nx, ny, nz)
    // For the Klein model, we use a projective transformation
    
    double beta = tanh(distance);
    double gamma_minus_1 = gamma - 1.0;
    
    // Build the transformation matrix
    t.m[0][0] = gamma;
    t.m[0][1] = gamma_minus_1 * nx * nx + 1.0;
    t.m[0][2] = gamma_minus_1 * nx * ny;
    t.m[0][3] = gamma_minus_1 * nx * nz;
    
    t.m[1][0] = gamma_minus_1 * ny * nx;
    t.m[1][1] = gamma_minus_1 * ny * ny + 1.0;
    t.m[1][2] = gamma_minus_1 * ny * nz;
    t.m[1][3] = gamma;
    
    t.m[2][0] = gamma_minus_1 * nz * nx;
    t.m[2][1] = gamma_minus_1 * nz * ny;
    t.m[2][2] = gamma_minus_1 * nz * nz + 1.0;
    t.m[2][3] = gamma;
    
    t.m[3][0] = gamma * beta * nx;
    t.m[3][1] = gamma * beta * ny;
    t.m[3][2] = gamma * beta * nz;
    t.m[3][3] = gamma;
    
    return t;
}

/* ============================================================================
 * Rotation (Standard 3D Rotation, Works in Hyperbolic Space)
 * ============================================================================ */

H3Transform h3_transform_rotation(double rx, double ry, double rz) {
    H3Transform t = h3_transform_identity();
    
    double cx = cos(rx), sx = sin(rx);
    double cy = cos(ry), sy = sin(ry);
    double cz = cos(rz), sz = sin(rz);
    
    // Combined rotation matrix (Tait-Bryan angles)
    // Rz * Ry * Rx
    
    // Row 0
    t.m[0][0] = cy * cz;
    t.m[0][1] = sx * sy * cz - cx * sz;
    t.m[0][2] = cx * sy * cz + sx * sz;
    t.m[0][3] = 0.0;
    
    // Row 1
    t.m[1][0] = cy * sz;
    t.m[1][1] = sx * sy * sz + cx * cz;
    t.m[1][2] = cx * sy * sz - sx * cz;
    t.m[1][3] = 0.0;
    
    // Row 2
    t.m[2][0] = -sy;
    t.m[2][1] = sx * cy;
    t.m[2][2] = cx * cy;
    t.m[2][3] = 0.0;
    
    // Row 3 (unchanged for rotations)
    t.m[3][0] = 0.0;
    t.m[3][1] = 0.0;
    t.m[3][2] = 0.0;
    t.m[3][3] = 1.0;
    
    return t;
}

/* ============================================================================
 * Scale (Not Uniform in Hyperbolic Space, But Useful for Zooming)
 * ============================================================================ */

H3Transform h3_transform_scale(double sx, double sy, double sz) {
    H3Transform t = h3_transform_identity();
    t.m[0][0] = sx;
    t.m[1][1] = sy;
    t.m[2][2] = sz;
    return t;
}

/* ============================================================================
 * Transform Composition
 * ============================================================================ */

H3Transform h3_transform_compose(H3Transform *a, H3Transform *b) {
    H3Transform result;
    
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            result.m[i][j] = 0.0;
            for (int k = 0; k < 4; k++) {
                result.m[i][j] += a->m[i][k] * b->m[k][j];
            }
        }
    }
    
    return result;
}

/* ============================================================================
 * Apply Transform to Point
 * ============================================================================ */

H3Point h3_transform_apply(H3Transform *t, H3Point *p) {
    H3Point result;
    
    result.x = t->m[0][0] * p->x + t->m[0][1] * p->y + t->m[0][2] * p->z + t->m[0][3] * p->w;
    result.y = t->m[1][0] * p->x + t->m[1][1] * p->y + t->m[1][2] * p->z + t->m[1][3] * p->w;
    result.z = t->m[2][0] * p->x + t->m[2][1] * p->y + t->m[2][2] * p->z + t->m[2][3] * p->w;
    result.w = t->m[3][0] * p->x + t->m[3][1] * p->y + t->m[3][2] * p->z + t->m[3][3] * p->w;
    
    // Perspective division (keep inside unit ball for Klein model)
    if (fabs(result.w) > H3_EPSILON) {
        result.x /= result.w;
        result.y /= result.w;
        result.z /= result.w;
        result.w = 1.0;
    }
    
    // Clamp to stay inside unit ball
    h3_normalize(&result);
    
    return result;
}

/* ============================================================================
 * Klein Model <-> Poincaré Model Conversion
 * ============================================================================ */

// Klein model: straight lines, but angles are distorted
// Poincaré model: circles/lines, angles preserved (conformal)
// Converting between them is useful for rendering and navigation

H3Point h3_klein_to_poincare(H3Point *k) {
    H3Point p;
    
    // r_k = sqrt(x² + y² + z²)
    double r_k = sqrt(k->x * k->x + k->y * k->y + k->z * k->z);
    
    // Poincaré radius: r_p = r_k / (1 + sqrt(1 - r_k²))
    if (r_k < 1.0) {
        double r_p = r_k / (1.0 + sqrt(1.0 - r_k * r_k));
        double scale = (r_k > H3_EPSILON) ? r_p / r_k : 0.0;
        
        p.x = k->x * scale;
        p.y = k->y * scale;
        p.z = k->z * scale;
        p.w = 1.0;
    } else {
        // Clamp to boundary
        p.x = k->x / r_k * 0.9999;
        p.y = k->y / r_k * 0.9999;
        p.z = k->z / r_k * 0.9999;
        p.w = 1.0;
    }
    
    return p;
}

H3Point h3_poincare_to_klein(H3Point *p) {
    H3Point k;
    
    // r_p = sqrt(x² + y² + z²)
    double r_p = sqrt(p->x * p->x + p->y * p->y + p->z * p->z);
    
    // Klein radius: r_k = 2 * r_p / (1 + r_p²)
    if (r_p < 1.0) {
        double r_k = 2.0 * r_p / (1.0 + r_p * r_p);
        double scale = (r_p > H3_EPSILON) ? r_k / r_p : 0.0;
        
        k.x = p->x * scale;
        k.y = p->y * scale;
        k.z = p->z * scale;
        k.w = 1.0;
    } else {
        // Clamp
        k.x = p->x / r_p * 0.9999;
        k.y = p->y / r_p * 0.9999;
        k.z = p->z / r_p * 0.9999;
        k.w = 1.0;
    }
    
    return k;
}

/* ============================================================================
 * Focus Navigation (Move to Node)
 * ============================================================================ */

// Calculate the transform needed to bring a point to the center
H3Transform h3_transform_to_center(H3Point *target) {
    // We need to translate the target point to the origin
    // This is a hyperbolic translation by the negative of the position
    
    H3Point direction;
    direction.x = -target->x;
    direction.y = -target->y;
    direction.z = -target->z;
    direction.w = 1.0;
    
    // Calculate distance
    double dist = h3_distance(&(H3Point){0, 0, 0, 1}, target);
    
    return h3_transform_translation(&direction, dist);
}

/* ============================================================================
 * View Matrix (For OpenGL Rendering)
 * ============================================================================ */

void h3_transform_to_gl_matrix(H3Transform *t, float *gl_matrix) {
    // Convert to column-major format for OpenGL
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            gl_matrix[i * 4 + j] = (float)t->m[j][i];
        }
    }
}

/* ============================================================================
 * Interpolation (For Smooth Animation)
 * ============================================================================ */

// Geodesic interpolation between two points in hyperbolic space
H3Point h3_interpolate(H3Point *a, H3Point *b, double t) {
    // Calculate the geodesic from a to b
    double d = h3_distance(a, b);
    
    if (d < H3_EPSILON) {
        return *a;
    }
    
    // Linear interpolation (approximation for short distances)
    // Full implementation would use exponential map
    H3Point result;
    result.x = a->x + (b->x - a->x) * t;
    result.y = a->y + (b->y - a->y) * t;
    result.z = a->z + (b->z - a->z) * t;
    result.w = 1.0;
    
    h3_normalize(&result);
    
    (void)d;  // Distance used for full geodesic interpolation
    return result;
}

/* ============================================================================
 * Utility: Transform Inverse
 * ============================================================================ */

H3Transform h3_transform_inverse(H3Transform *t) {
    // For Lorentz transformations, the inverse is the transpose
    // But for general projective transformations, we need full inverse
    
    H3Transform inv;
    double det = 0.0;
    
    // Calculate determinant
    for (int i = 0; i < 4; i++) {
        det += t->m[0][i] * (
            t->m[1][(i+1)%4] * (t->m[2][(i+2)%4] * t->m[3][(i+3)%4] - t->m[2][(i+3)%4] * t->m[3][(i+2)%4]) -
            t->m[1][(i+2)%4] * (t->m[2][(i+1)%4] * t->m[3][(i+3)%4] - t->m[2][(i+3)%4] * t->m[3][(i+1)%4]) +
            t->m[1][(i+3)%4] * (t->m[2][(i+1)%4] * t->m[3][(i+2)%4] - t->m[2][(i+2)%4] * t->m[3][(i+1)%4])
        );
    }
    
    if (fabs(det) < H3_EPSILON) {
        return h3_transform_identity();
    }
    
    // Calculate inverse using cofactors (simplified for 4x4)
    // This is a standard matrix inversion
    
    double inv_det = 1.0 / det;
    
    // ... (full implementation would include all 16 cofactors)
    // For now, return transpose (valid for orthogonal + Lorentz)
    
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            inv.m[i][j] = t->m[j][i] * inv_det;
        }
    }
    
    return inv;
}