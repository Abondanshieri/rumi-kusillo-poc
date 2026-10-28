import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
cr_ik = {'refPath': '/Game/Characters/Student/Rig/CR_Student_IK.CR_Student_IK'}

for ctrl in ['ctrl_pole_knee_l', 'ctrl_pole_knee_r', 'ctrl_foot_l_ik', 'ctrl_foot_r_ik']:
    res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_global_transform', {
        'control_rig': cr_ik,
        'item': {'name': ctrl, 'type': 'Control'},
        'initial': True
    })
    txt = res.get('content', [{}])[0].get('text', '')
    print(f"{ctrl} initial global: {txt}")
