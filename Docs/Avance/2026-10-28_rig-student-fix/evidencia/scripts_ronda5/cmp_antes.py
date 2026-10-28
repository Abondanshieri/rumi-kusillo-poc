import json,sys
E='..'
r=json.load(open('snap_ronda6_final.json'))
vn={'Get_LeanRoll':'VariableNode','Get_LeanPitch':'VariableNode_1','Get_PelvisOffset':'VariableNode_2','Get_LandCrouch':'VariableNode_3','Get_FootOffsetL':'VariableNode_4','Get_FootOffsetR':'VariableNode_5','ORFANO_Mul_Hips_Offset_1':'Mul_Hips_Offset_1'}
def norm(p):
    n,_,rest=p.partition('.'); return vn.get(n,n)+('.'+rest if rest else '')
out={}
for k,f in [('PR_fix','CR_Student_Procedural_fix'),('IK_fix','CR_Student_IK_fix')]:
    a=json.load(open(E+'/snap_antes/%s.json'%f))
    ea={frozenset(x.split(' <-> ')) for x in a['edges']}
    # nuestro: enlaces pin->pin; se emparejan en ambos sentidos
    en={frozenset((norm(x),norm(y))) for x,y in r[k]['links']}
    # el snapshot antiguo registra pines hijos y padres (p.ej. A.Transform y A.Transform.Rotation): se compara por enlaces
    perdidas=ea-en; nuevas=en-ea
    out[k]={'antes':len(ea),'ahora':len(en),'perdidas':sorted(map(sorted,perdidas)),'nuevas':sorted(map(sorted,nuevas))}
    print(k,len(ea),len(en),'perdidas',len(perdidas),'nuevas',len(nuevas))
json.dump(out,open('cmp_antes.json','w'),indent=1)
