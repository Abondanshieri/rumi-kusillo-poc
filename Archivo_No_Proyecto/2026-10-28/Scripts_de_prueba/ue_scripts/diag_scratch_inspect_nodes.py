import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'
g_path = f'{bp_path}:UpdateProceduralVariables'
nodes_res = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'find_nodes', {
    'blueprint': {'refPath': bp_path}, 'graph': {'refPath': g_path}, 'title': ''
})
nodes = json.loads(nodes_res['content'][0]['text'])['returnValue']
info_res = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'get_node_infos', {'nodes': nodes})
for n in json.loads(info_res['content'][0]['text'])['returnValue']:
    print(f"{n.get('node_name')}: {n.get('title')}")
