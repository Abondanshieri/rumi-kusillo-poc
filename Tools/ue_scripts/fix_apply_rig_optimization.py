import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
cr_path = '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'
cr = {'refPath': cr_path}
g = {'refPath': f'{cr_path}:RigVMModel'}
g_path = g['refPath']

def set_pin(node, pin, val):
    p = f"{g_path}.{node}.{pin}"
    res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'set_pin_value', {
        'control_rig': cr, 'graph': g, 'pin': {'refPath': p}, 'value': str(val)
    })
    return res

def connect(src_node, src_pin, tgt_node, tgt_pin):
    src = f"{g_path}.{src_node}.{src_pin}"
    tgt = f"{g_path}.{tgt_node}.{tgt_pin}"
    res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'connect_pins', {
        'control_rig': cr, 'graph': g, 'source_pin': {'refPath': src}, 'target_pin': {'refPath': tgt}
    })
    return res

def disconnect(src_node, src_pin, tgt_node, tgt_pin):
    src = f"{g_path}.{src_node}.{src_pin}"
    tgt = f"{g_path}.{tgt_node}.{tgt_pin}"
    res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'disconnect_pins', {
        'control_rig': cr, 'graph': g, 'source_pin': {'refPath': src}, 'target_pin': {'refPath': tgt}
    })
    return res

print("=== APPLYING RIG OPTIMIZATION FOR TWOBONEIK AND PELVIS ===")

# 1. FIX SET_HIPS WIRING (Direct Local Space Z translation, no Mul rotation skew)
print("\n[1/3] Fixing Set_Hips wiring...")
set_pin('Get_Hips', 'Space', 'LocalSpace')
set_pin('Set_Hips', 'Space', 'LocalSpace')
set_pin('Set_Hips', 'Weight', '1.0')
set_pin('Set_Hips', 'bPropagateToChildren', 'True')

# Disconnect Mul_Hips_Offset.Result -> Set_Hips.Value
disconnect('Mul_Hips_Offset', 'Result', 'Set_Hips', 'Value')

# Connect individual components directly
print("Connecting Get_Hips & Add_HipsZ -> Set_Hips.Value...")
connect('Get_Hips', 'Transform.Translation.X', 'Set_Hips', 'Value.Translation.X')
connect('Get_Hips', 'Transform.Translation.Y', 'Set_Hips', 'Value.Translation.Y')
connect('Add_HipsZ', 'Result', 'Set_Hips', 'Value.Translation.Z')
connect('Get_Hips', 'Transform.Rotation', 'Set_Hips', 'Value.Rotation')
connect('Get_Hips', 'Transform.Scale3D', 'Set_Hips', 'Value.Scale3D')

# Ensure Add_HipsZ is correctly wired: A = Get_Hips.Transform.Translation.Z, B = Add_PelvisLand.Result
connect('Get_Hips', 'Transform.Translation.Z', 'Add_HipsZ', 'A')
connect('Add_PelvisLand', 'Result', 'Add_HipsZ', 'B')

# 2. ADD CLAMPING TO FOOT EFFECTOR Z OFFSET (PREVENTS HYPEREXTENSION)
print("\n[2/3] Adding Clamping to Foot Effector Z offsets...")
# Check if Clamp nodes exist, if not create them
nodes_res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'list_nodes', {'control_rig': cr, 'graph': g})
existing_nodes = [n['refPath'].split('.')[-1] for n in json.loads(nodes_res['content'][0]['text'])['returnValue']]

if 'Clamp_LeftOffset' not in existing_nodes:
    print("Creating Clamp_LeftOffset node...")
    c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'create_node', {
        'control_rig': cr, 'graph': g, 'node_type': 'RigUnit_MathFloatClamp', 'node_name': 'Clamp_LeftOffset', 'position': {'x': 1050, 'y': 1050}
    })

if 'Clamp_RightOffset' not in existing_nodes:
    print("Creating Clamp_RightOffset node...")
    c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'create_node', {
        'control_rig': cr, 'graph': g, 'node_type': 'RigUnit_MathFloatClamp', 'node_name': 'Clamp_RightOffset', 'position': {'x': 1050, 'y': 1350}
    })

# Configure Clamps: Minimum = 0.0, Maximum = 35.0
set_pin('Clamp_LeftOffset', 'Minimum', '0.000000')
set_pin('Clamp_LeftOffset', 'Maximum', '35.000000')
set_pin('Clamp_RightOffset', 'Minimum', '0.000000')
set_pin('Clamp_RightOffset', 'Maximum', '35.000000')

# Wire Left: Sub_FootOffsetL.Result -> Clamp_LeftOffset.Value -> Add_LeftFootZ.B
disconnect('Sub_FootOffsetL', 'Result', 'Add_LeftFootZ', 'B')
connect('Sub_FootOffsetL', 'Result', 'Clamp_LeftOffset', 'Value')
connect('Clamp_LeftOffset', 'Result', 'Add_LeftFootZ', 'B')

# Wire Right: Sub_FootOffsetR.Result -> Clamp_RightOffset.Value -> Add_RightFootZ.B
disconnect('Sub_FootOffsetR', 'Result', 'Add_RightFootZ', 'B')
connect('Sub_FootOffsetR', 'Result', 'Clamp_RightOffset', 'Value')
connect('Clamp_RightOffset', 'Result', 'Add_RightFootZ', 'B')

# 3. VERIFY TWOBONEIK AXES AND POLE VECTORS
print("\n[3/3] Verifying TwoBoneIK axes and pole vectors...")
# Left Leg
set_pin('TwoBoneIK_Left', 'PrimaryAxis', '(X=1.000000,Y=0.000000,Z=0.000000)')
set_pin('TwoBoneIK_Left', 'SecondaryAxis', '(X=0.000000,Y=1.000000,Z=0.000000)')
set_pin('TwoBoneIK_Left', 'SecondaryAxisWeight', '1.000000')
set_pin('TwoBoneIK_Left', 'PoleVectorSpace', 'None')
set_pin('TwoBoneIK_Left', 'PoleVectorKind', 'Location')
set_pin('TwoBoneIK_Left', 'PoleVector', '(X=6.070472,Y=50.000000,Z=28.136766)')
set_pin('TwoBoneIK_Left', 'Weight', '1.000000')
set_pin('TwoBoneIK_Left', 'bPropagateToChildren', 'True')

# Right Leg
set_pin('TwoBoneIK_Right', 'PrimaryAxis', '(X=1.000000,Y=0.000000,Z=0.000000)')
set_pin('TwoBoneIK_Right', 'SecondaryAxis', '(X=0.000000,Y=1.000000,Z=0.000000)')
set_pin('TwoBoneIK_Right', 'SecondaryAxisWeight', '1.000000')
set_pin('TwoBoneIK_Right', 'PoleVectorSpace', 'None')
set_pin('TwoBoneIK_Right', 'PoleVectorKind', 'Location')
set_pin('TwoBoneIK_Right', 'PoleVector', '(X=-5.776374,Y=50.000000,Z=28.136766)')
set_pin('TwoBoneIK_Right', 'Weight', '1.000000')
set_pin('TwoBoneIK_Right', 'bPropagateToChildren', 'True')

# Compile CR
print("\nCompiling CR_Student_Procedural...")
comp_res = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'compile_blueprint', {'blueprint': cr})
print("Compile result:", comp_res.get('content', [{}])[0].get('text', ''))

# Save asset
save_res = c.run_tool('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': [cr_path]})
print("Save result:", save_res.get('content', [{}])[0].get('text', ''))

print("\n=== OPTIMIZATION SCRIPT COMPLETE ===")
