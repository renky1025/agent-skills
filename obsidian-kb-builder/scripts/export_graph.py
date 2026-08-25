#!/usr/bin/env python3
"""export_graph.py — 解析知识库全库的 [[wikilinks]]，导出 Obsidian 图数据。

用法:
  python3 export_graph.py --vault <vault> [--out <目录>] [--json]

输出（默认写到 vault 根目录 graph/）:
  graph-nodes.csv   节点：name,type,in_degree,out_degree,file
  graph-edges.csv   边：source,target
  graph.json        结构化（含 orphans / hubs），便于导入 Neo4j / Gephi

说明:
  - 节点 = 所有 .md 文件（去除扩展名） + 所有被链接的 target。
  - 边 = 每处 [[target]]（支持 [[target|alias]]，取 target）。
  - 孤儿页 = 存在于文件但没有任何入链的 wiki 页面（index.md / log.md / .wiki-schema.md 除外）。
  - 枢纽页 = 入链数最高的页面。
  - 这些是 Obsidian 双链图谱的结构化导出；Obsidian 本身直接读 [[链接]] 即可可视化。
"""
import argparse
import os
import re
import csv
import json
import datetime

WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")
SKIP_DIRS = {".obsidian", ".wiki-tmp", ".git", "node_modules"}
SKIP_FILES = {"index.md", "log.md", ".wiki-schema.md"}


def strip_fences(text):
    """移除围栏代码块，避免把示例代码里的 [[示例]] 误算成图边。"""
    return re.sub(r"```.*?```", "", text, flags=re.S)


def collect_md(vault):
    out = []
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if fn.lower().endswith(".md"):
                out.append(os.path.join(root, fn))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    ap.add_argument("--out", default=None, help="输出目录（默认 <vault>/graph）")
    ap.add_argument("--json", action="store_true", help="同时输出 graph.json")
    args = ap.parse_args()

    vault = os.path.abspath(args.vault)
    out_dir = args.out or os.path.join(vault, "graph")
    os.makedirs(out_dir, exist_ok=True)

    files = collect_md(vault)
    # 文件节点名 -> 相对路径
    file_nodes = {}
    for fp in files:
        if os.path.basename(fp) == ".wiki-schema.md":
            continue  # 配置文件，非知识库内容，跳过其模板示例链接
        name = os.path.splitext(os.path.basename(fp))[0]
        file_nodes.setdefault(name, os.path.relpath(fp, vault))

    edges = []          # (source_name, target_name)
    link_targets = set()
    for fp in files:
        if os.path.basename(fp) == ".wiki-schema.md":
            continue
        src = os.path.splitext(os.path.basename(fp))[0]
        with open(fp, "r", encoding="utf-8", errors="replace") as f:
            text = strip_fences(f.read())
        for m in WIKILINK.finditer(text):
            tgt = m.group(1).strip()
            link_targets.add(tgt)
            edges.append((src, tgt))

    all_nodes = set(file_nodes.keys()) | link_targets
    in_deg = {n: 0 for n in all_nodes}
    out_deg = {n: 0 for n in all_nodes}
    for s, t in edges:
        out_deg[s] = out_deg.get(s, 0) + 1
        in_deg[t] = in_deg.get(t, 0) + 1

    # 节点类型
    def ntype(n):
        if n in file_nodes:
            return "page"
        return "link_target_only"  # 被链接但无对应文件（悬空链接）

    # 孤儿页（有文件但无入链，排除索引/日志/schema）
    orphans = sorted(
        n for n in file_nodes
        if in_deg.get(n, 0) == 0 and n not in SKIP_FILES
    )
    hubs = sorted(
        ((n, in_deg[n]) for n in file_nodes if n not in SKIP_FILES),
        key=lambda x: x[1], reverse=True
    )[:10]

    # 写 CSV
    nodes_csv = os.path.join(out_dir, "graph-nodes.csv")
    with open(nodes_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "type", "in_degree", "out_degree", "file"])
        for n in sorted(all_nodes, key=lambda x: (-in_deg.get(x, 0), x)):
            w.writerow([n, ntype(n), in_deg.get(n, 0), out_deg.get(n, 0),
                        file_nodes.get(n, "")])

    edges_csv = os.path.join(out_dir, "graph-edges.csv")
    with open(edges_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source", "target"])
        for s, t in edges:
            w.writerow([s, t])

    if args.json:
        j = {
            "generated": datetime.datetime.now().isoformat(timespec="seconds"),
            "vault": vault,
            "node_count": len(all_nodes),
            "edge_count": len(edges),
            "nodes": [
                {"name": n, "type": ntype(n), "in_degree": in_deg.get(n, 0),
                 "out_degree": out_deg.get(n, 0), "file": file_nodes.get(n, "")}
                for n in sorted(all_nodes)
            ],
            "edges": [{"source": s, "target": t} for s, t in edges],
            "orphans": orphans,
            "hubs": [{"name": n, "in_degree": d} for n, d in hubs],
        }
        with open(os.path.join(out_dir, "graph.json"), "w", encoding="utf-8") as f:
            json.dump(j, f, ensure_ascii=False, indent=2)

    print("vault:", vault)
    print("nodes:", len(all_nodes), "| edges:", len(edges))
    print("orphans:", len(orphans), orphans[:10])
    print("top hubs:", [f"{n}({d})" for n, d in hubs])
    print("wrote:", nodes_csv)
    print("wrote:", edges_csv)
    if args.json:
        print("wrote:", os.path.join(out_dir, "graph.json"))


if __name__ == "__main__":
    main()
