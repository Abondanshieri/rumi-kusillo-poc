"""G1 layout v2: escalera de ejecucion. Rejilla 50u, pitch de columna 450u. Bloques apilados verticalmente.
Cajas = bbox estimado + margen 100 (titulo 250 arriba)."""
import math, json, itertools
P=450
def est(n):
    if n.startswith('RigUnit_Begin'): return (300,120)
    if n.startswith('Get_') and n[4:] in ('LeanRoll','LeanPitch','PelvisOffset','LandCrouch','FootOffsetL','FootOffsetR'): return (300,110)
    if n.startswith('TwoBoneIK') or n.startswith('IK_'): return (350,650)
    if n.startswith('Set'): return (400,380)
    if n.startswith('GetTransform_'): return (400,300)
    if n.startswith('Get_'): return (400,300)
    if n.startswith('Quat'): return (300,260)
    if n.startswith('Make'): return (350,300)
    if n.startswith('Mul_Hips') or n.startswith('ORFANO'): return (400,380)
    if n.startswith('Mul_LeftFoot') or n.startswith('Mul_RightFoot'): return (350,260)
    if n.startswith('Clamp'): return (300,220)
    return (300,200)
M=100; T=250; GAP=400
def snap50(v,up=False): return (math.ceil if up else math.floor)(v/50)*50
def box(pos,names):
    x0=min(pos[n][0] for n in names); y0=min(pos[n][1] for n in names)
    x1=max(pos[n][0]+est(n)[0] for n in names); y1=max(pos[n][1]+est(n)[1] for n in names)
    x=snap50(x0-M); y=snap50(y0-T)
    return dict(pos=(x,y),size=(snap50(x1+M-x,True),snap50(y1+M-y,True)))
def stack(blocks):
    pos={}; boxes={}; cur=0
    for name,nodes in blocks:
        loc={n:(c*P,y) for n,(c,y) in nodes.items()}
        b=box(loc,list(loc)); dy=snap50(cur-b['pos'][1],True)
        for n,(x,y) in loc.items(): pos[n]=(x,y+dy)
        boxes[name]=box(pos,list(loc)); boxes[name]['nodes']=list(loc)
        cur=boxes[name]['pos'][1]+boxes[name]['size'][1]+GAP
    return pos,boxes
BLUE=(0.10,0.25,0.60,0.5); GREEN=(0.15,0.45,0.20,0.5); ORANGE=(0.70,0.40,0.10,0.5); RED=(0.60,0.12,0.12,0.5); PURPLE=(0.40,0.20,0.55,0.5)
def proc():
    ent={'RigUnit_BeginExecution':(2,0)}
    lean={'Get_LeanPitch':(0,700),'Get_LeanRoll':(0,850),
      'Quat_Spine1':(1,0),'Get_Spine1':(1,300),'Mul_Spine1':(2,100),'Set_Spine1':(3,150),
      'Mul_Pitch_Spine2':(1,650),'Mul_Roll_Spine2':(1,900),'Quat_Spine2':(2,750),'Get_Spine2':(2,1050),'Mul_Spine2':(3,900),'Set_Spine2':(4,950),
      'Mul_Pitch_Neck':(2,1400),'Mul_Roll_Neck':(2,1650),'Quat_Neck':(3,1500),'Get_Neck_Lean':(3,1800),'Mul_Neck_Lean':(4,1650),'Set_Neck_Lean':(5,1700)}
    cad={'Get_LandCrouch':(1,0),'Mul_LandCrouch':(2,0),'Get_PelvisOffset':(1,650),'Add_PelvisLand':(3,150),
      'Make_Hips_Offset':(4,450),'Get_Hips':(4,50),'Add_HipsZ':(5,0),'Mul_Hips_Offset':(5,300),'Set_Hips':(6,300)}
    izq={'Get_FootOffsetL':(3,100),'Sub_FootOffsetL':(4,100),'Clamp_LeftOffset':(5,0),'Make_LeftFoot_Offset':(5,600),'Get_LeftFoot':(5,300),
      'Add_LeftFootZ':(6,0),'Mul_LeftFoot_Offset':(6,600),'TwoBoneIK_Left':(7,200)}
    der={'Get_FootOffsetR':(4,100),'Sub_FootOffsetR':(5,100),'Clamp_RightOffset':(6,0),'Make_RightFoot_Offset':(6,600),'Get_RightFoot':(6,300),
      'Add_RightFootZ':(7,0),'Mul_RightFoot_Offset':(7,600),'TwoBoneIK_Right':(8,0)}
    orf={'ORFANO_Mul_Hips_Offset_1':(0,0)}
    pos,boxes=stack([('ENTRADA',ent),('LEAN',lean),('CADERA',cad),('PIERNA IZQ',izq),('PIERNA DER',der),('ORFANO',orf)])
    col={'ENTRADA':BLUE,'LEAN':GREEN,'CADERA':GREEN,'PIERNA IZQ':ORANGE,'PIERNA DER':ORANGE,'ORFANO':RED}
    for k in boxes: boxes[k]['color']=col[k]
    boxes['ENTRADA']['size']=(700,boxes['ENTRADA']['size'][1]); boxes['ORFANO']['size']=(800,boxes['ORFANO']['size'][1])
    return pos,boxes
def ik():
    ent={'RigUnit_BeginExecution':(0,0)}
    cad={'GetTransform_ctrl_hips':(0,0),'SetTransform_Hips':(1,0)}
    blocks=[('ENTRADA',ent),('CADERA',cad)]
    names=[('PIERNA IZQ','foot_l_ik','pole_knee_l','IK_LeftLeg'),('PIERNA DER','foot_r_ik','pole_knee_r','IK_RightLeg'),('BRAZO IZQ','hand_l_ik','pole_elbow_l','IK_LeftArm'),('BRAZO DER','hand_r_ik','pole_elbow_r','IK_RightArm')]
    for i,(nm,a,b,n) in enumerate(names):
        c=3+i
        blocks.append((nm,{'GetTransform_ctrl_'+a:(c-1,0),'GetTransform_ctrl_'+b:(c-1,350),n:(c,0)}))
    pos,boxes=stack(blocks)
    col={'ENTRADA':BLUE,'CADERA':GREEN,'PIERNA IZQ':ORANGE,'PIERNA DER':ORANGE,'BRAZO IZQ':ORANGE,'BRAZO DER':ORANGE}
    for k in boxes: boxes[k]['color']=col[k]
    boxes['ENTRADA']['size']=(700,boxes['ENTRADA']['size'][1])
    return pos,boxes
ORDER=['ExecutePin','Item','A','Euler','Value','B','Effector','PoleVector','Transform','Result','Translation','Rotation','Scale3D']
def pin_y(y,path):
    rest=path.split('.',1)[1] if '.' in path else ''
    k=0
    for i,o in enumerate(ORDER):
        if rest.startswith(o): k=i; break
    return y+45+22*k
def metrics(pos,links):
    segs=[];back=[];long_=[]
    for a,b in links:
        na=a.split('.')[0]; nb=b.split('.')[0]
        if na not in pos or nb not in pos: continue
        x1=pos[na][0]+est(na)[0]; y1=pin_y(pos[na][1],a); x2=pos[nb][0]; y2=pin_y(pos[nb][1],b)
        segs.append(((x1,y1),(x2,y2),na,nb))
        if x1>x2: back.append((a,b,round(x1-x2)))
        d=math.hypot(x2-x1,y2-y1)
        if d>1500: long_.append((a,b,round(d)))
    def ccw(A,B,C): return (C[1]-A[1])*(B[0]-A[0])>(B[1]-A[1])*(C[0]-A[0])
    cr=0
    for s,t in itertools.combinations(segs,2):
        if {s[2],s[3]}&{t[2],t[3]}: continue
        A,B,C,D=s[0],s[1],t[0],t[1]
        if ccw(A,C,D)!=ccw(B,C,D) and ccw(A,B,C)!=ccw(A,B,D): cr+=1
    ov=[]
    for p,q in itertools.combinations(list(pos),2):
        (x1,y1),(x2,y2)=pos[p],pos[q]; wp,hp=est(p); wq,hq=est(q)
        if x1<x2+wq and x2<x1+wp and y1<y2+hq and y2<y1+hp: ov.append((p,q))
    return dict(links=len(segs),back=len(back),long=len(long_),cruces=cr,solapes=len(ov),back_l=back,long_l=long_,ov=ov)
if __name__=='__main__':
    import sys
    snap=json.load(open(sys.argv[1]))
    for key,fn in (('CR_Student_Procedural_fix',proc),('CR_Student_IK_fix',ik)):
        d=snap[key]; links=[tuple(l) for l in d['links']]
        old={n:tuple(v['pos']) for n,v in d['nodes'].items() if v['cls']!='RigVMCommentNode'}
        pos,boxes=fn()
        assert set(pos)==set(old),(set(pos)^set(old))
        for tag,p in (('antes',old),('despues',pos)):
            m=metrics(p,links); print(key,tag,{k:v for k,v in m.items() if not k.endswith('_l') and k!='ov'})
            if tag=='despues': print('  back',m['back_l'],'\n  long',m['long_l'],'\n  ov',m['ov'])
        for k,b in boxes.items(): print('  ',k,b['pos'],b['size'])
