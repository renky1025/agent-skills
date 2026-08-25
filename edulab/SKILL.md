---
name: edulab
description: 面向中高考数学的可视化解题工具：空间几何题生成可交互 3D 解题演示（建系向量法 + sympy 校验 + Three.js），函数表达式生成参数可控的 2D 图形（滑块实时联动）。触发词 /edulab。
---

# edulab

中高考数学可视化：空间几何 3D 解题演示 + 函数图形参数可控可视化。产物为单文件交互式 HTML。

## 何时使用

- 用户给出立体几何题（中高考风格），需要 3D 演示解题过程
- 用户想要函数图像且希望调参看变化（滑块联动）
- `/edulab <题目或函数>`

## 工作流

### 几何模块

1. 读题，确定立体类型与参数，写入 spec JSON（契约见 references/schema.md；题型清单见 references/taxonomy.md）。支持 query.type: line_plane_angle / line_line_angle / dihedral_angle / point_plane_distance / volume_tetra / parallel_perp / skew_distance / circumsphere / three_views / surface_shortest_path / insphere；solid: cube/cuboid/tetra/prism3/pyramid4/cylinder/cone/sphere。
2. 求解（必须用 managed venv 的 python）：
   ```
   cd ~/.workbuddy/skills/edulab/scripts/geometry
   ~/.workbuddy/binaries/python/envs/default/bin/python geometry_solver.py <spec.json> <scene.json>
   ```
   solver 内含 sympy 计算，输出精确值 + 数值。检查 steps 与 result 是否与标准答案一致，不一致则修 spec 重跑，不得静默交付错误答案。
3. 生成 HTML（加 --offline 内联 Three.js，无网环境可打开）：
   ```
   python3 build_html.py <scene.json> <out.html> [--offline]
   ```
4. present_files 打开 out.html。

### 函数模块

1. 确定函数族（quadratic/linear/inverse/trig/exp/log/power 或 custom 自由表达式）。custom 时 params 传 {"expr": "sin(x)/x"}，表达式经 safe_expr.py 安全解析（禁 eval），非法输入直接拒绝。
2. 生成 scene（参数写 JSON 文件传入）：
   ```
   cd ~/.workbuddy/skills/edulab/scripts/function
   ~/.workbuddy/binaries/python/envs/default/bin/python function_engine.py quadratic <params.json> <scene.json>
   ```
3. `python3 build_html.py <scene.json> <out.html>` 后 present_files。

## 扩展约定

- 新几何题型：geometry_solver.py 加 query type 分支 + taxonomy.md 更新状态。
- 新函数族：function_families.py 加项 + template_2d.html 的 f()/computeProps() 加分支。
- 新立体：solids.py 加 vertices/edges。
- 文件写入禁 Box Drawing 等 Unicode 装饰字符（防乱码）；中文标签走 DOM/Canvas 文本。
- 自由函数表达式若支持，禁 eval/Function，须安全 AST 解析。

## 设计文档

完整架构、阶段规划、已验证结论见 references/design.md。
