import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'
g_path = f'{bp_path}:UpdateProceduralVariables'

nodes_to_inspect = [
    'K2Node_CallFunction_24', 'K2Node_CallFunction_25',
    'K2Node_PromotableOperator_11', 'K2Node_PromotableOperator_12',
    'K2Node_PromotableOperator_13', 'K2Node_CallFunction_28', 'K2Node_CallFunction_29',
    'K2Node_PromotableOperator_14', 'K2Node_PromotableOperator_15',
    'K2Node_PromotableOperator_16', 'K2Node_CallFunction_33', 'K2Node_CallFunction_34',
    'K2Node_CommutativeAssociativeBinaryOperator_1'
]

info_res = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'get_node_infos', {
    'nodes': [{'refPath': f'{g_path}.{n}'} for n in nodes_to_inspect]
})
infos = json.loads(info_res['content'][0]['text'])['returnValue']

for nname, info in zip(nodes_to_inspect, infos):
    print(f"\n--- {nname} ({info.get('type_id')}) ---")
    for p in info.get('input_pins', []):
        conns = [c['node']['refPath'].split('.')[-1] for c in p.get('connected_pins', [])]
        print(f"  IN  {p['name']}: val='{p.get('value')}' conns={conns}")
    for p in info.get('output_pins', []):
        conns = [c['node']['refPath'].split('.')[-1] for c in p.get('connected_pins', [])]
        print(f"  OUT {p['name']}: conns={conns}")
