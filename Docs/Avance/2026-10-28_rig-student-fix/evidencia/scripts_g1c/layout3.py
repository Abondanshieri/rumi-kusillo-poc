"""G1 ronda 8. Layout con TAMANOS REALES (medidos en el editor) y metricas reales (geo.py).
Tubería horizontal: la ejecucion es UNA recta horizontal (fila y=0); cada bloque va a la derecha del anterior;
dentro de cada bloque: capas (variables -> operaciones -> Get -> Set/IK), datos por debajo de la fila de ejecucion.
Ramas sin salida: cajas 'SIN SALIDA' debajo de su bloque. Huerfano: caja roja aparte."""
import json, math, random, itertools, sys
from geo import *

SN = json.load(open(EV + 'snap_g1_despues.json'))
GAPX, GAPY, M, TOP, BG, DY0 = 200, 100, 100, 250, 500, 150
BLUE = (0.10, 0.25, 0.60, 0.5); GREEN = (0.15, 0.45, 0.20, 0.5); ORANGE = (0.70, 0.40, 0.10, 0.5)
RED = (0.60, 0.12, 0.12, 0.5); PURPLE = (0.40, 0.20, 0.55, 0.5)

def s50(v, up=False): return (math.ceil(v / 50 - 1e-9) if up else math.floor(v / 50 + 1e-9)) * 50

def is_exec(n): return n.startswith(('Set_', 'SetTransform_', 'TwoBoneIK', 'IK_', 'RigUnit_Begin'))

SPEC_PROC = [
    ('ENTRADA', BLUE, ['RigUnit_BeginExecution'], []),
    ('LEAN', GREEN, ['Get_LeanPitch', 'Get_LeanRoll', 'Quat_Spine1', 'Get_Spine1', 'Mul_Spine1', 'Set_Spine1',
                     'Mul_Pitch_Spine2', 'Mul_Roll_Spine2', 'Quat_Spine2', 'Get_Spine2', 'Mul_Spine2', 'Set_Spine2',
                     'Mul_Pitch_Neck', 'Mul_Roll_Neck', 'Quat_Neck', 'Get_Neck_Lean', 'Mul_Neck_Lean', 'Set_Neck_Lean'], []),
    ('CADERA', GREEN, ['Get_LandCrouch', 'Mul_LandCrouch', 'Get_PelvisOffset', 'Add_PelvisLand', 'Make_Hips_Offset', 'Get_Hips',
                       'Mul_Hips_Offset', 'Set_Hips'], ['Add_HipsZ']),
    ('PIERNA IZQ', ORANGE, ['Get_FootOffsetL', 'Sub_FootOffsetL', 'Make_LeftFoot_Offset', 'Get_LeftFoot', 'Mul_LeftFoot_Offset',
                            'TwoBoneIK_Left'], ['Clamp_LeftOffset', 'Add_LeftFootZ']),
    ('PIERNA DER', ORANGE, ['Get_FootOffsetR', 'Sub_FootOffsetR', 'Make_RightFoot_Offset', 'Get_RightFoot', 'Mul_RightFoot_Offset',
                            'TwoBoneIK_Right'], ['Clamp_RightOffset', 'Add_RightFootZ']),
]
SPEC_IK = [('ENTRADA', BLUE, ['RigUnit_BeginExecution'], []),
           ('CADERA', GREEN, ['GetTransform_ctrl_hips', 'SetTransform_Hips'], [])]
for nm, a, b, n in (('PIERNA IZQ', 'foot_l_ik', 'pole_knee_l', 'IK_LeftLeg'), ('PIERNA DER', 'foot_r_ik', 'pole_knee_r', 'IK_RightLeg'),
                    ('BRAZO IZQ', 'hand_l_ik', 'pole_elbow_l', 'IK_LeftArm'), ('BRAZO DER', 'hand_r_ik', 'pole_elbow_r', 'IK_RightArm')):
    SPEC_IK.append((nm, ORANGE, ['GetTransform_ctrl_' + a, 'GetTransform_ctrl_' + b, n], []))

def resolve_reroutes(links):
    """quita Reroute: devuelve enlaces origen->destino reales (para layering) """
    d = {}
    for s, t in links:
        if s.startswith('Reroute'): d.setdefault(s.split('.')[0], []).append(t)
    out = []
    for s, t in links:
        if s.startswith('Reroute'): continue
        st = [t]
        while st:
            x = st.pop()
            if x.startswith('Reroute'): st += d.get(x.split('.')[0], [])
            else: out.append((s, x))
    return out

def layers(nodes, links):
    N = set(nodes)
    pred = {n: set() for n in N}; succ = {n: set() for n in N}
    for a, b in links:
        na, nb = a.split('.')[0], b.split('.')[0]
        if na in N and nb in N and na != nb and not (a.endswith('ExecutePin') and b.endswith('ExecutePin')):
            pred[nb].add(na); succ[na].add(nb)
    col = {}
    def c(n):
        if n in col: return col[n]
        col[n] = 0 if not pred[n] else 1 + max(c(p) for p in pred[n]); return col[n]
    for n in N: c(n)
    # fuentes (sin predecesores): pegadas a su primer consumidor
    for _ in range(4):
        for n in N:
            if not pred[n] and succ[n]: col[n] = min(col[s] for s in succ[n]) - 1
    # ejecucion: columnas estrictamente crecientes en el orden de la cadena
    ex = [n for n in EXEC_ORDER if n in N]
    prev = -1
    for n in ex:
        col[n] = max(col[n], prev + 1); prev = col[n]
    mn = min(col.values())
    return {n: col[n] - mn for n in N}

EXEC_ORDER = []

def layout_block(nodes, links, sizes, seed=0, iters=250):
    col = layers(nodes, links)
    ncol = max(col.values()) + 1
    cols = [[n for n in nodes if col[n] == c] for c in range(ncol)]
    # x
    xs = []; x = 0
    for c in range(ncol):
        xs.append(x)
        w = max([sizes[n]['w'] for n in cols[c]] or [0])
        x = s50(x + w + GAPX, True)
    L = [(a, b) for a, b in links if a.split('.')[0] in col and b.split('.')[0] in col and a.split('.')[0] != b.split('.')[0]
         and not (a.endswith('ExecutePin') and b.endswith('ExecutePin'))]
    nb = {n: [] for n in nodes}
    for a, b in L:
        na, nbb = a.split('.')[0], b.split('.')[0]
        nb[na].append((a, nbb, 'out')); nb[nbb].append((b, na, 'in'))

    def place(order):
        """y por relajacion: orden fijo por columna"""
        y = {}
        for c in range(ncol):
            yy = 0 if any(is_exec(n) for n in order[c]) else DY0
            for n in order[c]:
                if is_exec(n): y[n] = 0
                else: y[n] = max(yy, DY0)
                yy = y[n] + sizes[n]['h'] + GAPY
        for it in range(6):
            for c in (list(range(ncol)) if it % 2 == 0 else list(range(ncol - 1, -1, -1))):
                want = {}
                for n in order[c]:
                    if is_exec(n): want[n] = 0; continue
                    ds = []
                    for a, b in L:
                        na, nbb = a.split('.')[0], b.split('.')[0]
                        if na == n and nbb in y and col[nbb] != col[n]:
                            pb = pin_rel(sizes[nbb], nbb, b, False); pa = pin_rel(sizes[n], n, a, True)
                            ds.append(y[nbb] + pb[1] - pa[1])
                        elif nbb == n and na in y and col[na] != col[n]:
                            pa = pin_rel(sizes[na], na, a, True); pb = pin_rel(sizes[n], n, b, False)
                            ds.append(y[na] + pa[1] - pb[1])
                    want[n] = sum(ds) / len(ds) if ds else y[n]
                # respetar orden, evitar solape
                cur = None
                for n in order[c]:
                    if is_exec(n): y[n] = 0; cur = sizes[n]['h'] + GAPY; continue
                    t = max(want[n], DY0, cur if cur is not None else DY0)
                    y[n] = t; cur = t + sizes[n]['h'] + GAPY
        return {n: (xs[col[n]], s50(y[n], True)) for n in nodes}

    def fix(pos):
        # tras redondear a 50 puede haber solape: empujar abajo
        for c in range(ncol):
            cur = None
            for n in sorted(cols_cur[c], key=lambda k: pos[k][1]):
                if is_exec(n): cur = pos[n][1] + sizes[n]['h'] + GAPY; continue
                if cur is not None and pos[n][1] < cur: pos[n] = (pos[n][0], s50(cur, True))
                cur = pos[n][1] + sizes[n]['h'] + GAPY
        return pos

    def cost(pos):
        m = metrics(pos, sizes, L)
        return len(m['cruces']) * 1000 + len(m['cable_sobre_nodo']) * 700 + len(m['solapes']) * 5000 + len(m['retroceso']) * 800 + \
            sum(abs(pin_rel(sizes[a.split('.')[0]], a.split('.')[0], a, True)[1] + pos[a.split('.')[0]][1] -
                    pin_rel(sizes[b.split('.')[0]], b.split('.')[0], b, False)[1] - pos[b.split('.')[0]][1]) for a, b in L) / 50.0

    rnd = random.Random(seed)
    order = [sorted(cols[c], key=lambda n: nodes.index(n)) for c in range(ncol)]
    global cols_cur
    cols_cur = cols
    best = fix(place(order)); bc = cost(best); bo = [list(o) for o in order]
    for it in range(iters):
        o2 = [list(o) for o in bo]
        c = rnd.randrange(ncol)
        if len([n for n in o2[c] if not is_exec(n)]) < 2 and len(o2[c]) < 2: continue
        i, j = rnd.sample(range(len(o2[c])), 2) if len(o2[c]) > 1 else (0, 0)
        o2[c][i], o2[c][j] = o2[c][j], o2[c][i]
        p2 = fix(place(o2)); c2 = cost(p2)
        if c2 < bc: best, bc, bo = p2, c2, o2
    return best, bc, xs, ncol

def build(rig_key, spec, seed=0, iters=250):
    d = SN[rig_key]
    nodes_all = d['nodes']
    sizes = load_sizes(rig_key, nodes_all)
    links_all = [tuple(l) for l in d['links']]
    real_links = resolve_reroutes(links_all)
    global EXEC_ORDER
    # cadena de ejecucion
    ex = {a.split('.')[0]: b.split('.')[0] for a, b in real_links if a.endswith('ExecutePin') and b.endswith('ExecutePin')}
    EXEC_ORDER = ['RigUnit_BeginExecution']
    while EXEC_ORDER[-1] in ex: EXEC_ORDER.append(ex[EXEC_ORDER[-1]])
    pos = {}; boxes = []; info = {}
    x0 = 0
    block_pos = {}
    for title, color, nodes, dead in spec:
        bp, bc, xs, ncol = layout_block(nodes, real_links, sizes, seed=seed, iters=iters)
        info[title] = dict(costo=bc, columnas=ncol)
        W = max(bp[n][0] + sizes[n]['w'] for n in nodes); Hh = max(bp[n][1] + sizes[n]['h'] for n in nodes)
        for n in nodes: pos[n] = (x0 + bp[n][0], bp[n][1])
        block_pos[title] = dict(x0=x0, W=W, H=Hh, nodes=nodes, dead=dead, color=color)
        bw = max(W + 2 * M, 80 * len(title) + 250)
        x0 = s50(x0 + bw + BG, True)
    # cajas principales
    ybot = 0
    for title, bpv in block_pos.items():
        bw = max(bpv['W'] + 2 * M, 80 * len(title) + 250)
        bx = s50(bpv['x0'] - M); by = -TOP
        bh = s50(bpv['H'] + M - by, True)
        boxes.append(dict(title=title, pos=(bx, by), size=(s50(bw + (bpv['x0'] - bx), True), bh), color=bpv['color'], nodes=bpv['nodes']))
        ybot = max(ybot, by + bh)
    # reroutes (cosmeticos): en los huecos entre cajas, por debajo de todas las cajas de proceso
    bx = {b['title']: b for b in boxes}
    rr = sorted(n for n in nodes_all if n.startswith('Reroute'))
    if len(rr) == 2 and 'CADERA' in bx:
        gy = s50(max(b['pos'][1] + b['size'][1] for b in boxes if b['title'] in ('CADERA', 'PIERNA IZQ', 'PIERNA DER')) + 250, True)
        for n, (l, r) in zip(rr, (('CADERA', 'PIERNA IZQ'), ('PIERNA IZQ', 'PIERNA DER'))):
            gx = bx[l]['pos'][0] + bx[l]['size'][0]; gx2 = bx[r]['pos'][0]
            pos[n] = (s50((gx + gx2) / 2 - 25), gy)
        for n in rr: sizes[n] = dict(w=50, h=50, rows=[], medido='estimado')
    # ramas sin salida
    ybot_low = max([b['pos'][1] + b['size'][1] for b in boxes if b['title'] in ('CADERA', 'PIERNA IZQ', 'PIERNA DER')] or [ybot])
    ydead = s50(ybot_low + 700, True)
    for title, color, nodes, dead in spec:
        if not dead: continue
        # x destino: tras las fuentes externas (dentro de pos), cadena Clamp->Add
        y = ydead + TOP
        cur_x = None
        placed = []
        for n in dead:
            preds = [a.split('.')[0] for a, b in real_links if b.split('.')[0] == n and a.split('.')[0] in pos]
            xx = max([pos[p][0] + sizes[p]['w'] for p in preds] or [block_pos[title]['x0']]) + 250
            pos[n] = (s50(xx, True), y)
        # orden izquierda a derecha por dependencia
        for n in dead:
            for a, b in real_links:
                if b.split('.')[0] == n and a.split('.')[0] in dead and a.split('.')[0] != n:
                    p = a.split('.')[0]
                    pos[n] = (max(pos[n][0], s50(pos[p][0] + sizes[p]['w'] + GAPX, True)), pos[n][1])
        xmin = min(pos[n][0] for n in dead); xmax = max(pos[n][0] + sizes[n]['w'] for n in dead)
        hmax = max(sizes[n]['h'] for n in dead)
        bw = max(xmax - xmin + 2 * M, 80 * len('SIN SALIDA') + 250)
        boxes.append(dict(title='SIN SALIDA', pos=(s50(xmin - M), ydead), size=(s50(bw, True), s50(TOP + hmax + M, True)), color=PURPLE, nodes=list(dead)))
    # huerfano
    orf = [n for n in nodes_all if n.startswith('ORFANO')]
    if orf:
        n = orf[0]; pos[n] = (0, ydead + TOP)
        boxes.append(dict(title='ORFANO', pos=(-M, ydead), size=(s50(max(sizes[n]['w'] + 2 * M, 80 * 6 + 250), True), s50(TOP + sizes[n]['h'] + M, True)), color=RED, nodes=[n]))
    return pos, boxes, sizes, real_links, links_all, info, block_pos, ybot

if __name__ == '__main__':
    for key, spec in (('CR_Student_Procedural_fix', SPEC_PROC), ('CR_Student_IK_fix', SPEC_IK)):
        pos, boxes, sizes, rl, la, info, bpos, ybot = build(key, spec, iters=int(sys.argv[1]) if len(sys.argv) > 1 else 60)
        print(key, info)
        for b in boxes: print('  ', b['title'], b['pos'], b['size'])
        print({n: p for n, p in pos.items()})
