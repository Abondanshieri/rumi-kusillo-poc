import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
p = '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'
g = {'refPath': f'{p}:RigVMModel'}
for node_name in ['Set_Hips', 'TwoBoneIK_Left', 'TwoBoneIK_Right']:
    print(f"=== {node_name} ===")
    for pin in ['BoneA', 'BoneB', 'EffectorBone', 'PrimaryAxis', 'SecondaryAxis', 'PoleVectorSpace', 'PoleVectorKind', 'PoleVector', 'bPropagateToChildren', 'Weight', 'Space']:
        v = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_pin_value', {
            'control_rig': {'refPath': p}, 'graph': g, 'pin': {'refPath': f'{p}:RigVMModel.{node_name}.{pin}'}
        })
        txt = v.get('content', [{}])[0].get('text', '')
        try:
            d = json.loads(txt)
            if 'returnValue' in d:
                print(f"  {pin}: {d['returnValue']}")
        except:
            pass

    # Check connected pins for Effector or Value
    for sub in ['Value', 'Effector', 'Value.Translation.Z', 'Effector.Translation.Z']:
        conn = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_connected_pins', {
            'control_rig': {'refPath': p}, 'graph': g, 'pin': {'refPath': f'{p}:RigVMModel.{node_name}.{sub}'}
        })
        txt = conn.get('content', [{}])[0].get('text', '')
        try:
            d = json.loads(txt)
            if 'returnValue' in d and d['returnValue']:
                conns = [x['refPath'].split(':RigVMModel.')[-1] for x in d['returnValue']]
                print(f"  CONN {sub} <- {conns}")
        except:
            pass
