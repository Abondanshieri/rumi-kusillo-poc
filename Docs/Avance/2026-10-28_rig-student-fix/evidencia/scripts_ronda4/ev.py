from a import *
CR="animation_toolset.toolsets.controlrig.ControlRigTools"
def Jv(ts,t,a):
    x=c.run_tool(ts,t,a)['content'][0]['text']
    try: return json.loads(x)['returnValue']
    except: return x
out={}
for rn,nodes in (('CR_Student_Procedural_fix',['TwoBoneIK_Left','TwoBoneIK_Right']),('CR_Student_IK_fix',['IK_LeftLeg','IK_RightLeg','IK_LeftArm','IK_RightArm']),('CR_Student_Procedural',['TwoBoneIK_Left','TwoBoneIK_Right']),('CR_Student_IK',['IK_LeftLeg','IK_RightLeg','IK_LeftArm','IK_RightArm'])):
    rig={'refPath':f'/Game/Characters/Student/Rig/{rn}.{rn}'}; Gp={'refPath':rig['refPath']+':RigVMModel'}
    for n in nodes:
        node={'refPath':Gp['refPath']+'.'+n}
        pins=Jv(CR,'list_pins',{'control_rig':rig,'node':node})
        d={}
        for p in pins:
            nm=p['refPath'].split('.')[-1]
            if any(k in nm for k in ('PrimaryAxis','SecondaryAxis','SecondaryAxisWeight','PoleVector','Weight','bPropagate','Alpha')) :
                d[nm]=Jv(CR,'get_pin_value',{'control_rig':rig,'pin':p})
        out[f'{rn}/{n}']=d
        print(rn,n,d)
json.dump(out,open('pins_rigs.json','w'),indent=1)
