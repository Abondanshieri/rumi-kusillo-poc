import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'
ref = {'refPath': f'{bp_path}:EventGraph.K2Node_PromotableOperator_12'}
info = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'get_node_infos', {'nodes': [ref]})
data = json.loads(info['content'][0]['text'])['returnValue'][0]
print("Pins of K2Node_PromotableOperator_12:")
for p in data['input_pins']:
    conns = [x['node']['refPath'].split('.')[-1] for x in p.get('connected_pins', [])]
    print(f"  IN {p['name']} val={p.get('value')} conn={conns}")
for p in data['output_pins']:
    conns = [x['node']['refPath'].split('.')[-1] for x in p.get('connected_pins', [])]
    print(f"  OUT {p['name']} conn={conns}")
