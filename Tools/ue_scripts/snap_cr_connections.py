"""Snapshot de nodos y conexiones (pin -> pin, incluye sub-pines) de un Control Rig, ejecutado DENTRO del editor via ProgrammaticToolset.
Uso: python -B -I snap_cr_connections.py <rig_name> <out.json>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ue_mcp import UnrealMCPClient
SCRIPT = r'''
import json
CRT = "animation_toolset.toolsets.controlrig.ControlRigTools"
SUB = ["Translation","Rotation","Scale","X","Y","Z","W","Pitch","Yaw","Roll"]
def T(name, a):
    return execute_tool(CRT + "." + name, json.dumps(a))["returnValue"]
def run():
    cr = {"refPath": "/Game/Characters/Student/Rig/@@N@@.@@N@@"}
    g = {"refPath": cr["refPath"] + ":RigVMModel"}
    base = g["refPath"] + "."
    nodes = {}
    edges = set()
    def split_top(v):
        out = []
        depth = 0
        q = False
        cur = ""
        for ch in v:
            if ch == '"':
                q = not q
            if not q and ch == "(":
                depth += 1
            if not q and ch == ")":
                depth -= 1
            if not q and depth == 0 and ch == ",":
                out.append(cur)
                cur = ""
            else:
                cur += ch
        if cur:
            out.append(cur)
        return out
    def walk(pref, v):
        try:
            r = T("get_connected_pins", {"control_rig": cr, "pin": {"refPath": pref}})
        except Exception as e:
            return
        for o in r:
            a = pref.replace(base, "")
            b = o["refPath"].replace(base, "")
            edges.add(a + " <-> " + b if a < b else b + " <-> " + a)
        if isinstance(v, str) and v.startswith("(") and v.endswith(")") and v != "()":
            parts = split_top(v[1:-1])
            if any(p.split("=",1)[0].strip() == "W" for p in parts):
                return
            for part in parts:
                if "=" in part:
                    k, val = part.split("=", 1)
                    k = k.strip()
                    if k.isidentifier() or k.replace("_", "").isalnum():
                        walk(pref + "." + k, val.strip())
    for n in T("list_nodes", {"control_rig": cr, "graph": g}):
        p = T("get_node_position", {"control_rig": cr, "node": n})
        nodes[n["refPath"].replace(base, "")] = [round(p["x"]), round(p["y"])]
        for pin in T("list_pins", {"control_rig": cr, "node": n}):
            walk(pin["refPath"], T("get_pin_value", {"control_rig": cr, "pin": pin}))
    return {"nodes": nodes, "edges": sorted(edges)}
'''
def snap(name, c=None):
    c = c or UnrealMCPClient()
    r = c.call_raw('tools/call', {'name': 'call_tool', 'arguments': {'toolset_name': 'editor_toolset.toolsets.programmatic.ProgrammaticToolset', 'tool_name': 'execute_tool_script', 'arguments': {'script': SCRIPT.replace('@@N@@', name)}}}, timeout=900)['result']
    t = r['content'][0]['text']
    i = t.rfind('{"returnValue"')
    if i < 0: open("C:/Users/franc/AppData/Local/Temp/raw.txt","w",encoding="utf8").write(t); raise RuntimeError(t[:800])
    x = json.loads(t[i:])['returnValue']
    return json.loads(x) if isinstance(x, str) else x
if __name__ == '__main__':
    r = snap(sys.argv[1])
    json.dump(r, open(sys.argv[2], 'w'), indent=1)
    print(sys.argv[1], len(r['nodes']), 'nodos', len(r['edges']), 'conexiones')
