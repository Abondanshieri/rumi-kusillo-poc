import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'
node_ref = {'refPath': f'{bp_path}:AnimGraph.AnimGraphNode_ControlRig_1'}
res = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'get_node_infos', {'nodes': [node_ref]})
data = json.loads(res['content'][0]['text'])['returnValue'][0]
print('Node details for AnimGraphNode_ControlRig_1:')
for p in data.get('input_pins', []):
    conns = [x['node']['refPath'].split('.')[-1] for x in p.get('connected_pins', [])]
    print(f"  IN: {p['name']} (type={p.get('type_id')}) val={p.get('value')} conn={conns}")
for p in data.get('output_pins', []):
    conns = [x['node']['refPath'].split('.')[-1] for x in p.get('connected_pins', [])]
    print(f"  OUT: {p['name']} conn={conns}")
