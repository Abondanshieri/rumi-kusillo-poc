import sys; sys.path.insert(0,'.')
from u import *
S('Click',{'ref':'x3440'}); time.sleep(1.2)
print(shot('abp_sel2.png',(1536,56,1920,520)))
L=snap()
print([l.strip()[:120] for l in L if re.search(r'Tamaño de fuente|Color del comentario|Texto del comentario|Font Size|Comment',l)][:8])
