import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'
root_node = {'refPath': f'{bp_path}:AnimGraph.AnimGraphNode_Root_0'}
res = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'get_connected_subgraph', {'node': root_node})
data = json.loads(res['content'][0]['text'])['returnValue']
print(f'Total nodes in AnimGraph: {len(data)}')
for n in data:
    node_name = n['node']['refPath'].split('.')[-1]
    print(f"  {node_name} ({n['type_id']})")
    for pin in n.get('input_pins', []):
        conns = [p['node']['refPath'].split('.')[-1] for p in pin.get('connected_pins', [])]
        v = pin.get('value', '')
        if conns or (v and v not in ['', '()', 'None', 'false']):
            print(f"     IN {pin['name']}: val={v} conn={conns}")
    for pin in n.get('output_pins', []):
        conns = [p['node']['refPath'].split('.')[-1] for p in pin.get('connected_pins', [])]
        if conns:
            print(f"    OUT {pin['name']}: conn={conns}")
