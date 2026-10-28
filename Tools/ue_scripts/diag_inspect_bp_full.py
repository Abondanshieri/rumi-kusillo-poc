import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'
entry_node = {'refPath': f'{bp_path}:UpdateProceduralVariables.K2Node_FunctionEntry_0'}
res = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'get_connected_subgraph', {'node': entry_node})
data = json.loads(res['content'][0]['text'])['returnValue']

# Find all nodes related to foot traces
nodes_by_name = {}
for n in data:
    name = n['node']['refPath'].split('.')[-1]
    nodes_by_name[name] = n

print("Total nodes:", len(nodes_by_name))
for name in sorted(nodes_by_name.keys()):
    if any(k in name for k in ['22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', 'Select_1', 'Select_2', 'Set_5', 'Set_6', 'Set_7', 'Set_11', 'Set_12', 'Set_13', 'Set_14', 'Operator_11', 'Operator_12', 'Operator_13', 'Operator_14', 'Operator_15', 'Operator_16', 'MakeArray']):
        n = nodes_by_name[name]
        print(f"\nNode: {name} ({n['type_id']}) at ({n['position']['x']}, {n['position']['y']})")
        for pin in n['input_pins']:
            conns = [p['node']['refPath'].split('.')[-1] + '.' + str(p['index_id']) for p in pin.get('connected_pins', [])]
            if conns or pin.get('value'):
                print(f"  IN  {pin['name']} ({pin['type_id']}): val={pin.get('value')} conn={conns}")
        for pin in n['output_pins']:
            conns = [p['node']['refPath'].split('.')[-1] + '.' + str(p['index_id']) for p in pin.get('connected_pins', [])]
            if conns:
                print(f"  OUT {pin['name']} ({pin['type_id']}): conn={conns}")
