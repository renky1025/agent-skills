"""函数族定义：参数配置 + 渲染类型(kind)。

每个 family 给出可调参数（默认/范围/步长），kind 告诉前端模板如何求值与计算性质。
新增函数族 = 在此加一项 + 在 template_2d.html 的 f()/props_* 中加对应分支。
"""

FAMILIES = {
    "quadratic": {
        "label": "二次函数 y = ax^2 + bx + c",
        "kind": "quadratic",
        "params": {
            "a": {"default": 1, "min": -3, "max": 3, "step": 0.1},
            "b": {"default": 0, "min": -5, "max": 5, "step": 0.1},
            "c": {"default": -1, "min": -5, "max": 5, "step": 0.1},
        },
    },
    "linear": {
        "label": "一次函数 y = kx + b",
        "kind": "linear",
        "params": {
            "k": {"default": 1, "min": -3, "max": 3, "step": 0.1},
            "b": {"default": 0, "min": -5, "max": 5, "step": 0.1},
        },
    },
    "inverse": {
        "label": "反比例函数 y = k/x",
        "kind": "inverse",
        "params": {
            "k": {"default": 2, "min": -6, "max": 6, "step": 0.1},
        },
    },
    "trig": {
        "label": "三角函数 y = A*sin(w*x + p) + k",
        "kind": "trig",
        "params": {
            "A": {"default": 1, "min": -3, "max": 3, "step": 0.1},
            "w": {"default": 1, "min": -4, "max": 4, "step": 0.1},
            "p": {"default": 0, "min": -3.14, "max": 3.14, "step": 0.01},
            "k": {"default": 0, "min": -3, "max": 3, "step": 0.1},
        },
    },
    "exp": {
        "label": "指数函数 y = a^x",
        "kind": "exp",
        "params": {
            "a": {"default": 2, "min": 0.1, "max": 4, "step": 0.1},
        },
    },
    "log": {
        "label": "对数函数 y = log_a(x)",
        "kind": "log",
        "params": {
            "a": {"default": 2, "min": 1.1, "max": 4, "step": 0.1},
        },
    },
    "power": {
        "label": "幂函数 y = x^p",
        "kind": "power",
        "params": {
            "p": {"default": 2, "min": -2, "max": 4, "step": 0.5},
        },
    },
}
