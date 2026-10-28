import struct, sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ua import load, exports

Z = bytes(4)


def analyze(path):
    b, names = load(path)
    ex = exports(b, names)
    u32 = lambda p: struct.unpack_from('<I', b, p)[0]
    r1 = ex[0][0]
    base = None
    for m in range(0, 3000):
        cand = r1 - 112 * m
        for pos in range(0, 3000):
            if u32(pos) == cand:
                base = cand
                break
        if base:
            break

    def ename(k):
        r = base + 112 * k
        return names[u32(r + 16)] + ("_%d" % (u32(r + 20) - 1) if u32(r + 20) else "")

    idx = {s: i for i, s in reversed(list(enumerate(names)))}
    res = []
    for (r, num, outer, off, size) in ex:
        reg = b[off:off + size]
        d = {"name": "EdGraphNode_Comment_%d" % num if num else "EdGraphNode_Comment",
             "outer": ename(outer - 1) if outer > 0 else None}
        for prop in ["NodePosX", "NodePosY", "NodeWidth", "NodeHeight", "FontSize"]:
            if prop in idx:
                p = reg.find(struct.pack('<I', idx[prop]) + Z)
                if p >= 0:
                    d[prop] = struct.unpack_from('<i', reg, p + 25)[0]
        for prop in ["Position", "Size"]:
            if prop in idx:
                p = reg.find(struct.pack('<I', idx[prop]) + Z)
                if p >= 0 and struct.unpack_from('<I', reg, p + 44)[0] == 16:
                    d[prop] = [round(v, 1) for v in struct.unpack_from('<dd', reg, p + 49)]
        res.append(d)
    return res


if __name__ == "__main__":
    for d in analyze(sys.argv[1]):
        print(d)
