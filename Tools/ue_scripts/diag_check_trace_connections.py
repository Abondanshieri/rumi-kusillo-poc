import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'
fn_graph = {'refPath': f'{bp_path}:UpdateProceduralVariables'}

for node_name in ['K2Node_CallFunction_26', 'K2Node_CallFunction_31']:
    ref = {'refPath': f"{fn_graph['refPath']}.{node_name}"}
    info = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'get_node_infos', {'nodes': [ref]})
    data = json.loads(info['content'][0]['text'])['returnValue'][0]
    print(f"\n=== PINS FOR {node_name} ===")
    for p in data['input_pins']:
        conns = [x['node']['refPath'].split('.')[-1] for x in p.get('connected_pins', [])]
        print(f"  IN {p['name']}: val={p.get('value')} conn={conns}")
