"""Layout g1: escalera de ejecucion. Cada nodo de ejecucion 450 u a la derecha del anterior; datos a su izquierda en bandas verticales apiladas.
Cajas calculadas desde el bbox estimado de los nodos (margen 80, titulo 240 arriba)."""
import math
def est(nm):
    if nm.startswith('RigUnit_Begin'): return (260,100)
    if nm.startswith('Get_') and nm[4:] in ('LeanRoll','LeanPitch','PelvisOffset','LandCrouch','FootOffsetL','FootOffsetR'): return (230,100)
    if nm.startswith('TwoBoneIK') or nm.startswith('IK_'): return (400,480)
    if nm.startswith('Set') : return (330,260)
    if nm.startswith('Get') : return (330,220)
    if nm.startswith('Quat'): return (320,200)
    if nm.startswith('Make'): return (320,200)
    return (320,150)
def bbox(L,names):
    xs=[];ys=[];xe=[];ye=[]
    for n in names:
        x,y=L[n]; w,h=est(n); xs.append(x); ys.append(y); xe.append(x+w); ye.append(y+h)
    return min(xs),min(ys),max(xe),max(ye)
def box(L,names,m=80,t=240):
    x0,y0,x1,y1=bbox(L,names)
    x=math.floor((x0-m)/50)*50; y=math.floor((y0-t)/50)*50
    return dict(pos=(x,y),size=(math.ceil((x1+m-x)/50)*50, math.ceil((y1+m-y)/50)*50))
GAP=150
def stack(blocks):
    """blocks: lista de (nombre, {nodo:(x,ylocal)}). Devuelve posiciones y cajas; cada bloque se desplaza en y para que su caja quede GAP debajo de la anterior."""
    pos={}; boxes={}; cur=0
    for name,nodes in blocks:
        b=box(nodes,list(nodes)); top=b['pos'][1]
        dy=cur-top
        dy=int(math.ceil(dy/50))*50
        for n,(x,y) in nodes.items(): pos[n]=(x,y+dy)
        bb=box(pos,list(nodes)); boxes[name]=bb
        cur=bb['pos'][1]+bb['size'][1]+GAP
    return pos,boxes
BLUE=(0.10,0.25,0.60,0.5); GREEN=(0.15,0.45,0.20,0.5); ORANGE=(0.70,0.40,0.10,0.5); RED=(0.60,0.12,0.12,0.5); PURPLE=(0.40,0.20,0.55,0.5)
def proc(row=600):
    ent={'RigUnit_BeginExecution':(900,0)}
    lean={'Get_LeanPitch':(0,0),'Get_LeanRoll':(0,250),'Quat_Spine1':(450,0),'Get_Spine1':(450,350),'Mul_Spine1':(900,250),'Set_Spine1':(1350,250)}
    y=row
    lean.update({'Mul_Pitch_Spine2':(450,y),'Mul_Roll_Spine2':(450,y+250),'Quat_Spine2':(900,y),'Get_Spine2':(900,y+350),'Mul_Spine2':(1350,y+250),'Set_Spine2':(1800,y+250)})
    y=2*row
    lean.update({'Mul_Pitch_Neck':(900,y),'Mul_Roll_Neck':(900,y+250),'Quat_Neck':(1350,y),'Get_Neck_Lean':(1350,y+350),'Mul_Neck_Lean':(1800,y+250),'Set_Neck_Lean':(2250,y+250)})
    cad={'Get_LandCrouch':(450,0),'Mul_LandCrouch':(900,0),'Get_PelvisOffset':(900,400),'Add_PelvisLand':(1350,200),'Add_HipsZ':(2250,550),'Make_Hips_Offset':(1800,250),'Get_Hips':(1800,500),'Mul_Hips_Offset':(2250,300),'Set_Hips':(2700,300)}
    izq={'Get_FootOffsetL':(1350,0),'Sub_FootOffsetL':(1800,0),'Clamp_LeftOffset':(2250,0),'Make_LeftFoot_Offset':(2250,250),'Get_LeftFoot':(2250,500),'Add_LeftFootZ':(2700,550),'Mul_LeftFoot_Offset':(2700,300),'TwoBoneIK_Left':(3150,250)}
    der={'Get_FootOffsetR':(1800,0),'Sub_FootOffsetR':(2250,0),'Clamp_RightOffset':(2700,0),'Make_RightFoot_Offset':(2700,250),'Get_RightFoot':(2700,500),'Add_RightFootZ':(3150,550),'Mul_RightFoot_Offset':(3150,300),'TwoBoneIK_Right':(3600,250)}
    orf={'ORFANO_Mul_Hips_Offset_1':(0,0)}
    pos,boxes=stack([('ENTRADA',ent),('LEAN',lean),('CADERA',cad),('PIERNA IZQ',izq),('PIERNA DER',der),('ORFANO',orf)])
    col={'ENTRADA':BLUE,'LEAN':GREEN,'CADERA':GREEN,'PIERNA IZQ':ORANGE,'PIERNA DER':ORANGE,'ORFANO':RED}
    for k in boxes: boxes[k]['color']=col[k]
    boxes['ENTRADA']['size']=(max(boxes['ENTRADA']['size'][0],600),boxes['ENTRADA']['size'][1])
    boxes['ORFANO']['size']=(max(boxes['ORFANO']['size'][0],700),boxes['ORFANO']['size'][1])
    # ENTRADA y ORFANO: pos con x pegada
    return pos,boxes
def ik():
    ent={'RigUnit_BeginExecution':(0,0)}
    cad={'GetTransform_ctrl_hips':(0,0),'SetTransform_Hips':(450,0)}
    blocks=[('ENTRADA',ent),('CADERA',cad)]
    for i,(nm,a,b) in enumerate([('PIERNA IZQ','foot_l_ik','pole_knee_l'),('PIERNA DER','foot_r_ik','pole_knee_r'),('BRAZO IZQ','hand_l_ik','pole_elbow_l'),('BRAZO DER','hand_r_ik','pole_elbow_r')]):
        X=900+450*i; ik_n={'L':'IK_LeftLeg'}
        n={'PIERNA IZQ':'IK_LeftLeg','PIERNA DER':'IK_RightLeg','BRAZO IZQ':'IK_LeftArm','BRAZO DER':'IK_RightArm'}[nm]
        blocks.append((nm,{'GetTransform_ctrl_'+a:(X-450,100),'GetTransform_ctrl_'+b:(X-450,350),n:(X,0)}))
    pos,boxes=stack(blocks)
    col={'ENTRADA':BLUE,'CADERA':GREEN,'PIERNA IZQ':ORANGE,'PIERNA DER':ORANGE,'BRAZO IZQ':ORANGE,'BRAZO DER':ORANGE}
    for k in boxes: boxes[k]['color']=col[k]
    boxes['ENTRADA']['size']=(max(boxes['ENTRADA']['size'][0],600),boxes['ENTRADA']['size'][1])
    return pos,boxes
