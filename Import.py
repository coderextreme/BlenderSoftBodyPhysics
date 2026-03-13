import bpy
import json
import os

def import_softbody_simulation_data(filepath, obj):
    """
    Scenario 1: Imports baked vertex positions from a JSON file and 
    applies them as animated Shape Keys frame-by-frame.
    """
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} not found.")
        return

    with open(filepath, 'r') as f:
        data = json.load(f)

    # Ensure the object has a base shape key first
    if not obj.data.shape_keys:
        obj.shape_key_add(name="Basis")

    frames = data.get("frames", {})
    
    for frame_str, vertices in frames.items():
        frame_num = int(frame_str)
        
        # Add a new shape key for the current frame
        sk = obj.shape_key_add(name=f"Frame_{frame_num}")
        
        # Assign new vertex coordinates
        # Note: The JSON vertex list must match the Blender object's vertex count
        for i, v_co in enumerate(vertices):
            if i < len(sk.data):
                sk.data[i].co = (v_co[0], v_co[1], v_co[2])
        
        # Animate the shape key so it only activates on this exact frame
        sk.value = 0.0
        sk.keyframe_insert(data_path="value", frame=frame_num - 1)
        
        sk.value = 1.0
        sk.keyframe_insert(data_path="value", frame=frame_num)
        
        sk.value = 0.0
        sk.keyframe_insert(data_path="value", frame=frame_num + 1)
        
    print(f"Successfully imported {len(frames)} frames of soft body cache.")

def import_softbody_modifier_settings(filepath, obj):
    """
    Scenario 2: Imports physics setup parameters from a JSON file and 
    applies them to a Soft Body modifier on the object.
    """
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} not found.")
        return

    with open(filepath, 'r') as f:
        data = json.load(f)
        
    settings_data = data.get("settings", {})
    if not settings_data:
        return

    # Create the soft body modifier if it doesn't exist
    modifier = obj.modifiers.get("SoftBodyImport")
    if not modifier:
        modifier = obj.modifiers.new(name="SoftBodyImport", type='SOFT_BODY')
        
    sb = modifier.settings

    # Apply properties from the JSON file mapping
    if "mass" in settings_data:
        sb.mass = settings_data["mass"]
    if "friction" in settings_data:
        sb.friction = settings_data["friction"]
    if "push" in settings_data:
        sb.push = settings_data["push"]
    if "pull" in settings_data:
        sb.pull = settings_data["pull"]
    if "bending" in settings_data:
        sb.bend = settings_data["bending"]
    if "use_edges" in settings_data:
        sb.use_edges = settings_data["use_edges"]

    print("Successfully applied Soft Body settings.")

# ==========================================
# Execution / Usage Example
# ==========================================
if __name__ == "__main__":
    # Get the currently selected active object
    active_obj = bpy.context.active_object
    
    if active_obj and active_obj.type == 'MESH':
        # Define the path to your JSON data
        # Update this path to where your actual JSON file is located
        json_file_path = "C:/path/to/your/softbody_data.json" 
        
        # Uncomment the function you want to use (or use both):
        
        # 1. To import custom physics engine vertex cache:
        # import_softbody_simulation_data(json_file_path, active_obj)
        
        # 2. To import modifier settings:
        # import_softbody_modifier_settings(json_file_path, active_obj)
        
    else:
        print("Please select a valid Mesh object first.")
