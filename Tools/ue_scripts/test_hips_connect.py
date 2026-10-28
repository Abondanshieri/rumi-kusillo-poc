import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
cr_path = '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'
cr = {'refPath': cr_path}
g = {'refPath': f'{cr_path}:RigVMModel'}

def disc(src, tgt):
    return c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'disconnect_pins', {
        'control_rig': cr, 'graph': g,
        'source_pin': {'refPath': f"{g['refPath']}.{src}"},
        'target_pin': {'refPath': f"{g['refPath']}.{tgt}"}
    })

def conn(src, tgt):
    res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'connect_pins', {
        'control_rig': cr, 'graph': g,
        'source_pin': {'refPath': f"{g['refPath']}.{src}"},
        'target_pin': {'refPath': f"{g['refPath']}.{tgt}"}
    })
    print(f"Connect {src} -> {tgt}:", res)
    return res

# Disconnect individual X, Y
disc('Get_Hips.Transform.Translation.X', 'Set_Hips.Value.Translation.X')
disc('Get_Hips.Transform.Translation.Y', 'Set_Hips.Value.Translation.Y')

# Connect full transform
conn('Get_Hips.Transform', 'Set_Hips.Value')

# Now reconnect Add_HipsZ to Value.Translation.Z
conn('Add_HipsZ.Result', 'Set_Hips.Value.Translation.Z')

# Compile and check
comp = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'compile_blueprint', {'blueprint': cr})
print("Compile:", comp)
