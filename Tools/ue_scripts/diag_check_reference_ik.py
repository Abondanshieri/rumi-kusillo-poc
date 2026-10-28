import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
p = '/Game/Characters/Student/Rig/CR_Student_IK.CR_Student_IK'
g = {'refPath': f'{p}:RigVMModel'}
res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'list_nodes', {'control_rig': {'refPath': p}, 'graph': g})
nodes = json.loads(res['content'][0]['text'])['returnValue']
for n in nodes:
    ref = n['refPath']
    name = ref.split('.')[-1]
    if 'TwoBone' in name or 'IK' in name:
        print(f"=== {name} in CR_Student_IK ===")
        pins = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'list_pins', {'control_rig': {'refPath': p}, 'graph': g, 'node': {'refPath': ref}})
        for pin in json.loads(pins['content'][0]['text'])['returnValue']:
            p_name = pin['refPath'].split(':RigVMModel.')[-1]
            # check conn
            conn = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_connected_pins', {'control_rig': {'refPath': p}, 'graph': g, 'pin': pin})
            try:
                conns = json.loads(conn['content'][0]['text']).get('returnValue', [])
                conn_names = [x['refPath'].split(':RigVMModel.')[-1] for x in conns]
            except:
                conn_names = []
            # check val
            val = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_pin_value', {'control_rig': {'refPath': p}, 'graph': g, 'pin': pin})
            try:
                v_str = json.loads(val['content'][0]['text']).get('returnValue', '')
            except:
                v_str = ''
            if conn_names or (v_str and v_str not in ['', '()', 'None', 'false', '0']):
                print(f"  {p_name}: val={v_str} conn={conn_names}")
