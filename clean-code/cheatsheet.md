# Clean Code Cheat Sheet — 决策辅助

压在手边的一页纸。每行帮你做决定：if X → do Y, because Z。

## 命名决策
- 名字需注释才懂 → 改名（reveal intent），不要加注释。
- 名字不同但含义同（`a1/a2`、`ProductInfo/Data`）→ 拒绝；差异本身须可理解。
- 作用域越大 → 名字越长；短方法局部变量才用单字母（`i/j/k`，绝不用 `l/O`）。
- 不是 `List` 就别叫 `xxxList`；避免误导假线索。
- 一词一义（fetch/retrieve/get 选一个），别 pun（集合插入用 `insert`/`append`）。
- 方法返回新实例而非改 `this` → 叫 `plusDays` 而非 `addDays`（G20）。
- 名字掩盖副作用 → 改名显式化（`getOos()`→`createOrReturnOos`）（N7）。

## 函数设计决策
- 参数个数：`niladic > monadic > dyadic`；**>3 需特别理由**（F1）。
- 函数尽量 < 20 行；块内语句抽成一行的命名函数；缩进 ≤ 1–2 层。
- 能抽出非"复述实现"的名字 → 原函数在做多件事，拆。
- 传 boolean 选行为（flag argument）→ 拆成两个函数（F3）。
- 输出参数（appendFooter(s)）→ 改为 `report.appendFooter()`（F2）。
- 既改状态又返回状态 → 拆 command/query，遵守 CQS。
- switch 躲不掉 → 只放一次，藏进 Abstract Factory 产出多态对象（ONE SWITCH）。

## 注释决策
- 想注释解释烂代码 → 先重构，别注释（注释是表达失败）。
- 可保留：legal、意图解释、后果警告、TODO（定期清）、public API Javadoc。
- 删除：冗余/误导性/署名/变更史/注释掉的代码（C1–C5）。

## 错误处理决策
- 能失败 → 抛异常，不用返回码（解耦 happy path）。
- 新错误代码 → 先写 try-catch-finally 界定事务作用域。
- 第三方 API → 包装，多类异常收敛为单一自有类型。
- "无结果"是合法默认 → 用 Special Case 对象，不抛、不分支。
- **绝不返回 null**（用 `emptyList()`/特殊对象）；**绝不传 null**（视为 bug 信号）。
- 用语言惯用错误机制，不用返回码（见 [appendix-lang-map.md §2](appendix-lang-map.md)：Java 用 unchecked 异常、C# 用 Exception、Python 抛异常、Go/Rust 用 error/Result 值返回；checked 异常违反 OCP 会级联改签名）。

## 测试决策（F.I.R.S.T.）
- 测试代码 = 生产代码整洁度；脏测试比没测试更糟。
- 慢/互相依赖/需人工判定 → 套件会被弃用。
- 每测试单概念（断言数可多，概念只一个）；用领域测试语言。
- TDD 三律：先失败测试 → 最小测试 → 最小通过代码。
- 重构前先有覆盖工具量化空白（T2）；边界、邻近 bug 必测（T5/T6）。

## 类 / 职责决策
- 能用 25 词、无 if/and/or/but 描述类吗？不能 → 拆（SRP）。
- 命名含 Manager/Processor/Super → 职责过多告警。
- 方法与变量共依赖 → 内聚下降即拆类。
- 客户端依赖易变具体类 → DIP：抽接口 + 构造函数注入。
- 要加类型 → objects（多态）；要加函数且类型稳 → data structures。
- 对象间"告诉它去做"（Demeter）；对纯数据结构才允许 `a.b().c()` 导航。

## 并发决策
- 并发是解耦 what/when 的策略；把线程相关代码从 POJO 中隔离（SRP）。
- 能用副本/独立线程就不用共享；必须共享 → 用语言原生独占锁（`synchronized`/mutex/lock）圈出最小临界区。
- 别信"并发必更快"；只在有可共享等待时才提速。
- 用语言并发原语（Java `ConcurrentHashMap`/`Executor`、C++ `std::mutex`/`std::thread`、Go goroutine+channel、Rust `async`+Mutex+channel，见 [appendix-lang-map.md §4](appendix-lang-map.md)）；用 jiggling 逼出罕见排序 bug，绝不忽略偶发失败。

## 味道速查（C/E/F/G/J/N/T）
- **C**: C1 变更史 / C3 冗余注释 / C5 注释掉的代码 → 删。
- **E**: E1 构建多步 / E2 测试多步 → 一条命令完成。
- **F**: F1 参数>3 / F3 flag 参数 / F4 死函数 → 拆或删。
- **G**: G5 重复(DRY) / G9 死代码 / G14 Feature Envy / G23 重复 switch→多态 / G25 魔法数 / G28 条件未封装 / G36 传递导航。
- **J**: J2 别继承常量（通用：常量归属拥有者，勿横向混入接口）/ J3 用 enum 不用 int 常量（通用：用类型安全的枚举/代数类型代替裸数值，见 [appendix-lang-map.md §3](appendix-lang-map.md)）。
- **N**: N1 描述性名 / N6 去类型编码 / N7 名字表副作用。
- **T**: T2 覆盖率工具 / T5 边界测试 / T9 测试要快。

> 用法：读/写代码时逐条问"这里有没有 Gxx/Nx/Tx 的味道"，有就改。
