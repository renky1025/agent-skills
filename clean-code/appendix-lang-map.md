# Clean Code — 跨语言映射附录 (Language-Agnostic Map)

本附录让 `clean-code` 技能适配**任何编程语言**，而不被 Java 语境绑死。

## 0. 总原则

- 本书的**命名 / 函数 / 注释 / 格式化 / 对象与数据结构 / SRP / 测试 / 代码味道**原则，都是语言无关的工程真理。
- 各章节里的 **Java 代码只是示例载体**，用来说明通用原则。换语言，原则不变，只是语法不同——不要因为看到 Java 语法就觉得"这条不适用"。
- 本附录做两件事：(1) 标明哪些启发式是 **Java 专属、需转译**；(2) 给出 **TypeScript / Python / C++ / Go / Rust** 的对应写法（可继续扩展）。

## 1. 启发式分类：通用 vs Java 专属

| 类别 | 适用范围 | 说明 |
|---|---|---|
| C / E / F / G / N / T 系列 | **通用** | Comments、Environment、Functions、General、Names、Tests 全部直接适用 |
| SRP / CQS / Law of Demeter / Four Rules of Simple Design / TDD 三律 / F.I.R.S.T. / Boy Scout Rule | **通用** | 与语言无关的设计与纪律 |
| **J 系列** (J1–J3) | **Java 专属** | 通配导入 / 别继承常量 / enum 替 int 常量——需按 §3 转译 |
| 异常处理 (checked/unchecked) | **半通用** | 概念通用，"不用返回码"铁律不变；Java 的 checked 仅 Java 有 |
| 并发原语 (synchronized/Executor) | **半通用** | 概念通用；具体原语按语言不同（见 §4） |
| null 处理 | **半通用** | "别返回/传 null"通用；各语言实现机制不同（见 §5） |

## 2. 错误处理（对应 ch07 转译）

**通用原则**：用语言**惯用**的错误表达机制，绝不用"返回错误码 / 特殊哨兵值"把错误检查缠进主逻辑。Try-Catch-Finally（或等价的事务作用域）、Wrap 第三方 API、Special Case 对象、Don't return null——这些抽象在所有语言都成立。

| 语言 | 惯用做法 |
|---|---|
| **Java** | 优先 **unchecked** 异常（避免 OCP 级联改签名）；wrap 第三方为多类→单一自有异常 |
| **C#** | 异常惯用，无 checked；用 `try/catch/finally` + `using`(RAII) |
| **C++** | 异常惯用 + `noexcept` 纪律 + RAII；**不要**退回错误码返回 |
| **Python** | 异常惯用（`raise/try`），无 checked；**不要**返回 `None` 当错误哨兵 |
| **JS/TS** | `throw/try` 惯用；可引入 `Result` 类型把错误显式化，避免 `null/undefined` 哨兵 |
| **Go** | `error` 是返回值（惯用），但别让它退化成"返回码面条"——在边界 wrap/处理；**不要**用 `panic` 当控制流 |
| **Rust** | `Result<T,E>` 就是"既不用异常也不用返回码"的答案；`Option<T>` 直接实现 "Don't return null" |

**映射**：Special Case Pattern → 各语言的 `Option`/`Maybe`/零值+`ok`/null 对象；"Don't return null" → **Rust 天然满足（无 null）**。

## 3. 常量与枚举（J3 转译）：用类型安全的枚举 / 代数类型替魔法 int

**通用原则**（J3 的本质）：不要用裸整数常量表达离散取值集合；用语言提供的类型安全枚举，编译期即可捕获非法值。

| 语言 | 写法 |
|---|---|
| **TS** | `type Color = 'red' \| 'green' \| 'blue'` + `as const` 对象 |
| **Python** | `enum.Enum` / `enum.StrEnum` |
| **C++** | `enum class` / `std::variant` |
| **Go** | `iota` + 自定义类型 / 字符串常量 |
| **Rust** | `enum`（一等公民，可携带数据） |

- **J2 "别继承常量"** → 通用：不要把常量耦合进继承体系；用模块 / 命名空间 / 静态导入承载。
- **J1 "通配导入"** → 通用：最小化导入面；非 Java 用模块 / 命名空间导入，避免隐式耦合。

## 4. 并发（对应 ch13 转译）：通用原则不变

**通用原则**（全部语言成立）：SRP + 并发（把线程相关代码隔离进独立类）、限制共享数据的**作用域**、用**副本 / 隔离**替代加锁、让线程各自活在独立世界（local 变量）、三大经典模型（Producer-Consumer / Readers-Writers / Dining Philosophers）、用 **jiggling** 逼出罕见排序 bug、绝不忽略偶发失败。

**各语言原语对照**（仅替换 `synchronized`/`Executor` 等 Java 字眼）：

| 语言 | 并发原语 |
|---|---|
| **Java** | `synchronized` / `ReentrantLock` / `ConcurrentHashMap` / `Executor` / `java.util.concurrent` |
| **C++** | `std::thread` / `std::mutex` / `std::atomic` / `std::condition_variable` / `std::async` |
| **Python** | GIL 限制真并行；`threading.Lock` / `queue.Queue` / `asyncio`（协程） |
| **JS/TS** | 单线程事件循环；`Worker` / `Promise` / `async-await`；共享用 `SharedArrayBuffer`+`Atomics` 或消息传递 |
| **Go** | goroutine + channel（CSP 模型）；`sync.Mutex`；优先通信而非共享内存 |
| **Rust** | `async/await`（tokio）；`std::sync::Mutex`；`mpsc` channel；**所有权天然防数据竞争** |

**铁律**：无论哪种语言，"限制共享可变状态"这一条不可妥协；能隔离 / 用副本就别加锁。

## 5. Null 处理（对应 ch07 转译）

- **通用**："Don't return null / Don't pass null" 在所有语言都成立——null 是 Open Invitation to 崩溃。
- **Java**：`Optional<T>`；**C#**：nullable 注解；**Python/TS**：显式 `Option` 类型 + 穷尽检查；**Go**：零值 + `ok` 或显式返回；**Rust**：`Option<T>`（无 null，天然满足）。

## 6. 如何调用

直接问：
- "clean-code 在 **Rust** 里怎么处理错误？" → 读 §2 + ch07 给转译
- "**Go** 里怎么避免 null / 表示枚举？" → 读 §3/§5 + ch02/ch07
- "**Python/JS** 里怎么应用并发章节？" → 读 §4 + ch13

技能会结合本章节与对应 ch 给出**针对你语言**的建议，而不是复述 Java 代码。
