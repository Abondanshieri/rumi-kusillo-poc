# Revierte los movimientos de una fecha: python -B -I Archivo_No_Proyecto/revertir.py 2026-10-28 [--solo <texto>]
import os,sys,shutil
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fecha=sys.argv[1]; solo=sys.argv[sys.argv.index('--solo')+1] if '--solo' in sys.argv else ''
n=0
for l in open(os.path.join(root,'Archivo_No_Proyecto',fecha,'MANIFIESTO.txt'),encoding='utf-8'):
    if ' -> ' not in l: continue
    s,d=l.strip().split(' -> ')
    if solo and solo not in s: continue
    S,D=os.path.join(root,s),os.path.join(root,d)
    if os.path.exists(D) and not os.path.exists(S):
        os.makedirs(os.path.dirname(S),exist_ok=True); shutil.move(D,S); n+=1
print('revertidos',n)
