import ue_mcp, json

c = ue_mcp.UnrealMCPClient()
p = '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'
g = {'refPath': f'{p}:RigVMModel'}

script = '''
import json
def run():
    p = '/Game/Characters/Student/Rig/CR_Student_Procedural.CR_Student_Procedural'
    g = {'refPath': f'{p}:RigVMModel'}
    extra = ['TestMul', 'TestSRT', 'Mul_Hips_Offset', 'Clamp_LeftOffset', 'Clamp_RightOffset']
    out = {}
    for name in extra:
        pins = execute_tool('animation_toolset.toolsets.controlrig.ControlRigTools.list_pins', json.dumps({'control_rig': {'refPath': p}, 'graph': g, 'node': {'refPath': f'{p}:RigVMModel.{name}'}}))['returnValue']
        node_info = {}
        for pin in pins:
            pname = pin['refPath'].split(':RigVMModel.')[-1]
            conns = execute_tool('animation_toolset.toolsets.controlrig.ControlRigTools.get_connected_pins', json.dumps({'control_rig': {'refPath': p}, 'graph': g, 'pin': pin}))['returnValue']
            if conns:
                node_info[pname] = [x['refPath'].split(':RigVMModel.')[-1] for x in conns]
        out[name] = node_info
    return out
'''
res = c.run_tool('editor_toolset.toolsets.programmatic.ProgrammaticToolset', 'execute_tool_script', {'script': script})
print(json.dumps(json.loads(res['content'][0]['text'])['returnValue'], indent=2))
