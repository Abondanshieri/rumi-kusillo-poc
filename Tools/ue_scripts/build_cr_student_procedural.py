import json
import os
import sys
from ue_mcp import UnrealMCPClient

def build_procedural_control_rig():
    print("=== STARTING PROCEDURAL CONTROL RIG GENERATION ===")
    client = UnrealMCPClient()

    cr_path = "/Game/Characters/Student/Rig/CR_Student_Procedural"
    mesh_path = "/Game/Characters/Student/Student.Student"

    # Step 1: Create the Control Rig asset
    print(f"\n[1/5] Creating Control Rig at {cr_path}...")
    create_res = client.run_tool(
        "animation_toolset.toolsets.controlrig.ControlRigTools",
        "create",
        {"path": cr_path}
    )
    print("Create response:", create_res)
    cr_data = json.loads(create_res["content"][0]["text"])
    cr_ref = cr_data["returnValue"]
    print(f"Control Rig created: {cr_ref['refPath']}")

    # Import bone hierarchy from Skeletal Mesh
    print(f"\nImporting bones from {mesh_path}...")
    mesh_ref = {"refPath": mesh_path}
    import_res = client.run_tool(
        "animation_toolset.toolsets.controlrig.ControlRigTools",
        "import_bones_from_asset",
        {"control_rig": cr_ref, "skeletal_mesh": mesh_ref}
    )
    imported_bones = json.loads(import_res["content"][0]["text"])["returnValue"]
    print(f"Successfully imported {len(imported_bones)} bones into Control Rig hierarchy.")

    # Step 2: Declare the 8 public variables
    print("\n[2/5] Declaring 8 public variables...")
    variables = [
        ("LeanPitch", "float", "0.000000"),
        ("LeanRoll", "float", "0.000000"),
        ("FootOffsetL", "float", "0.000000"),
        ("FootOffsetR", "float", "0.000000"),
        ("PelvisOffset", "float", "0.000000"),
        ("LandCrouch", "float", "0.000000"),
        ("LookAlpha", "float", "1.000000"),
        ("LookTarget", "Vector", "(X=0.000000,Y=0.000000,Z=0.000000)")
    ]

    for name, vtype, default_val in variables:
        add_var_res = client.run_tool(
            "animation_toolset.toolsets.controlrig.ControlRigTools",
            "add_variable",
            {
                "control_rig": cr_ref,
                "name": name,
                "type_path": vtype,
                "is_public": True,
                "is_read_only": False,
                "default_value": default_val
            }
        )
        print(f" - Declared variable '{name}' ({vtype}, default={default_val})")

    # Verify declared variables
    list_vars_res = client.run_tool(
        "animation_toolset.toolsets.controlrig.ControlRigTools",
        "list_variables",
        {"control_rig": cr_ref}
    )
    declared_vars = json.loads(list_vars_res["content"][0]["text"])["returnValue"]
    print(f"Verified {len(declared_vars)} variables in Control Rig:")
    for v in declared_vars:
        print(f"   * {v['name']} ({v['cPPType']}) public={v['bPublic']}")

    # Step 3: Get Forward Solve Graph
    print("\n[3/5] Setting up Forward Solve Graph...")
    graph_res = client.run_tool(
        "animation_toolset.toolsets.controlrig.ControlRigTools",
        "get_forward_solve_graph",
        {"control_rig": cr_ref}
    )
    graph_ref = json.loads(graph_res["content"][0]["text"])["returnValue"]
    print("Forward Solve Graph ref:", graph_ref["refPath"])

    # Add Forward Solve entry event node
    begin_res = client.run_tool(
        "animation_toolset.toolsets.controlrig.ControlRigTools",
        "add_event_node",
        {
            "control_rig": cr_ref,
            "graph": graph_ref,
            "event_type": "FORWARD_SOLVE",
            "position": {"x": 0.0, "y": 0.0}
        }
    )
    begin_node = json.loads(begin_res["content"][0]["text"])["returnValue"]
    print("Created BeginExecution node:", begin_node["refPath"])

    # Helper function to create node
    def create_rig_node(node_type, node_name, x, y):
        res = client.run_tool(
            "animation_toolset.toolsets.controlrig.ControlRigTools",
            "create_node",
            {
                "control_rig": cr_ref,
                "graph": graph_ref,
                "node_type": node_type,
                "node_name": node_name,
                "position": {"x": float(x), "y": float(y)}
            }
        )
        text = res["content"][0]["text"]
        if "isError" in res and res["isError"]:
            raise RuntimeError(f"Error creating node {node_name} ({node_type}): {text}")
        data = json.loads(text)
        return data["returnValue"]

    # Helper function to add variable getter node
    def add_var_getter(var_name, x, y):
        res = client.run_tool(
            "animation_toolset.toolsets.controlrig.ControlRigTools",
            "add_variable_node",
            {
                "control_rig": cr_ref,
                "graph": graph_ref,
                "variable_name": var_name,
                "is_getter": True,
                "position": {"x": float(x), "y": float(y)}
            }
        )
        text = res["content"][0]["text"]
        if "isError" in res and res["isError"]:
            raise RuntimeError(f"Error adding variable node {var_name}: {text}")
        data = json.loads(text)
        return data["returnValue"]

    # Helper function to set pin value
    def set_pin(node_ref, pin_subpath, val_str):
        full_pin = f"{node_ref['refPath']}.{pin_subpath}"
        res = client.run_tool(
            "animation_toolset.toolsets.controlrig.ControlRigTools",
            "set_pin_value",
            {
                "control_rig": cr_ref,
                "graph": graph_ref,
                "pin": {"refPath": full_pin},
                "value": str(val_str)
            }
        )
        if "isError" in res and res["isError"]:
            raise RuntimeError(f"Error setting pin {full_pin} = {val_str}: {res['content'][0]['text']}")

    # Helper function to connect pins
    def connect(source_node, source_pin_sub, target_node, target_pin_sub):
        src = f"{source_node['refPath']}.{source_pin_sub}"
        tgt = f"{target_node['refPath']}.{target_pin_sub}"
        res = client.run_tool(
            "animation_toolset.toolsets.controlrig.ControlRigTools",
            "connect_pins",
            {
                "control_rig": cr_ref,
                "graph": graph_ref,
                "source_pin": {"refPath": src},
                "target_pin": {"refPath": tgt}
            }
        )
        if "isError" in res and res["isError"]:
            raise RuntimeError(f"Error connecting {src} -> {tgt}: {res['content'][0]['text']}")

    print("\n--- Constructing Part A (Lean / Inclinación al correr) ---")
    # Getters for Lean variables
    get_lean_roll = add_var_getter("LeanRoll", 50, 100)
    get_lean_pitch = add_var_getter("LeanPitch", 50, 200)

    # 1. Spine1 (Full weight = 1.0)
    quat_spine1 = create_rig_node("RigUnit_MathQuaternionFromEuler", "Quat_Spine1", 350, 150)
    connect(get_lean_roll, "Value", quat_spine1, "Euler.X")
    connect(get_lean_pitch, "Value", quat_spine1, "Euler.Y")

    get_spine1 = create_rig_node("RigUnit_GetTransform", "Get_Spine1", 350, 50)
    set_pin(get_spine1, "Item", '(Type=Bone,Name="Spine1")')
    set_pin(get_spine1, "Space", "LocalSpace")

    mul_spine1 = create_rig_node("RigUnit_MathQuaternionMul", "Mul_Spine1", 600, 100)
    connect(get_spine1, "Transform.Rotation", mul_spine1, "A")
    connect(quat_spine1, "Result", mul_spine1, "B")

    set_spine1 = create_rig_node("RigUnit_SetTransform", "Set_Spine1", 850, 100)
    set_pin(set_spine1, "Item", '(Type=Bone,Name="Spine1")')
    set_pin(set_spine1, "Space", "LocalSpace")
    set_pin(set_spine1, "Weight", "1.0")
    connect(get_spine1, "Transform", set_spine1, "Value")
    connect(mul_spine1, "Result", set_spine1, "Value.Rotation")
    connect(begin_node, "ExecutePin", set_spine1, "ExecutePin")
    print(" - Part A1: Spine1 Lean configured.")

    # 2. Spine2 (Medium weight = 0.5)
    mul_roll_spine2 = create_rig_node("RigUnit_MathFloatMul", "Mul_Roll_Spine2", 300, 320)
    connect(get_lean_roll, "Value", mul_roll_spine2, "A")
    set_pin(mul_roll_spine2, "B", "0.5")

    mul_pitch_spine2 = create_rig_node("RigUnit_MathFloatMul", "Mul_Pitch_Spine2", 300, 420)
    connect(get_lean_pitch, "Value", mul_pitch_spine2, "A")
    set_pin(mul_pitch_spine2, "B", "0.5")

    quat_spine2 = create_rig_node("RigUnit_MathQuaternionFromEuler", "Quat_Spine2", 500, 370)
    connect(mul_roll_spine2, "Result", quat_spine2, "Euler.X")
    connect(mul_pitch_spine2, "Result", quat_spine2, "Euler.Y")

    get_spine2 = create_rig_node("RigUnit_GetTransform", "Get_Spine2", 500, 270)
    set_pin(get_spine2, "Item", '(Type=Bone,Name="Spine2")')
    set_pin(get_spine2, "Space", "LocalSpace")

    mul_spine2 = create_rig_node("RigUnit_MathQuaternionMul", "Mul_Spine2", 750, 320)
    connect(get_spine2, "Transform.Rotation", mul_spine2, "A")
    connect(quat_spine2, "Result", mul_spine2, "B")

    set_spine2 = create_rig_node("RigUnit_SetTransform", "Set_Spine2", 1000, 320)
    set_pin(set_spine2, "Item", '(Type=Bone,Name="Spine2")')
    set_pin(set_spine2, "Space", "LocalSpace")
    set_pin(set_spine2, "Weight", "1.0")
    connect(get_spine2, "Transform", set_spine2, "Value")
    connect(mul_spine2, "Result", set_spine2, "Value.Rotation")
    connect(set_spine1, "ExecutePin", set_spine2, "ExecutePin")
    print(" - Part A2: Spine2 Lean configured.")

    # 3. Neck Lean (One third weight = 0.333333)
    mul_roll_neck = create_rig_node("RigUnit_MathFloatMul", "Mul_Roll_Neck", 300, 550)
    connect(get_lean_roll, "Value", mul_roll_neck, "A")
    set_pin(mul_roll_neck, "B", "0.333333")

    mul_pitch_neck = create_rig_node("RigUnit_MathFloatMul", "Mul_Pitch_Neck", 300, 650)
    connect(get_lean_pitch, "Value", mul_pitch_neck, "A")
    set_pin(mul_pitch_neck, "B", "0.333333")

    quat_neck = create_rig_node("RigUnit_MathQuaternionFromEuler", "Quat_Neck", 500, 600)
    connect(mul_roll_neck, "Result", quat_neck, "Euler.X")
    connect(mul_pitch_neck, "Result", quat_neck, "Euler.Y")

    get_neck_lean = create_rig_node("RigUnit_GetTransform", "Get_Neck_Lean", 500, 500)
    set_pin(get_neck_lean, "Item", '(Type=Bone,Name="Neck")')
    set_pin(get_neck_lean, "Space", "LocalSpace")

    mul_neck_lean = create_rig_node("RigUnit_MathQuaternionMul", "Mul_Neck_Lean", 750, 550)
    connect(get_neck_lean, "Transform.Rotation", mul_neck_lean, "A")
    connect(quat_neck, "Result", mul_neck_lean, "B")

    set_neck_lean = create_rig_node("RigUnit_SetTransform", "Set_Neck_Lean", 1000, 550)
    set_pin(set_neck_lean, "Item", '(Type=Bone,Name="Neck")')
    set_pin(set_neck_lean, "Space", "LocalSpace")
    set_pin(set_neck_lean, "Weight", "1.0")
    connect(get_neck_lean, "Transform", set_neck_lean, "Value")
    connect(mul_neck_lean, "Result", set_neck_lean, "Value.Rotation")
    connect(set_spine2, "ExecutePin", set_neck_lean, "ExecutePin")
    print(" - Part A3: Neck Lean configured.")

    print("\n--- Constructing Part B (Foot IK & PelvisOffset) ---")
    # PelvisOffset on Hips
    get_pelvis_offset = add_var_getter("PelvisOffset", 50, 800)
    get_land_crouch = add_var_getter("LandCrouch", 50, 900)

    mul_land_crouch = create_rig_node("RigUnit_MathFloatMul", "Mul_LandCrouch", 300, 900)
    connect(get_land_crouch, "Value", mul_land_crouch, "A")
    set_pin(mul_land_crouch, "B", "25.0")

    add_pelvis_land = create_rig_node("RigUnit_MathFloatAdd", "Add_PelvisLand", 500, 850)
    connect(get_pelvis_offset, "Value", add_pelvis_land, "A")
    connect(mul_land_crouch, "Result", add_pelvis_land, "B")

    get_hips = create_rig_node("RigUnit_GetTransform", "Get_Hips", 500, 750)
    set_pin(get_hips, "Item", '(Type=Bone,Name="Hips")')
    set_pin(get_hips, "Space", "LocalSpace")

    add_hips_z = create_rig_node("RigUnit_MathFloatAdd", "Add_HipsZ", 750, 800)
    connect(get_hips, "Transform.Translation.Z", add_hips_z, "A")
    connect(add_pelvis_land, "Result", add_hips_z, "B")

    set_hips = create_rig_node("RigUnit_SetTransform", "Set_Hips", 1000, 800)
    set_pin(set_hips, "Item", '(Type=Bone,Name="Hips")')
    set_pin(set_hips, "Space", "LocalSpace")
    set_pin(set_hips, "Weight", "1.0")
    connect(get_hips, "Transform", set_hips, "Value")
    connect(add_hips_z, "Result", set_hips, "Value.Translation.Z")
    connect(set_neck_lean, "ExecutePin", set_hips, "ExecutePin")
    print(" - Part B1: Hips PelvisOffset (+ LandCrouch * 25.0 cm) configured.")

    # TwoBoneIK Left Leg
    get_foot_offset_l = add_var_getter("FootOffsetL", 50, 1100)
    sub_foot_l = create_rig_node("RigUnit_MathFloatSub", "Sub_FootOffsetL", 300, 1100)
    connect(get_foot_offset_l, "Value", sub_foot_l, "A")
    connect(get_pelvis_offset, "Value", sub_foot_l, "B")

    get_left_foot = create_rig_node("RigUnit_GetTransform", "Get_LeftFoot", 500, 1050)
    set_pin(get_left_foot, "Item", '(Type=Bone,Name="LeftFoot")')
    set_pin(get_left_foot, "Space", "GlobalSpace")

    add_left_foot_z = create_rig_node("RigUnit_MathFloatAdd", "Add_LeftFootZ", 750, 1100)
    connect(get_left_foot, "Transform.Translation.Z", add_left_foot_z, "A")
    connect(sub_foot_l, "Result", add_left_foot_z, "B")

    ik_left = create_rig_node("RigUnit_TwoBoneIKSimple", "TwoBoneIK_Left", 1000, 1100)
    set_pin(ik_left, "BoneA", "LeftUpLeg")
    set_pin(ik_left, "BoneB", "LeftLeg")
    set_pin(ik_left, "EffectorBone", "LeftFoot")
    set_pin(ik_left, "PoleVector", "(X=1.000000,Y=0.000000,Z=0.000000)")
    set_pin(ik_left, "PoleVectorKind", "Direction")
    set_pin(ik_left, "PrimaryAxis", "(X=1.000000,Y=0.000000,Z=0.000000)")
    set_pin(ik_left, "SecondaryAxis", "(X=0.000000,Y=1.000000,Z=0.000000)")
    set_pin(ik_left, "Weight", "1.0")
    connect(get_left_foot, "Transform", ik_left, "Effector")
    connect(add_left_foot_z, "Result", ik_left, "Effector.Translation.Z")
    connect(set_hips, "ExecutePin", ik_left, "ExecutePin")
    print(" - Part B2: Left Leg TwoBoneIK (LeftUpLeg -> LeftLeg -> LeftFoot) configured.")

    # TwoBoneIK Right Leg
    get_foot_offset_r = add_var_getter("FootOffsetR", 50, 1350)
    sub_foot_r = create_rig_node("RigUnit_MathFloatSub", "Sub_FootOffsetR", 300, 1350)
    connect(get_foot_offset_r, "Value", sub_foot_r, "A")
    connect(get_pelvis_offset, "Value", sub_foot_r, "B")

    get_right_foot = create_rig_node("RigUnit_GetTransform", "Get_RightFoot", 500, 1300)
    set_pin(get_right_foot, "Item", '(Type=Bone,Name="RightFoot")')
    set_pin(get_right_foot, "Space", "GlobalSpace")

    add_right_foot_z = create_rig_node("RigUnit_MathFloatAdd", "Add_RightFootZ", 750, 1350)
    connect(get_right_foot, "Transform.Translation.Z", add_right_foot_z, "A")
    connect(sub_foot_r, "Result", add_right_foot_z, "B")

    ik_right = create_rig_node("RigUnit_TwoBoneIKSimple", "TwoBoneIK_Right", 1000, 1350)
    set_pin(ik_right, "BoneA", "RightUpLeg")
    set_pin(ik_right, "BoneB", "RightLeg")
    set_pin(ik_right, "EffectorBone", "RightFoot")
    set_pin(ik_right, "PoleVector", "(X=1.000000,Y=0.000000,Z=0.000000)")
    set_pin(ik_right, "PoleVectorKind", "Direction")
    set_pin(ik_right, "PrimaryAxis", "(X=1.000000,Y=0.000000,Z=0.000000)")
    set_pin(ik_right, "SecondaryAxis", "(X=0.000000,Y=1.000000,Z=0.000000)")
    set_pin(ik_right, "Weight", "1.0")
    connect(get_right_foot, "Transform", ik_right, "Effector")
    connect(add_right_foot_z, "Result", ik_right, "Effector.Translation.Z")
    connect(ik_left, "ExecutePin", ik_right, "ExecutePin")
    print(" - Part B3: Right Leg TwoBoneIK (RightUpLeg -> RightLeg -> RightFoot) configured.")

    print("\n--- Constructing Part C (Mirada / Look-At) ---")
    get_look_target = add_var_getter("LookTarget", 50, 1600)
    get_look_alpha = add_var_getter("LookAlpha", 50, 1750)

    # Angle limit parameter node (-60.0 to +60.0)
    clamp_angle = create_rig_node("RigUnit_MathFloatClamp", "Clamp_LookAngle60Deg", 300, 1650)
    set_pin(clamp_angle, "Minimum", "-60.0")
    set_pin(clamp_angle, "Maximum", "60.0")

    # Neck Aim (half LookAlpha weight)
    mul_look_neck = create_rig_node("RigUnit_MathFloatMul", "Mul_LookAlpha_Neck", 500, 1750)
    connect(get_look_alpha, "Value", mul_look_neck, "A")
    set_pin(mul_look_neck, "B", "0.5")

    aim_neck = create_rig_node("RigUnit_AimBone", "Aim_Neck", 800, 1600)
    set_pin(aim_neck, "Bone", "Neck")
    set_pin(aim_neck, "Primary.Axis", "(X=1.000000,Y=0.000000,Z=0.000000)")
    set_pin(aim_neck, "Primary.Kind", "Location")
    set_pin(aim_neck, "Secondary.Axis", "(X=0.000000,Y=0.000000,Z=1.000000)")
    set_pin(aim_neck, "Secondary.Target", "(X=0.000000,Y=0.000000,Z=1.000000)")
    set_pin(aim_neck, "Secondary.Kind", "Direction")
    connect(get_look_target, "Value", aim_neck, "Primary.Target")
    connect(mul_look_neck, "Result", aim_neck, "Weight")
    connect(ik_right, "ExecutePin", aim_neck, "ExecutePin")
    print(" - Part C1: Neck Aim configured.")

    # Head Aim (full LookAlpha weight)
    aim_head = create_rig_node("RigUnit_AimBone", "Aim_Head", 1100, 1600)
    set_pin(aim_head, "Bone", "Head")
    set_pin(aim_head, "Primary.Axis", "(X=1.000000,Y=0.000000,Z=0.000000)")
    set_pin(aim_head, "Primary.Kind", "Location")
    set_pin(aim_head, "Secondary.Axis", "(X=0.000000,Y=0.000000,Z=1.000000)")
    set_pin(aim_head, "Secondary.Target", "(X=0.000000,Y=0.000000,Z=1.000000)")
    set_pin(aim_head, "Secondary.Kind", "Direction")
    connect(get_look_target, "Value", aim_head, "Primary.Target")
    connect(get_look_alpha, "Value", aim_head, "Weight")
    connect(aim_neck, "ExecutePin", aim_head, "ExecutePin")
    print(" - Part C2: Head Aim configured.")

    # Step 4: Save Asset
    print(f"\n[4/5] Saving asset {cr_path}...")
    save_res = client.run_tool(
        "editor_toolset.toolsets.asset.AssetTools",
        "save_assets",
        {"asset_paths": [cr_path]}
    )
    print("Save result:", save_res)

    # Step 5: Verify on disk
    expected_file = r"D:\Dev\Computacion_Grafica\Rumi 5.8\Content\Characters\Student\Rig\CR_Student_Procedural.uasset"
    print(f"\n[5/5] Verifying physical existence on disk:\n{expected_file}")
    if os.path.exists(expected_file):
        file_size = os.path.getsize(expected_file)
        print(f"SUCCESS: File exists on disk! Size = {file_size:,} bytes")
    else:
        print(f"ERROR: File not found on disk at {expected_file}")
        sys.exit(1)

    print("\n=== ALL PROCEDURAL CONTROL RIG REQUIREMENTS COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    build_procedural_control_rig()
