# Clean Code Patterns

具体技术、设计模式、重构手法。每条含 When to use / How / Trade-offs。

## Adapter
**When to use**: 真实 API 尚未定义，或第三方接口与领域模型不匹配时。
**How**: 先定义自己想要的接口；真实 API 就绪后写 Adapter 实现桥接，把所有交互封进一处。
**Trade-offs**: 多一层间接，但换来单一变更点与可测试的 seam；迁移成本降到一处。

## Learning Tests
**When to use**: 集成不熟悉的第三方库、需确认其行为符合预期时。
**How**: 像生产代码那样调用 API，把理解编码成受控实验；每次升级重跑，立刻暴露破坏性变更。
**Trade-offs**: 前期额外写测试，但免费获得回归保护；升级踩坑风险大幅下降。

## Special Case Pattern
**When to use**: "无结果/异常"其实代表正常的默认值（如无餐费按 per diem）。
**How**: 创建一个代表特殊情形的对象（如 `PerDiemMealExpenses`），`getTotal()` 返回默认值；client 免分支。
**Trade-offs**: 多一个类，但消除调用方 if/else 与 null 检查，逻辑更干净。

## Wrapper / Wrap Third-Party API
**When to use**: 集成任何外部/第三方 API 时（Ch 7, Ch 8）。
**How**: 捕获其各类异常并翻译为单一自有异常（如 `PortDeviceFailure`）；隔离供应商 API 便于 mock 与换库。
**Trade-offs**: 隔离依赖、调用方只认一个 catch；代价是多一层包装类。

## Abstract Factory / Dependency Injection
**When to use**: 客户端依赖易变的具体实现（如外部 API、待定类型）时。
**How**: 抽出接口，构造函数注入接口引用；`main` 侧工厂选择具体实现，调用方只依赖抽象 (DIP)。
**Trade-offs**: 解耦且易测；比直接 new 多接口与装配代码，但有 DI 容器可兜底。

## Template Method / Strategy (替代 switch 重复)
**When to use**: 多个方法共享同一流程、仅少数步骤不同（如分区域规则）。
**How**: 基类固定算法骨架，变体步骤 abstract 留给子类；或把变体提为 Strategy 对象注入。
**Trade-offs**: 消除复制粘贴；模板法靠继承（结构重），Strategy 靠组合（更灵活但类更多）。

## Command-Query Separation
**When to use**: 一个函数既改状态又返回状态/状态码时。
**How**: 拆成 query（`exists(username)`）+ command（`setAttribute(...)`），二选一。
**Trade-offs**: 调用方不再含糊（避免 `if (set(...))`）；需两次调用，但语义清晰。

## POLYMORPHISM over switch (G23)
**When to use**: 同一 switch/if-else 选择在多处重复出现时。
**How**: 遵守 ONE SWITCH rule——全系统至多一个 switch，其 case 产出多态对象；其余分发靠多态。
**Trade-offs**: 消除重复的 type-case（DRY）；需建类层次与工厂，初建成本略高但可扩展。

## enum over int constants (J3)
**When to use**: 一组相关常量（月/星期/季度）原本用 `public static final int` 表示时。
**How**: 改 `enum`，加 `index` 字段与 `make/fromInt` 工厂；把校验逻辑内联进 enum 方法（如 `quarter()`）。
**Trade-offs**: 编译期安全、可携方法、IDE 改名无忧；比 int 略多代码，但彻底消除魔法数。

## Explanatory Variables (G19)
**When to use**: 一行表达式里塞了多个计算、可读性差时。
**How**: 拆成带含义的中间变量（如 `offsetToFutureTarget`），几乎不会过度 (Kent Beck)。
**Trade-offs**: 多几行，但意图显式、更易测与调试；几乎零副作用。

## Encapsulate Conditionals (G28)
**When to use**: `if (timer.hasExpired() && !timer.isRecurrent())` 这类裸条件难读时。
**How**: 抽成 `shouldBeDeleted(timer)` 之类意图命名方法。
**Trade-offs**: 多一个方法，但调用点读如散文，且条件可复用。

## Extract Method (to Explain Intent)
**When to use**: 裸条件/裸逻辑块读起来像"在干什么"而非"为什么"时。
**How**: 把块抽成有名字的函数；顺手反转负向条件为正向（如 `canBeCompacted()` 替代 `!shouldNotCompact()`）。
**Trade-offs**: 函数变多但更小；提升表达力，是 successive refinement 的主力手法。

## Collecting Parameter
**When to use**: 多步骤需要累计同一结果（如遍历拼装、多步设置）时。
**How**: 传一个累积对象（或 `Iterator`）给各步骤，避免散落多个返回/输出参数。
**Trade-offs**: 显式化状态流动；比返回值拼装略啰嗦，但顺序与归属清晰。

## Try-Catch-Finally First
**When to use**: 写可能抛异常的新代码时。
**How**: 先写 try 界定事务作用域（保证一致状态）；在 try 内用 TDD 填充主逻辑，把 catch 体抽成独立函数。
**Trade-offs**: 错误处理与 happy path 分离、各自可独立理解；需先把异常设计想清楚。
