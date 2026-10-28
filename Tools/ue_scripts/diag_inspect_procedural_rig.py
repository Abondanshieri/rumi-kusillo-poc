import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
p = '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'
g = {'refPath': f'{p}:RigVMModel'}
res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'list_nodes', {'control_rig': {'refPath': p}, 'graph': g})
nodes = json.loads(res['content'][0]['text'])['returnValue']
print(f"Total nodes in CR_Student_Procedural: {len(nodes)}")

for n in nodes:
    ref = n['refPath']
    name = ref.split('.')[-1]
    pins = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'list_pins', {'control_rig': {'refPath': p}, 'graph': g, 'node': {'refPath': ref}})
    pin_list = json.loads(pins['content'][0]['text'])['returnValue']
    
    # get connections and values
    has_info = False
    lines = []
    for pin in pin_list:
        p_name = pin['refPath'].split(':RigVMModel.')[-1]
        val = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_pin_value', {
            'control_rig': {'refPath': p}, 'graph': g, 'pin': pin
        })
        val_str = json.loads(val['content'][0]['text']).get('returnValue', '')
        conn = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_connected_pins', {
            'control_rig': {'refPath': p}, 'graph': g, 'pin': pin
        })
        conns = json.loads(conn['content'][0]['text']).get('returnValue', [])
        conn_names = [x['refPath'].split(':RigVMModel.')[-1] for x in conns]
        if conn_names or (val_str and val_str not in ['()', '', 'None', 'false', '0', '0.000000', '0.0', '1.000000']):
            lines.append(f"    {p_name.split('.')[-1]}: val={val_str} conn={conn_names}")
    
    print(f"\n--- Node: {name} ---")
    for l in lines:
        print(l)
