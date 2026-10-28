import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
bp_path = '/Game/Characters/Student/Student_Skeleton_AnimBlueprint.Student_Skeleton_AnimBlueprint'
entry_node = {'refPath': f'{bp_path}:UpdateProceduralVariables.K2Node_FunctionEntry_0'}
res = c.run_tool('editor_toolset.toolsets.blueprint.BlueprintTools', 'get_connected_subgraph', {'node': entry_node})
data = json.loads(res['content'][0]['text'])['returnValue']
target_nodes = ['K2Node_CallFunction_22', 'K2Node_CallFunction_23', 'K2Node_CallFunction_24', 'K2Node_CallFunction_25', 
                'K2Node_CallFunction_26', 'K2Node_CallFunction_27', 'K2Node_CallFunction_28', 'K2Node_CallFunction_29',
                'K2Node_CallFunction_30', 'K2Node_CallFunction_31', 'K2Node_CallFunction_32', 'K2Node_CallFunction_33',
                'K2Node_CallFunction_34', 'K2Node_Select_1', 'K2Node_Select_2', 'K2Node_VariableSet_5', 'K2Node_VariableSet_6',
                'K2Node_VariableSet_7', 'K2Node_VariableSet_11', 'K2Node_VariableSet_12', 'K2Node_VariableSet_13', 'K2Node_VariableSet_14',
                'K2Node_PromotableOperator_11', 'K2Node_PromotableOperator_12', 'K2Node_PromotableOperator_13',
                'K2Node_PromotableOperator_14', 'K2Node_PromotableOperator_15', 'K2Node_PromotableOperator_16']

for n in data:
    node_name = n['node']['refPath'].split('.')[-1]
    if node_name in target_nodes:
        print(f"=== {node_name} ({n['type_id']}) ===")
        for pin in n.get('input_pins', []):
            conns = [p['node']['refPath'].split('.')[-1] + ' (' + p['direction'] + ')' for p in pin.get('connected_pins', [])]
            v = pin.get('value', '')
            if conns or (v and v not in ['()', '', 'None', 'false']):
                print(f"   IN  {pin['name']}: val={v} conn={conns}")
        for pin in n.get('output_pins', []):
            conns = [p['node']['refPath'].split('.')[-1] + ' (' + p['direction'] + ')' for p in pin.get('connected_pins', [])]
            if conns:
                print(f"  OUT  {pin['name']}: conn={conns}")
