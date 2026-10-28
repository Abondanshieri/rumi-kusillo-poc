"""Geometria REAL para G1 ronda 8: tamanos medidos en el editor (Slate Snapshot a zoom 1:1), pines por fila, cables como spline Hermite.
Metricas: cruces cable-cable, cables que atraviesan nodos ajenos, retroceso, largos, solapes de nodos, margen a cajas."""
import json, math, itertools, re, os
EV = 'D:/Dev/Computacion_Grafica/Rumi 5.8/Docs/Avance/2026-10-28_rig-student-fix/evidencia/'

def load_sizes(rig_key, nodes):
    """devuelve {nodo: dict(w,h,rows)} usando medidas reales; si faltan, por tipo (misma clase+titulo)"""
    f = EV + ('tamanos_reales_Procedural.json' if 'Procedural' in rig_key else 'tamanos_reales_IK.json')
    real = json.load(open(f)) if os.path.exists(f) else {}
    other = {}
    for ff in ('tamanos_reales_Procedural.json', 'tamanos_reales_IK.json'):
        if os.path.exists(EV + ff):
            other.update(json.load(open(EV + ff)))
    # por titulo: primer nodo medido con ese titulo
    ref_title = {}
    allsnap = json.load(open(EV + 'snap_g1_despues.json'))
    for k, d in allsnap.items():
        src = json.load(open(EV + ('tamanos_reales_Procedural.json' if 'Procedural' in k else 'tamanos_reales_IK.json'))) if os.path.exists(EV + ('tamanos_reales_Procedural.json' if 'Procedural' in k else 'tamanos_reales_IK.json')) else {}
        for n, v in d['nodes'].items():
            if n in src and 'w' in src[n]:
                ref_title.setdefault(v['title'], src[n])
    out = {}
    for n, v in nodes.items():
        if v['cls'] == 'RigVMCommentNode':
            continue
        if n in real and 'w' in real[n]:
            out[n] = dict(real[n]); out[n]['medido'] = True
        elif v['title'] in ref_title:
            out[n] = dict(ref_title[v['title']]); out[n]['medido'] = 'por_tipo'
        elif v['cls'] == 'RigVMRerouteNode':
            out[n] = dict(w=50, h=50, rows=[], medido='estimado')
        else:
            out[n] = dict(w=300, h=200, rows=[], medido='estimado')
    return out

def pin_rel(sz, node, path, is_out):
    """posicion relativa (x,y) del pin dentro del nodo; path = 'Nodo.Pin.Sub'"""
    w, h = sz['w'], sz['h']
    comps = path.split('.')[1:]
    rows = sz.get('rows', [])
    if sz.get('medido') == 'estimado' or not rows or node.startswith('Reroute'):
        return (w if is_out else 0, h / 2 if node.startswith('Reroute') else 40)
    if comps and comps[0] == 'ExecutePin':
        return (w if is_out else 0, 40)
    # buscar de lo mas profundo a lo mas general
    for c in reversed(comps):
        cand = [r for r in rows if r[0].replace(' ', '') == c and r[2] > 24]
        if is_out:
            cand = [r for r in cand if r[1] > w * 0.35] or cand
        else:
            cand = [r for r in cand if r[1] < w * 0.5] or cand
        if cand:
            r = cand[0]
            return (w if is_out else 0, r[2] + 7)
    return (w if is_out else 0, 40)

def hermite(p0, p1, n=24):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    # UE: tangente = delta (con empuje horizontal minimo)
    tx = dx if dx > 0 else dx - 200
    t0 = (max(tx, 60), 0.0) if dx > 0 else (tx * -1 + 60, 0)
    t0 = (abs(dx) + 60 if dx > 0 else 200 + abs(dx), 0.0)
    pts = []
    for i in range(n + 1):
        t = i / n
        h00 = 2*t**3 - 3*t**2 + 1; h10 = t**3 - 2*t**2 + t; h01 = -2*t**3 + 3*t**2; h11 = t**3 - t**2
        x = h00*p0[0] + h10*t0[0] + h01*p1[0] + h11*t0[0]
        y = h00*p0[1] + h10*t0[1] + h01*p1[1] + h11*t0[1]
        pts.append((x, y))
    return pts

def seg_inter(a, b, c, d):
    def ccw(A, B, C): return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])
    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)

def seg_rect(a, b, r):
    x0, y0, x1, y1 = r
    # Liang-Barsky
    dx, dy = b[0]-a[0], b[1]-a[1]; t0, t1 = 0.0, 1.0
    for p, q in ((-dx, a[0]-x0), (dx, x1-a[0]), (-dy, a[1]-y0), (dy, y1-a[1])):
        if p == 0:
            if q < 0: return False
        else:
            t = q / p
            if p < 0:
                if t > t1: return False
                t0 = max(t0, t)
            else:
                if t < t0: return False
                t1 = min(t1, t)
    return True

def metrics(pos, sizes, links, boxes=None, exclude_nodes=()):
    names = [n for n in pos if n in sizes]
    rect = {n: (pos[n][0], pos[n][1], pos[n][0]+sizes[n]['w'], pos[n][1]+sizes[n]['h']) for n in names}
    polys = []; back = []; long_ = []
    for a, b in links:
        na, nb = a.split('.')[0], b.split('.')[0]
        if na not in pos or nb not in pos: continue
        pa = pin_rel(sizes[na], na, a, True); pb = pin_rel(sizes[nb], nb, b, False)
        p0 = (pos[na][0]+pa[0], pos[na][1]+pa[1]); p1 = (pos[nb][0]+pb[0], pos[nb][1]+pb[1])
        pl = hermite(p0, p1)
        polys.append((pl, na, nb, a, b))
        if p0[0] > p1[0]: back.append((a, b, round(p0[0]-p1[0])))
        d = math.hypot(p1[0]-p0[0], p1[1]-p0[1])
        if d > 1500: long_.append((a, b, round(d)))
    # cruces
    cr = []
    for (pa, a1, a2, sa, ta), (pb, b1, b2, sb, tb) in itertools.combinations(polys, 2):
        if {a1, a2} & {b1, b2}: continue
        hit = False
        for i in range(len(pa)-1):
            for j in range(len(pb)-1):
                if seg_inter(pa[i], pa[i+1], pb[j], pb[j+1]): hit = True; break
            if hit: break
        if hit: cr.append((sa+'>'+ta, sb+'>'+tb))
    # cables sobre nodos ajenos (rect reducido 4u)
    over = []
    for pl, na, nb, sa, ta in polys:
        for n in names:
            if n in (na, nb): continue
            x0, y0, x1, y1 = rect[n]; r = (x0+4, y0+4, x1-4, y1-4)
            if any(seg_rect(pl[i], pl[i+1], r) for i in range(len(pl)-1)):
                over.append((sa+'>'+ta, n))
    # solapes de nodos (con holgura minima 20u)
    ov = []
    for p, q in itertools.combinations(names, 2):
        a, b = rect[p], rect[q]
        if a[0] < b[2]+20 and b[0] < a[2]+20 and a[1] < b[3]+20 and b[1] < a[3]+20:
            ov.append((p, q))
    return dict(enlaces=len(polys), retroceso=back, largos=long_, cruces=cr, cable_sobre_nodo=over, solapes=ov)
