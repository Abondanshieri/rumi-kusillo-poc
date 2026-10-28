import ue_mcp, json, sys

sys.stdout.reconfigure(encoding='utf-8')
c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'
fn_graph = {'refPath': f'{bp_path}:UpdateProceduralVariables'}

types = [
    "Matemáticas|Vector|BreakVector",
    "Utilidades|Operadores|Restar",
    "Matemáticas|Vector|MakeVector",
    "Matemáticas|Booleano|ANDBoolean",
    "Matemáticas|Booleano|NOTBoolean"
]

for t in types:
    res = c.run_tool("editor_toolset.toolsets.blueprint.BlueprintTools", "create_node", {
        "graph": fn_graph, "type_id": t, "pos": {"x": 0, "y": 0}
    })
    txt = res.get('content', [{}])[0].get('text', '')
    is_err = res.get('isError', False)
    if not is_err:
        node_ref = json.loads(txt)["returnValue"]
        print(f"Created {t}: {node_ref['refPath'].split('.')[-1]}")
        # delete
        c.run_tool("editor_toolset.toolsets.blueprint.BlueprintTools", "delete_node", {
            "graph": fn_graph, "node": node_ref
        })
    else:
        print(f"FAILED {t}: {txt}")
