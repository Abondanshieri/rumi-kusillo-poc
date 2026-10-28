import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'
fn_graph = {'refPath': f'{bp_path}:UpdateProceduralVariables'}

for n in ['K2Node_Select_1', 'K2Node_Select_2', 'K2Node_CallFunction_28', 'K2Node_CallFunction_33', 'K2Node_CallFunction_29', 'K2Node_CallFunction_34']:
    ref = {'refPath': f"{fn_graph['refPath']}.{n}"}
    info = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'get_node_infos', {'nodes': [ref]})
    data = json.loads(info['content'][0]['text'])['returnValue'][0]
    print(f"\nNode {n} ({data['type_id']}):")
    for p in data['input_pins']:
        conns = [x['node']['refPath'].split('.')[-1] for x in p.get('connected_pins', [])]
        print(f"  IN {p['name']} val={p.get('value')} conn={conns}")
    for p in data['output_pins']:
        conns = [x['node']['refPath'].split('.')[-1] for x in p.get('connected_pins', [])]
        print(f"  OUT {p['name']} conn={conns}")
