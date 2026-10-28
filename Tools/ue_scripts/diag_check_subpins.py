import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
p = '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'
g = {'refPath': f'{p}:RigVMModel'}
for node_name in ['TwoBoneIK_Left', 'TwoBoneIK_Right']:
    print(f"=== {node_name} Effector subpins ===")
    for sub in ['Translation.X', 'Translation.Y', 'Translation.Z', 'Rotation.X', 'Rotation.Y', 'Rotation.Z', 'Rotation.W']:
        pin_ref = f'{p}:RigVMModel.{node_name}.Effector.{sub}'
        conn = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_connected_pins', {'control_rig': {'refPath': p}, 'graph': g, 'pin': {'refPath': pin_ref}})
        val = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_pin_value', {'control_rig': {'refPath': p}, 'graph': g, 'pin': {'refPath': pin_ref}})
        conns = json.loads(conn.get('content', [{}])[0].get('text', '{}')).get('returnValue', [])
        val_str = json.loads(val.get('content', [{}])[0].get('text', '{}')).get('returnValue', '')
        print(f"  {sub}: val={val_str} conn={[x['refPath'].split(':RigVMModel.')[-1] for x in conns]}")
