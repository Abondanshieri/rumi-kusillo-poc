import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
cr = {'refPath': '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'}
g = {'refPath': '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural:RigVMModel'}
g_path = g['refPath']

# Test creating RigUnit_MathFloatMax
res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'create_node', {
    'control_rig': cr, 'graph': g, 'node_type': 'RigUnit_MathFloatMax', 'node_name': 'TestFloatMax', 'position': {'x': 100, 'y': 100}
})
print("Create RigUnit_MathFloatMax:", res.get('content', [{}])[0].get('text', ''))

# Test creating RigUnit_MathFloatClamp
res2 = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'create_node', {
    'control_rig': cr, 'graph': g, 'node_type': 'RigUnit_MathFloatClamp', 'node_name': 'TestFloatClamp', 'position': {'x': 100, 'y': 200}
})
print("Create RigUnit_MathFloatClamp:", res2.get('content', [{}])[0].get('text', ''))

# Clean up test nodes
c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'remove_node', {
    'control_rig': cr, 'graph': g, 'node_name': 'TestFloatMax'
})
c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'remove_node', {
    'control_rig': cr, 'graph': g, 'node_name': 'TestFloatClamp'
})
