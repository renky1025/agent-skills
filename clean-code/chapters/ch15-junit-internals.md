# Chapter 15: JUnit Internals

## Core Idea
JUnit 内部的 `ComparisonCompactor` 是一个"已经很干净"的模块；本章用 Boy Scout Rule 把它打磨得更干净，展示 successive refinement 在他人代码上的实战——抽取方法、重命名、反转负向条件、暴露时间耦合、消除死代码，最终把模块分成"分析函数"与"合成函数"两组。

## Frameworks Introduced
- **Boy Scout Rule（童子军规则）**: 离开一个模块时，让它比你来时更干净。即使原作者（Kent Beck & Erich Gamma）已写得很好，仍有改进空间 ([G23] 相关)。
  - When to use: 触碰任何既有模块、修 bug、加测试时。
  - How: 不做大改写，只做一系列小改进；每次改进单独提交并保持测试绿。
- **Extract Method to Explain Intent（抽取方法以表意）**: 把一个"裸条件/裸逻辑块"抽成有名字的方法，让调用处读起来像散文。
  - When to use: `if (expected == null || actual == null || areStringsEqual())` 这类无封装条件 ([G28])。
  - How: 抽成 `shouldNotCompact()` / `canBeCompacted()`，名字直接表达意图。
- **Invert Negative Condition（反转负向条件）**: 负向判断比正向难懂，把 `if (!shouldNotBeCompacted())` 翻转为正向语义 ([G29])。
  - When to use: 早期返回里嵌着否定含义时。
  - How: 抽 `canBeCompacted()` = `expected != null && actual != null && !areStringsEqual()`，主流程走正向分支。
- **Expose Temporal Coupling（暴露时间耦合）**: 当 `findCommonSuffix` 依赖 `findCommonPrefix` 先跑，把两者合并为 `findCommonPrefixAndSuffix()` 以显式固化顺序 ([G31])。
  - When to use: 两个函数有隐含的先后依赖，乱序会出难调的 bug。
  - How: 不要只靠传参（`findCommonSuffix(prefixIndex)` 太任意、易被后人撤销），而是直接合并成一个函数显式调用顺序。
- **Eliminate Dead Code / Non-functional Guard（消除死代码与非功能守卫）**: 借重构发现的"永远为真的 if"应删掉，并用测试验证 ([G9])。
  - When to use: 改命名/索引基准后，发现某守卫永远成立。
  - How: 注释掉可疑 if → 跑测试 → 通过即删除，使 `compactString` 退化为纯片段拼接。

## Key Concepts
- **ComparisonCompactor**: 给定两串（如 `ABCDE` 与 `ABXDE`）生成 `<...B[X]D...>`，高亮差异并带上下文省略号。
- **Context Length（上下文长度）**: 构造参数 `contextLength`，控制差异两侧保留多少字符 + `ELLIPSIS("...")`。
- **Compact vs Format**: 原函数名 `compact` 有副作用（内部做错误检查并返回整条格式化消息），应改名 `formatCompactedComparison` 以表意 ([N7])。
- **Analysis vs Synthesis 拓扑分层**: 最终模块被分成"分析函数组"（找 prefix/suffix、判是否可压缩）在前、"合成函数组"（拼 `startingEllipsis/startingContext/delta/endingContext/endingEllipsis`）在后，定义紧随使用处。
- **Index vs Length 基准**: 把 1-based 的 `suffixIndex` 改为 0-based 的 `suffixLength`，消除满屏 `+1` ([G33])。
- **Temporal Coupling（时间耦合）**: `findCommonSuffix` 必须在 `findCommonPrefix` 之后，否则 `prefixIndex` 未初始化。

## Mental Models
- Use **Extract Method 命名意图** when 一个条件或代码块读起来像"它在干什么"而不像"为什么"——用方法名替你说话。
- Use **反转负向条件** when `if (!xxx)` 早期返回让主流程难读——翻成正向 `canBeCompacted()`。
- Use **合并为 findCommonPrefixAndSuffix** when 两个函数有隐式先后依赖——用函数结构本身固化顺序，比传参更抗误操作。
- Use **删死代码前先注释+跑测试** when 怀疑某个 if 永远成立——让测试替你确认，而非凭直觉删。

## Anti-patterns
- **成员变量的匈牙利式 `f` 前缀（如 `fExpected`）**: 现代 IDE 让作用域编码冗余，应直接叫 `expected` ([N6])。
- **函数内局部变量与成员变量同名（靠 `this.` 区分）**: 表明命名有歧义，应改成 `compactExpected` / `compactActual` ([N4])。
- **名字掩盖副作用**: `compact()` 实际还做错误检查并返回格式化消息，名字误导——应叫 `formatCompactedComparison` ([N7])。
- **用参数传递来"暗示"顺序（如 `findCommonSuffix(prefixIndex)`）**: 参数只是凑顺序，无语义，后人会撤销——应合并函数 ([G32])。
- **1-based 索引导致 `+1` 满天飞**: `suffixIndex` 非 0-based 导致 `computeCommonSuffix` 全是 `+1`，既难读又藏 bug ([G33])。
- **非功能守卫（永远为真的 if）**: `suffixIndex` 从不为 0 使 `if (suffixLength > 0)` 永真——死代码应删。

## Code Examples
```java
// 重构前（Listing 15-2 片段）
public String compact(String message) {
  if (fExpected == null || fActual == null || areStringsEqual())
    return Assert.format(message, fExpected, fActual);
  findCommonPrefix();
  findCommonSuffix();
  String expected = compactString(fExpected);
  String actual = compactString(fActual);
  return Assert.format(message, expected, actual);
}
```
- **What it demonstrates**: `f` 前缀、`this.` 歧义、负向条件、名字 `compact` 掩盖"返回格式化消息"的副作用。

```java
// 最终形态（Listing 15-5 合成函数组）
private String compact(String s) {
  return new StringBuilder()
    .append(startingEllipsis())
    .append(startingContext())
    .append(DELTA_START)
    .append(delta(s))
    .append(DELTA_END)
    .append(endingContext())
    .append(endingEllipsis())
    .toString();
}
private String delta(String s) {
  return s.substring(prefixLength, s.length() - suffixLength);
}
```
- **What it demonstrates**: `compactString` 从"带两个 if 的拼接"退化为纯片段组合；`delta` 因改用 0-based `suffixLength` 而去掉 `+1`。

## Worked Example
**ComparisonCompactor 的精炼（基于 ComparisonCompactorTest，100% 覆盖率）**

源文件只含本模块（本书 ch15 的架构部分未在此 excerpt）。`ComparisonCompactorTest` 用 19 个测试用例把 `compact` 的边界（null 端、首尾相同、重叠匹配、`S&P500` bug #609972 等）全部覆盖——这是敢于动手的前提。

重构序列（每步测试全绿）：
1. **去 `f` 前缀**：`fExpected→expected`、`fPrefix→prefix` 等 ([N6])。
2. **封装条件**：`if (expected==null||actual==null||areStringsEqual())` → `if (shouldNotCompact())` ([G28])。
3. **消除 `this.` 歧义**：`String expected = compactString(this.expected)` → `compactExpected = compactString(expected)` ([N4])。
4. **反转负向**：`shouldNotCompact()` 翻为 `canBeCompacted()`，主流程走正向分支 ([G29])。
5. **改名 + 拆分职责**：`compact` → `formatCompactedComparison`（只做格式化）；真正的压缩抽成 `compactExpectedAndActual()`，并把 `findCommonPrefix/Suffix` 改为 `return` 值而非写成员变量（统一约定，[G11]）。
6. **暴露时间耦合**：`findCommonSuffix` 依赖 `prefixIndex`，先试传参 `findCommonSuffix(prefixIndex)`（太任意，[G32]）→ 改为合并 `findCommonPrefixAndSuffix()` 显式固化顺序 ([G31])。
7. **清理 suffix 逻辑**：抽出 `charFromEnd(s,i)` 与 `suffixOverlapsPrefix()`，把循环写清楚。
8. **基准统一**：`suffixIndex`（1-based）改 `suffixLength`（0-based），`+1` 移到 `charFromEnd` 的 `-1` 与 `suffixOverlapsPrefix` 的 `<=`，可读性大增 ([G33])。
9. **发现并删死代码**：改基准后注意到 `if (suffixLength > 0)` 本应改 `>=` 才有意义——说明它以前永真（因 `suffixIndex` 从不为 0）。注释掉两个 if → 测试仍过 → 删除，使 `compactString` 成纯拼接 ([G9])。
10. **拓扑分层（最终 Listing 15-5）**：分析函数（shouldBeCompacted / findCommonPrefixAndSuffix / findCommonPrefix / charFromEnd / suffixOverlapsPrefix）在前，合成函数（compact / startingEllipsis / startingContext / delta / endingContext / endingEllipsis）在后；定义紧随使用。作者还回退了早先几步（如把某些抽取又 inline 回 `formatCompactedComparison`、把 `shouldNotBeCompacted` 再翻回负向）——证明重构是试错收敛，而非单向前进。

**结论**：即便原作者（Beck/Gamma）已写得专业，Boy Scout Rule 仍能让我们留得更干净一点；而 100% 测试覆盖给了我们无恐惧动手的底气。

## Key Takeaways
1. 即使"好代码"也可再干净——Boy Scout Rule 适用于所有模块，包括大师写的。
2. 动手前先确认有测试护体（本例 100% 覆盖），否则不要重构。
3. 抽方法用"名字表达意图"，比注释和裸条件都强；负向条件翻转为正向更易读。
4. 时间耦合要用函数结构（合并）固化，而非用参数"暗示"，否则会被后人撤销。
5. 统一索引基准（0-based）能消灭 `+1` 噪音，并顺带暴露死代码。
6. 删死代码前先注释 + 跑测试确认；重构是迭代试错、常回退早先步骤，最终收敛。

## Connects To
- **Ch 14 (Successive Refinement)**: 同一套小步 + 测试绿纪律，这里用于他人代码。
- **Ch 1 / Ch 2 (Names)**: `f` 前缀、`compact` 掩盖副作用、`this.` 歧义都是命名问题。
- **Ch 6 (Objects & Data Structures)**: 用方法拆分替代大函数，是职责分配的微观版。
- **Ch 17 (Smells & Heuristics)**: [G9]/[G11]/[G28]/[G29]/[G31]/[G32]/[G33]/[N4]/[N6]/[N7] 均对应书中 smell 编号。
