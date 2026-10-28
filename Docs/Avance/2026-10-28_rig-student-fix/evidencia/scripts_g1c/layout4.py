"""G1 ronda 8, layout v4: escalera de ejecucion con TAMANOS REALES.
Cada bloque va debajo del anterior y desplazado a la derecha lo justo para que su primer nodo de ejecucion quede a la derecha
del ultimo del bloque anterior (cable de ejecucion forward y corto). Dentro del bloque: capas por etapa (variables -> operaciones ->
Get -> Set/IK), orden por columna optimizado contra cruces/cables sobre nodos con geometria real."""
import sys, json, math, random
sys.path.insert(0, '.')
import layout3 as L3
from layout3 import SN, SPEC_PROC, SPEC_IK, GAPX, GAPY, M, TOP, BLUE, GREEN, ORANGE, RED, PURPLE, s50, is_exec, layers, resolve_reroutes
from geo import *

GAPV = 300
DEAD_DX = 250
BOTTOM = {'Get_PelvisOffset'}
EXEC_GAP = 150

def layout_block(nodes_main, links, sizes, seed=0, iters=300, dead=()):
    nodes = list(nodes_main) + list(dead)
    col = layers(list(nodes_main), links)
    maxc = max(col.values())
    # ramas sin salida: columnas extra a la derecha de la ultima columna (caja propia, adyacente)
    dcol = {}
    for d in dead:
        dcol[d] = 0
    for _ in range(3):
        for d in dead:
            for a, b in links:
                if b.split('.')[0] == d and a.split('.')[0] in dead and a.split('.')[0] != d:
                    dcol[d] = max(dcol[d], dcol[a.split('.')[0]] + 1)
    for d in dead: col[d] = maxc + 1 + dcol[d]
    ncol = max(col.values()) + 1
    cols = [[n for n in nodes if col[n] == c] for c in range(ncol)]
    xs = []; x = 0
    for c in range(ncol):
        xs.append(x)
        x = s50(x + max([sizes[n]['w'] for n in cols[c]] or [0]) + (GAPX + (2 * M + 100 if (c == maxc and dead) else 0)), True)
    N = set(nodes)
    L = [(a, b) for a, b in links if a.split('.')[0] in N and b.split('.')[0] in N and a.split('.')[0] != b.split('.')[0]]
    Ld = [(a, b) for a, b in L if not (a.endswith('ExecutePin') and b.endswith('ExecutePin'))]

    def place(order):
        y = {}
        for c in range(ncol):
            yy = 0
            for n in order[c]:
                y[n] = yy; yy += sizes[n]['h'] + GAPY
        for it in range(8):
            for c in (range(ncol) if it % 2 == 0 else range(ncol - 1, -1, -1)):
                want = {}
                for n in order[c]:
                    ds = []
                    for a, b in Ld:
                        na, nb = a.split('.')[0], b.split('.')[0]
                        if na == n and col[nb] != col[n]:
                            ds.append(y[nb] + pin_rel(sizes[nb], nb, b, False)[1] - pin_rel(sizes[n], n, a, True)[1])
                        elif nb == n and col[na] != col[n]:
                            ds.append(y[na] + pin_rel(sizes[na], na, a, True)[1] - pin_rel(sizes[n], n, b, False)[1])
                    want[n] = sum(ds) / len(ds) if ds else y[n]
                cur = 0
                for n in order[c]:
                    t = max(want[n], cur)
                    if n in BOTTOM: t = cur
                    y[n] = t; cur = t + sizes[n]['h'] + GAPY
        # al final: bajar para que ymin = 0
        mn = min(y.values())
        return {n: (xs[col[n]], y[n] - mn) for n in nodes}

    def snap(pos):
        pos = {n: (p[0], s50(p[1], True)) for n, p in pos.items()}
        for c in range(ncol):
            cur = 0
            for n in sorted(cols[c], key=lambda k: pos[k][1]):
                if pos[n][1] < cur: pos[n] = (pos[n][0], s50(cur, True))
                cur = pos[n][1] + sizes[n]['h'] + GAPY
        return pos

    def cost(pos):
        m = metrics(pos, sizes, L)
        ln = 0
        for a, b in L:
            na, nb = a.split('.')[0], b.split('.')[0]
            pa = pin_rel(sizes[na], na, a, True); pb = pin_rel(sizes[nb], nb, b, False)
            ln += abs(pos[na][1] + pa[1] - pos[nb][1] - pb[1]) / 100.0
        H = max(pos[n][1] + sizes[n]['h'] for n in pos)
        return len(m['cruces']) * 1000 + len(m['cable_sobre_nodo']) * 800 + len(m['solapes']) * 5000 + len(m['retroceso']) * 800 + ln + H / 200.0

    rnd = random.Random(seed)
    order = [sorted(cols[c], key=lambda n: nodes.index(n)) for c in range(ncol)]
    best = snap(place(order)); bc = cost(best); bo = [list(o) for o in order]
    for it in range(iters):
        o2 = [list(o) for o in bo]
        c = rnd.randrange(ncol)
        if len(o2[c]) < 2: continue
        i, j = rnd.sample(range(len(o2[c])), 2)
        o2[c][i], o2[c][j] = o2[c][j], o2[c][i]
        if rnd.random() < 0.3 and len(o2[c]) > 2:
            k = rnd.randrange(len(o2[c])); n = o2[c].pop(k); o2[c].insert(rnd.randrange(len(o2[c]) + 1), n)
        p2 = snap(place(o2)); c2 = cost(p2)
        if c2 < bc: best, bc, bo = p2, c2, o2
    W = max(best[n][0] + sizes[n]['w'] for n in nodes_main); H = max(best[n][1] + sizes[n]['h'] for n in nodes_main)
    return best, bc, W, H, col

def build(rig_key, spec, seed=0, iters=300, gapv=GAPV):
    d = SN[rig_key]
    nodes_all = d['nodes']
    sizes = load_sizes(rig_key, nodes_all)
    for n in nodes_all:
        if n.startswith('Reroute'): sizes[n] = dict(w=50, h=50, rows=[], medido='estimado')
    links_all = [tuple(l) for l in d['links']]
    rl = resolve_reroutes(links_all)
    ex = {a.split('.')[0]: b.split('.')[0] for a, b in rl if a.endswith('ExecutePin') and b.endswith('ExecutePin')}
    chain = ['RigUnit_BeginExecution']
    while chain[-1] in ex: chain.append(ex[chain[-1]])
    L3.EXEC_ORDER = chain
    pos = {}; boxes = []; info = {}; blocks = {}
    prev_last = None; ybot = None; dead_boxes = []
    for title, color, nodes, dead in spec:
        nodes = list(nodes) + list(dead); dead = []
        bp, bc, W, H, col = layout_block(nodes, rl, sizes, seed=seed, iters=iters, dead=dead)
        exn = [n for n in chain if n in nodes]
        if prev_last is None:
            x0 = 0; y0 = 0
        else:
            x0 = s50(pos[prev_last][0] + sizes[prev_last]['w'] + EXEC_GAP - bp[exn[0]][0], True)
            y0 = s50(ybot + gapv + TOP, True)
        for n in list(nodes) + list(dead): pos[n] = (x0 + bp[n][0], y0 + bp[n][1])
        if dead:
            dx0 = min(pos[n][0] for n in dead); dx1 = max(pos[n][0] + sizes[n]['w'] for n in dead)
            dy0 = min(pos[n][1] for n in dead); dy1 = max(pos[n][1] + sizes[n]['h'] for n in dead)
            dw = max(dx1 - dx0 + 2 * M, 80 * len('SIN SALIDA') + 250)
            dead_boxes.append(dict(title='SIN SALIDA', pos=(s50(dx0 - M), s50(dy0 - TOP)), size=(s50(dw, True), s50(dy1 - dy0 + TOP + M, True)), color=PURPLE, nodes=list(dead)))
        bw = max(W + 2 * M, 80 * len(title) + 250, 0)
        bx = s50(x0 - M); by = y0 - TOP
        bwid = s50(max(W + 2 * M, 80 * len(title) + 250) + (x0 - bx), True)
        bhei = s50(H + M + TOP, True)
        boxes.append(dict(title=title, pos=(bx, by), size=(bwid, bhei), color=color, nodes=list(nodes)))
        blocks[title] = dict(x0=x0, y0=y0, W=W, H=H, box=boxes[-1])
        ybot = by + bhei
        prev_last = exn[-1]
        info[title] = dict(costo=round(bc, 1), columnas=max(col.values()) + 1)
    boxes.extend(dead_boxes)
    return pos, boxes, sizes, rl, links_all, info, blocks, chain

def place_dead(pos, boxes, sizes, rl, spec, blocks):
    """ramas sin salida: caja 'SIN SALIDA' a la derecha de su bloque; y elegida entre candidatos por la metrica real"""
    for title, color, nodes, dead in spec:
        if not dead: continue
        bl = blocks[title]; bx = bl['box']
        xr = bx['pos'][0] + bx['size'][0]
        # x: tras columna de ejecucion y cable de salida de ejecucion
        x_start = s50(xr + DEAD_DX + M, True)
        Ld = [(a, b) for a, b in rl if (a.split('.')[0] in dead or b.split('.')[0] in dead)]
        best = None
        ys = range(s50(bl['y0'] - 100), s50(bl['y0'] + bl['H'] + 100), 50)
        for yy in ys:
            p2 = dict(pos)
            cx = x_start
            for n in dead:
                p2[n] = (cx, yy)
                cx = s50(cx + sizes[n]['w'] + GAPX, True)
            # reubicar cada nodo en orden de dependencia si hay cadena Clamp->Add
            m = metrics(p2, sizes, Ld + [])
            m_all = metrics(p2, sizes, rl)
            sc = len(m_all['cruces']) * 1000 + len(m_all['cable_sobre_nodo']) * 800 + len(m_all['solapes']) * 5000
            if best is None or sc < best[0]: best = (sc, yy, p2)
        pos.update({n: best[2][n] for n in dead})
        xmin = min(pos[n][0] for n in dead); xmax = max(pos[n][0] + sizes[n]['w'] for n in dead)
        ymin = min(pos[n][1] for n in dead); ymax = max(pos[n][1] + sizes[n]['h'] for n in dead)
        wbox = s50(max(xmax - xmin + 2 * M, 80 * len('SIN SALIDA') + 250), True)
        boxes.append(dict(title='SIN SALIDA', pos=(s50(xmin - M), s50(ymin - TOP)), size=(wbox, s50(ymax - ymin + TOP + M, True)), color=PURPLE, nodes=list(dead)))

def place_orfano(pos, boxes, sizes, nodes_all):
    orf = [n for n in nodes_all if n.startswith('ORFANO')]
    if not orf: return
    n = orf[0]
    ent = [b for b in boxes if b['title'] == 'ENTRADA'][0]
    x = s50(ent['pos'][0] + ent['size'][0] + 700, True); y = 0
    pos[n] = (x, y)
    boxes.append(dict(title='ORFANO', pos=(s50(x - M), -TOP), size=(s50(max(sizes[n]['w'] + 2 * M, 80 * 6 + 250), True), s50(sizes[n]['h'] + TOP + M, True)), color=RED, nodes=[n]))

def place_reroutes(pos, boxes, sizes, links_all, rl):
    rr = sorted(n for n in sizes if n.startswith('Reroute'))
    if not rr: return None
    for n in rr: pos.setdefault(n, (0, 0))
    isr = lambda a, b: a.split('.')[0] in rr or b.split('.')[0] in rr
    stat = []
    for a, b in links_all:
        if isr(a, b): continue
        na, nb = a.split('.')[0], b.split('.')[0]
        pa = pin_rel(sizes[na], na, a, True); pb = pin_rel(sizes[nb], nb, b, False)
        stat.append((hermite((pos[na][0]+pa[0], pos[na][1]+pa[1]), (pos[nb][0]+pb[0], pos[nb][1]+pb[1]), 14), na, nb))
    rects = {n: (pos[n][0]+4, pos[n][1]+4, pos[n][0]+sizes[n]['w']-4, pos[n][1]+sizes[n]['h']-4) for n in pos if n not in rr}
    rrl = [(a, b) for a, b in links_all if isr(a, b)]
    bx = {b['title']: b for b in boxes}
    x1s = [s50(bx['PIERNA IZQ']['pos'][0] - 250), s50(bx['PIERNA IZQ']['pos'][0] - 150)]
    x2s = [s50(bx['PIERNA DER']['pos'][0] - 250), s50(bx['PIERNA DER']['pos'][0] - 150)]
    g1 = bx['CADERA']['pos'][1] + bx['CADERA']['size'][1]; t1 = bx['PIERNA IZQ']['pos'][1]
    g2 = bx['PIERNA IZQ']['pos'][1] + bx['PIERNA IZQ']['size'][1]; t2 = bx['PIERNA DER']['pos'][1]
    y1s = sorted({s50(g1 + (t1 - g1) * f) for f in (0.2, 0.4, 0.5, 0.6, 0.8)})
    y2s = sorted({s50(g2 + (t2 - g2) * f) for f in (0.2, 0.4, 0.5, 0.6, 0.8)})
    best = None
    for x1 in x1s:
        for y1 in y1s:
            for x2 in x2s:
                for y2 in y2s:
                    if x2 < x1 + 50: continue
                    p2 = dict(pos); p2[rr[0]] = (x1, y1); p2[rr[1]] = (x2, y2)
                    sc = 0
                    for a, b in rrl:
                        na, nb = a.split('.')[0], b.split('.')[0]
                        sa = sizes[na]; sb = sizes[nb]
                        pa = pin_rel(sa, na, a, True); pb = pin_rel(sb, nb, b, False)
                        p0 = (p2[na][0]+pa[0], p2[na][1]+pa[1]); p1 = (p2[nb][0]+pb[0], p2[nb][1]+pb[1])
                        if p0[0] > p1[0]: sc += 800
                        d = math.hypot(p1[0]-p0[0], p1[1]-p0[1])
                        if d > 1500: sc += 600 + d / 10
                        pl = hermite(p0, p1, 14)
                        for n, r in rects.items():
                            if n in (na, nb): continue
                            if any(seg_rect(pl[i], pl[i+1], r) for i in range(len(pl)-1)): sc += 800
                        for ps, sa_, sb_ in stat:
                            if {sa_, sb_} & {na, nb}: continue
                            if any(seg_inter(pl[i], pl[i+1], ps[j], ps[j+1]) for i in range(len(pl)-1) for j in range(len(ps)-1)): sc += 1000
                    if best is None or sc < best[0]: best = (sc, x1, y1, x2, y2)
    pos[rr[0]] = (best[1], best[2]); pos[rr[1]] = (best[3], best[4])
    return best

def rl_with(links_all): return links_all

def full(key, spec, seed=1, iters=300, gapv=GAPV):
    pos, boxes, sizes, rl, la, info, blocks, chain = build(key, spec, seed, iters, gapv)
    place_orfano(pos, boxes, sizes, SN[key]['nodes'])
    rr = place_reroutes(pos, boxes, sizes, la, rl) if key.endswith('Procedural_fix') else None
    return pos, boxes, sizes, la, info, rr

if __name__ == '__main__':
    from report import rep
    which = sys.argv[3] if len(sys.argv) > 3 else 'proc'
    key, spec = ('CR_Student_Procedural_fix', SPEC_PROC) if which == 'proc' else ('CR_Student_IK_fix', SPEC_IK)
    pos, boxes, sizes, la, info, rr = full(key, spec, int(sys.argv[2]), int(sys.argv[1]), int(sys.argv[4]) if len(sys.argv) > 4 else GAPV)
    m = rep(key, pos, sizes, la, 'DESPUES')
    print(info, rr)
    print(' cruces', m['cruces']); print(' sobre', m['cable_sobre_nodo']); print(' retro', m['retroceso'], 'largos', m['largos'], 'solapes', m['solapes'])
    for b in boxes: print(b['title'], b['pos'], b['size'])
    json.dump(dict(pos={k: list(v) for k, v in pos.items()}, boxes=[dict(b, color=list(b['color'])) for b in boxes], metricas={k: v for k, v in m.items()}),
              open('out4_%s_%s.json' % (which, sys.argv[2]), 'w'))
