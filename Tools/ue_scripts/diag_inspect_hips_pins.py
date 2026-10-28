import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
cr_path = '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'
cr = {'refPath': cr_path}
g = {'refPath': f'{cr_path}:RigVMModel'}

for n in ['Get_Hips', 'Set_Hips', 'TwoBoneIK_Left']:
    pins = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'list_pins', {
        'control_rig': cr, 'graph': g, 'node': {'refPath': f'{g["refPath"]}.{n}'}
    })
    print(f"\n=== PINS FOR {n} ===")
    for p in json.loads(pins['content'][0]['text'])['returnValue']:
        pref = p['refPath'].split(':RigVMModel.')[-1]
        val = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_pin_value', {
            'control_rig': cr, 'graph': g, 'pin': p
        })
        v_str = json.loads(val['content'][0]['text']).get('returnValue', '')
        print(f"  {pref}: {v_str}")
