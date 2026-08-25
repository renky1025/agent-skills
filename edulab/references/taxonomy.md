# 中高考空间几何与函数题型清单 (taxonomy)

## 空间几何

| 学段 | 题型 | 解法/可视化 | 状态 |
|---|---|---|---|
| 高考 | 线面角 | 向量法 sin=abs(v.n)/(|v||n|) | 已支持 (line_plane_angle) |
| 高考 | 线线角(异面) | 向量法 cos=abs(v1.v2)/(|v1||v2|) | 已支持 (line_line_angle) |
| 高考 | 二面角 | 半平面法向量夹角 | 已支持 (dihedral_angle) |
| 高考 | 点到面距离 | 投影 abs(AP.n)/|n|, 含垂足虚线 | 已支持 (point_plane_distance) |
| 高考 | 三棱锥体积 | 混合积 /6 | 已支持 (volume_tetra) |
| 高考 | 垂直/平行判定 | 点积/叉积判定 | 已支持 (parallel_perp) |
| 高考 | 异面直线距离 | 公垂向量投影, 含公垂足虚线 | 已支持 (skew_distance) |
| 高考 | 外接球 | 四点定球心线性方程组, 球线框渲染 | 已支持 (circumsphere) |
| 高考 | 内切球 | 等体积法 R=3V/S, 球线框渲染 | 已支持 (insphere) |
| 中考 | 三视图 | 正交投影三视图 + 2D 小图面板 | 已支持 (three_views) |
| 中考 | 展开图 | 十字形展开网面板 | 已支持 (net) |
| 中考 | 表面最短路径 | 展开枚举取最小 | 已支持 (surface_shortest_path) |
| 中考 | 表面积/体积(旋转体) | 公式分解步骤 + mesh 渲染 | 已支持 (surface_volume) |

## 函数图形

| 函数族 | 参数 | 联动性质 | 状态 |
|---|---|---|---|
| 二次 y=ax^2+bx+c | a,b,c | 顶点/对称轴/零点/y截距/开口 | 已支持 |
| 一次 y=kx+b | k,b | 斜率/截距/零点 | 族已定义, 模板分支待加 |
| 反比例 y=k/x | k | 渐近线/象限/每支单调性 | 已支持 |
| 三角 y=A sin(wx+p)+k | A,w,p,k | 振幅/周期/相位平移/值域 | 已支持 |
| 指数 y=a^x | a | 渐近线 y=0/过(0,1)/单调 | 已支持 |
| 对数 y=log_a(x) | a | 定义域 x>0/渐近线 x=0/过(1,0) | 已支持 |
| 幂 y=x^p | p | 恒过(1,1)/0处定义性 | 已支持 |
| 自由表达式 | 用户输入 | safe_expr 递归下降 AST(禁 eval), Python 端采样前端零求值 | 已支持 (custom) |

## 立体积木库

| solid | 参数化 | 状态 |
|---|---|---|
| cube | side | 已支持 |
| cuboid | a,b,c | 已支持 |
| tetra 正四面体 | side,h | 已支持 |
| prism3 直三棱柱(直角底) | a,b,c | 已支持 |
| pyramid4 正四棱锥 | side,h | 已支持 |
| cylinder 圆柱 | r,h | 已支持(mesh) |
| cone 圆锥 | r,h | 已支持(mesh) |
| sphere 球 | r | 已支持(mesh) |
