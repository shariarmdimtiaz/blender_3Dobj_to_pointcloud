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

# Find the texture image in the object's material.
def get_material_texture(obj):
    if not obj.active_material or not obj.active_material.node_tree:
        return None
    
    nodes = obj.active_material.node_tree.nodes
    for node in nodes:
        if node.type == 'TEX_IMAGE' and node.image:
            return node.image
    return None

# Find the color from the texture at given UV coordinates.
def sample_texture(image, uv):
    if not image or not image.pixels:
        return (255, 255, 255)  # Default white color
    
    width, height = image.size
    px_x = int(uv[0] * width) % width
    px_y = int(uv[1] * height) % height
    pixel_index = (px_y * width + px_x) * 4  # RGBA channels
    color = image.pixels[pixel_index:pixel_index + 3]
    return tuple(int(c * 255) for c in color)


# Get the selected mesh object
obj = bpy.context.object

if obj and obj.type == 'MESH':
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    
    density = 10000 # Point density
    point_cloud = []
    world_matrix = obj.matrix_world
    image = get_material_texture(obj)
    uv_layer = obj.data.uv_layers.active

    if not uv_layer:
        print("No active UV map found!")
    else:
        for face in bm.faces:
            if len(face.verts) < 3:
                continue
            
            uv1 = uv_layer.data[face.loops[0].index].uv
            uv2 = uv_layer.data[face.loops[1].index].uv
            uv3 = uv_layer.data[face.loops[2].index].uv
            v1, v2, v3 = [world_matrix @ v.co for v in face.verts[:3]]
            sampled_points, uvs = random_points_in_triangle_3d(v1, v2, v3, uv1, uv2, uv3, density)
            
            # Get UV coordinates from face
            
            
            for p, uv in zip(sampled_points, uvs):
                r, g, b = sample_texture(image, uv)       # UV → RGB
                point_cloud.append((*p, r, g, b))         # XYZ + RGB
    
    bm.free()

    output_dir = "E:/projects/Blender 3DModel/point_data/room_5/table_1.txt"
    output_path = bpy.path.abspath(output_dir)  
    with open(output_path, "w") as f:
        for x, y, z, r, g, b in point_cloud:
            f.write(f"{x} {y} {z} {r} {g} {b}\n")

    print(f"Point cloud data saved!")
else:
    print("No mesh object selected!")