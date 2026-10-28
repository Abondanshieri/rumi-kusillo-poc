import sys; sys.path.insert(0,".")
from pasteops import *
gn=sys.argv[1]; mode=sys.argv[2]   # calib | paste
COL={'ref':(0.20,0.45,0.80,0.5),'ent':(0.55,0.35,0.85,0.5),'proc':(0.25,0.70,0.35,0.5),'caida':(0.90,0.55,0.15,0.5),
 'data':(0.85,0.30,0.60,0.5),'debug':(1.0,0.15,0.15,0.6),'sal':(0.15,0.75,0.75,0.5),'lean':(0.55,0.75,0.20,0.5),'pies':(0.80,0.60,0.15,0.5),
 'aterr':(0.60,0.40,0.85,0.5),'mira':(0.30,0.55,0.95,0.5),'orf':(0.55,0.55,0.55,0.6)}
plan=json.load(open(EV+'G3b_plan.json'))[gn]
g,base,before=read_nodes(gn)
def attempt(clip,expect_new):
    for t in range(8):
        set_clip(clip)
        ok=atomic_paste(gn)
        g2,b2,after=read_nodes(gn)
        if after-before: return after-before
        time.sleep(1.5)
    return set()
if mode=='calib':
    new=attempt(t3d_knot('K2Node_Knot_9990',0,0),1)
    for n in new:
        inf=J('get_node_infos',{'nodes':[{'refPath':base+n}]})[0]; P=inf['position']; print('LOC',gn,P)
        json.dump({'x':P['x'],'y':P['y']},open(SP+'loc_%s.json'%gn,'w'))
        print(J('delete_node',{'node':{'refPath':base+n}}))
else:
    loc=json.load(open(SP+'loc_%s.json'%gn)); Lx,Ly=loc['x'],loc['y']
    items=[]
    for name,gr in plan['groups'].items():
        bx,by,bw,bh=gr['box']
        x1=(bx//16)*16; y1=(by//16)*16
        w=bw+(bx-x1); h=bh+(by-y1)
        items.append((name,x1,y1,w,h,gr))
    ux=[x-Lx for (_,x,_,_,_,_) in items]; uy=[y-Ly for (_,_,y,_,_,_) in items]
    Ux=sum(ux); Uy=sum(uy)
    txt=t3d_knot('K2Node_Knot_9990',0,0)
    for i,(name,x1,y1,w,h,gr) in enumerate(items):
        txt+=t3d_comment('EdGraphNode_Comment_G3_%d'%i, ux[i]+Ux, uy[i]+Uy, w,h, gr['text'], COL[gr['color']], 90)
    expectA=(Lx-Ux,Ly-Uy)
    new=attempt(txt,1)
    print('nuevos',new)
    for n in new:
        inf=J('get_node_infos',{'nodes':[{'refPath':base+n}]})[0]; P=inf['position']; print('ANCLA',P,'esperada',expectA)
        ok=(P['x']==expectA[0] and P['y']==expectA[1]); print('ancla coincide',ok)
        print(J('delete_node',{'node':{'refPath':base+n}}))
    json.dump([(n,x,y,w,h) for (n,x,y,w,h,_) in items],open(EV+'G3b_comentarios_pegados_%s.json'%gn,'w'))
