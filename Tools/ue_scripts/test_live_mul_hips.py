import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
cr = {'refPath': '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'}
g = {'refPath': '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural:RigVMModel'}
g_path = g['refPath']

# In RigVM, SetPinValue on Mul_Hips_Offset.A:
# Let's set A to (Rotation=(X=0.707107,Y=0.000000,Z=0.000000,W=0.707107),Translation=(X=0.150000,Y=0.290000,Z=52.720000),Scale3D=(X=1.000000,Y=1.000000,Z=1.000000))
# which is the exact initial transform of Hips (Roll=90)
# and B to (Rotation=(X=0.000000,Y=0.000000,Z=0.000000,W=1.000000),Translation=(X=0.000000,Y=0.000000,Z=-20.000000),Scale3D=(X=1.000000,Y=1.000000,Z=1.000000))
c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'set_pin_value', {
    'control_rig': cr, 'graph': g, 'pin': {'refPath': f'{g_path}.TestMul_1.A'},
    'value': '(Rotation=(X=0.707107,Y=0.000000,Z=0.000000,W=0.707107),Translation=(X=0.150000,Y=0.290000,Z=52.720000),Scale3D=(X=1.000000,Y=1.000000,Z=1.000000))'
})
c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'set_pin_value', {
    'control_rig': cr, 'graph': g, 'pin': {'refPath': f'{g_path}.TestMul_1.B'},
    'value': '(Rotation=(X=0.000000,Y=0.000000,Z=0.000000,W=1.000000),Translation=(X=0.000000,Y=0.000000,Z=-20.000000),Scale3D=(X=1.000000,Y=1.000000,Z=1.000000))'
})

res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_pin_value', {
    'control_rig': cr, 'graph': g, 'pin': {'refPath': f'{g_path}.TestMul_1.Result'}
})
print("Result of Hips * (Z=-20):", res.get('content', [{}])[0].get('text', ''))
