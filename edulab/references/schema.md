# edulab 规格 JSON 契约

## 几何 spec (geometry_solver 输入)

```json
{
  "title": "题目标题(可选)",
  "solid": "cube | cuboid",
  "params": {"side": 1} 或 {"a": 2, "b": 1, "c": 1},
  "query": {
    "type": "line_plane_angle",
    "line": ["A1", "B"],
    "plane": ["A", "D", "C"]
  }
}
```

query.type 当前支持: line_plane_angle。后续扩展见 taxonomy.md。
plane 为平面内不共线三点，顶点名须在 solids.py 的 vertices 内。

## 几何 scene (solver 输出 / build_html 输入)

- points: {名称: [x,y,z]}
- edges: [[p1,p2],...] 棱
- highlight_line: {from,to,color} 待求直线(红)
- plane: {points:[三点名], color} 待求平面(绿, 半透明)
- normal: {origin, vec, color} 法向量箭头(橙)
- steps: [步骤文本...]
- result: {html, ...数值}

## 函数 scene (function_engine 输出 / build_html 输入)

```json
{
  "type": "function",
  "kind": "quadratic | linear",
  "label": "二次函数 y = ax^2 + bx + c",
  "params": {"a": {"default":1,"min":-3,"max":3,"step":0.1}, ...},
  "current": {"a":1,...},
  "xrange": [-6,6],
  "properties": {...Python 侧基线值}
}
```

模板内 JS 会按滑块实时重算 properties（computeProps），Python 的 properties 仅作离线对照验证。
