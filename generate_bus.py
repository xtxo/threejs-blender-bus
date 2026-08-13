import bpy
import math
import os

# Clear existing factory scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Helper function to create PBR Car Paint and PBR Materials in Blender 4.x / 5.x
def make_mat(name, color=(1, 1, 1, 1), roughness=0.1, metallic=0.05, clearcoat=0.0, transmission=0.0, emissive=(0, 0, 0, 1), emissive_intensity=1.0):
    mat = bpy.data.materials.new(name=name)
    mat.diffuse_color = color  # Viewport Display Color for Solid Mode
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        if 'Base Color' in bsdf.inputs:
            bsdf.inputs['Base Color'].default_value = color
        if 'Roughness' in bsdf.inputs:
            bsdf.inputs['Roughness'].default_value = roughness
        if 'Metallic' in bsdf.inputs:
            bsdf.inputs['Metallic'].default_value = metallic
        if 'Coat Weight' in bsdf.inputs:
            bsdf.inputs['Coat Weight'].default_value = clearcoat
        elif 'Clearcoat' in bsdf.inputs:
            bsdf.inputs['Clearcoat'].default_value = clearcoat
        if 'Coat Roughness' in bsdf.inputs:
            bsdf.inputs['Coat Roughness'].default_value = 0.03
        elif 'Clearcoat Roughness' in bsdf.inputs:
            bsdf.inputs['Clearcoat Roughness'].default_value = 0.03

        for key in ['Transmission Weight', 'Transmission']:
            if key in bsdf.inputs:
                bsdf.inputs[key].default_value = transmission
                break
        if transmission > 0:
            mat.blend_method = 'BLEND'
        for key in ['Emission Color', 'Emissive Color', 'Emission']:
            if key in bsdf.inputs:
                bsdf.inputs[key].default_value = emissive
                break
        if 'Emission Strength' in bsdf.inputs:
            bsdf.inputs['Emission Strength'].default_value = emissive_intensity
    return mat

# Materials Palette matching bus_ref.jpg
mat_carpaint_white = make_mat("Mat_White", color=(0.98, 0.99, 1.0, 1.0), roughness=0.08, metallic=0.05, clearcoat=1.0)
mat_carpaint_cyan = make_mat("Mat_Cyan", color=(0.0, 0.7, 0.85, 1.0), roughness=0.08, metallic=0.08, clearcoat=1.0)
mat_chassis = make_mat("Mat_Chassis", color=(0.06, 0.08, 0.12, 1.0), roughness=0.85, metallic=0.2)
mat_glass = make_mat("Mat_Glass", color=(0.8, 0.95, 1.0, 0.25), roughness=0.02, metallic=0.02, transmission=0.96)
mat_black_frame = make_mat("Mat_BlackFrame", color=(0.02, 0.03, 0.05, 1.0), roughness=0.25, metallic=0.7)
mat_rubber = make_mat("Mat_Rubber", color=(0.08, 0.08, 0.09, 1.0), roughness=0.9, metallic=0.0)
mat_rim = make_mat("Mat_Rim", color=(0.85, 0.87, 0.9, 1.0), roughness=0.15, metallic=0.9)
mat_headlight = make_mat("Mat_Headlight", color=(1.0, 1.0, 1.0, 1.0), roughness=0.05, emissive=(0.3, 0.8, 1.0, 1.0), emissive_intensity=3.5)
mat_taillight = make_mat("Mat_Taillight", color=(0.95, 0.1, 0.1, 1.0), roughness=0.1, emissive=(1.0, 0.1, 0.1, 1.0), emissive_intensity=2.5)
mat_orange_panto = make_mat("Mat_PantoOrange", color=(0.96, 0.38, 0.05, 1.0), roughness=0.25, metallic=0.8, clearcoat=0.8)
mat_led_display = make_mat("Mat_LED", color=(0.02, 0.02, 0.05, 1.0), roughness=0.2, emissive=(0.98, 0.65, 0.08, 1.0), emissive_intensity=2.2)
mat_seat_blue = make_mat("Mat_SeatBlue", color=(0.01, 0.52, 0.78, 1.0), roughness=0.5)
mat_rail_yellow = make_mat("Mat_RailYellow", color=(0.98, 0.76, 0.1, 1.0), roughness=0.2, metallic=0.5)

# Root Empty
root_bus = bpy.data.objects.new("Bus_Root", None)
bpy.context.collection.objects.link(root_bus)

def add_box(name, location, scale, material=None, parent=root_bus):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    if material:
        obj.data.materials.append(material)
    if parent:
        obj.parent = parent
    return obj

def add_cylinder(name, location, radius, depth, rotation=(0,0,0), material=None, parent=root_bus):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    if parent:
        obj.parent = parent
    return obj

# Dimensions matching 1:1 Bus Scale: L=11.8m, W=2.6m, H=3.1m
L, W, H = 11.8, 2.6, 3.1
groundY = 0.45

# 1. Main Body Shell (White Glossy Roof & Lower Cyan Skirt Graphics)
# Upper White Roof & Pillars
roof_white = add_box("Bus_Roof_White", (0, groundY + 2.75, 0), (W, 0.32, L), mat_carpaint_white)
roof_bevel = roof_white.modifiers.new(name="Bevel", type='BEVEL')
roof_bevel.width = 0.15
roof_bevel.segments = 4

# Cyan Lower Skirt Panel (Electric Cyan Accent)
body_skirt = add_box("Bus_Body_Skirt", (0, groundY + 0.65, 0), (W + 0.02, 0.72, L + 0.02), mat_carpaint_cyan)
skirt_bevel = body_skirt.modifiers.new(name="Bevel", type='BEVEL')
skirt_bevel.width = 0.12
skirt_bevel.segments = 3

# Chassis & Floor
chassis = add_box("Bus_Chassis", (0, groundY + 0.18, 0), (W * 0.94, 0.35, L * 0.95), mat_chassis)
rear_wall = add_box("Bus_Rear_Wall", (0, groundY + 1.8, -L/2 + 0.15), (W, 1.8, 0.3), mat_carpaint_white)

# 2. Wheel Axles & Rims (1:1 Double-Wheel Axle Setup)
def create_wheel(name, pos):
    wheel_group = bpy.data.objects.new(name, None)
    wheel_group.location = pos
    wheel_group.parent = root_bus
    bpy.context.collection.objects.link(wheel_group)
    
    tire = add_cylinder(name + "_Tire", (0, 0, 0), radius=0.48, depth=0.38, rotation=(0, 0, math.pi/2), material=mat_rubber, parent=wheel_group)
    rim = add_cylinder(name + "_Rim", (0, 0, 0), radius=0.3, depth=0.4, rotation=(0, 0, math.pi/2), material=mat_rim, parent=wheel_group)
    cap = add_cylinder(name + "_Cap", (0, 0, 0), radius=0.12, depth=0.42, rotation=(0, 0, math.pi/2), material=mat_black_frame, parent=wheel_group)
    return wheel_group

create_wheel("Bus_Wheel_FL", (-W/2 + 0.15, groundY + 0.48, L*0.32))
create_wheel("Bus_Wheel_FR", (W/2 - 0.15, groundY + 0.48, L*0.32))
create_wheel("Bus_Wheel_RL", (-W/2 + 0.15, groundY + 0.48, -L*0.3))
create_wheel("Bus_Wheel_RR", (W/2 - 0.15, groundY + 0.48, -L*0.3))

# 3. Transparent Glass Windows (Curved Windshield & Side Panels)
windshield = add_cylinder("Bus_Windshield", (0, groundY + 1.95, L/2 - 0.2), radius=W*0.8, depth=1.3, rotation=(math.pi/2, 0, 0), material=mat_glass)
windshield.scale = (1.0, 0.6, 1.0)

# Right & Left Side Windows
add_box("Bus_Glass_SideR", (W/2 + 0.005, groundY + 1.85, 0), (0.01, 1.3, L * 0.84), mat_glass)
add_box("Bus_Glass_SideL", (-W/2 - 0.005, groundY + 1.85, 0), (0.01, 1.3, L * 0.84), mat_glass)

# Pillar Trims
for z in [-L*0.35, -L*0.15, 0.0, L*0.15, L*0.35]:
    add_box("Bus_Pillar_R", (W/2 + 0.01, groundY + 1.85, z), (0.04, 1.32, 0.08), mat_black_frame)
    add_box("Bus_Pillar_L", (-W/2 - 0.01, groundY + 1.85, z), (0.04, 1.32, 0.08), mat_black_frame)

# 4. Doors (Front & Mid Double Doors with Glass)
add_box("Bus_Door_FL", (W/2 + 0.01, groundY + 1.35, L*0.35), (0.02, 1.7, 0.55), mat_glass)
add_box("Bus_Door_FR", (W/2 + 0.01, groundY + 1.35, L*0.25), (0.02, 1.7, 0.55), mat_glass)
add_box("Bus_Door_ML", (W/2 + 0.01, groundY + 1.35, -L*0.05), (0.02, 1.7, 0.55), mat_glass)
add_box("Bus_Door_MR", (W/2 + 0.01, groundY + 1.35, -L*0.15), (0.02, 1.7, 0.55), mat_glass)

# 5. Roof Equipment (AC Unit, Battery Pod, Pantograph/Trolley Arm in Orange)
roof_ac = add_box("Bus_Roof_AC", (0, groundY + 3.05, L*0.1), (W*0.75, 0.35, 2.8), mat_carpaint_white)
roof_ac_bevel = roof_ac.modifiers.new(name="Bevel", type='BEVEL')
roof_ac_bevel.width = 0.1

add_cylinder("Bus_AC_Fan1", (-W*0.2, groundY + 3.23, L*0.2), radius=0.3, depth=0.05, material=mat_black_frame)
add_cylinder("Bus_AC_Fan2", (-W*0.2, groundY + 3.23, 0.0), radius=0.3, depth=0.05, material=mat_black_frame)

# Pantograph (Orange Metallic Arm & Base)
add_box("Bus_Panto_Base", (0, groundY + 2.95, -L*0.28), (W*0.6, 0.15, 1.8), mat_black_frame)
panto_arm1 = add_box("Bus_Panto_Arm1", (0, groundY + 3.35, -L*0.3), (0.08, 0.8, 0.08), mat_orange_panto)
panto_arm1.rotation_euler = (math.pi/6, 0, 0)
add_box("Bus_Panto_TopBar", (0, groundY + 3.65, -L*0.18), (W*0.6, 0.06, 0.08), mat_orange_panto)

# 6. Front LED Display & Headlights
add_box("Bus_LED_Board", (0, groundY + 2.5, L/2 + 0.02), (W*0.7, 0.3, 0.05), mat_led_display)
add_box("Bus_Headlight_L", (-W*0.35, groundY + 0.65, L/2 + 0.02), (0.4, 0.2, 0.05), mat_headlight)
add_box("Bus_Headlight_R", (W*0.35, groundY + 0.65, L/2 + 0.02), (0.4, 0.2, 0.05), mat_headlight)

add_box("Bus_Taillight_L", (-W*0.38, groundY + 1.2, -L/2 - 0.02), (0.2, 0.6, 0.05), mat_taillight)
add_box("Bus_Taillight_R", (W*0.38, groundY + 1.2, -L/2 - 0.02), (0.2, 0.6, 0.05), mat_taillight)

add_box("Bus_Mirror_L", (-W/2 - 0.35, groundY + 2.2, L/2 - 0.1), (0.1, 0.4, 0.2), mat_black_frame)
add_box("Bus_Mirror_R", (W/2 + 0.35, groundY + 2.2, L/2 - 0.1), (0.1, 0.4, 0.2), mat_black_frame)

# 7. Interior Seats & Floor
add_box("Bus_Floor", (0, groundY + 0.38, 0), (W * 0.92, 0.05, L * 0.9), mat_chassis)

for z in range(int(-L*0.35 * 10), int(L*0.3 * 10), 11):
    z_pos = z / 10.0
    if abs(z_pos - (-L*0.05)) < 0.6 or abs(z_pos - (L*0.3)) < 0.6:
        continue
    add_box("Bus_Seat_L", (-W*0.3, groundY + 0.85, z_pos), (0.6, 0.5, 0.5), mat_seat_blue)
    add_box("Bus_Seat_R", (W*0.3, groundY + 0.85, z_pos), (0.6, 0.5, 0.5), mat_seat_blue)

# Select all objects
bpy.ops.object.select_all(action='SELECT')

# Export to GLB
output_path = "D:/work/workai/test/bus.glb"
bpy.ops.export_scene.gltf(
    filepath=output_path,
    export_format='GLB',
    use_selection=True
)

print("SUCCESSFULLY_EXPORTED_1TO1_PBR_BUS_GLB")
