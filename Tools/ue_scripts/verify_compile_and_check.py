import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
cr = {'refPath': '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'}
g = {'refPath': '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural:RigVMModel'}
g_path = g['refPath']

c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'compile_blueprint', {'blueprint': cr})
res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_pin_value', {
    'control_rig': cr, 'graph': g, 'pin': {'refPath': f'{g_path}.TestMul_1.Result'}
})
print("After compile TestMul_1.Result:", res.get('content', [{}])[0].get('text', ''))
