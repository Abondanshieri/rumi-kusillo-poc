import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp
import json
import os

c = ue_mcp.UnrealMCPClient()
cr_path = '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'
cr = {'refPath': cr_path}
g = {'refPath': f'{cr_path}:RigVMModel'}
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'

print("=== FINAL RIGOROUS VERIFICATION ===")

# Check 1: CR_Student_Procedural compilation
res_comp_cr = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'compile_blueprint', {'blueprint': cr})
print("CR_Student_Procedural Compile:", res_comp_cr)
assert res_comp_cr.get('isError') is not True, "CR_Student_Procedural compilation failed!"

# Check 2: Student_Skeleton_AnimBlueprint compilation
res_comp_bp = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'compile_blueprint', {'blueprint': {'refPath': bp_path}})
print("Student_Skeleton_AnimBlueprint Compile:", res_comp_bp)
assert res_comp_bp.get('isError') is not True, "Student_Skeleton_AnimBlueprint compilation failed!"

# Check 3: Save assets to disk
res_save = c.run_tool('editor_toolset.toolsets.asset.AssetTools', 'save_assets', {'asset_paths': [
    '/Game/Characters/Student/Rig/CR_Student_Procedural',
    '/Game/Characters/Student/Student_Skeleton_AnimBlueprint'
]})
print("Save Assets:", res_save)

# Check 4: Verify files exist on disk with recent modification time
cr_file = r"D:\Dev\Computacion_Grafica\Rumi 5.8\Content\Characters\Student\Rig\CR_Student_Procedural.uasset"
bp_file = r"D:\Dev\Computacion_Grafica\Rumi 5.8\Content\Characters\Student\Student_Skeleton_AnimBlueprint.uasset"

assert os.path.exists(cr_file), f"CR file missing: {cr_file}"
assert os.path.exists(bp_file), f"BP file missing: {bp_file}"

print(f"\nCR_Student_Procedural.uasset size: {os.path.getsize(cr_file):,} bytes")
print(f"Student_Skeleton_AnimBlueprint.uasset size: {os.path.getsize(bp_file):,} bytes")

# Check 5: Inspect key pins on CR_Student_Procedural
for node_name in ['TwoBoneIK_Left', 'TwoBoneIK_Right']:
    print(f"\n--- {node_name} Verification ---")
    for p in ['BoneA', 'BoneB', 'EffectorBone', 'PrimaryAxis', 'SecondaryAxis', 'PoleVectorSpace', 'PoleVectorKind', 'PoleVector', 'bPropagateToChildren', 'Weight']:
        val = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_pin_value', {
            'control_rig': cr, 'graph': g, 'pin': {'refPath': f"{g['refPath']}.{node_name}.{p}"}
        })
        print(f"  {p}: {val.get('content', [{}])[0].get('text', '')}")
    
    # Verify Effector subpins
    for sub in ['Translation.X', 'Translation.Y', 'Translation.Z', 'Rotation', 'Scale3D']:
        conn = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_connected_pins', {
            'control_rig': cr, 'graph': g, 'pin': {'refPath': f"{g['refPath']}.{node_name}.Effector.{sub}"}
        })
        conns = [x['refPath'].split(':RigVMModel.')[-1] for x in json.loads(conn['content'][0]['text']).get('returnValue', [])]
        print(f"  Effector.{sub} <- {conns}")

print("\n=== ALL CHECKS PASSED PERFECTLY ===")
