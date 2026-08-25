"""几何求解器：坐标系参数化建模 + sympy 符号/数值双重校验。

输入 spec JSON（几何规格），输出 scene JSON（供 build_html 渲染）。
支持的 query.type:
- line_plane_angle      直线与平面的夹角 {line:[P,Q], plane:[A,B,C]}
- line_line_angle       异面直线所成角   {line1:[P,Q], line2:[R,S]}
- dihedral_angle        二面角           {edge:[A,B], face1:[A,B,P], face2:[A,B,Q]}
- point_plane_distance  点到平面距离     {point:P, plane:[A,B,C]}
- volume_tetra          三棱锥体积       {apex:P, base:[A,B,C]}
- parallel_perp         平行/垂直判定     {check:"parallel"|"perp", v1:[P,Q], v2:[R,S]}

用法:
    python geometry_solver.py <spec.json> <scene.json>
"""

import json
import sys

import sympy as sp

from solids import scaled_vertices, edges_of, mesh_of

RED = "#ff5a5a"
GREEN = "#5fd38a"
AMBER = "#d38a5f"
BLUE = "#6c8cff"


def fmt_num(v):
    r = sp.nsimplify(v)
    if r.is_Integer:
        return str(int(r))
    if r.is_Rational:
        return str(r)
    return str(sp.N(r, 4))


def vec_str(m):
    return "(" + ", ".join(fmt_num(x) for x in m) + ")"


def _base_scene(spec, pts, edges):
    return {
        "type": "geometry",
        "title": spec.get("title", "立体几何解题演示"),
        "points": {name: [float(x) for x in coord] for name, coord in pts.items()},
        "edges": [[x, y] for x, y in edges],
        "steps": [],
        "result": {},
    }


def solve(spec):
    solid = spec["solid"]
    params = spec.get("params", {})
    verts = scaled_vertices(solid, params)
    edges = edges_of(solid)
    q = spec["query"]
    mesh = mesh_of(solid)

    # _r 是旋转体半径标记，不参与点渲染
    pts = {name: sp.Matrix(coord) for name, coord in verts.items() if name != "_r"}
    radius = float(verts["_r"][0]) if "_r" in verts else None

    dispatch = {
        "line_plane_angle": _line_plane_angle,
        "line_line_angle": _line_line_angle,
        "dihedral_angle": _dihedral_angle,
        "point_plane_distance": _point_plane_distance,
        "volume_tetra": _volume_tetra,
        "parallel_perp": _parallel_perp,
        "skew_distance": _skew_distance,
        "circumsphere": _circumsphere,
        "three_views": _three_views,
        "surface_shortest_path": _surface_shortest_path,
        "insphere": _insphere,
        "net": _net,
        "surface_volume": _surface_volume,
    }
    fn = dispatch.get(q["type"])
    if fn is None:
        raise ValueError("unsupported query type: %s" % q["type"])
    scene = fn(spec, pts, edges, q)
    if mesh:
        scene["mesh"] = {"kind": mesh["kind"], "r": radius}
    return scene


def _plane_normal(pts, plane):
    a, b, c = pts[plane[0]], pts[plane[1]], pts[plane[2]]
    n = (b - a).cross(c - a)
    if n.dot(n) == 0:
        raise ValueError("plane points are collinear: %s" % (plane,))
    return a, b, c, n


def _line_plane_angle(spec, pts, edges, q):
    line = q["line"]
    plane = q["plane"]

    p1, p2 = pts[line[0]], pts[line[1]]
    v = p2 - p1  # 直线方向向量

    a, b, c, n = _plane_normal(pts, plane)
    u1 = b - a
    u2 = c - a

    sin_theta = abs(v.dot(n)) / (sp.sqrt(v.dot(v)) * sp.sqrt(n.dot(n)))
    sin_exact = sp.simplify(sin_theta)
    theta = sp.asin(sin_exact)
    deg = float(theta.evalf() * 180 / sp.pi)

    steps = [
        "写出相关点坐标：%s%s, %s%s, %s%s, %s%s, %s%s。"
        % (
            line[0], vec_str(p1), line[1], vec_str(p2),
            plane[0], vec_str(a), plane[1], vec_str(b), plane[2], vec_str(c),
        ),
        "直线 %s%s 的方向向量 v = %s - %s = %s。"
        % (line[0], line[1], line[1], line[0], vec_str(v)),
        "平面 %s%s%s 内取两向量 u1 = %s - %s = %s，u2 = %s - %s = %s；法向量 n = u1 x u2 = %s。"
        % (
            plane[0], plane[1], plane[2],
            plane[1], plane[0], vec_str(u1),
            plane[2], plane[0], vec_str(u2),
            vec_str(n),
        ),
        "线面角 theta 满足 sin(theta) = |v·n| / (|v|·|n|) = %s。" % fmt_num(sin_exact),
        "故 theta = arcsin(%s) ≈ %.1f°。" % (fmt_num(sin_exact), deg),
    ]

    scene = _base_scene(spec, pts, edges)
    scene.update({
        "highlight_line": {"from": line[0], "to": line[1], "color": RED},
        "plane": {"points": list(plane), "color": GREEN},
        "normal": {"origin": plane[0], "vec": [float(x) for x in n], "color": AMBER},
        "steps": steps,
        "result": {
            "html": "直线与平面的夹角 theta 满足 sin(theta) = %s，theta ≈ %.1f°。"
            % (fmt_num(sin_exact), deg),
            "sin": fmt_num(sin_exact),
            "deg": round(deg, 1),
        },
    })
    return scene


def _line_line_angle(spec, pts, edges, q):
    l1, l2 = q["line1"], q["line2"]
    v1 = pts[l1[1]] - pts[l1[0]]
    v2 = pts[l2[1]] - pts[l2[0]]

    cos_theta = abs(v1.dot(v2)) / (sp.sqrt(v1.dot(v1)) * sp.sqrt(v2.dot(v2)))
    cos_exact = sp.simplify(cos_theta)
    theta = sp.acos(cos_exact)
    deg = float(theta.evalf() * 180 / sp.pi)

    steps = [
        "写出端点坐标：%s%s, %s%s, %s%s, %s%s。"
        % (l1[0], vec_str(pts[l1[0]]), l1[1], vec_str(pts[l1[1]]),
           l2[0], vec_str(pts[l2[0]]), l2[1], vec_str(pts[l2[1]])),
        "直线 %s%s 方向向量 v1 = %s；直线 %s%s 方向向量 v2 = %s。"
        % (l1[0], l1[1], vec_str(v1), l2[0], l2[1], vec_str(v2)),
        "异面直线所成角 cos(theta) = |v1·v2| / (|v1|·|v2|) = %s。" % fmt_num(cos_exact),
        "故 theta = arccos(%s) ≈ %.1f°。" % (fmt_num(cos_exact), deg),
    ]

    scene = _base_scene(spec, pts, edges)
    scene.update({
        "highlight_lines": [
            {"from": l1[0], "to": l1[1], "color": RED},
            {"from": l2[0], "to": l2[1], "color": BLUE},
        ],
        "steps": steps,
        "result": {
            "html": "异面直线 %s%s 与 %s%s 所成角 cos(theta) = %s，theta ≈ %.1f°。"
            % (l1[0], l1[1], l2[0], l2[1], fmt_num(cos_exact), deg),
            "cos": fmt_num(cos_exact),
            "deg": round(deg, 1),
        },
    })
    return scene


def _dihedral_angle(spec, pts, edges, q):
    edge = q["edge"]
    f1, f2 = q["face1"], q["face2"]

    # 半平面法向量：n_i = (棱向量) x (面内第三点方向)，并调整朝向指向另一侧
    e = pts[edge[1]] - pts[edge[0]]
    p1 = pts[f1[2]] - pts[edge[0]]
    p2 = pts[f2[2]] - pts[edge[0]]
    n1 = e.cross(p1)
    n2 = e.cross(p2)

    cos_raw = sp.simplify(n1.dot(n2) / (sp.sqrt(n1.dot(n1)) * sp.sqrt(n2.dot(n2))))
    # 二面角取 [0, pi]，用两个半平面法向量（同绕棱方向）的夹角
    if cos_raw < 0:
        theta_val = sp.acos(cos_raw)
    else:
        theta_val = sp.acos(cos_raw)
    deg = float(theta_val.evalf() * 180 / sp.pi)

    steps = [
        "二面角沿棱 %s%s，两个半平面分别为 %s%s%s 与 %s%s%s。"
        % (edge[0], edge[1],
           f1[0], f1[1], f1[2], f2[0], f2[1], f2[2]),
        "取棱方向向量 e = %s - %s = %s。"
        % (edge[1], edge[0], vec_str(e)),
        "半平面 1 法向量 n1 = e x (%s - %s) = %s；半平面 2 法向量 n2 = e x (%s - %s) = %s。"
        % (f1[2], edge[0], vec_str(n1), f2[2], edge[0], vec_str(n2)),
        "二面角 cos(theta) = n1·n2 / (|n1||n2|) = %s。" % fmt_num(cos_raw),
        "故 theta ≈ %.1f°。" % deg,
    ]

    scene = _base_scene(spec, pts, edges)
    scene.update({
        "highlight_line": {"from": edge[0], "to": edge[1], "color": AMBER},
        "planes": [
            {"points": list(f1), "color": GREEN},
            {"points": list(f2), "color": BLUE},
        ],
        "normals": [
            {"origin": edge[0], "vec": [float(x) for x in n1], "color": GREEN},
            {"origin": edge[0], "vec": [float(x) for x in n2], "color": BLUE},
        ],
        "steps": steps,
        "result": {
            "html": "沿棱 %s%s 的二面角 cos(theta) = %s，theta ≈ %.1f°。"
            % (edge[0], edge[1], fmt_num(cos_raw), deg),
            "cos": fmt_num(cos_raw),
            "deg": round(deg, 1),
        },
    })
    return scene


def _point_plane_distance(spec, pts, edges, q):
    pname = q["point"]
    plane = q["plane"]
    p = pts[pname]

    a, b, c, n = _plane_normal(pts, plane)
    ap = p - a
    dist = sp.simplify(abs(ap.dot(n)) / sp.sqrt(n.dot(n)))

    foot = p - ap.dot(n) / n.dot(n) * n  # 垂足

    steps = [
        "点 %s%s，平面 %s%s%s 过 %s%s, %s%s, %s%s。"
        % (pname, vec_str(p),
           plane[0], plane[1], plane[2],
           plane[0], vec_str(a), plane[1], vec_str(b), plane[2], vec_str(c)),
        "平面法向量 n = (%s - %s) x (%s - %s) = %s。"
        % (plane[1], plane[0], plane[2], plane[0], vec_str(n)),
        "取 AP = P - A = %s，距离 d = |AP·n| / |n| = %s。" % (vec_str(ap), fmt_num(dist)),
        "垂足 H = P - (AP·n/|n|^2)·n = %s。" % vec_str(foot),
    ]

    scene = _base_scene(spec, pts, edges)
    scene.update({
        "highlight_point": {"name": pname, "color": RED},
        "plane": {"points": list(plane), "color": GREEN},
        "normal": {"origin": plane[0], "vec": [float(x) for x in n], "color": AMBER},
        "dashed_lines": [
            {"from": pname, "to": "H_foot", "color": RED}
        ],
        "extra_points": {
            "H_foot": [float(x) for x in foot]
        },
        "steps": steps,
        "result": {
            "html": "点 %s 到平面 %s%s%s 的距离 d = %s。" % (pname, plane[0], plane[1], plane[2], fmt_num(dist)),
            "dist": fmt_num(dist),
        },
    })
    return scene


def _volume_tetra(spec, pts, edges, q):
    apex, base = q["apex"], q["base"]
    p = pts[apex]
    a, b, c = pts[base[0]], pts[base[1]], pts[base[2]]
    ab = b - a
    ac = c - a
    ap_v = p - a
    vol = sp.simplify(abs(ab.dot(ac.cross(ap_v))) / 6)

    steps = [
        "顶点 %s%s，底面 %s%s%s：%s%s, %s%s, %s%s。"
        % (apex, vec_str(p), base[0], base[1], base[2],
           base[0], vec_str(a), base[1], vec_str(b), base[2], vec_str(c)),
        "取向量 AB = %s，AC = %s，AP = %s。" % (vec_str(ab), vec_str(ac), vec_str(ap_v)),
        "体积 V = |(AB x AC)·AP| / 6 = %s。" % fmt_num(vol),
    ]

    scene = _base_scene(spec, pts, edges)
    scene.update({
        "highlight_line": {"from": apex, "to": base[0], "color": RED},
        "plane": {"points": list(base), "color": GREEN},
        "steps": steps,
        "result": {
            "html": "三棱锥 %s-%s%s%s 的体积 V = %s。" % (apex, base[0], base[1], base[2], fmt_num(vol)),
            "volume": fmt_num(vol),
        },
    })
    return scene


def _parallel_perp(spec, pts, edges, q):
    check = q["check"]
    v1p, v2p = q["v1"], q["v2"]
    v1 = pts[v1p[1]] - pts[v1p[0]]
    v2 = pts[v2p[1]] - pts[v2p[0]]
    dot = sp.simplify(v1.dot(v2))

    if check == "perp":
        is_yes = dot == 0
        concl = "垂直" if is_yes else "不垂直"
        basis = "v1·v2 = %s %s 0" % (fmt_num(dot), "=" if is_yes else "!=")
    elif check == "parallel":
        cross = v1.cross(v2)
        zero = all(sp.simplify(x) == 0 for x in cross)
        is_yes = zero and dot != 0
        concl = "平行" if is_yes else ("共线(重合方向)" if zero else "不平行")
        basis = "v1 x v2 = %s，%s" % (
            vec_str(cross), "且不共点故为异面平行" if is_yes else "")
    else:
        raise ValueError("check must be 'parallel' or 'perp'")

    steps = [
        "取向量 v1 = %s - %s = %s，v2 = %s - %s = %s。"
        % (v1p[1], v1p[0], vec_str(v1), v2p[1], v2p[0], vec_str(v2)),
        "判定依据：%s。" % basis,
        "结论：直线 %s%s 与 %s%s %s。" % (v1p[0], v1p[1], v2p[0], v2p[1], concl),
    ]

    scene = _base_scene(spec, pts, edges)
    scene.update({
        "highlight_lines": [
            {"from": v1p[0], "to": v1p[1], "color": RED},
            {"from": v2p[0], "to": v2p[1], "color": BLUE},
        ],
        "steps": steps,
        "result": {
            "html": "直线 %s%s 与 %s%s %s（%s）。" % (v1p[0], v1p[1], v2p[0], v2p[1], concl, basis),
            "verdict": concl,
        },
    })
    return scene


def _skew_distance(spec, pts, edges, q):
    """异面直线距离：公垂向量法。d = |(v1 x v2)·(P2-P1)| / |v1 x v2|"""
    l1, l2 = q["line1"], q["line2"]
    v1 = pts[l1[1]] - pts[l1[0]]
    v2 = pts[l2[1]] - pts[l2[0]]
    w = v1.cross(v2)
    if w.dot(w) == 0:
        raise ValueError("lines are parallel or coplanar, not skew")
    diff = pts[l2[0]] - pts[l1[0]]
    dist = sp.simplify(abs(w.dot(diff)) / sp.sqrt(w.dot(w)))

    # 公垂足（参数化求最近点对）
    t1, t2 = sp.symbols("t1 t2")
    pA = pts[l1[0]] + t1 * v1
    pB = pts[l2[0]] + t2 * v2
    eqs = [sp.Eq((pB - pA).dot(v1), 0), sp.Eq((pB - pA).dot(v2), 0)]
    sol = sp.solve(eqs, [t1, t2], dict=True)[0]
    foot1 = sp.simplify(pts[l1[0]] + sol[t1] * v1)
    foot2 = sp.simplify(pts[l2[0]] + sol[t2] * v2)

    steps = [
        "直线 %s%s 方向向量 v1 = %s；直线 %s%s 方向向量 v2 = %s。"
        % (l1[0], l1[1], vec_str(v1), l2[0], l2[1], vec_str(v2)),
        "公垂方向 w = v1 x v2 = %s。" % vec_str(w),
        "距离 d = |w·(%s - %s)| / |w| = %s。"
        % (l2[0], l1[0], fmt_num(dist)),
        "公垂足 H1%s 在直线上，H2%s 在另一条直线上，验证 |H1H2| = %s。"
        % (vec_str(foot1), vec_str(foot2), fmt_num(sp.sqrt((foot2 - foot1).dot(foot2 - foot1)))),
    ]

    scene = _base_scene(spec, pts, edges)
    scene.update({
        "highlight_lines": [
            {"from": l1[0], "to": l1[1], "color": RED},
            {"from": l2[0], "to": l2[1], "color": BLUE},
        ],
        "dashed_lines": [{"from": "H1_common", "to": "H2_common", "color": AMBER}],
        "extra_points": {
            "H1_common": [float(x) for x in foot1],
            "H2_common": [float(x) for x in foot2],
        },
        "steps": steps,
        "result": {
            "html": "异面直线 %s%s 与 %s%s 的距离 d = %s。"
            % (l1[0], l1[1], l2[0], l2[1], fmt_num(dist)),
            "dist": fmt_num(dist),
        },
    })
    return scene


def _circumsphere(spec, pts, edges, q):
    """外接球：四点定球心（到各点等距），解线性方程组。"""
    names = q["points"]
    assert len(names) == 4, "circumsphere needs exactly 4 points"
    p = {n: pts[n] for n in names}
    o = p[names[0]]

    # |O-A|^2 = |O-X|^2 -> 2(OX-OA)·O = |OX|^2-|OA|^2，O 为未知球心
    xs = sp.symbols("cx cy cz")
    center = sp.Matrix(list(xs))
    eqs = []
    for n in names[1:]:
        lhs = 2 * (p[n] - o).dot(center)
        rhs = p[n].dot(p[n]) - o.dot(o)
        eqs.append(sp.Eq(lhs, rhs))
    sol = sp.solve(eqs, list(xs), dict=True)[0]
    C = sp.Matrix([sol[xs[0]], sol[xs[1]], sol[xs[2]]])
    R = sp.simplify(sp.sqrt((C - o).dot(C - o)))

    steps = [
        "取四点：%s。"
        % ", ".join("%s%s" % (n, vec_str(p[n])) for n in names),
        "设球心 O(cx, cy, cz)，由 |O-%s| = |O-%s| 等距条件得线性方程组。" % (names[0], names[1]),
        "解得球心 O%s。" % vec_str(C),
        "半径 R = |O-%s| = %s ≈ %s。" % (names[0], fmt_num(R), str(round(float(R.evalf()), 4))),
    ]

    scene = _base_scene(spec, pts, edges)
    scene.update({
        "highlight_point": {"name": names[0], "color": RED},
        "dashed_lines": [{"from": "C_sphere", "to": names[0], "color": AMBER}],
        "extra_points": {"C_sphere": [float(x) for x in C]},
        "sphere_wire": {"center": "C_sphere", "r": float(R.evalf())},
        "steps": steps,
        "result": {
            "html": "外接球球心 O%s，半径 R = %s ≈ %.4f。"
            % (vec_str(C), fmt_num(R), float(R.evalf())),
            "R": fmt_num(R),
        },
    })
    return scene


def _three_views(spec, pts, edges, q):
    """三视图：主视(x-z 平面, 投影掉 y)、左视(y-z, 投影掉 x)、俯视(x-y, 投影掉 z)。

    输出各视图的线段列表（2D 坐标），前端画三张小图。
    可见性简化处理：多面体轮廓投影 = 所有棱投影的并集，重叠线段去重。
    """
    def project(edges_list, drop_axis, flip):
        segs = set()
        for a, b in edges_list:
            pa = [float(x) for i, x in enumerate(pts[a]) if i != drop_axis]
            pb = [float(x) for i, x in enumerate(pts[b]) if i != drop_axis]
            key = tuple(sorted([tuple(pa), tuple(pb)]))
            segs.add(key)
        return [[list(s[0]), list(s[1])] for s in sorted(segs)]

    # 主视: 看 -y 方向 -> x 横轴, z 纵轴 (drop y=index 1)
    front = project(edges, 1, False)
    # 左视: 看 +x 方向 -> y 横轴, z 纵轴 (drop x=index 0)
    side = project(edges, 0, False)
    # 俯视: 看 -z 方向 -> x 横轴, y 纵轴 (drop z=index 2)
    top = project(edges, 2, False)

    scene = _base_scene(spec, pts, edges)
    scene.update({
        "views": {
            "front": {"label": "主视图", "segs": front},
            "side": {"label": "左视图", "segs": side},
            "top": {"label": "俯视图", "segs": top},
        },
        "steps": [
            "主视图：从正前方（-y 方向）观察，投影到 x-z 平面。",
            "左视图：从左侧（+x 方向）观察，投影到 y-z 平面。",
            "俯视图：从上方（-z 方向）观察，投影到 x-y 平面。",
            "对照 3D 图旋转到对应角度，可验证每个视图的轮廓。",
        ],
        "result": {
            "html": "三视图已生成：主视图、左视图、俯视图（见右侧面板下方）。",
        },
    })
    return scene


def _surface_shortest_path(spec, pts, edges, q):
    """长方体/正方体表面最短路径：枚举 6 种展开方式取最小。

    q: {"from": "A", "to": "G"}，点须是长方体顶点。
    展开：把终点所在面翻平到起点所在面所在平面，直线距离即路径长。
    """
    dims = spec.get("params", {})
    a = float(dims.get("a", 1))  # x 宽
    b = float(dims.get("b", 1))  # y 深
    c = float(dims.get("c", 1))  # z 高

    p_from = pts[q["from"]]
    p_to = pts[q["to"]]

    # 长方体 6 面：每面由法向 + 固定坐标定义。将 to 点绕棱翻转到 from 所在平面。
    # 简化通用做法：对每个轴向翻转组合展开。经典结论：三种横跨展开 (a+b+c 取两和)。
    # 这里用通用枚举：to 相对 from 的位移 (dx,dy,dz)，展开等价于把某一维"镜像叠加"到另外两维：
    # 候选路径 = sqrt((dx)^2+(dy+dz)^2), sqrt((dx+dy)^2+(dz)^2), sqrt((dx)^2... ) 全排列去重
    dx = abs(float(p_to[0] - p_from[0]))
    dy = abs(float(p_to[1] - p_from[1]))
    dz = abs(float(p_to[2] - p_from[2]))
    ds = [dx, dy, dz]
    candidates = []
    for i in range(3):
        j, k2 = [(0, 1), (0, 2), (1, 2)][i] if False else [(0, 1), (0, 2), (1, 2)][i]
        # 组合 i: 一维保持 d[i]，另两维相加
        rest = [ds[m] for m in range(3) if m != i]
        L = sp.sqrt(ds[i] ** 2 + (rest[0] + rest[1]) ** 2)
        candidates.append((sp.simplify(L), i))
    best = min(candidates, key=lambda t: float(t[0].evalf()))
    length = best[0]

    steps = [
        "长方体尺寸 %s x %s x %s，从 %s 到 %s 沿表面爬行。" % (fmt_num(a), fmt_num(b), fmt_num(c), q["from"], q["to"]),
        "将终点所在面分别沿三条不同棱展开到底面所在平面，得到三种候选直线距离。",
        "候选 1: sqrt(%s^2 + (%s+%s)^2)；候选 2: sqrt(%s^2 + (%s+%s)^2)；候选 3: sqrt(%s^2 + (%s+%s)^2)。"
        % tuple(x for i in range(3) for x in (fmt_num(ds[i]), fmt_num(ds[(i + 1) % 3]), fmt_num(ds[(i + 2) % 3]))),
        "最短为第 %d 种：L = %s ≈ %.4f。" % (best[1] + 1, fmt_num(length), float(length.evalf())),
    ]

    scene = _base_scene(spec, pts, edges)
    scene.update({
        "highlight_line": {"from": q["from"], "to": q["to"], "color": AMBER},
        "steps": steps,
        "result": {
            "html": "%s 到 %s 的表面最短路径 L = %s ≈ %.4f（展开成直线后两点间距离）。"
            % (q["from"], q["to"], fmt_num(length), float(length.evalf())),
            "length": fmt_num(length),
        },
    })
    return scene


def _insphere(spec, pts, edges, q):
    """内切球：利用对称性，球心在高线上，半径 = 到底面距离 = 到侧面距离。

    正四棱锥 P-ABCD / 正四面体 P-ABC：球心 O 在顶点与底面重心连线上，
    用等体积法 R = 3V / S_total。
    """
    solid = spec["solid"]
    apex = q.get("apex", "P" if "P" in pts else None)
    if apex is None:
        raise ValueError("insphere needs apex key in points")
    base_names = [n for n in pts if n != apex and n != "C_sphere"]
    # 底面取 z 最小的点
    zmin = min(float(pts[n][2]) for n in base_names)
    base = [n for n in base_names if abs(float(pts[n][2]) - zmin) < 1e-9]
    p = pts[apex]

    # 底面多边形面积（扇形三角化）
    def poly_area(names):
        s = sp.Matrix(0, 0, 0) if False else None
        total = sp.Matrix([0, 0, 0])
        a0 = pts[names[0]]
        for i in range(1, len(names) - 1):
            v1 = pts[names[i]] - a0
            v2 = pts[names[i + 1]] - a0
            total = total + v1.cross(v2)
        return sp.simplify(total.dot(total) ** sp.Rational(1, 2) / 2)

    S_base = poly_area(base)
    V_tet_parts = []
    S_side = sp.Integer(0)
    n_side = len(base)
    for i in range(n_side):
        tri = [base[i], base[(i + 1) % n_side], apex]
        s = sp.Matrix(3, 1, lambda r, c2: (pts[tri[1]] - pts[tri[0]])[r] * (pts[tri[2]] - pts[tri[0]])[(r + 1) % 3] - (pts[tri[2]] - pts[tri[0]])[r] * (pts[tri[1]] - pts[tri[0]])[(r + 1) % 3])
        area_i = sp.simplify(s.dot(s) ** sp.Rational(1, 2) / 2)
        S_side += area_i

    # 高 h: apex 到底面平面距离
    b0 = pts[base[0]]
    u1 = pts[base[1]] - b0
    u2 = pts[base[2]] - b0
    nvec = u1.cross(u2)
    h = sp.simplify(abs((p - b0).dot(nvec)) / sp.sqrt(nvec.dot(nvec)))
    V = sp.simplify(S_base * h / 3)
    R = sp.simplify(3 * V / (S_base + S_side))

    # 球心在底面重心正上方 R 处（沿法向）
    n_unit = nvec.normalized()
    if float(n_unit.dot(p - b0).evalf()) < 0:
        n_unit = -n_unit
    cen = pts[base[0]]
    for n in base[1:]:
        cen = cen + pts[n]
    centroid = cen / len(base)
    C = centroid + n_unit * R

    steps = [
        "立体为 %s，顶点 %s，底面 %s。" % (solid, apex, "".join(base)),
        "表面积 = 底面积 + 侧面积 = %s + %s = %s。"
        % (fmt_num(S_base), fmt_num(S_side), fmt_num(S_base + S_side)),
        "体积 V = 底面积 x 高 / 3 = %s x %s / 3 = %s。" % (fmt_num(S_base), fmt_num(h), fmt_num(V)),
        "等体积法：R = 3V / S_total = %s ≈ %.4f。" % (fmt_num(R), float(R.evalf())),
        "球心在底面重心沿法向上方 R 处：%s。" % vec_str(C),
    ]

    scene = _base_scene(spec, pts, edges)
    scene.update({
        "highlight_point": {"name": apex, "color": RED},
        "extra_points": {"C_sphere": [float(x) for x in C]},
        "sphere_wire": {"center": "C_sphere", "r": float(R.evalf())},
        "steps": steps,
        "result": {
            "html": "内切球球心 %s，半径 R = %s ≈ %.4f（等体积法 R = 3V/S）。"
            % (vec_str(C), fmt_num(R), float(R.evalf())),
            "R": fmt_num(R),
        },
    })
    return scene


def _net(spec, pts, edges, q):
    """正方体/长方体展开图：十字形展开（下、前、右、后、左 + 上）。

    输出 2D 面片列表 [{name, corners:[[x,y]x4], label}]，前端画展开网。
    坐标系：底面 ABCD (z=0)。展开：底面不动，四个侧面绕底边翻平，顶面接在后面上。
    """
    dims = spec.get("params", {})
    if spec["solid"] == "cuboid":
        a, b, c = float(dims.get("a", 1)), float(dims.get("b", 1)), float(dims.get("c", 1))
    else:
        s = float(dims.get("side", 1))
        a = b = c = s

    faces = []
    # 底面 ABCD: 展开后放在原位 (x,y)
    faces.append({"name": "bottom", "label": "底面 ABCD",
                  "corners": [[0, 0], [a, 0], [a, b], [0, b]]})
    # 前(AB 边一侧, y=0): 向 -y 翻平
    faces.append({"name": "front", "label": "侧面 ABBA1",
                  "corners": [[0, 0], [a, 0], [a, -c], [0, -c]]})
    # 右(BC 边一侧, x=a): 向 +x 翻平
    faces.append({"name": "right", "label": "侧面 BCCB1",
                  "corners": [[a, 0], [a, b], [a + c, b], [a + c, 0]]})
    # 后(CD 边一侧, y=b): 向 +y 翻平
    faces.append({"name": "back", "label": "侧面 CDDC1",
                  "corners": [[a, b], [0, b], [0, b + c], [a, b + c]]})
    # 左(DA 边一侧, x=0): 向 -x 翻平
    faces.append({"name": "left", "label": "侧面 DAA D1",
                  "corners": [[0, b], [0, 0], [-c, 0], [-c, b]]})
    # 顶面: 接在后侧面上方 (与 back 共边 y=b+c)
    faces.append({"name": "top", "label": "顶面 A1B1C1D1",
                  "corners": [[a, b + c], [0, b + c], [0, 2 * b + c], [a, 2 * b + c]]})

    scene = _base_scene(spec, pts, edges)
    scene.update({
        "net": {"faces": faces},
        "steps": [
            "展开方式：底面 ABCD 不动，四个侧面分别绕各自底边翻平，顶面 A1B1C1D1 接在后面上。",
            "展开图共 %d 个面，面积之和 = 表面积 = 2(ab+bc+ca) = %s。"
            % (len(faces), fmt_num(2 * (a * b + b * c + c * a))),
            "相对面不相邻：底面与顶面隔着一个侧面；展开图中它们也不共边。",
        ],
        "result": {
            "html": "展开图为 6 面十字形，表面积 S = 2(ab+bc+ca) = %s。" % fmt_num(2 * (a * b + b * c + c * a)),
            "area": fmt_num(2 * (a * b + b * c + c * a)),
        },
    })
    return scene


def _surface_volume(spec, pts, edges, q):
    """表面积/体积：多面体按面求和，旋转体按公式。"""
    solid = spec["solid"]
    params = spec.get("params", {})

    def poly_area(names):
        total = sp.Matrix([0, 0, 0])
        for i in range(1, len(names) - 1):
            v1 = pts[names[i]] - pts[names[0]]
            v2 = pts[names[i + 1]] - pts[names[0]]
            total = total + v1.cross(v2)
        return sp.simplify(sp.sqrt(total.dot(total)) / 2)

    if solid == "cylinder":
        r = float(params.get("r", 0.5))
        h = float(params.get("h", 1))
        side_area = sp.Integer(2) * sp.pi * sp.Rational(str(r)) * sp.Rational(str(h))
        S = sp.simplify(side_area + 2 * sp.pi * sp.Rational(str(r)) ** 2)
        V = sp.simplify(sp.pi * sp.Rational(str(r)) ** 2 * sp.Rational(str(h)))
        detail = ["侧面积 = 2*pi*r*h = %s" % fmt_num(side_area),
                  "两底面积合计 = 2*pi*r^2 = %s" % fmt_num(2 * sp.pi * sp.Rational(str(r)) ** 2)]
        formula = "S = 2*pi*r*h + 2*pi*r^2, V = pi*r^2*h"
    elif solid == "cone":
        r = float(params.get("r", 0.5))
        h = float(params.get("h", 1))
        l = sp.sqrt(sp.Rational(str(r)) ** 2 + sp.Rational(str(h)) ** 2)  # 母线
        side_area = sp.simplify(sp.pi * sp.Rational(str(r)) * l)
        base_area = sp.simplify(sp.pi * sp.Rational(str(r)) ** 2)
        S = sp.simplify(side_area + base_area)
        V = sp.simplify(sp.pi * sp.Rational(str(r)) ** 2 * sp.Rational(str(h)) / 3)
        detail = ["母线 l = sqrt(r^2+h^2) = %s" % fmt_num(l),
                  "侧面积 = pi*r*l = %s" % fmt_num(side_area),
                  "底面积 = pi*r^2 = %s" % fmt_num(base_area)]
        formula = "S = pi*r*l + pi*r^2, V = pi*r^2*h/3"
    elif solid == "sphere":
        r = float(params.get("r", 1))
        S = sp.simplify(4 * sp.pi * sp.Rational(str(r)) ** 2)
        V = sp.simplify(sp.Rational(4, 3) * sp.pi * sp.Rational(str(r)) ** 3)
        detail = ["球面积 = 4*pi*r^2"]
        formula = "S = 4*pi*r^2, V = (4/3)*pi*r^3"
    else:
        # 多面体: 枚举所有三角面（棱锥/棱柱/台体通用做法：逐三角形累加）
        face_names = q.get("faces")
        if not face_names:
            raise ValueError("surface_volume needs explicit 'faces' list of point-name lists")
        S_parts = []
        S_total = sp.Integer(0)
        for fn in face_names:
            area_i = poly_area(fn)
            S_parts.append((fn, area_i))
            S_total += area_i
        S = sp.simplify(S_total)
        detail = ["%s: %s" % ("-".join(fn), fmt_num(ar)) for fn, ar in S_parts]
        # 体积: 以第一个面为底, 对凸多面体用发散定理较复杂; 这里要求 q 提供 apex 或直接给 volume via 分解
        if q.get("volume_decomp"):
            V = sp.Integer(0)
            for tri in q["volume_decomp"]:
                a0, b0, c0 = pts[tri[0]], pts[tri[1]], pts[tri[2]]
                d0 = pts[q["volume_apex"]]
                vol_i = abs((b0 - a0).cross(c0 - a0).dot(d0 - a0)) / 6
                V += sp.simplify(vol_i)
            V = sp.simplify(V)
        else:
            V = None
        formula = "逐面求和"

    steps = ["立体为 %s。" % solid]
    steps += ["%s。" % d if not d.endswith("。") else d for d in detail]
    steps.append("%s。" % formula)
    steps.append("S = %s ≈ %.4f%s。" % (fmt_num(S), float(S.evalf()),
                 ("；V = %s ≈ %.4f" % (fmt_num(V), float(V.evalf()))) if V is not None else ""))

    result_html = "表面积 S = %s ≈ %.4f" % (fmt_num(S), float(S.evalf()))
    if V is not None:
        result_html += "，体积 V = %s ≈ %.4f" % (fmt_num(V), float(V.evalf()))
    result_html += "。"

    scene = _base_scene(spec, pts, edges)
    if solid in ("cylinder", "cone", "sphere"):
        r = float(params.get("r", 0.5))
        scene["mesh"] = {"kind": solid, "r": r}
    scene.update({
        "steps": steps,
        "result": {"html": result_html, "S": fmt_num(S)},
    })
    if V is not None:
        scene["result"]["V"] = fmt_num(V)
    return scene


def main():
    if len(sys.argv) < 3:
        print("usage: python geometry_solver.py <spec.json> <scene.json>", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        spec = json.load(f)
    scene = solve(spec)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        json.dump(scene, f, ensure_ascii=False, indent=2)
    print("scene written:", sys.argv[2])


if __name__ == "__main__":
    main()
