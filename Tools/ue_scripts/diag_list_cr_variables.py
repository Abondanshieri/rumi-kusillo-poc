import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ue_mcp, json

sys.stdout.reconfigure(encoding='utf-8')

c = ue_mcp.UnrealMCPClient()
cr = {'refPath': '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'}
g = {'refPath': '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural:RigVMModel'}
g_path = g['refPath']

# In ControlRig, VariableNodes have a pin named 'Variable' or 'Value'
# Let's inspect all VariableNodes in the rig
res = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'list_nodes', {'control_rig': cr, 'graph': g})
nodes = json.loads(res['content'][0]['text'])['returnValue']
var_nodes = [n['refPath'].split('.')[-1] for n in nodes if 'VariableNode' in n['refPath']]

print("Variable nodes:", var_nodes)
for vn in var_nodes:
    # let's get the variable name bound to this node
    val = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_pin_value', {
        'control_rig': cr, 'graph': g, 'pin': {'refPath': f'{g_path}.{vn}.Variable'}
    })
    print(f"  {vn}.Variable: {val.get('content', [{}])[0].get('text', '')}")
    val2 = c.run_tool('animation_toolset.toolsets.controlrig.ControlRigTools', 'get_pin_value', {
        'control_rig': cr, 'graph': g, 'pin': {'refPath': f'{g_path}.{vn}.Value'}
    })
    print(f"  {vn}.Value: {val2.get('content', [{}])[0].get('text', '')}")
