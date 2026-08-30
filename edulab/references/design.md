# edulab 设计文档

## 定位

面向中高考数学的可视化解题 Skill，双模块：

1. 空间几何模块：中文题目 -> 结构化规格 -> 建系向量法求解（sympy 校验）-> 可交互 3D 演示 HTML。
2. 函数图形模块：函数族 + 参数 -> Canvas2D 绘图 + 参数滑块实时联动。

产物统一为单文件自包含交互式 HTML。

## 架构

- 输入路由：LLM 判断意图，分派到几何或函数模块。
- 共享层：
  - 模板库：solids.py（立体参数坐标库）、function_families.py（函数族定义）。
  - 引擎：geometry_solver.py（sympy 符号/数值双重校验）、function_engine.py（采样 + 性质计算）。
- 渲染层：template_3d.html（Three.js + CSS2DRenderer 中文标签）、template_2d.html（Canvas2D + 滑块）。
- 生成器：build_html.py x2（scene JSON 注入模板占位符 /*__DATA__*/）。

## 数据流契约

spec(JSON) --geometry_solver--> scene(JSON) --build_html--> out.html
family+params(JSON) --function_engine--> scene(JSON) --build_html--> out.html

scene 是唯一中间契约；模板只消费 scene，不关心求解细节。新增题型 = 扩展 solver 的 query type；新增函数族 = function_families 加项 + template_2d.html 的 f()/computeProps() 加分支。

## 关键决策记录

- 选交互式 3D HTML 而非文生 3D/视频：网格不保证数学精确且无法叠加步骤标注。
- 3D 中文标签走 CSS2DRenderer DOM，避开 TextGeometry 字体文件问题。
- 几何答案必须经 sympy 独立重算，不符不交付（当前切片在 solve 内计算并输出精确分数/根式）。
- 函数自由表达式如后续支持，禁 eval/Function，须走安全 AST 解析器。
- 文件写入禁 Box Drawing 等 Unicode 装饰字符，防 U+FFFD 乱码。

## 阶段规划

- P0 脚手架 + schema + taxonomy [已完成]
- P1 几何垂直切片：正方体线面角 [已完成]
- P2 函数垂直切片：二次函数滑块 [已完成]
- P3 扩几何题型 [已完成]：
  - 新题型 5 种: line_line_angle(异面角) / dihedral_angle(二面角) / point_plane_distance(点面距离, 含垂足虚线) / volume_tetra(混合积体积) / parallel_perp(垂直平行判定)
  - 新立体 3 种: tetra 正四面体(side,h) / prism3 直三棱柱(a,b,c) / pyramid4 正四棱锥(side,h)
  - 模板升级: highlight_lines 多高亮线 / planes 多平面 / normals 多箭头 / dashed_lines 虚线 / extra_points 额外点
  - 6 道新例题端到端验证通过(独立解析核验: 异面角60°/二面角90°/距离1/体积1/6/不垂直判定/arcsin(1/sqrt3)=35.3°), 全 HTML 无乱码
- P4 函数族全量 + 几何进阶 [已完成]：
  - 新函数族 5 种: inverse(反比例) / trig(三角 A,w,p,k) / exp(指数) / log(对数) / power(幂)，性质联动 + 定点标注。
  - 新题型 2 种: skew_distance(异面距离, 公垂向量+公垂足虚线) / circumsphere(外接球, 四点定心, 球线框)。
  - 新立体 3 种: cylinder/cone/sphere(mesh 渲染, _r 半径标记约定)。
  - 验证: 异面距离 d=1、外接球 R=sqrt(3)/2 独立核验通过; 5 函数族性质核验通过; 全 HTML 无乱码。
- P5 收尾 [已完成]：
  - three_views 三视图: 正交投影线段 + 面板三张 2D 小图。
  - surface_shortest_path 表面最短路径: 展开枚举三种候选, sqrt(41)=6.4031 核验通过。
  - insphere 内切球: 等体积法 R=3V/S, 正四棱锥(2,1) R=sqrt(2)-1=0.4142 核验通过。
  - 自由表达式 custom: safe_expr.py 递归下降 AST, 禁 eval; 8 项正确性 + 4 项注入拒绝测试通过; Python 端采样前端零求值架构。
  - 离线打包: build_html.py --offline 内联 Three.js 三件套(+630KB), assets/vendor 本地缓存; 验证产物无 unpkg 依赖。
- P6 扩展 [已完成]：
  - net 展开图: 十字形展开网, 面板彩色面片渲染(3x2x1 表面积 S=22 核验通过)。
  - surface_volume 表面积/体积: 多面体逐面求和+体积分解 / 旋转体公式; 正四棱锥(side2,h1) S=4+4sqrt2, V=4/3 核验通过。
  - multi 多函数对比: items 数组同图多曲线+图例, 每条独立安全采样 481 点。
  - README.md 落地: 定位/架构图/能力清单/快速上手/扩展指南/验证记录/已知边界。

## 运行环境

运行环境：Python 3 + sympy 1.14.0

## 已验证

- 正方体 A1B 与底面 ADC 线面角 = 45 度（sin = sqrt(2)/2），sympy 计算 + 数值一致。
- 二次函数 y = ax^2 + bx + c 滑块实时重绘，顶点/零点/开口方向联动。
- 两 HTML 无 U+FFFD，数据注入完整。
