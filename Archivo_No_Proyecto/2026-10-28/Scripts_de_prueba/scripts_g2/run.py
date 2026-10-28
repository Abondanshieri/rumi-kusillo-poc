import sys;sys.path.insert(0,'.')
from u import *
code=open(sys.argv[1],encoding='utf8').read()
r=pyrun(code,sys.argv[2]+'.out',wait=int(sys.argv[3]) if len(sys.argv)>3 else 12)
json.dump(r,open(sys.argv[2]+'.json','w'),indent=1,ensure_ascii=False)
print(json.dumps(r,indent=0,ensure_ascii=False)[:int(sys.argv[4]) if len(sys.argv)>4 else 3500])
