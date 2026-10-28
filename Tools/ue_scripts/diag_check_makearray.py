import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'
fn_graph = {'refPath': f'{bp_path}:UpdateProceduralVariables'}
ref = {'refPath': f"{fn_graph['refPath']}.K2Node_MakeArray_0"}
info = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'get_node_infos', {'nodes': [ref]})
data = json.loads(info['content'][0]['text'])['returnValue'][0]
print([(p['name'], [x['node']['refPath'].split('.')[-1] for x in p.get('connected_pins', [])]) for p in data['input_pins']])
