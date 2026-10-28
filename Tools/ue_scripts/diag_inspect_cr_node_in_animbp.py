import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'
g_path = f'{bp_path}:AnimGraph'

# Find nodes in AnimGraph
res = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'find_nodes', {
    'blueprint': {'refPath': bp_path},
    'graph': {'refPath': g_path},
    'title': ''
})
nodes = json.loads(res['content'][0]['text'])['returnValue']
info_res = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'get_node_infos', {'nodes': nodes})
infos = json.loads(info_res['content'][0]['text'])['returnValue']

for info in infos:
    title = info.get('title', '')
    node_name = info.get('node_name', '')
    type_id = info.get('type_id', '')
    if any(k in str(title).lower() or k in str(node_name).lower() or k in str(type_id).lower() for k in ['controlrig', 'control rig', 'rig', 'cr_student']):
        print(f"Node: {node_name} | Title: {title} | Type: {type_id}")
        for p in info.get('input_pins', []):
            conns = [c['node']['refPath'].split('.')[-1] for c in p.get('connected_pins', [])]
            print(f"  IN  {p['name']}: val='{p.get('value')}' conns={conns}")
        for p in info.get('output_pins', []):
            conns = [c['node']['refPath'].split('.')[-1] for c in p.get('connected_pins', [])]
            print(f"  OUT {p['name']}: conns={conns}")
