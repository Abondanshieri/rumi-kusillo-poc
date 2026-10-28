"""Snapshot nodos/conexiones de los grafos del ABP _fix. Uso: python -B -I snap_abp_connections.py <out.json>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ue_mcp import UnrealMCPClient
B = 'editor_toolset.toolsets.blueprint.BlueprintTools'
c = UnrealMCPClient()
def J(t, a):
    x = c.run_tool(B, t, a)['content'][0]['text']
    try: return json.loads(x).get('returnValue')
    except Exception: return x
bp = {'refPath': '/Game/Characters/Student/Student_Skeleton_AnimBlueprint_fix.Student_Skeleton_AnimBlueprint_fix'}
def snap():
    res = {}
    for gn in ('AnimGraph', 'EventGraph', 'UpdateProceduralVariables', 'TestFunc'):
        g = J('get_graph', {'blueprint': bp, 'graph_name': gn})
        base = g['refPath'] + '.'
        ns = J('find_nodes', {'graph': g, 'title': '', 'node_class': '', 'entry_points_only': False})
        nodes, edges = {}, set()
        for i in range(0, len(ns), 20):
            for inf in J('get_node_infos', {'nodes': ns[i:i+20]}):
                nn = inf['node']['refPath'].replace(base, '')
                nodes[nn] = {'x': round(inf['position']['x']), 'y': round(inf['position']['y']), 'type': inf.get('type_id')}
                for p in inf['input_pins']:
                    for cp in p['connected_pins']:
                        src = cp['node']['refPath'].replace(base, '')
                        edges.add((f"{src}#out{cp['index_id']}", f"{nn}.{p['name']}"))
        res[gn] = {'nodes': nodes, 'edges': sorted(edges)}
    return res
if __name__ == '__main__':
    r = snap()
    json.dump(r, open(sys.argv[1], 'w'), indent=1)
    for k, v in r.items(): print(k, len(v['nodes']), len(v['edges']))
