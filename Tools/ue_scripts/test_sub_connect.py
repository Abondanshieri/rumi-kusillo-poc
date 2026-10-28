import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
cr_path = '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'
cr = {'refPath': cr_path}
g = {'refPath': f'{cr_path}:RigVMModel'}
for sub in ['X', 'Y', 'Z', 'W']:
    src = f"{g['refPath']}.Get_LeftFoot.Transform.Rotation.{sub}"
    tgt = f"{g['refPath']}.TwoBoneIK_Left.Effector.Rotation.{sub}"
    res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'connect_pins', {
        'control_rig': cr, 'graph': g, 'source_pin': {'refPath': src}, 'target_pin': {'refPath': tgt}
    })
    print(f"Connect Rotation.{sub}:", res)
