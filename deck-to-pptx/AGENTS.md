# deck-to-pptx

本 skill 负责把主题、说明或本地资料压成结构清晰、观感优先的 `.pptx`。

## 目录结构

```text
deck-to-pptx/
├── AGENTS.md
├── SKILL.md
├── deck_to_pptx.py
└── deck_to_pptx_lib/
    ├── cli.py
    ├── config.py
    ├── models.py
    ├── intake/
    ├── planner/
    ├── renderer/
    └── utils/
```

## 职责边界

- `intake/`: 识别输入类型，做本地资料读取与轻量联网补料。
- `planner/`: 把资料变成 scenes，再变成 deck spec，并执行轻量 QA。
- `renderer/`: 只消费 deck spec，不直接解析原始资料。
- `utils/`: 文本和文件辅助逻辑，不放业务决策。

## 设计原则

- 叙事顺序优先于“图片多就排前面”。
- 单页主张必须清晰，不能靠缩小字号塞文案。
- `deck spec` 是系统中心；未来加 HTML renderer 时，优先复用它，不重写 planner。
