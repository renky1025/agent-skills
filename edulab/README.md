# edulab - 中高考数学可视化解题 Skill

面向中高考数学的可视化工具：**空间几何题生成可交互 3D 解题演示，函数表达式生成参数可控的 2D 图形**。产物为单文件自包含 HTML，浏览器直接打开即可使用。

- 触发词：`/edulab <题目或函数>`
- 位置：`~/.claude/skills/edulab/`（用户级）
- 运行环境：Python 3 + sympy 1.14.0（建议：`python3 -m venv .venv && .venv/bin/pip install sympy`）

## 架构

```
输入(中文题目 / 函数表达式)
    |
    v
[LLM 读题路由] --> 空间几何模块          --> 函数图形模块
                    |                       |
            spec JSON(契约)           family+params JSON
                    |                       |
            geometry_solver.py       function_engine.py
            (坐标建模+sympy求解)      (safe_expr安全采样)
                    |                       |
                scene JSON ------------- scene JSON
                    |                       |
            template_3d.html         template_2d.html
        (Three.js+CSS2D中文标签)   (Canvas2D+参数滑块)
                    |                       |
                    +------> build_html.py <-+
                                 |
                    单文件交互式 HTML (可 --offline 离线打包)
```

设计原则：
- **scene JSON 是唯一中间契约**——模板只消费 scene，不关心求解细节。
- **所有几何答案经 sympy 计算**，另做独立解析核验，不符不交付。
- **前端零求值**——自定义表达式由 Python 端 safe_expr 安全解析后采样传点集。
- 文件写入禁 Box Drawing 等 Unicode 装饰字符（防乱码）。

## 目录结构

```
edulab/
  SKILL.md                  # 触发词与工作流
  README.md                 # 本文档
  references/
    design.md               # 架构决策 + 阶段规划(P0-P6) + 验证记录
    taxonomy.md             # 中高考题型清单与支持状态
    schema.md               # spec/scene JSON 契约
  scripts/
    geometry/
      solids.py             # 立体积木库(8种参数化坐标)
      geometry_solver.py    # 求解器(11种题型, sympy 校验)
      template_3d.html      # Three.js r128 + CSS2DRenderer 中文标签
      build_html.py         # scene -> HTML (--offline 可内联依赖)
    function/
      function_families.py  # 7 个函数族定义
      function_engine.py    # 性质计算 + 采样 (+multi 多曲线 +custom)
      safe_expr.py          # 递归下降 AST 安全表达式解析器(禁 eval)
      template_2d.html      # Canvas2D + 参数滑块实时联动
      build_html.py         # scene -> HTML
  assets/vendor/            # Three.js 三件套本地缓存(离线打包用)
  examples/                 # 17 个样例 spec
  output/                   # 生成的演示 HTML
```

## 能力清单

### 空间几何（11 种题型）

| query.type | 说明 | 可视化 |
|---|---|---|
| line_plane_angle | 线面角 | 高亮直线 + 半透明平面 + 法向量箭头 |
| line_line_angle | 异面直线角 | 双色高亮线 |
| dihedral_angle | 二面角 | 双平面 + 双法向量 |
| point_plane_distance | 点面距离 | 垂足点 + 虚线 |
| skew_distance | 异面直线距离 | 公垂足虚线段 |
| volume_tetra | 三棱锥体积 | 顶点-底面标注 |
| parallel_perp | 平行/垂直判定 | 双色高亮线 |
| circumsphere | 外接球 | 四点定心 + 球线框 |
| insphere | 内切球 | 等体积法 R=3V/S + 球线框 |
| three_views | 三视图 | 面板三张正交投影小图 |
| surface_shortest_path | 表面最短路径 | 展开枚举取最小 |
| net | 展开图 | 彩色十字展开网面板 |
| surface_volume | 表面积/体积 | 公式分解步骤 |

立体积木库（8 种）：`cube`(side)、`cuboid`(a,b,c)、`tetra` 正四面体(side,h)、`prism3` 直三棱柱(a,b,c)、`pyramid4` 正四棱锥(side,h)、`cylinder`(r,h)、`cone`(r,h)、`sphere`(r)。旋转体走 mesh 渲染，`_r` 为半径标记约定。

### 函数图形

| 类型 | 参数 | 联动性质 |
|---|---|---|
| quadratic y=ax^2+bx+c | a,b,c | 顶点/对称轴/零点/y截距/开口 |
| linear y=kx+b | k,b | 斜率/截距/零点 |
| inverse y=k/x | k | 渐近线/象限/单调性 |
| trig y=A sin(wx+p)+k | A,w,p,k | 振幅/周期/相位/值域 |
| exp y=a^x | a | 渐近线/过(0,1)/单调 |
| log y=log_a(x) | a | 定义域/渐近线/过(1,0) |
| power y=x^p | p | 恒过(1,1)/0处定义性 |
| custom 自由表达式 | expr 字符串 | safe_expr 解析, Python 端采样 |
| multi 多函数对比 | items 数组 | 同图多曲线+图例 |

## 快速上手

### 几何题

```bash
# 1. 写 spec JSON
cat > /tmp/spec.json << 'EOF'
{
  "title": "正方体线面角",
  "solid": "cube",
  "params": {"side": 1},
  "query": {"type": "line_plane_angle", "line": ["A1","B"], "plane": ["A","D","C"]}
}
EOF

# 2. 求解(Python 3 + sympy)
cd ~/.claude/skills/edulab/scripts/geometry
python3 geometry_solver.py /tmp/spec.json /tmp/scene.json

# 3. 生成 HTML(--offline 内联 Three.js, 无网可开)
python3 build_html.py /tmp/scene.json /tmp/out.html --offline
```

### 函数图

```bash
cd ~/.claude/skills/edulab/scripts/function

# 参数族: family + params JSON
echo '{"a":1,"b":0,"c":-1}' > /tmp/p.json
python3 function_engine.py quadratic /tmp/p.json /tmp/scene.json
python3 build_html.py /tmp/scene.json /tmp/out.html

# 自由表达式(custom): 表达式经 safe_expr 解析, 非法输入拒绝
echo '{"expr":"sin(x)/x"}' > /tmp/c.json
python3 function_engine.py custom /tmp/c.json /tmp/scene2.json

# 多函数对比(multi)
cat > /tmp/m.json << 'EOF'
{"items":[{"expr":"x^2","label":"y=x^2"},{"expr":"-x^2+3","label":"y=-x^2+3"}]}
EOF
python3 function_engine.py multi /tmp/m.json /tmp/scene3.json
```

## 扩展指南

- **新几何题型**：`geometry_solver.py` 加 dispatch 分支 + `_xxx` 函数 + `taxonomy.md` 更新状态。向量法模板：取方向向量/法向量 -> sympy 计算精确值 -> steps 数组写解题步骤 -> result 输出 html 与数值。
- **新函数族**：`function_families.py` 加项 + `template_2d.html` 的 `f()`/`computeProps()` 加分支。
- **新立体**：`solids.py` 加 vertices/edges（旋转体加 mesh 定义）。
- **安全红线**：自由表达式只允许走 `safe_expr.py`（禁 eval/Function）；文件写入禁 Unicode 装饰字符；几何答案必须 sympy 核验后才可交付。

## 验证记录（摘要）

全部题型端到端验证通过，关键核验：

| 题目 | 结果 | 方法 |
|---|---|---|
| A1B 与底面 ADC 线面角 | sin=sqrt(2)/2, 45 度 | sympy + 解析 |
| A1B 与 AC 异面角 | cos=1/2, 60 度 | 解析 |
| C1 到平面 ABD 距离 | 1 | 解析 |
| D1-ABC 体积 | 1/6 | 解析 |
| AB 与 B1C1 异面距离 | 1 | 平行平面间距 |
| 正方体外接球 | O(1/2,1/2,1/2), R=sqrt(3)/2 | 解析 |
| 正四棱锥内切球(side2,h1) | R=sqrt(2)-1=0.4142 | 等体积法解析 |
| 4x3x2 表面最短路 A->C1 | sqrt(41)=6.4031 | 展开枚举 |
| safe_expr 注入测试 | 4/4 拒绝 | __import__/eval/分号/open |

完整验证记录见 `references/design.md`。

## 已知边界

- 几何读题依赖 LLM 把中文题映射到 spec JSON，复杂辅助线构造题需拆解为多步查询。
- `three_views` 采用轮廓投影简化（所有棱投影并集），非遮挡剔除的严格可见性算法。
- 展开图为固定十字形方案（一种），未覆盖 11 种正方体展开全枚举。
- CDN 版 HTML 依赖 unpkg（Three.js r128）；无网环境务必用 `--offline`。
