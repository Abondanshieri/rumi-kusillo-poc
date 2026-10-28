import sys; sys.path.insert(0,'.')
from g3u import *
L=snap()
im=[]
for l in L:
    m=re.match(r'\s*(\w+)[^\[]*\[pos=(-?\d+),(-?\d+) size=(\d+),(\d+)\] \[ref=(\w+)\]',l)
    if m and m.group(1) in('image',) : im.append((int(m.group(2)),int(m.group(3)),int(m.group(4)),int(m.group(5)),m.group(6)))
im=[i for i in im if 461<=i[0]<1531 and 160<i[1]<850]
print(len(im))
from collections import Counter
print(Counter((i[2],i[3]) for i in im).most_common(15))
json.dump(im,open(SP+'imgs.json','w'))
