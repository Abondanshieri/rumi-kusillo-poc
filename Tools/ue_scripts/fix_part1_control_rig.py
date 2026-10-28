import ue_mcp, json, sys

c = ue_mcp.UnrealMCPClient()
cr_path = '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'
cr = {'refPath': cr_path}
g = {'refPath': f'{cr_path}:RigVMModel'}

def p_ref(node, pin):
    return {'refPath': f"{g['refPath']}.{node}.{pin}"}

def conn(src_node, src_pin, tgt_node, tgt_pin):
    res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'connect_pins', {
        'control_rig': cr, 'graph': g,
        'source_pin': p_ref(src_node, src_pin),
        'target_pin': p_ref(tgt_node, tgt_pin)
    })
    if res.get('isError'):
        print(f"FAILED connect {src_node}.{src_pin} -> {tgt_node}.{tgt_pin}: {res}")
    else:
        print(f"Connected {src_node}.{src_pin} -> {tgt_node}.{tgt_pin}")
    return res

def disc(src_node, src_pin, tgt_node, tgt_pin):
    return c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'disconnect_pins', {
        'control_rig': cr, 'graph': g,
        'source_pin': p_ref(src_node, src_pin),
        'target_pin': p_ref(tgt_node, tgt_pin)
    })

def set_pin(node, pin, val):
    res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'set_pin_value', {
        'control_rig': cr, 'graph': g,
        'pin': p_ref(node, pin),
        'value': str(val)
    })
    return res

def create_node(ntype, nname, x, y):
    res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'create_node', {
        'control_rig': cr, 'graph': g,
        'node_type': ntype, 'node_name': nname,
        'position': {'x': float(x), 'y': float(y)}
    })
    return res

def delete_node(nname):
    return c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'delete_node', {
        'control_rig': cr, 'graph': g,
        'node': {'refPath': f"{g['refPath']}.{nname}"}
    })

print("=== PART 1: FIXING CR_STUDENT_PROCEDURAL ROTATIONS & TRANSFORMS ===")

# Delete stale test nodes if they exist
for stale in ['TestMul', 'TestSRT', 'Test_MakeXform']:
    try:
        delete_node(stale)
    except:
        pass

# ------------------------------------------------------------------------------
# 1. HIPS: Add Z offset via MathTransformMake + MathTransformMul in LocalSpace
# ------------------------------------------------------------------------------
# Disconnect previous Set_Hips subpins
disc('Get_Hips', 'Transform.Translation.X', 'Set_Hips', 'Value.Translation.X')
disc('Get_Hips', 'Transform.Translation.Y', 'Set_Hips', 'Value.Translation.Y')
disc('Add_HipsZ', 'Result', 'Set_Hips', 'Value.Translation.Z')

# Ensure Make_Hips_Offset exists
try:
    create_node('RigUnit_MathTransformMake', 'Make_Hips_Offset', 600, 850)
except:
    pass

# Ensure Mul_Hips_Offset exists
try:
    create_node('RigUnit_MathTransformMul', 'Mul_Hips_Offset', 800, 800)
except:
    pass

# Connect Add_PelvisLand.Result -> Make_Hips_Offset.Translation.Z
conn('Add_PelvisLand', 'Result', 'Make_Hips_Offset', 'Translation.Z')
# Connect Get_Hips.Transform -> Mul_Hips_Offset.A
conn('Get_Hips', 'Transform', 'Mul_Hips_Offset', 'A')
# Connect Make_Hips_Offset.Result -> Mul_Hips_Offset.B
conn('Make_Hips_Offset', 'Result', 'Mul_Hips_Offset', 'B')
# Connect Mul_Hips_Offset.Result -> Set_Hips.Value
conn('Mul_Hips_Offset', 'Result', 'Set_Hips', 'Value')
set_pin('Set_Hips', 'Space', 'LocalSpace')
set_pin('Set_Hips', 'Weight', '1.0')
set_pin('Set_Hips', 'bPropagateToChildren', 'True')
print("Hips Transform wiring complete.")

# ------------------------------------------------------------------------------
# 2. LEFT FOOT: Add Z offset via MathTransformMake + MathTransformMul in GlobalSpace
# ------------------------------------------------------------------------------
# Disconnect previous TwoBoneIK_Left subpins
disc('Get_LeftFoot', 'Transform.Translation.X', 'TwoBoneIK_Left', 'Effector.Translation.X')
disc('Get_LeftFoot', 'Transform.Translation.Y', 'TwoBoneIK_Left', 'Effector.Translation.Y')
disc('Add_LeftFootZ', 'Result', 'TwoBoneIK_Left', 'Effector.Translation.Z')

try:
    create_node('RigUnit_MathTransformMake', 'Make_LeftFoot_Offset', 600, 1150)
except:
    pass

try:
    create_node('RigUnit_MathTransformMul', 'Mul_LeftFoot_Offset', 800, 1100)
except:
    pass

# Sub_FootOffsetL.Result is (FootOffsetL - PelvisOffset)
conn('Sub_FootOffsetL', 'Result', 'Make_LeftFoot_Offset', 'Translation.Z')
conn('Get_LeftFoot', 'Transform', 'Mul_LeftFoot_Offset', 'A')
conn('Make_LeftFoot_Offset', 'Result', 'Mul_LeftFoot_Offset', 'B')
conn('Mul_LeftFoot_Offset', 'Result', 'TwoBoneIK_Left', 'Effector')

# Configure Pole Vector and axes to match CR_Student_IK
set_pin('TwoBoneIK_Left', 'PrimaryAxis', '(X=1.000000,Y=0.000000,Z=0.000000)')
set_pin('TwoBoneIK_Left', 'SecondaryAxis', '(X=0.000000,Y=1.000000,Z=0.000000)')
set_pin('TwoBoneIK_Left', 'PoleVectorSpace', 'None')
set_pin('TwoBoneIK_Left', 'PoleVectorKind', 'Location')
set_pin('TwoBoneIK_Left', 'PoleVector', '(X=6.070472,Y=34.979931,Z=28.136766)')
set_pin('TwoBoneIK_Left', 'Weight', '1.0')
set_pin('TwoBoneIK_Left', 'bPropagateToChildren', 'True')
print("Left Foot TwoBoneIK wiring complete.")

# ------------------------------------------------------------------------------
# 3. RIGHT FOOT: Add Z offset via MathTransformMake + MathTransformMul in GlobalSpace
# ------------------------------------------------------------------------------
# Disconnect previous TwoBoneIK_Right subpins
disc('Get_RightFoot', 'Transform.Translation.X', 'TwoBoneIK_Right', 'Effector.Translation.X')
disc('Get_RightFoot', 'Transform.Translation.Y', 'TwoBoneIK_Right', 'Effector.Translation.Y')
disc('Add_RightFootZ', 'Result', 'TwoBoneIK_Right', 'Effector.Translation.Z')

try:
    create_node('RigUnit_MathTransformMake', 'Make_RightFoot_Offset', 600, 1400)
except:
    pass

try:
    create_node('RigUnit_MathTransformMul', 'Mul_RightFoot_Offset', 800, 1350)
except:
    pass

conn('Sub_FootOffsetR', 'Result', 'Make_RightFoot_Offset', 'Translation.Z')
conn('Get_RightFoot', 'Transform', 'Mul_RightFoot_Offset', 'A')
conn('Make_RightFoot_Offset', 'Result', 'Mul_RightFoot_Offset', 'B')
conn('Mul_RightFoot_Offset', 'Result', 'TwoBoneIK_Right', 'Effector')

set_pin('TwoBoneIK_Right', 'PrimaryAxis', '(X=1.000000,Y=0.000000,Z=0.000000)')
set_pin('TwoBoneIK_Right', 'SecondaryAxis', '(X=0.000000,Y=1.000000,Z=0.000000)')
set_pin('TwoBoneIK_Right', 'PoleVectorSpace', 'None')
set_pin('TwoBoneIK_Right', 'PoleVectorKind', 'Location')
set_pin('TwoBoneIK_Right', 'PoleVector', '(X=-5.776374,Y=34.926186,Z=28.136766)')
set_pin('TwoBoneIK_Right', 'Weight', '1.0')
set_pin('TwoBoneIK_Right', 'bPropagateToChildren', 'True')
print("Right Foot TwoBoneIK wiring complete.")

# Compile and Save
comp = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'compile_blueprint', {'blueprint': cr})
print("CR Compile result:", comp)

save = c.run_tool('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': ['/Game/Characters/Student/Rig/CR_Student_Procedural']})
print("CR Save result:", save)
print("=== PART 1 SUCCESSFUL ===")
