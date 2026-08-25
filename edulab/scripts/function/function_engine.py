"""函数引擎：采样 + 关键点性质计算（Python 侧基线，供前端对照验证）。

输入 family 名 + params（当前参数值），输出 scene JSON。
用法:
    python function_engine.py <family> <params.json> <scene.json>
其中 params.json 形如 {"a":1,"b":0,"c":-1}（可缺省，用默认值）。
"""

import json
import math
import sys

from function_families import FAMILIES
from safe_expr import SafeExpr


def compute_multi(params):
    """多函数叠加对比。

    params: {"items": [{"expr": "x^2", "label": "y=x^2"}, ...], "xr": [xmin, xmax](可选)}
    每条曲线独立采样（Python 端安全求值），前端只画不评。
    """
    items = params.get("items", [])
    if not items:
        raise ValueError("multi needs non-empty items")
    xr = params.get("xr", [-6, 6])
    curves = []
    palette = ["#6c8cff", "#5fd38a", "#ff7a9e", "#ffc46b", "#c79fe0", "#7fd4e0"]
    for idx, it in enumerate(items):
        expr_text = str(it.get("expr", "0"))
        se = SafeExpr(expr_text)
        pts_list = []
        n = 480
        for i in range(n + 1):
            x = xr[0] + (xr[1] - xr[0]) * i / n
            try:
                y = se.eval({"x": x})
            except (ZeroDivisionError, OverflowError):
                y = float("nan")
            pts_list.append([round(x, 4), y])
        curves.append({
            "expr": expr_text,
            "label": str(it.get("label", "y = " + expr_text)),
            "color": palette[idx % len(palette)],
            "points": pts_list,
        })
    return {
        "type": "function",
        "kind": "multi",
        "label": "函数对比",
        "curves": curves,
        "params": {},
        "current": {},
        "xrange": list(xr),
        "properties": {"note": "%d curves" % len(curves)},
    }


def compute(family, params):
    if family == "custom":
        expr_text = str(params.get("expr", "sin(x)"))
        se = SafeExpr(expr_text)  # 解析失败即抛 ValueError, 不静默
        # Python 侧采样若干点作为基线
        samples = []
        i = -60
        while i <= 60:
            x = i / 10.0
            try:
                y = se.eval({"x": x})
            except (ZeroDivisionError, OverflowError):
                y = float("nan")
            samples.append([x, y])
            i += 1
        return {
            "type": "function",
            "kind": "custom",
            "label": "y = " + expr_text,
            "expr": expr_text,
            "samples": samples,
            "params": {},
            "current": {},
            "xrange": [-6, 6],
            "properties": {"note": "custom expression, rendered from server-side safe-parsed samples"},
        }

    cfg = FAMILIES[family]
    cur = {}
    for name, p in cfg["params"].items():
        cur[name] = float(params.get(name, p["default"]))

    props = {}
    if cfg["kind"] == "quadratic":
        a, b, c = cur["a"], cur["b"], cur["c"]
        vx = -b / (2 * a)
        vy = c - b * b / (4 * a)
        D = b * b - 4 * a * c
        roots = []
        if D >= 0:
            roots = [(-b - math.sqrt(D)) / (2 * a), (-b + math.sqrt(D)) / (2 * a)]
        props = {"vertex": [vx, vy], "axis": vx, "roots": roots, "y_intercept": c}
    elif cfg["kind"] == "linear":
        k, b = cur["k"], cur["b"]
        zero = (-b / k) if k != 0 else None
        props = {"slope": k, "intercept": b, "zero": zero}
    elif cfg["kind"] == "inverse":
        k = cur["k"]
        props = {"k": k,
                 "asymptotes": ["x=0", "y=0"],
                 "quadrants": [1, 3] if k > 0 else ([2, 4] if k < 0 else []),
                 "decreasing_on_each_branch": k > 0}
    elif cfg["kind"] == "trig":
        A, w, p, k = cur["A"], cur["w"], cur["p"], cur["k"]
        period = (2 * math.pi / abs(w)) if w != 0 else None
        props = {"amplitude": abs(A),
                 "period": round(period, 4) if period else None,
                 "phase_shift": round(p / w, 4) if w else None,
                 "range": [k - abs(A), k + abs(A)]}
    elif cfg["kind"] == "exp":
        a = cur["a"]
        props = {"base": a,
                 "asymptote": "y=0",
                 "y_intercept": 1,
                 "monotonic": "increasing" if a > 1 else ("decreasing" if 0 < a < 1 else "constant")}
    elif cfg["kind"] == "log":
        a = cur["a"]
        props = {"base": a,
                 "domain": "x>0",
                 "asymptote": "x=0",
                 "passes_through": [1, 0],
                 "monotonic": "increasing" if a > 1 else "decreasing"}
    elif cfg["kind"] == "power":
        p = cur["p"]
        fixed = []
        for x in (1.0,):
            fixed.append([x, x ** p])
        props = {"exponent": p,
                 "always_passes": [1, 1],
                 "defined_at_0": p > 0}

    return {
        "type": "function",
        "kind": cfg["kind"],
        "label": cfg["label"],
        "params": cfg["params"],
        "current": cur,
        "xrange": [-6, 6],
        "properties": props,
    }


def main():
    if len(sys.argv) < 4:
        print("usage: python function_engine.py <family> <params.json> <scene.json>", file=sys.stderr)
        sys.exit(1)
    family = sys.argv[1]
    with open(sys.argv[2], "r", encoding="utf-8") as f:
        params = json.load(f)
    scene = compute_multi(params) if family == "multi" else compute(family, params)
    with open(sys.argv[3], "w", encoding="utf-8") as f:
        json.dump(scene, f, ensure_ascii=False, indent=2)
    print("scene written:", sys.argv[3])


if __name__ == "__main__":
    main()
