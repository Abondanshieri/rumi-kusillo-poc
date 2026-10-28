import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
cr = {'refPath': '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'}
g = {'refPath': '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural:RigVMModel'}
g_path = g['refPath']

for pin in ['A', 'B', 'Result']:
    p_ref = f'{g_path}.Add_HipsZ.{pin}'
    val = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_pin_value', {'control_rig': cr, 'graph': g, 'pin': {'refPath': p_ref}})
    conns = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_connected_pins', {'control_rig': cr, 'graph': g, 'pin': {'refPath': p_ref}})
    print(f"Add_HipsZ.{pin}: val={val.get('content',[{}])[0].get('text','')} conns={conns.get('content',[{}])[0].get('text','')}")
