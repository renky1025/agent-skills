# Chapter 7: Error Handling

## Core Idea
错误处理很重要，但若它遮蔽了逻辑就是错的。把错误当作独立关注点（separate concern）看待，使其可脱离主逻辑单独推理——健壮与可读并不冲突。本章由 Michael Feathers 撰写。

## Frameworks Introduced
- **Use Exceptions, Not Return Codes**: 出错时抛异常而非返回错误码/标志，让调用方逻辑不被错误检查弄乱。
  - When to use: 方法能检测到错误时。
  - How: 抛自定义异常（如 `DeviceShutDownError`），调用方用 try-catch 包住，算法与错误处理解耦。
- **Write Try-Catch-Finally First**: try 块像事务——无论 try 内发生什么，catch 必须把程序留在一致状态；先写 try-catch-finally 界定作用域。
  - When to use: 写可能抛异常的新代码时。
  - How: 先写一个"文件不存在就抛异常"的测试 → 实现 stub 抛异常 → 用 TDD 在 try 内逐步填充主逻辑，逻辑可假装一切正常。
- **Use the Language's Idiomatic Error Mechanism (not return codes)**: 通用规则——用语言惯用的错误表达（异常，或 Rust 的 `Result`、Go 的 `error` 返回）替代返回错误码 / 哨兵值；让调用方逻辑不被错误检查淹没。*Java 专属细节*：在 Java 中这表现为"优先 unchecked 异常"，原因是有 checked 异常会违反 Open/Closed Principle——低层抛 checked 异常会级联迫使所有中间方法改签名、重建重部署。跨语言转译见 [appendix-lang-map.md](appendix-lang-map.md) §2。
  - When to use: 方法能检测到错误时（所有语言）。
  - How: 抛自定义异常（Java/Python/C#）、或用 `Result`/`error` 返回（Rust/Go）；调用方用 try-catch（或 `match`/`if err != nil`）包住，算法与错误处理解耦；仅在编写关键库且"调用方必须捕获"时才考虑 checked（Java）。
- **Wrap Third-Party APIs**: 包装第三方库，捕获其各类异常并翻译为单一自有异常类型，最小化依赖、便于 mock 与换库。
  - When to use: 集成任何外部/第三方 API 时。
  - How: `LocalPort` 包 `ACMEPort`，把 `DeviceResponseException`/`ATM1212UnlockedException`/`GMXError` 都转成 `PortDeviceFailure`。
- **Special Case Pattern**: 创建一个处理特殊情形的对象，让 client 代码不必分支处理异常行为。
  - When to use: 异常其实代表"正常的默认值"时（如没有餐费就按 per diem）。
  - How: `ExpenseReportDAO.getMeals()` 总返回 `MealExpenses`，无餐费时返回 `PerDiemMealExpenses`（getTotal 返回 per diem 默认）。
- **Don't Return Null / Don't Pass Null**: 用抛异常或返回 special case 对象替代返回 null；默认禁止向方法传 null。
  - When to use: 方法可能"无结果"或调用方可能传 null 时。
  - How: 返回 `Collections.emptyList()` 而非 null；对第三方 null-returning 方法加包装；把 null 参视为 bug 信号。

## Key Concepts
- **Return Codes**: 古老语言无异常时用的错误标志/错误码，会弄脏调用方且易被遗忘检查。
- **Transaction Scope of try**: try 块界定一个可中止、在 catch 中恢复一致性的作用域。
- **Open/Closed violation of checked exceptions**: 低层 checked 异常导致高层签名连锁改动，破坏封装。
- **Exception Context**: 抛出的每个异常都应带足够上下文（失败操作 + 失败类型）以定位来源。
- **Exception Class by Caller's Needs**: 异常类应按"如何被捕获"来定义，而非按来源/类型分类；同一区域常一个类足矣，仅在需分别捕获时才分多类。
- **Train wreck of catch blocks**: 对第三方库逐类 catch 且每支都做相同 record+log，属重复应消除。

## Mental Models
- Use **exceptions, not return codes** when a method detects an error — keep the caller's logic unobscured by error checks.
- Use **try-catch-finally first** when starting error-prone code — define the transaction scope before filling in the happy path.
- Use the **language's idiomatic error mechanism** (exceptions, or `Result`/`error` returns) instead of return codes — in Java that means unchecked exceptions to avoid the Open/Closed-violating cascade of checked signatures.
- Use **Special Case object** when "no result" is really a valid default — let the client skip the if/else branch entirely.

## Anti-patterns
- **Returning null**: 制造大量 null 检查，少一处即 NullPointer；应抛异常或返回 special case 对象。
- **Passing null**: 比返回 null 更糟；多数语言无法优雅处理调用方误传的 null，应默认禁止。
- **Cascading checked exceptions (Java) / error-handling that forces signature cascades**: 低层加 checked 异常 → 中间每层改签名 → 全链路重建重部署，破坏封装；其他语言表现为"错误处理迫使大量函数改签名"或返回码面条，同样要隔离在边界。
- **Per-exception-type catch duplication**: 对第三方库每类异常写相同 record+log，应包装成单一异常类型消除重复。

## Code Examples
```java
// Wrap third-party API, translate to one exception type
public class LocalPort {
  private ACMEPort innerPort;
  public LocalPort(int portNumber) { innerPort = new ACMEPort(portNumber); }
  public void open() {
    try {
      innerPort.open();
    } catch (DeviceResponseException e) { throw new PortDeviceFailure(e); }
    catch (ATM1212UnlockedException e) { throw new PortDeviceFailure(e); }
    catch (GMXError e) { throw new PortDeviceFailure(e); }
  }
}
```
- **What it demonstrates**: 把混乱的多类型 catch 收敛为单一 `PortDeviceFailure`，调用方只需一个 catch，且隔离了供应商 API。

## Worked Example
作者以 `DeviceController.sendShutDown()` 为例：Listing 7-1 用 `handle != INVALID` 和 `record.getStatus() != SUSPENDED` 的返回码/标志，错误检查与关机算法缠绕。重构为 Listing 7-2 后，`sendShutDown` 只包一个 try-catch 调 `tryToShutDown()`，算法与错误处理被分开、各自可独立理解。`tryToShutDown` 调 `getHandle` 失败即抛 `DeviceShutDownError`，调用方干净。另一个例子：`getMeals` 在无餐费时抛 `MealExpensesNotFound`，逼出 `try/catch` 加 per diem 的丑陋分支；改用 `PerDiemMealExpenses` special case 后，client 只需 `m_total += expenses.getTotal()`。

## Key Takeaways
1. 用异常替代返回码，让主逻辑不被错误检查淹没。
2. 先写 try-catch-finally 界定事务作用域，再用 TDD 填充正常逻辑。
3. 用异常 / `Result` 等语言惯用机制替代返回码（Java 中优先 unchecked 异常）；用 wrapper 把第三方 API 异常收敛为自有单一类型。
4. 绝不返回 null（用异常/special case/emptyList 替代），绝不向方法传 null。

## Connects To
- **Ch 3 (Functions)**: 错误处理让函数主逻辑更干净、单一职责。
- **Ch 6 (Objects and Data Structures)**: wrapper 类与 special case 对象都是"对象隐藏数据"的实践。
- **Special Case Pattern [Fowler]**: 直接引用 Refactoring。
- **Open/Closed Principle [Martin]**: checked 异常代价正是违反 OCP。
