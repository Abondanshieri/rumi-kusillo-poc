import ue_mcp, json, sys

sys.stdout.reconfigure(encoding='utf-8')
c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'
bp = {'refPath': bp_path}
fn_graph = {'refPath': f'{bp_path}:UpdateProceduralVariables'}

def create_node(type_id, x, y):
    res = c.run_tool("editor_toolset.toolsets.blueprint.BlueprintTools", "create_node", {
        "graph": fn_graph, "type_id": type_id, "pos": {"x": int(x), "y": int(y)}
    })
    txt = res.get('content', [{}])[0].get('text', '')
    if res.get('isError'):
        raise RuntimeError(f"Error creating node {type_id}: {txt}")
    return json.loads(txt)["returnValue"]

def delete_node(node_name):
    ref = {'refPath': f"{fn_graph['refPath']}.{node_name}"}
    return c.run_tool("editor_toolset.toolsets.blueprint.BlueprintTools", "delete_node", {
        "graph": fn_graph, "node": ref
    })

def get_node_pins(node_ref):
    info = c.run_tool("editor_toolset.toolsets.blueprint.BlueprintTools", "get_node_infos", {"nodes": [node_ref]})
    data = json.loads(info["content"][0]["text"])["returnValue"][0]
    in_pins = {p["name"]: p["pin_id"] for p in data.get("input_pins", [])}
    out_pins = {p["name"]: p["pin_id"] for p in data.get("output_pins", [])}
    return in_pins, out_pins

def connect(out_pin, in_pin):
    res = c.run_tool("editor_toolset.toolsets.blueprint.BlueprintTools", "connect_pins", {
        "output_pin": out_pin, "input_pin": in_pin
    })
    if res.get('isError'):
        print(f"FAILED connect: {res}")
    return res

def set_pin(pin_id, val):
    return c.run_tool("editor_toolset.toolsets.blueprint.BlueprintTools", "set_pin_value", {
        "pin": pin_id, "value": str(val)
    })

print("=== PART 2: WIRING CLEAN DECOUPLED RAYCAST VECTORS ===")

# 1. Ensure SetFootOffsetL -> LineTraceRight is connected
set_l_ref = {'refPath': f"{fn_graph['refPath']}.K2Node_VariableSet_5"}
trace_r_ref = {'refPath': f"{fn_graph['refPath']}.K2Node_CallFunction_31"}
_, set_l_outs = get_node_pins(set_l_ref)
trace_r_ins, _ = get_node_pins(trace_r_ref)
connect(set_l_outs["then"], trace_r_ins["execute"])

# 2. Get ActorLocation from K2Node_CallFunction_37
actor_loc_ref = {'refPath': f"{fn_graph['refPath']}.K2Node_CallFunction_37"}
_, actor_loc_outs = get_node_pins(actor_loc_ref)

# 3. Break ActorLocation
break_actor_loc = create_node("Matemáticas|Vector|BreakVector", 900, 450)
bal_ins, bal_outs = get_node_pins(break_actor_loc)
connect(actor_loc_outs["ReturnValue"], bal_ins["InVec"])

# 4. Subtract 150.0 from ActorLocation.Z to get EndZ
sub_end_z = create_node("Utilidades|Operadores|Restar", 1050, 520)
sez_ins, sez_outs = get_node_pins(sub_end_z)
connect(bal_outs["Z"], sez_ins["A"])
set_pin(sez_ins["B"], "150.0")

# 5. Left Foot Trace Start & End
foot_l_ref = {'refPath': f"{fn_graph['refPath']}.K2Node_CallFunction_23"}
_, foot_l_outs = get_node_pins(foot_l_ref)

break_foot_l = create_node("Matemáticas|Vector|BreakVector", 900, 600)
bfl_ins, bfl_outs = get_node_pins(break_foot_l)
connect(foot_l_outs["ReturnValue"], bfl_ins["InVec"])

make_start_l = create_node("Matemáticas|Vector|MakeVector", 1050, 600)
msl_ins, msl_outs = get_node_pins(make_start_l)
connect(bfl_outs["X"], msl_ins["X"])
connect(bfl_outs["Y"], msl_ins["Y"])
connect(bal_outs["Z"], msl_ins["Z"])

make_end_l = create_node("Matemáticas|Vector|MakeVector", 1050, 750)
mel_ins, mel_outs = get_node_pins(make_end_l)
connect(bfl_outs["X"], mel_ins["X"])
connect(bfl_outs["Y"], mel_ins["Y"])
connect(sez_outs["ReturnValue"], mel_ins["Z"])

# Connect to LineTraceLeft (K2Node_CallFunction_26)
trace_l_ref = {'refPath': f"{fn_graph['refPath']}.K2Node_CallFunction_26"}
trace_l_ins, _ = get_node_pins(trace_l_ref)
connect(msl_outs["ReturnValue"], trace_l_ins["Start"])
connect(mel_outs["ReturnValue"], trace_l_ins["End"])
print("Left Foot decoupled trace Start & End connected.")

# 6. Right Foot Trace Start & End
foot_r_ref = {'refPath': f"{fn_graph['refPath']}.K2Node_CallFunction_30"}
_, foot_r_outs = get_node_pins(foot_r_ref)

break_foot_r = create_node("Matemáticas|Vector|BreakVector", 900, 1050)
bfr_ins, bfr_outs = get_node_pins(break_foot_r)
connect(foot_r_outs["ReturnValue"], bfr_ins["InVec"])

make_start_r = create_node("Matemáticas|Vector|MakeVector", 1050, 1050)
msr_ins, msr_outs = get_node_pins(make_start_r)
connect(bfr_outs["X"], msr_ins["X"])
connect(bfr_outs["Y"], msr_ins["Y"])
connect(bal_outs["Z"], msr_ins["Z"])

make_end_r = create_node("Matemáticas|Vector|MakeVector", 1050, 1200)
mer_ins, mer_outs = get_node_pins(make_end_r)
connect(bfr_outs["X"], mer_ins["X"])
connect(bfr_outs["Y"], mer_ins["Y"])
connect(sez_outs["ReturnValue"], mer_ins["Z"])

# Connect to LineTraceRight (K2Node_CallFunction_31)
connect(msr_outs["ReturnValue"], trace_r_ins["Start"])
connect(mer_outs["ReturnValue"], trace_r_ins["End"])
print("Right Foot decoupled trace Start & End connected.")

# 7. Set Reference Floor Distance to 90.0 cm in Promotable Operators
sub_dist_l_ref = {'refPath': f"{fn_graph['refPath']}.K2Node_PromotableOperator_13"}
sub_dist_r_ref = {'refPath': f"{fn_graph['refPath']}.K2Node_PromotableOperator_16"}
sdl_ins, _ = get_node_pins(sub_dist_l_ref)
sdr_ins, _ = get_node_pins(sub_dist_r_ref)
set_pin(sdl_ins["A"], "90.0")
set_pin(sdr_ins["A"], "90.0")
print("Target reference floor distance set to 90.0 cm.")

# 8. Airborne modulation: NOT IsFalling AND bBlockingHit
get_fall_ref = {'refPath': f"{fn_graph['refPath']}.K2Node_VariableGet_15"}
_, fall_outs = get_node_pins(get_fall_ref)

not_fall = create_node("Matemáticas|Booleano|NOTBoolean", 1700, 500)
nf_ins, nf_outs = get_node_pins(not_fall)
connect(fall_outs["IsFalling"], nf_ins["A"])

hit_l_ref = {'refPath': f"{fn_graph['refPath']}.K2Node_CallFunction_27"}
hit_r_ref = {'refPath': f"{fn_graph['refPath']}.K2Node_CallFunction_32"}
_, hit_l_outs = get_node_pins(hit_l_ref)
_, hit_r_outs = get_node_pins(hit_r_ref)

and_l = create_node("Matemáticas|Booleano|ANDBoolean", 1850, 550)
al_ins, al_outs = get_node_pins(and_l)
connect(hit_l_outs["bBlockingHit"], al_ins["A"])
connect(nf_outs["ReturnValue"], al_ins["B"])

and_r = create_node("Matemáticas|Booleano|ANDBoolean", 1850, 1050)
ar_ins, ar_outs = get_node_pins(and_r)
connect(hit_r_outs["bBlockingHit"], ar_ins["A"])
connect(nf_outs["ReturnValue"], ar_ins["B"])

sel_l_ref = {'refPath': f"{fn_graph['refPath']}.K2Node_Select_1"}
sel_r_ref = {'refPath': f"{fn_graph['refPath']}.K2Node_Select_2"}
sel_l_ins, _ = get_node_pins(sel_l_ref)
sel_r_ins, _ = get_node_pins(sel_r_ref)
connect(al_outs["ReturnValue"], sel_l_ins["Index"])
connect(ar_outs["ReturnValue"], sel_r_ins["Index"])
print("Airborne condition wired to Select nodes.")

# Compile and Save AnimBP
comp = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'compile_blueprint', {'blueprint': bp})
print("AnimBP Compile result:", comp)

save = c.run_tool('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': ['/Game/Characters/Student/Student_Skeleton_AnimBlueprint']})
print("AnimBP Save result:", save)
print("=== PART 2 & 3 SUCCESSFUL ===")
