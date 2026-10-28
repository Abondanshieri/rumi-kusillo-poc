import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp
import json

c = ue_mcp.UnrealMCPClient()
cr_path = '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'
cr = {'refPath': cr_path}
g = {'refPath': f'{cr_path}:RigVMModel'}

def set_pin(node_name, pin_name, val):
    p = f"{g['refPath']}.{node_name}.{pin_name}"
    res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'set_pin_value', {
        'control_rig': cr, 'graph': g, 'pin': {'refPath': p}, 'value': str(val)
    })
    return res

def connect_pin(src_node, src_pin, tgt_node, tgt_pin):
    src = f"{g['refPath']}.{src_node}.{src_pin}"
    tgt = f"{g['refPath']}.{tgt_node}.{tgt_pin}"
    res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'connect_pins', {
        'control_rig': cr, 'graph': g, 'source_pin': {'refPath': src}, 'target_pin': {'refPath': tgt}
    })
    return res

def disconnect_pin(src_node, src_pin, tgt_node, tgt_pin):
    src = f"{g['refPath']}.{src_node}.{src_pin}"
    tgt = f"{g['refPath']}.{tgt_node}.{tgt_pin}"
    res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'disconnect_pins', {
        'control_rig': cr, 'graph': g, 'source_pin': {'refPath': src}, 'target_pin': {'refPath': tgt}
    })
    return res

print("=== FIXING CR_STUDENT_PROCEDURAL ===")

# 1. FIX EXECUTION CHAIN
print("1. Hooking execution chain...")
connect_pin('RigUnit_BeginExecution', 'ExecutePin', 'Set_Spine1', 'ExecutePin')
connect_pin('Set_Spine1', 'ExecutePin', 'Set_Spine2', 'ExecutePin')
connect_pin('Set_Spine2', 'ExecutePin', 'Set_Neck_Lean', 'ExecutePin')
connect_pin('Set_Neck_Lean', 'ExecutePin', 'Set_Hips', 'ExecutePin')
connect_pin('Set_Hips', 'ExecutePin', 'TwoBoneIK_Left', 'ExecutePin')
connect_pin('TwoBoneIK_Left', 'ExecutePin', 'TwoBoneIK_Right', 'ExecutePin')

# Disconnect Aim_Neck and Aim_Head from execution
disconnect_pin('TwoBoneIK_Right', 'ExecutePin', 'Aim_Neck', 'ExecutePin')
disconnect_pin('Aim_Neck', 'ExecutePin', 'Aim_Head', 'ExecutePin')
set_pin('Aim_Neck', 'Weight', '0.0')
set_pin('Aim_Head', 'Weight', '0.0')

# 2. FIX SET_HIPS TRANSFORM PINS
print("2. Fixing Set_Hips pins...")
set_pin('Set_Hips', 'Space', 'GlobalSpace')
set_pin('Set_Hips', 'bPropagateToChildren', 'True')
set_pin('Set_Hips', 'Weight', '1.0')

# Disconnect top-level Value pin if connected
disconnect_pin('Get_Hips', 'Transform', 'Set_Hips', 'Value')

# Connect individual components
connect_pin('Get_Hips', 'Transform.Translation.X', 'Set_Hips', 'Value.Translation.X')
connect_pin('Get_Hips', 'Transform.Translation.Y', 'Set_Hips', 'Value.Translation.Y')
connect_pin('Add_HipsZ', 'Result', 'Set_Hips', 'Value.Translation.Z')
connect_pin('Get_Hips', 'Transform.Rotation', 'Set_Hips', 'Value.Rotation')
connect_pin('Get_Hips', 'Transform.Scale3D', 'Set_Hips', 'Value.Scale3D')

# 3. FIX LEFT LEG TWOBONEIK
print("3. Fixing Left Leg TwoBoneIK...")
set_pin('TwoBoneIK_Left', 'BoneA', 'LeftUpLeg')
set_pin('TwoBoneIK_Left', 'BoneB', 'LeftLeg')
set_pin('TwoBoneIK_Left', 'EffectorBone', 'LeftFoot')
set_pin('TwoBoneIK_Left', 'PrimaryAxis', '(X=0.000000,Y=-1.000000,Z=0.000000)')
set_pin('TwoBoneIK_Left', 'SecondaryAxis', '(X=0.000000,Y=0.000000,Z=-1.000000)')
set_pin('TwoBoneIK_Left', 'SecondaryAxisWeight', '1.0')
set_pin('TwoBoneIK_Left', 'PoleVectorKind', 'Location')
set_pin('TwoBoneIK_Left', 'PoleVectorSpace', 'LeftLeg')
set_pin('TwoBoneIK_Left', 'PoleVector', '(X=0.000000,Y=0.000000,Z=-50.000000)')
set_pin('TwoBoneIK_Left', 'bPropagateToChildren', 'True')
set_pin('TwoBoneIK_Left', 'Weight', '1.0')

# Disconnect top-level Effector pin
disconnect_pin('Get_LeftFoot', 'Transform', 'TwoBoneIK_Left', 'Effector')

# Connect individual components
connect_pin('Get_LeftFoot', 'Transform.Translation.X', 'TwoBoneIK_Left', 'Effector.Translation.X')
connect_pin('Get_LeftFoot', 'Transform.Translation.Y', 'TwoBoneIK_Left', 'Effector.Translation.Y')
connect_pin('Add_LeftFootZ', 'Result', 'TwoBoneIK_Left', 'Effector.Translation.Z')
connect_pin('Get_LeftFoot', 'Transform.Rotation', 'TwoBoneIK_Left', 'Effector.Rotation')
connect_pin('Get_LeftFoot', 'Transform.Scale3D', 'TwoBoneIK_Left', 'Effector.Scale3D')

# 4. FIX RIGHT LEG TWOBONEIK
print("4. Fixing Right Leg TwoBoneIK...")
set_pin('TwoBoneIK_Right', 'BoneA', 'RightUpLeg')
set_pin('TwoBoneIK_Right', 'BoneB', 'RightLeg')
set_pin('TwoBoneIK_Right', 'EffectorBone', 'RightFoot')
set_pin('TwoBoneIK_Right', 'PrimaryAxis', '(X=0.000000,Y=-1.000000,Z=0.000000)')
set_pin('TwoBoneIK_Right', 'SecondaryAxis', '(X=0.000000,Y=0.000000,Z=-1.000000)')
set_pin('TwoBoneIK_Right', 'SecondaryAxisWeight', '1.0')
set_pin('TwoBoneIK_Right', 'PoleVectorKind', 'Location')
set_pin('TwoBoneIK_Right', 'PoleVectorSpace', 'RightLeg')
set_pin('TwoBoneIK_Right', 'PoleVector', '(X=0.000000,Y=0.000000,Z=-50.000000)')
set_pin('TwoBoneIK_Right', 'bPropagateToChildren', 'True')
set_pin('TwoBoneIK_Right', 'Weight', '1.0')

# Disconnect top-level Effector pin
disconnect_pin('Get_RightFoot', 'Transform', 'TwoBoneIK_Right', 'Effector')

# Connect individual components
connect_pin('Get_RightFoot', 'Transform.Translation.X', 'TwoBoneIK_Right', 'Effector.Translation.X')
connect_pin('Get_RightFoot', 'Transform.Translation.Y', 'TwoBoneIK_Right', 'Effector.Translation.Y')
connect_pin('Add_RightFootZ', 'Result', 'TwoBoneIK_Right', 'Effector.Translation.Z')
connect_pin('Get_RightFoot', 'Transform.Rotation', 'TwoBoneIK_Right', 'Effector.Rotation')
connect_pin('Get_RightFoot', 'Transform.Scale3D', 'TwoBoneIK_Right', 'Effector.Scale3D')

# 5. COMPILE AND SAVE ASSET
print("5. Compiling and saving asset...")
compile_res = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'compile_blueprint', {'blueprint': cr})
print("Compile result:", compile_res)

save_res = c.run_tool('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': ['/Game/Characters/Student/Rig/CR_Student_Procedural']})
print("Save result:", save_res)

print("=== FIX COMPLETED SUCCESSFULLY ===")
