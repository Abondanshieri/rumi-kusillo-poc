import struct,sys,math,json
from math import gcd
def load(path):
    b=open(path,'rb').read()
    n=len(b)
    u32=lambda p:struct.unpack_from('<I',b,p)[0]
    i32=lambda p:struct.unpack_from('<i',b,p)[0]
    # name table
    names=None
    for pos in range(20,3000):
        cnt=u32(pos); off=u32(pos+4)
        if not(50<cnt<200000 and 200<off<n-100): continue
        try:
            p=off; nm=[]
            for k in range(cnt):
                l=i32(p); p+=4
                if l>0:
                    s=b[p:p+l-1].decode('ascii'); p+=l
                elif l<0:
                    s=b[p:p-2*l-2].decode('utf-16le'); p+=-2*l
                else: raise ValueError
                p+=4; nm.append(s)
            names=nm; break
        except Exception: continue
    assert names, "no name table"
    return b,names
def exports(b,names):
    idx={}
    for i,s in enumerate(names): idx.setdefault(s,i)
    u32=lambda p:struct.unpack_from('<I',b,p)[0]
    i32=lambda p:struct.unpack_from('<i',b,p)[0]
    i64=lambda p:struct.unpack_from('<q',b,p)[0]
    n=len(b)
    # candidates for any record whose name is comment
    cands=[]
    for nm in [s for s in names if s.startswith('EdGraphNode_Comment') or s.startswith('RigVMCommentNode')]:
        pass
    ci=[i for i,s in enumerate(names) if s=='EdGraphNode_Comment']
    out=[]
    for c in ci:
        pat=struct.pack('<I',c)
        p=-1
        while True:
            p=b.find(pat,p+1)
            if p<0: break
            r=p-16
            if r<0: continue
            num=u32(p+4); size=i64(r+28); off=i64(r+36)
            if 0<num<500 and 0<size<200000 and 0<off<n and off+size<=n and i32(r)<0:
                out.append((r,num-1,i32(r+12),off,size))
    return out
if __name__=="__main__":
    b,names=load(sys.argv[1]); ex=exports(b,names)
    print(len(names),len(ex))
    rs=sorted(e[0] for e in ex)
    g=0
    for a,c in zip(rs,rs[1:]): g=gcd(g,c-a)
    print("stride",g)
    for e in ex[:50]: print(e)
