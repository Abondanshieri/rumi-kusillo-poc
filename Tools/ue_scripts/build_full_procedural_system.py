import ue_mcp
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

client = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'
bp = {'refPath': bp_path}
fn_graph = {'refPath': f'{bp_path}:UpdateProceduralVariables'}
event_graph = {'refPath': f'{bp_path}:EventGraph'}

def create_fn_node(type_id, x, y):
    res = client.run_tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools",
        "create_node",
        {"graph": fn_graph, "type_id": type_id, "pos": {"x": int(x), "y": int(y)}}
    )
    raw = json.loads(res["content"][0]["text"])
    return raw["returnValue"]

def get_node_pins(node_ref):
    info = client.run_tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools",
        "get_node_infos",
        {"nodes": [node_ref]}
    )
    data = json.loads(info["content"][0]["text"])["returnValue"][0]
    in_pins = {p["name"]: p["pin_id"] for p in data.get("input_pins", [])}
    out_pins = {p["name"]: p["pin_id"] for p in data.get("output_pins", [])}
    return in_pins, out_pins

def connect(out_pin, in_pin):
    res = client.run_tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools",
        "connect_pins",
        {"output_pin": out_pin, "input_pin": in_pin}
    )
    return res

def set_pin(pin_id, val_str):
    res = client.run_tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools",
        "set_pin_value",
        {"pin": pin_id, "value": str(val_str)}
    )
    return res

print("=== BUILDING FULL PROCEDURAL SYSTEM IN ANIMBLUEPRINT ===")

# Query function sequence and entry nodes
seq_ref = {'refPath': f'{bp_path}:UpdateProceduralVariables.K2Node_ExecutionSequence_0'}
entry_ref = {'refPath': f'{bp_path}:UpdateProceduralVariables.K2Node_FunctionEntry_0'}
seq_ins, seq_outs = get_node_pins(seq_ref)
entry_ins, entry_outs = get_node_pins(entry_ref)
dt_pin = entry_outs["DeltaTimeX"]

# ==============================================================================
# BRANCH 1 & 2 ALREADY WIRED
# ==============================================================================
print("\n--- [1/4] Branch 1: Lean Roll already wired ---")
print("--- [2/4] Branch 2: Foot Traces & PelvisOffset already wired ---")

# ==============================================================================
# BRANCH 3: LAND CROUCH
# ==============================================================================
print("\n--- [3/4] Wiring Branch 3: LandCrouch ---")
then_3 = seq_outs["then_3"]

get_falling = create_fn_node("Variables|Predeterminado|ObtenerIsFalling", 500, 1500)
get_tti = create_fn_node("Variables|Predeterminado|ObtenerTimetoImpact", 500, 1600)
get_pfs = create_fn_node("Variables|Predeterminado|ObtenerPeakFallSpeed", 500, 1750)
_, fall_outs = get_node_pins(get_falling)
_, tti_outs = get_node_pins(get_tti)
_, pfs_outs = get_node_pins(get_pfs)

comp_tti = create_fn_node("Utilidades|Operadores|Menorque(<)", 750, 1600)
ctti_ins, ctti_outs = get_node_pins(comp_tti)
connect(tti_outs["TimeToImpact"], ctti_ins["A"])
set_pin(ctti_ins["B"], "0.35")

and_land = create_fn_node("Matemáticas|Booleano|ANDBoolean", 950, 1550)
and_ins, and_outs = get_node_pins(and_land)
connect(fall_outs["IsFalling"], and_ins["A"])
connect(ctti_outs["ReturnValue"], and_ins["B"])

div_pfs = create_fn_node("Utilidades|Operadores|Dividir", 750, 1750)
dpfs_ins, dpfs_outs = get_node_pins(div_pfs)
connect(pfs_outs["PeakFallSpeed"], dpfs_ins["A"])
set_pin(dpfs_ins["B"], "1000.0")

clamp_pfs = create_fn_node("Matemáticas|Float|Clamp(Float)", 950, 1750)
cpfs_ins, cpfs_outs = get_node_pins(clamp_pfs)
connect(dpfs_outs["ReturnValue"], cpfs_ins["Value"])
set_pin(cpfs_ins["Min"], "0.2")
set_pin(cpfs_ins["Max"], "1.0")

div_tti = create_fn_node("Utilidades|Operadores|Dividir", 950, 1900)
dtti_ins, dtti_outs = get_node_pins(div_tti)
connect(tti_outs["TimeToImpact"], dtti_ins["A"])
set_pin(dtti_ins["B"], "0.35")

sub_tti = create_fn_node("Utilidades|Operadores|Restar", 1150, 1900)
stti_ins, stti_outs = get_node_pins(sub_tti)
set_pin(stti_ins["A"], "1.0")
connect(dtti_outs["ReturnValue"], stti_ins["B"])

mul_target_land = create_fn_node("Utilidades|Operadores|Multiplicar", 1350, 1800)
mtl_ins, mtl_outs = get_node_pins(mul_target_land)
connect(cpfs_outs["ReturnValue"], mtl_ins["A"])
connect(stti_outs["ReturnValue"], mtl_ins["B"])

sel_land = create_fn_node("Utilidades|Seleccionar", 1550, 1600)
sland_ins, sland_outs = get_node_pins(sel_land)
set_pin(sland_ins["Option 0"], "0.0")
connect(mtl_outs["ReturnValue"], sland_ins["Option 1"])
connect(and_outs["ReturnValue"], sland_ins["Index"])

get_cur_lc = create_fn_node("Variables|Predeterminado|ObtenerLandCrouch", 1550, 1750)
_, gclc_outs = get_node_pins(get_cur_lc)

interp_lc = create_fn_node("Matemáticas|Interpolación|FInterpTo", 1800, 1650)
intlc_ins, intlc_outs = get_node_pins(interp_lc)
connect(gclc_outs["LandCrouch"], intlc_ins["Current"])
connect(sland_outs["ReturnValue"], intlc_ins["Target"])
connect(dt_pin, intlc_ins["DeltaTime"])
set_pin(intlc_ins["InterpSpeed"], "10.0")

set_land_crouch = create_fn_node("Variables|Predeterminado|EstablecerLandCrouch", 2050, 1650)
slc_ins, _ = get_node_pins(set_land_crouch)
connect(intlc_outs["ReturnValue"], slc_ins["LandCrouch"])

# Wire exec
connect(then_3, slc_ins["execute"])
print("Branch 3 (LandCrouch) wired successfully.")

# ==============================================================================
# BRANCH 4: LOOK TARGET & LOOK ALPHA
# ==============================================================================
print("\n--- [4/4] Wiring Branch 4: LookTarget & LookAlpha ---")
then_4 = seq_outs["then_4"]

get_char_4 = create_fn_node("Variables|Predeterminado|ObtenerCharacter", 500, 2200)
_, char4_outs = get_node_pins(get_char_4)

get_loc = create_fn_node("Transformación|GetActorLocation", 700, 2150)
get_fwd = create_fn_node("Transformación|GetActorForwardVector", 700, 2300)
gloc_ins, gloc_outs = get_node_pins(get_loc)
gfwd_ins, gfwd_outs = get_node_pins(get_fwd)
connect(char4_outs["Character"], gloc_ins["self"])
connect(char4_outs["Character"], gfwd_ins["self"])

mul_fwd = create_fn_node("Utilidades|Operadores|Multiplicar", 950, 2300)
mfwd_ins, mfwd_outs = get_node_pins(mul_fwd)
connect(gfwd_outs["ReturnValue"], mfwd_ins["A"])
set_pin(mfwd_ins["B"], "500.0")

add_loc_fwd = create_fn_node("Utilidades|Operadores|Añadir", 1150, 2200)
alf_ins, alf_outs = get_node_pins(add_loc_fwd)
connect(gloc_outs["ReturnValue"], alf_ins["A"])
connect(mfwd_outs["ReturnValue"], alf_ins["B"])

make_vlook = create_fn_node("Matemáticas|Vector|MakeVector", 1150, 2350)
mvl_ins, mvl_outs = get_node_pins(make_vlook)
set_pin(mvl_ins["Z"], "50.0")

add_final_look = create_fn_node("Utilidades|Operadores|Añadir", 1350, 2250)
afl_ins, afl_outs = get_node_pins(add_final_look)
connect(alf_outs["ReturnValue"], afl_ins["A"])
connect(mvl_outs["ReturnValue"], afl_ins["B"])

set_look_target = create_fn_node("Variables|Predeterminado|EstablecerLookTarget", 1600, 2200)
slt_ins, slt_outs = get_node_pins(set_look_target)
connect(afl_outs["ReturnValue"], slt_ins["LookTarget"])

set_look_alpha = create_fn_node("Variables|Predeterminado|EstablecerLookAlpha", 1900, 2200)
sla_ins, _ = get_node_pins(set_look_alpha)
set_pin(sla_ins["LookAlpha"], "1.0")

connect(then_4, slt_ins["execute"])
connect(slt_outs["then"], sla_ins["execute"])
print("Branch 4 (LookTarget & LookAlpha) wired successfully.")

# ==============================================================================
# HOOK INTO EVENTGRAPH (from K2Node_ExecutionSequence_0.then_4)
# ==============================================================================
print("\n--- Connecting UpdateProceduralVariables to EventGraph Sequence ---")
eg_seq_ref = {'refPath': f'{bp_path}:EventGraph.K2Node_ExecutionSequence_0'}
eg_event0_ref = {'refPath': f'{bp_path}:EventGraph.K2Node_Event_0'}

eg_seq_ins, eg_seq_outs = get_node_pins(eg_seq_ref)
eg_ev0_ins, eg_ev0_outs = get_node_pins(eg_event0_ref)

# Find CallFunction node or create it
call_fn_res = client.run_tool(
    "editor_toolset.toolsets.blueprint.BlueprintTools",
    "create_node",
    {
        "graph": event_graph,
        "type_id": "Funcióndellamada|UpdateProceduralVariables",
        "pos": {"x": 500, "y": 800}
    }
)
call_fn_ref = json.loads(call_fn_res["content"][0]["text"])["returnValue"]
print(f"Created CallFunction node: {call_fn_ref['refPath']}")

cf_ins, cf_outs = get_node_pins(call_fn_ref)

# Connect then_4 from Sequence to CallFunction execute
connect(eg_seq_outs["then_4"], cf_ins["execute"])
# Connect DeltaTimeX from EventBlueprintUpdateAnimation to CallFunction DeltaTimeX
connect(eg_ev0_outs["DeltaTimeX"], cf_ins["DeltaTimeX"])
print("Hooked into EventGraph successfully!")

# ==============================================================================
# COMPILE AND SAVE
# ==============================================================================
print("\n--- Compiling Student_Skeleton_AnimBlueprint ---")
comp_res = client.run_tool(
    "editor_toolset.toolsets.blueprint.BlueprintTools",
    "compile_blueprint",
    {"blueprint": bp}
)
print("Compile result:", comp_res)

print("\n--- Saving Assets ---")
save_res = client.run_tool(
    "editor_toolset.toolsets.asset.AssetTools",
    "save_assets",
    {"assets": [bp_path]}
)
print("Save result:", save_res)
print("\n=== PROCEDURAL SYSTEM COMPLETE AND SAVED ===")
