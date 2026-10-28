import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'
g_path = f'{bp_path}:UpdateProceduralVariables'

# We want to see all nodes connected from Sequence then_1 (or then_2, etc.)
res = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'find_nodes', {
    'blueprint': {'refPath': bp_path},
    'graph': {'refPath': g_path},
    'title': ''
})
nodes = json.loads(res['content'][0]['text'])['returnValue']
info_res = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'get_node_infos', {'nodes': nodes})
infos = json.loads(info_res['content'][0]['text'])['returnValue']

print(f"Total nodes: {len(infos)}")

# Print all nodes that do math, trace, variable set/get
for info in infos:
    nname = info.get('node', {}).get('refPath', '').split('.')[-1]
    tid = info.get('type_id', '')
    # Check if node has anything to do with feet, trace, or pelvis
    in_pins = info.get('input_pins', [])
    out_pins = info.get('output_pins', [])
    
    # print nodes that set or get FootOffset, PelvisOffset, or do LineTrace
    relevant = False
    for p in in_pins + out_pins:
        pname = p.get('name', '')
        pval = p.get('value', '')
        if any(k in pname.lower() or k in pval.lower() for k in ['footoffset', 'pelvisoffset', 'trace', 'socket', 'bone', 'hit']):
            relevant = True
            break
    if relevant or 'LineTrace' in tid or 'Select' in nname:
        print(f"\n--- {nname} ({tid}) ---")
        for p in in_pins:
            conns = [c['node']['refPath'].split('.')[-1] for c in p.get('connected_pins', [])]
            print(f"  IN  {p['name']}: val='{p.get('value')}' conns={conns}")
        for p in out_pins:
            conns = [c['node']['refPath'].split('.')[-1] for c in p.get('connected_pins', [])]
            print(f"  OUT {p['name']}: conns={conns}")
