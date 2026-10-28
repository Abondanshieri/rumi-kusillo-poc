import json,itertools,sys
sys.path.insert(0,'.')
import layout2 as L
d=json.load(open('../snap_g1_base2.json'))['CR_Student_Procedural_fix']
links=[tuple(l) for l in d['links']]
pos,_=L.proc()
segs=[]
for a,b in links:
    na=a.split('.')[0]; nb=b.split('.')[0]
    segs.append(((pos[na][0]+L.est(na)[0],L.pin_y(pos[na][1],a)),(pos[nb][0],L.pin_y(pos[nb][1],b)),a,b,na,nb))
def ccw(A,B,C): return (C[1]-A[1])*(B[0]-A[0])>(B[1]-A[1])*(C[0]-A[0])
for s,t in itertools.combinations(segs,2):
    if {s[4],s[5]}&{t[4],t[5]}: continue
    A,B,C,D=s[0],s[1],t[0],t[1]
    if ccw(A,C,D)!=ccw(B,C,D) and ccw(A,B,C)!=ccw(A,B,D): print(s[2],'->',s[3],'X',t[2],'->',t[3])
