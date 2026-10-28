import ue_mcp, json

c = ue_mcp.UnrealMCPClient()

def dump_rig(rig_name):
    p = f'/Game/Characters/Student/Rig/{rig_name}.{rig_name}'
    g = {'refPath': f'{p}:RigVMModel'}
    res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'list_nodes', {'control_rig': {'refPath': p}, 'graph': g})
    nodes = json.loads(res['content'][0]['text'])['returnValue']
    print(f"\n==================== {rig_name} ====================")
    for n in nodes:
        ref = n['refPath']
        name = ref.split('.')[-1]
        pins = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'list_pins', {'control_rig': {'refPath': p}, 'graph': g, 'node': {'refPath': ref}})
        pin_list = json.loads(pins['content'][0]['text'])['returnValue']
        print(f"--- Node: {name} ---")
        for pin in pin_list:
            p_name = pin['refPath'].split('.')[-1]
            # only check important pins or subpins
            val = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_pin_value', {
                'control_rig': {'refPath': p}, 'graph': g, 'pin': pin
            })
            val_str = json.loads(val['content'][0]['text']).get('returnValue', '')
            conn = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_connected_pins', {
                'control_rig': {'refPath': p}, 'graph': g, 'pin': pin
            })
            conns = json.loads(conn['content'][0]['text']).get('returnValue', [])
            conn_names = [x['refPath'].split(':RigVMModel.')[-1] for x in conns]
            if conn_names or (val_str and val_str not in ['()', '', 'None', 'false', '0', '0.000000', '0.0']):
                print(f"    {p_name}: val={val_str} conn={conn_names}")

if __name__ == '__main__':
    dump_rig('CR_Student_IK')
