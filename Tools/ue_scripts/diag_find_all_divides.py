import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'

for graph_name in ['EventGraph', 'UpdateProceduralVariables']:
    ref = {'refPath': f'{bp_path}:{graph_name}'}
    # get all nodes
    entry = {'refPath': f'{bp_path}:{graph_name}.K2Node_FunctionEntry_0'} if graph_name != 'EventGraph' else {'refPath': f'{bp_path}:EventGraph.K2Node_Event_0'}
    sub = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'get_connected_subgraph', {'node': entry})
    nodes = json.loads(sub['content'][0]['text'])['returnValue']
    print(f"\n=== GRAPH: {graph_name} ({len(nodes)} nodes) ===")
    for n in nodes:
        type_id = n['type_id']
        name = n['node']['refPath'].split('.')[-1]
        if 'div' in type_id.lower() or '/' in type_id or 'dividir' in type_id.lower():
            print(f"  DIVISION NODE: {name} ({type_id})")
            for p in n['input_pins']:
                conns = [x['node']['refPath'].split('.')[-1] for x in p.get('connected_pins', [])]
                print(f"     IN {p['name']}: val={p.get('value')} conn={conns}")
