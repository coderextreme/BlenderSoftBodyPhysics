import bpy

def setup_pc2_cache(obj, pc2_filepath):
    # Add a Mesh Cache modifier
    cache_mod = obj.modifiers.new(name="SoftBodyCache", type='MESH_CACHE')
    
    # Configure it for Point Cache 2 (.pc2)
    cache_mod.cache_format = 'PC2'
    cache_mod.filepath = pc2_filepath
    cache_mod.forward_axis = 'Y'
    cache_mod.up_axis = 'Z'
    
# Usage:
# setup_pc2_cache(bpy.context.active_object, "C:/path/to/physics_bake.pc2")
