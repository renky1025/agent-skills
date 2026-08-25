"""立体积木参数化坐标库。

每个 solid 给出标准顶点 labeling 与 edges（棱），坐标基于单位尺度，
geometry_solver 会按 params 中的 side/scale 缩放。坐标系约定：
- 正方体/长方体: 底面 ABCD 在 z=0 平面，A 为原点，AB 沿 x，AD 沿 y，竖直沿 z，
  对应顶点加 '1' 后缀表示顶面（如 A1）。
"""

SOLIDS = {
    "cube": {
        "labeling": "ABCD-A1B1C1D1",
        "vertices": {
            "A": (0, 0, 0), "B": (1, 0, 0), "C": (1, 1, 0), "D": (0, 1, 0),
            "A1": (0, 0, 1), "B1": (1, 0, 1), "C1": (1, 1, 1), "D1": (0, 1, 1),
        },
        "edges": [
            ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
            ("A1", "B1"), ("B1", "C1"), ("C1", "D1"), ("D1", "A1"),
            ("A", "A1"), ("B", "B1"), ("C", "C1"), ("D", "D1"),
        ],
    },
    "cuboid": {
        "labeling": "ABCD-A1B1C1D1",
        "vertices": {
            "A": (0, 0, 0), "B": (1, 0, 0), "C": (1, 1, 0), "D": (0, 1, 0),
            "A1": (0, 0, 1), "B1": (1, 0, 1), "C1": (1, 1, 1), "D1": (0, 1, 1),
        },
        "edges": [
            ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
            ("A1", "B1"), ("B1", "C1"), ("C1", "D1"), ("D1", "A1"),
            ("A", "A1"), ("B", "B1"), ("C", "C1"), ("D", "D1"),
        ],
    },
    # 正四面体 P-ABC: 底面正三角形边长 side，P 为顶点（单位尺度下高为 1）
    "tetra": {
        "labeling": "P-ABC",
        "vertices": {
            "A": (0, 0, 0),
            "B": (1, 0, 0),
            "C": (0.5, 0.866025403784439, 0),
            "P": (0.5, 0.288675134594813, 1),
        },
        "edges": [
            ("A", "B"), ("B", "C"), ("C", "A"),
            ("P", "A"), ("P", "B"), ("P", "C"),
        ],
    },
    # 直三棱柱 ABC-A1B1C1: 底面直角三角形(直角在 A)，cuboid 缩放 a/b/c
    "prism3": {
        "labeling": "ABC-A1B1C1",
        "vertices": {
            "A": (0, 0, 0), "B": (1, 0, 0), "C": (0, 1, 0),
            "A1": (0, 0, 1), "B1": (1, 0, 1), "C1": (0, 1, 1),
        },
        "edges": [
            ("A", "B"), ("B", "C"), ("C", "A"),
            ("A1", "B1"), ("B1", "C1"), ("C1", "A1"),
            ("A", "A1"), ("B", "B1"), ("C", "C1"),
        ],
    },
    # 正四棱锥 P-ABCD: 底面正方形边长 side，顶点 P 在中心上方高 h
    "pyramid4": {
        "labeling": "P-ABCD",
        "vertices": {
            "A": (0, 0, 0), "B": (1, 0, 0), "C": (1, 1, 0), "D": (0, 1, 0),
            "P": (0.5, 0.5, 1),
        },
        "edges": [
            ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
            ("P", "A"), ("P", "B"), ("P", "C"), ("P", "D"),
        ],
    },
    # 旋转体：无棱，渲染走 mesh（scene 里用 "mesh" 字段描述），顶点只放关键点
    "cylinder": {
        "labeling": "O-O1 (r, h)",
        "vertices": {
            "O": (0, 0, 0), "O1": (0, 0, 1),
        },
        "edges": [],
        "mesh": {"kind": "cylinder"},
    },
    "cone": {
        "labeling": "S-O (r, h)",
        "vertices": {
            "O": (0, 0, 0), "S": (0, 0, 1),
        },
        "edges": [],
        "mesh": {"kind": "cone"},
    },
    "sphere": {
        "labeling": "O (r)",
        "vertices": {
            "O": (0, 0, 0),
        },
        "edges": [],
        "mesh": {"kind": "sphere"},
    },
}


def mesh_of(solid):
    return SOLIDS[solid].get("mesh")


def scaled_vertices(solid, params):
    """返回按尺度缩放后的顶点坐标 dict（float 元组）。

    cuboid/prism3 支持 a/b/c 三边长；
    pyramid4 支持 side(底边) 与 h(高)，默认 1/1；
    tetra 支持 side(底边长) 与 h(高)，默认 1/1；
    cube 默认边长 1。
    """
    base = SOLIDS[solid]["vertices"]
    if solid in ("cuboid", "prism3"):
        a = float(params.get("a", 1))
        b = float(params.get("b", 1))
        c = float(params.get("c", 1))
        scale = {"x": a, "y": b, "z": c}
    elif solid == "pyramid4":
        s = float(params.get("side", 1))
        h = float(params.get("h", 1))
        scale = {"x": s, "y": s, "z": 1}
        out = {}
        for name, (x, y, z) in base.items():
            if name == "P":
                out[name] = (x * s, y * s, z * h)
            else:
                out[name] = (x * s, y * s, z)
        return out
    elif solid == "tetra":
        s = float(params.get("side", 1))
        h = float(params.get("h", 1))
        out = {}
        for name, (x, y, z) in base.items():
            if name == "P":
                # P 的 x,y 是底面重心位置，随 side 缩放; z 为高
                out[name] = (x * s, y * s, z * h)
            else:
                # C 的 y 分量是 sqrt(3)/2 底面高度，随 side 缩放
                out[name] = (x * s, y * s, z)
        return out
    elif solid == "cylinder":
        r = float(params.get("r", 0.5))
        h = float(params.get("h", 1))
        return {"O": (0.0, 0.0, 0.0), "O1": (0.0, 0.0, h)} | {"_r": (r, 0, 0)}
    elif solid == "cone":
        r = float(params.get("r", 0.5))
        h = float(params.get("h", 1))
        return {"O": (0.0, 0.0, 0.0), "S": (0.0, 0.0, h)} | {"_r": (r, 0, 0)}
    elif solid == "sphere":
        r = float(params.get("r", 1))
        return {"O": (0.0, 0.0, 0.0)} | {"_r": (r, 0, 0)}
    else:
        s = float(params.get("side", 1))
        scale = {"x": s, "y": s, "z": s}
    out = {}
    for name, (x, y, z) in base.items():
        out[name] = (x * scale["x"], y * scale["y"], z * scale["z"])
    return out


def edges_of(solid):
    return list(SOLIDS[solid]["edges"])
