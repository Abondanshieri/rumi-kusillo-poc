import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'
ref = {'refPath': f'{bp_path}:EventGraph.K2Node_Event_1'}
res = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'get_connected_subgraph', {'node': ref})
data = json.loads(res['content'][0]['text'])['returnValue']
for n in data:
    name = n['node']['refPath'].split('.')[-1]
    print(name, f"({n['type_id']})")
    for p in n.get('output_pins', []):
        conns = [x['node']['refPath'].split('.')[-1] for x in p.get('connected_pins', [])]
        if conns:
            print(f"   OUT {p['name']} -> {conns}")
