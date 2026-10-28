import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
cr = {'refPath': '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'}
g = {'refPath': '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural:RigVMModel'}
g_path = g['refPath']

# Let's check TestMul or test with SetPinValue on Mul_Hips_Offset
# If A = (Rot=(P=0,Y=0,R=90), Trans=(0, 0, 50), Scale=(1,1,1))
# and B = (Rot=(0,0,0), Trans=(0, 0, -20), Scale=(1,1,1))
# In UE, RigUnit_MathTransformMul:
# Let's inspect TestMul_1 or create a small test node
print("=== VERIFYING TRANSFORM MULTIPLICATION IN RIGVM ===")
# Let's see what TestSRT or TestMul nodes are in the graph
for node in ['TestMul', 'TestMul_1', 'TestMul_2']:
    res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_pin_value', {
        'control_rig': cr, 'graph': g, 'pin': {'refPath': f'{g_path}.{node}.Result'}
    })
    print(f"{node}.Result: {res.get('content', [{}])[0].get('text', '')}")
