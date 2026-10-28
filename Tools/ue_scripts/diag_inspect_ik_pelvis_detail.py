import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
cr = {'refPath': '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'}
g = {'refPath': '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural:RigVMModel'}
g_path = g['refPath']

nodes_to_inspect = [
    'VariableNode_2', 'VariableNode_3', 'Mul_LandCrouch', 'Add_PelvisLand',
    'Get_Hips', 'Mul_Hips_Offset', 'Set_Hips',
    'VariableNode_4', 'Sub_FootOffsetL', 'Get_LeftFoot', 'Add_LeftFootZ', 'TwoBoneIK_Left',
    'VariableNode_5', 'Sub_FootOffsetR', 'Get_RightFoot', 'Add_RightFootZ', 'TwoBoneIK_Right'
]

print("=== DETAILED NODE INSPECTION ===")

for n in nodes_to_inspect:
    print(f"\n--- Node: {n} ---")
    # inspect common pins
    for pin in ['Value', 'A', 'B', 'Result', 'Space', 'Weight', 'PrimaryAxis', 'SecondaryAxis', 'PoleVector', 'PoleVectorKind', 'PoleVectorSpace', 'bPropagateToChildren']:
        res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_pin_value', {
            'control_rig': cr, 'graph': g, 'pin': {'refPath': f'{g_path}.{n}.{pin}'}
        })
        val = res.get('content', [{}])[0].get('text', '')
        if 'not found' not in val.lower() and 'is not valid' not in val.lower():
            try:
                parsed = json.loads(val).get('returnValue')
            except:
                parsed = val
            print(f"  {pin} = {parsed}")
            
    # inspect connections on Result or output pins or Effector / Value
    for check_pin in ['Result', 'Value', 'Transform', 'Effector', 'A', 'B', 'ExecutePin']:
        res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_connected_pins', {
            'control_rig': cr, 'graph': g, 'pin': {'refPath': f'{g_path}.{n}.{check_pin}'}
        })
        val = res.get('content', [{}])[0].get('text', '')
        if 'not found' not in val.lower() and 'is not valid' not in val.lower():
            try:
                conns = [x['refPath'].split(':RigVMModel.')[-1] for x in json.loads(val).get('returnValue', [])]
                if conns:
                    print(f"  {check_pin} connects to/from: {conns}")
            except:
                pass
