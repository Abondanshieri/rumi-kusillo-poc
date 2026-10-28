import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
cr_path = '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'
cr = {'refPath': cr_path}
g = {'refPath': f'{cr_path}:RigVMModel'}
src = f"{g['refPath']}.Get_Hips.Transform.Rotation"
tgt = f"{g['refPath']}.Set_Hips.Value.Rotation"
res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'connect_pins', {
    'control_rig': cr, 'graph': g, 'source_pin': {'refPath': src}, 'target_pin': {'refPath': tgt}
})
print("Result:", res)
