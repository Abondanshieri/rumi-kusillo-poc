import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
cr = {'refPath': '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'}

res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'add_variable', {
    'control_rig': cr,
    'variable_name': 'LegIKAlpha',
    'variable_type': 'float',
    'default_value': '1.000000',
    'is_public': True
})
print("Add LegIKAlpha:", res.get('content', [{}])[0].get('text', ''))
