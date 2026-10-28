import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'
node_ref = {'refPath': f'{bp_path}:AnimGraph.AnimGraphNode_ControlRig_1'}
info_res = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'get_node_infos', {'nodes': [node_ref]})
info = json.loads(info_res['content'][0]['text'])['returnValue'][0]
print('Class:', info.get('class_name'))
print('Input pins:')
for p in info.get('input_pins', []):
    conns = [c['node']['refPath'].split(':AnimGraph.')[-1] for c in p.get('connected_pins', [])]
    print(f"  {p['name']}: val='{p.get('value')}' conns={conns}")
