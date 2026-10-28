import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'
g_path = f'{bp_path}:AnimGraph'

res = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'read_graph_dsl', {
    'graph': {'refPath': g_path}
})
text = res.get('content', [{}])[0].get('text', '')
print("AnimGraph DSL:")
print(text[:3000])
