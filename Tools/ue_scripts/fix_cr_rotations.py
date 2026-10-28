import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
cr_path = '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'
cr = {'refPath': cr_path}
g = {'refPath': f'{cr_path}:RigVMModel'}

def connect(src_node, src_pin, tgt_node, tgt_pin):
    src = f"{g['refPath']}.{src_node}.{src_pin}"
    tgt = f"{g['refPath']}.{tgt_node}.{tgt_pin}"
    res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'connect_pins', {
        'control_rig': cr, 'graph': g, 'source_pin': {'refPath': src}, 'target_pin': {'refPath': tgt}
    })
    print(f"Connect {src_node}.{src_pin} -> {tgt_node}.{tgt_pin}:", res.get('isError', False))

print("Connecting Rotations and Scales in CR_Student_Procedural...")
# 1. Hips
connect('Get_Hips', 'Transform.Rotation', 'Set_Hips', 'Value.Rotation')
connect('Get_Hips', 'Transform.Scale3D', 'Set_Hips', 'Value.Scale3D')

# 2. LeftFoot
connect('Get_LeftFoot', 'Transform.Rotation', 'TwoBoneIK_Left', 'Effector.Rotation')
connect('Get_LeftFoot', 'Transform.Scale3D', 'TwoBoneIK_Left', 'Effector.Scale3D')

# 3. RightFoot
connect('Get_RightFoot', 'Transform.Rotation', 'TwoBoneIK_Right', 'Effector.Rotation')
connect('Get_RightFoot', 'Transform.Scale3D', 'TwoBoneIK_Right', 'Effector.Scale3D')

# Compile and Save
comp = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'compile_blueprint', {'blueprint': cr})
print("CR Compile:", comp)

save = c.run_tool('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': ['/Game/Characters/Student/Rig/CR_Student_Procedural']})
print("CR Save:", save)
