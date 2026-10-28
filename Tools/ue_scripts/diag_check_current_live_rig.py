import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
cr = {'refPath': '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'}
g = {'refPath': '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural:RigVMModel'}
g_path = g['refPath']

def get_pin(node, pin):
    res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_pin_value', {
        'control_rig': cr, 'graph': g, 'pin': {'refPath': f'{g_path}.{node}.{pin}'}
    })
    return res.get('content', [{}])[0].get('text', '')

def get_conns(node, pin):
    res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_connected_pins', {
        'control_rig': cr, 'graph': g, 'pin': {'refPath': f'{g_path}.{node}.{pin}'}
    })
    try:
        data = json.loads(res.get('content', [{}])[0].get('text', ''))
        return [x['refPath'].split(':RigVMModel.')[-1] for x in data.get('returnValue', [])]
    except Exception as e:
        return str(e)

print("=== CHECKING CURRENT WIRING IN CR_STUDENT_PROCEDURAL ===")

# Check TwoBoneIK_Left
print("TwoBoneIK_Left:")
print("  Weight val:", get_pin('TwoBoneIK_Left', 'Weight'))
print("  Weight conns:", get_conns('TwoBoneIK_Left', 'Weight'))
print("  PrimaryAxis:", get_pin('TwoBoneIK_Left', 'PrimaryAxis'))
print("  SecondaryAxis:", get_pin('TwoBoneIK_Left', 'SecondaryAxis'))
print("  PoleVector:", get_pin('TwoBoneIK_Left', 'PoleVector'))
print("  PoleVectorSpace:", get_pin('TwoBoneIK_Left', 'PoleVectorSpace'))
print("  Effector conns:", get_conns('TwoBoneIK_Left', 'Effector'))
print("  Effector.Translation.Z conns:", get_conns('TwoBoneIK_Left', 'Effector.Translation.Z'))

# Check TwoBoneIK_Right
print("\nTwoBoneIK_Right:")
print("  Weight val:", get_pin('TwoBoneIK_Right', 'Weight'))
print("  Weight conns:", get_conns('TwoBoneIK_Right', 'Weight'))
print("  PrimaryAxis:", get_pin('TwoBoneIK_Right', 'PrimaryAxis'))
print("  SecondaryAxis:", get_pin('TwoBoneIK_Right', 'SecondaryAxis'))
print("  PoleVector:", get_pin('TwoBoneIK_Right', 'PoleVector'))
print("  PoleVectorSpace:", get_pin('TwoBoneIK_Right', 'PoleVectorSpace'))
print("  Effector conns:", get_conns('TwoBoneIK_Right', 'Effector'))
print("  Effector.Translation.Z conns:", get_conns('TwoBoneIK_Right', 'Effector.Translation.Z'))

# Check Set_Hips
print("\nSet_Hips:")
print("  Space:", get_pin('Set_Hips', 'Space'))
print("  Value conns:", get_conns('Set_Hips', 'Value'))
print("  Value.Translation.Z conns:", get_conns('Set_Hips', 'Value.Translation.Z'))

# Check Mul_Hips_Offset
print("\nMul_Hips_Offset:")
print("  A conns:", get_conns('Mul_Hips_Offset', 'A'))
print("  B.Translation.Z conns:", get_conns('Mul_Hips_Offset', 'B.Translation.Z'))
print("  Result conns:", get_conns('Mul_Hips_Offset', 'Result'))

# Check Add_LeftFootZ & Sub_FootOffsetL
print("\nAdd_LeftFootZ & Sub_FootOffsetL:")
print("  Sub_FootOffsetL A conns:", get_conns('Sub_FootOffsetL', 'A'))
print("  Sub_FootOffsetL B conns:", get_conns('Sub_FootOffsetL', 'B'))
print("  Sub_FootOffsetL Result conns:", get_conns('Sub_FootOffsetL', 'Result'))
print("  Add_LeftFootZ A conns:", get_conns('Add_LeftFootZ', 'A'))
print("  Add_LeftFootZ B conns:", get_conns('Add_LeftFootZ', 'B'))
print("  Add_LeftFootZ Result conns:", get_conns('Add_LeftFootZ', 'Result'))

