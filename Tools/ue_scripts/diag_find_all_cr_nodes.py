import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'

# Query all graphs in AnimBP
graphs_res = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'find_nodes', {
    'blueprint': {'refPath': bp_path},
    'title': ''
})
nodes = json.loads(graphs_res['content'][0]['text'])['returnValue']
print(f"Total nodes across AnimBP: {len(nodes)}")

# Find any node with ControlRig in refPath
cr_nodes = [n for n in nodes if 'controlrig' in n['refPath'].lower()]
print(f"ControlRig nodes in AnimBP: {cr_nodes}")

# Let's inspect each cr_node
for n in cr_nodes:
    info = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'get_node_infos', {'nodes': [n]})
    data = json.loads(info['content'][0]['text'])['returnValue'][0]
    print(f"\nNode {n['refPath']}:")
    for pin in data.get('input_pins', []):
        print(f"  In: {pin['name']} (val='{pin.get('value')}')")
    for pin in data.get('output_pins', []):
        print(f"  Out: {pin['name']}")
