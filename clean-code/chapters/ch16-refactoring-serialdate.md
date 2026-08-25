# Chapter 16: Refactoring SerialDate

## Core Idea
作者以重构 David Gilbert 的 JCommon `SerialDate` 类为实战案例，演示"先让它工作、再让它正确"的完整纪律：用覆盖率工具驱动、消除重复与坏味道、把 int 常量提升为 enum、把静态方法改为实例方法、用工厂隔离抽象与实现。

## Frameworks Introduced
- **Month enum (enum over int constants)**: 用 `enum Month { JANUARY(1)... }` 替代 `MonthConstants` 接口里的 `static final int`。
  - When to use: 任何一组相关常量（月份、星期、季度、区间类型）原本用 int 表示时。
  - How: 为 enum 加 `index` 字段与 `make(int)`/`fromInt(int)` 工厂；把 `isValidMonthCode`、`monthCodeToQuarter` 这类校验逻辑直接内联进 enum 的方法（`quarter()`），删除散落的 int 校验。
- **DayDateFactory (ABSTRACT FACTORY + SINGLETON + DECORATOR)**: 用工厂默认持有 `SpreadsheetDateFactory`，对外暴露 `makeDate(...)` 与 `getMinimumYear()/getMaximumYear()`。
  - When to use: 基类需要知道实现细节（如最小/最大年份）但又不能依赖派生类时。
  - How: `setInstance(DayDateFactory)` 可替换实现；静态方法委托给内部的抽象 `_makeDate` 方法。
- **DateInterval enum (polymorphism over switch)**: 把 `isInRange` 里的 switch 搬进 `OPEN/CLOSED_LEFT/CLOSED_RIGHT/CLOSED` 各自的 `isIn(int d,int left,int right)`。
  - When to use: 同一个选择逻辑在多处用 switch/if-else 重复时（G23）。
- **EXPLAINING TEMPORARY VARIABLES**: 把复杂算法拆成带含义的中间变量（如 `offsetToFutureTarget`、`lastDayOfResultMonth`）。
  - When to use: 一行表达式里塞了多个计算、可读性差时。
- **DateUtil (responsibility relocation)**: 把 `dateFormatSymbols`、`getMonthNames`、`isLeapYear`、`lastDayOfMonth` 等无状态工具迁到独立类。

## Key Concepts
- **Boy Scout Rule**: 离开代码时比接手时更干净——覆盖率提升、修 bug、精简、重命名。
- **Feature Envy**: 方法大量通过别的对象的 accessor 操作其数据，说明该方法应搬进那个对象（如 `monthCodeToQuarter` 属于 `Month`）。
- **serial number vs ordinal**: 作者认为 "serial number" 命名不准，应叫 "ordinal"（自 1899-12-30 起的天数偏移）。
- **coverage-driven refactoring**: 用 Clover 发现只覆盖 ~50% 语句，先补到 92% 再动手重构。
- **selector argument**: 用布尔/标志参数在一个函数里选择多种行为（如 `weekInMonthToString` 的 flag），应拆成独立函数。

## Mental Models
- Use **enum** when a set of related constants is passed around as `int`—readers can't tell what `2` means, and the compiler can't help you.
- Make a method **instance (non-static)** when it operates on `this`'s data and you might later want polymorphism (e.g. `addDays` → `plusDays`).
- Prefer **nonstatic** over static unless you are certain the function will never need to be polymorphic (G18).
- Push implementation-specific constants/variables **down** into the derivative (e.g. `EARLIEST_DATE_ORDINAL` → `SpreadsheetDate`) so the base class stays at the right abstraction level.

## Anti-patterns
- **Inherit constants (`MonthConstants`)**: 让 `DayDate` 继承一个只有 `static final` 的接口只为少写前缀——应该用 enum 或 `static import`。
- **Change history in source comments [C1]**: 1960 年代的做法；版本控制工具已替我们记录，留着只是堆积无关文字。
- **Ambiguous method names like `addDays`**: 读者分不清是改原对象还是返回新对象；应改名 `plusDays` 让"返回新实例"的意图显式化。
- **Dead code / unused tables**: `AGGREGATE_DAYS_TO_END_OF_MONTH`、`description` 字段、`isValidMonthCode` 等从未被使用，只增加噪音。
- **Magic numbers `1`**: 用 `Month.JANUARY.toInt()`、`Day.SUNDAY.toInt()` 取代裸 `1`。

## Code Examples
```java
public static enum Month {
  JANUARY(1), FEBRUARY(2), /* ... */ DECEMBER(12);
  Month(int index) { this.index = index; }
  public final int index;
  public int quarter() { return 1 + (index-1)/3; }
  public static Month make(int monthIndex) {
    for (Month m : Month.values())
      if (m.index == monthIndex) return m;
    throw new IllegalArgumentException("Invalid month index " + monthIndex);
  }
}

public abstract class DayDateFactory {
  private static DayDateFactory factory = new SpreadsheetDateFactory();
  public static DayDate makeDate(int day, DayDate.Month month, int year) {
    return factory._makeDate(day, month, year);
  }
  protected abstract DayDate _makeDate(int day, DayDate.Month month, int year);
}

public DayDate plusDays(int days) {
  return DayDateFactory.makeDate(toOrdinal() + days);
}

public DayDate getNearestDayOfWeek(final Day targetDay) {
  int offsetToThisWeeksTarget = targetDay.index - getDayOfWeek().index;
  int offsetToFutureTarget = (offsetToThisWeeksTarget + 7) % 7;
  int offsetToPreviousTarget = offsetToFutureTarget - 7;
  if (offsetToFutureTarget > 3)
    return plusDays(offsetToPreviousTarget);
  else
    return plusDays(offsetToFutureTarget);
}
```
- **What it demonstrates**: enum 把校验/行为内聚；工厂用 ABSTRACT FACTORY 隔离"创建哪种实现"；`plusDays` 用命名消除"是否修改原对象"的歧义；EXPLAINING TEMPORARY VARIABLES 让边界算法清晰。

## Worked Example
复现作者把 `SerialDate` 重构为 `DayDate` 的关键步骤（忠实紧凑）：
1. **First, Make It Work** — Clover 显示 185 条可执行语句只覆盖 ~50%。作者写独立测试套件，覆盖升到 92%。测试暴露真实 bug：`getFollowingDayOfWeek` 在跨年边界（2004-12-25 的下一个 Saturday 应是 2005-01-01）返回错误；`getNearestDayOfWeek` 当目标在未来时算法错误；`weekInMonthToString`/`relativeToString` 应抛 `IllegalArgumentException` 而非返回错误串。
2. **Then Make It Right（自顶向下）** — 删 change-history 注释（C1）；`MonthConstants` 改 `Month` enum，顺带删除 `isValidMonthCode` 与 `monthCodeToQuarter` 中的 int 校验；`EARLIEST_DATE_ORDINAL`/`LATEST_DATE_ORDINAL` 与 `MINIMUM_YEAR_SUPPORTED` 下移到 `SpreadsheetDate`；用 `DayDateFactory` 解决"基类依赖派生类"问题（G7）。
3. **Feature Envy 消除** — `monthCodeToQuarter` → `Month.quarter()`；`stringToMonthCode`/`monthCodeToString` 搬进 `Month` enum；`stringToWeekdayCode`/`weekdayCodeToString` 搬进 `Day` enum（并独立成文件，G13）。
4. **静态 → 实例** — `addDays`/`addMonths`/`getPreviousDayOfWeek` 等改为实例方法；`toSerial`→`toOrdinal`→`getOrdinalDay`；为消除"是否修改原对象"歧义，改名 `plusDays`/`plusMonths`/`plusYears`。
5. **抽象方法上提** — `toDate`、`getDayOfWeek`、`compare`(改名 `daysSince`)、`isInRange` 等从 `SpreadsheetDate` 上提到 `DayDate`；`getDayOfWeek` 的逻辑依赖（ordinal 0 的星期）被物理化为 `getDayOfWeekForOrdinalZero()`，由 `SpreadsheetDate` 返回 `Day.SATURDAY`（G22）。
6. **收尾** — `isInRange` 的 switch 移入 `DateInterval` enum；`plusYears`/`plusMonths` 重复逻辑抽成 `correctLastDayOfMonth`；魔法数字 `1` 替换；覆盖率降到 84.9% 只是因为类缩小了，绝对覆盖行数更稳定。

## Key Takeaways
1. 重构前先用覆盖率工具量化"没测到的地方"，独立测试套件是安全网（T2）。
2. 用 **enum** 替代 int 常量：编译期安全、可携方法、IDE 改名无忧。
3. 基类不应知道派生类（G7）；需要实现信息时通过 ABSTRACT FACTORY 询问实例。
4. 方法名要消除歧义——`addDays` 让人误以为改原对象，改成 `plusDays` 显式表达"返回新实例"。
5. 把逻辑依赖物理化（G22），把重复代码抽成方法（G5/DRY），把死代码与废弃注释一并删除（C1/C5/G9）。

## Connects To
- **Ch 17**: 本章每个改动都是 Ch17 某条 smell/heuristic 的实例（G5 Duplication、G7、G13、G14 Feature Envy、G18、G22、G25 等）。
- **Ch 1 (Clean Code)**: Boy Scout Rule 是哪个章节精神的落地。
- **Refactoring (Fowler)**: Feature Envy、EXPLAINING TEMPORARY VARIABLES 源自 Fowler/Beck 的重构手法。
