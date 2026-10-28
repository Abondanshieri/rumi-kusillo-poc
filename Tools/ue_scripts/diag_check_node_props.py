import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'

# Try to check properties of AnimGraphNode_ControlRig_1
res = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'get_node_property', {
    'blueprint': {'refPath': bp_path},
    'graph': {'refPath': f'{bp_path}:AnimGraph'},
    'node': {'refPath': f'{bp_path}:AnimGraph.AnimGraphNode_ControlRig_1'},
    'property_name': 'Node'
})
print("get_node_property 'Node':", res)

res2 = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'get_node_property', {
    'blueprint': {'refPath': bp_path},
    'graph': {'refPath': f'{bp_path}:AnimGraph'},
    'node': {'refPath': f'{bp_path}:AnimGraph.AnimGraphNode_ControlRig_1'},
    'property_name': 'ControlRigClass'
})
print("get_node_property 'ControlRigClass':", res2)
