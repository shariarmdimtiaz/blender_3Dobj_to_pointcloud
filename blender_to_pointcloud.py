import bpy
import bmesh
import numpy as np
import random

# Calculate triangle are
def triangle_area_3d(v1, v2, v3):
    """Compute the area of a triangle in 3D space."""
    vec1 = np.array(v2) - np.array(v1)
    vec2 = np.array(v3) - np.array(v1)
    return 0.5 * np.linalg.norm(np.cross(vec1, vec2))

# Random points in triangle
def random_points_in_triangle_3d(v1, v2, v3, uv1, uv2, uv3, density):
    """Generate random points inside a 3D triangle using barycentric coordinates."""
    area = triangle_area_3d(v1, v2, v3)
    n = max(1, int(area * density))  #max(1, int(area * density))  # Ensure at least 1 point per triangle


    r1 = np.sqrt(np.random.rand(n))
    r2 = np.random.rand(n)
    w1 = 1 - r1
    w2 = r1 * (1 - r2)
    w3 = r1 * r2

    # Points
    sampled_points = w1[:, None] * v1 + w2[:, None] * v2 + w3[:, None] * v3
    # UV map
    uvs    = w1[:, None] * uv1 + w2[:, None] * uv2 + w3[:, None] * uv3

    return sampled_points, uvs