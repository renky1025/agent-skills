# Chapter 2: Meaningful Names

(by Tim Ottinger)

## Core Idea
命名无处不在（变量、函数、参数、类、包、文件……），而好名字的代价会被它省下的时间加倍偿还——命名的铁律是：名字应当揭示意图（reveal intent），若需要注释来解释，说明名字没做到。

## Frameworks Introduced
- **Use Intention-Revealing Names**: 变量/函数/类的名字要回答“为何存在、做什么、怎么用”。
  - When to use: 给任何标识符起名或看到 `int d;` 这类名字时。
  - How: 选能指明“被测度的是什么 + 单位”的名字，例如 `int d; // elapsed time in days` → `int elapsedTimeInDays;` / `daysSinceCreation;` / `fileAgeInDays;`。若名字需要注释，就改名字。
- **Avoid Disinformation**: 不要留下误导性的假线索。
  - When to use: 选词可能与其固定含义冲突时（如 `hp`、`aix`、`sco` 是 Unix 平台名）。
  - How: 不是真正的 `List` 就别叫 `xxxList`（用 `accountGroup`/`bunchOfAccounts`/`accounts`）；避免 `XYZControllerForEfficientHandlingOfStrings` 与 `...StorageOfStrings` 这种只在细微处不同的名字；绝不用小写 `l` 或大写 `O` 作变量名（易与 1/0 混淆）。
- **Make Meaningful Distinctions**: 名字不同，必须含义不同；数字序列与 noise words 不算区分。
  - When to use: 因编译器要求而不得不改名的时。
  - How: 拒绝 `a1,a2 ... aN` 与 `ProductInfo`/`ProductData`/`klass` 这类；`getActiveAccount()` vs `getActiveAccounts()` vs `getActiveAccountInfo()` 会让调用者无从选择——要让差异本身可理解。
- **Use Pronounceable Names**: 人脑为“词”而生，不可发音就无法讨论。
  - When to use: 设计会被团队口头讨论的字段/类时。
  - How: `genymdhms`（generation date, y,m,d,h,m,s）→ `generationTimestamp;`；`DtaRcrd102` → `Customer`，`pszqint` → `recordId`。
- **Use Searchable Names**: 单字母名与魔法数字难以全局检索。
  - When to use: 变量/常量可能被多处引用时。
  - How: 单字母名只用在极短方法里的局部变量；`7` → `MAX_CLASSES_PER_STUDENT`；`5` → `WORK_DAYS_PER_WEEK`；`e` 是最糟选择（英语最常见字母）。名字长度应随作用域增大而增大。
- **Avoid Encodings**: 不要在名字里编码类型/作用域——它是额外的破译负担。
  - When to use: 用现代强类型语言（Java/C#/C++）时。
  - How: 弃用 Hungarian Notation（`PhoneNumber phoneString;` 类型改了名字却没改）；弃用 `m_` 前缀成员（`m_dsc` → `description`）；接口不加 `I`（用 `ShapeFactory` 而非 `IshapeFactory`），若必须编码则编码实现（`ShapeFactoryImp`/`CShapeFactory`）。
- **Avoid Mental Mapping**: 读者不应把你的名字在脑中翻译成已知概念。
  - When to use: 选用既不属问题域也不属解域的单字母名时。
  - How: 循环计数器 `i/j/k` 在小作用域可接受（但绝不用 `l`）；不要因为 `a,b` 被占用就用 `c`；专业程序员明白 clarity is king，用清晰换聪明。
- **Add Meaningful Context / Don't Add Gratuitous Context**: 用类/函数/命名空间给名字以语境，但别画蛇添足。
  - When to use: 孤立看到 `state` 不知它是地址一部分时；或整个应用被加统一前缀时。
  - How: 用 `Address` 类而非 `addrState` 前缀；别给“Gas Station Deluxe”里每个类加 `GSD` 前缀（IDE 补全反而变长 list，且 `GSDAccountAddress` 冗余）。

## Key Concepts
- **Intention-Revealing**: 名字自身说明意图，无需注释补充。
- **Implicity（书中自造词）**: 上下文未显式落在代码里的程度——`getThem()` 难懂不是因为复杂，而是因为 implicity 太高。
- **Noise words**: `Info`/`Data`/`Variable`/`Table`/`theMessage` 这类不增加含义的冗余词（`NameString` 不比 `Name` 好）。
- **One word per concept**: 一个抽象概念固定一个词，别在 `fetch`/`retrieve`/`get` 间漂移。
- **Don't Pun**: 同一词别用于两种语义（集合的“插入”不该叫 `add`，该叫 `insert`/`append`）。
- **Solution vs Problem Domain Names**: 程序员读得懂就用 CS/模式名（如 `AccountVisitor`、`JobQueue`）；无“程序术语”时才用问题域名，便于请教领域专家。

## Mental Models
- **Use Intention-Revealing Names when 一个名字需要注释**：需要注释 = 名字失败，直接把意图写进名字。
- **Think of 编码前缀（HN / m_ / I） as 给读者额外发明一门语言**：现代编译器与 IDE 已记住类型，编码只增加认知负担与误写风险。
- **Use Solution Domain Names when 读者是程序员且概念有现成术语**：`JobQueue` 谁不懂？别逼同事跑去问客户。
- **Think of 语境 as 由 enclosing class/function 提供，而非靠前缀拼出来**：`state` 孤独出现难懂，放进 `Address` 类就清晰——类本身就是语境。

## Anti-patterns
- **Disinformation（误导）**: `accountList` 实际不是 List；`hp` 易被当成 Unix 平台；`l`/`O` 当变量名——假线索让代码更难懂。
- **数字序列 / noise words**: `a1,a2`、`ProductInfo`、`klass`——名字不同但没区分含义，调用者无从选。
- **不可发音名**: `genymdhms`、`pszqint`——无法在讨论中正常念出，新人只能靠“黑话”交流。
- **非搜索友好名**: 单字母 `e`、魔法数字 `7`——grep 时淹没在噪声里，改值时极易漏改。
- **Be Cute（耍小聪明）**: `HolyHandGrenade` 不如 `DeleteItems`；`whack()` 表 kill、`eatMyShorts()` 表 abort——只有懂你梗的人记得住。
- **Gratuitous Context**: 全应用统一前缀 `GSD`——对抗工具，且 `GSDAccountAddress` 中 10/17 字符冗余。

## Code Examples
```java
// 起点：意图全靠隐式（implicity 高）
public List<int[]> getThem() {
  List<int[]> list1 = new ArrayList<int[]>();
  for (int[] x : theList)
    if (x[0] == 4)
      list1.add(x);
  return list1;
}

// 终态：用 Cell 类 + 意图揭示名，魔法数字被隐藏
public List<Cell> getFlaggedCells() {
  List<Cell> flaggedCells = new ArrayList<Cell>();
  for (Cell cell : gameBoard)
    if (cell.isFlagged())
      flaggedCells.add(cell);
  return flaggedCells;
}
```
- **What it demonstrates**: 同样的操作符与嵌套层级，仅通过命名（theList→gameBoard、x[0]==4→cell.isFlagged()）就把 implicity 降到几乎为零——这是好名字的力量。

## Worked Example
**扫雷游戏的 `getFlaggedCells` 重构（书中主线示例）**：
1. 原始 `getThem()` 只有 3 个变量、2 个常量，却无人能答：theList 装什么？下标 0 何意？值 4 何意？返回的列表怎么用？——问题在 implicity。
2. 引入语境：这是扫雷盘，`theList` 是 `gameBoard`；下标 0 是 `STATUS_VALUE`，值 4 表示“已标记（FLAGGED）”。改名后：`getFlaggedCells()` 遍历 `gameBoard`，`if (cell[STATUS_VALUE] == FLAGGED)`。
3. 再进一步：用 `Cell` 类取代 `int[]`，把魔法数字藏进 `cell.isFlagged()`。三步走完，代码无需注释即可读懂。

**配套示例 — `GuessStatisticsMessage`（Add Meaningful Context）**：
- Listing 2-1 中 `printGuessStatistics` 的 `number/verb/pluralModifier` 三个变量只在读完函数后才知属于“猜统计消息”，孤立看含义不透明。
- 解法：抽出 `GuessStatisticsMessage` 类，使三变量成为其字段，并把大函数拆成 `thereAreNoLetters()`/`thereIsOneLetter()`/`thereAreManyLetters()` 等小方法——语境清晰了，算法也更干净（Listing 2-2）。

## Key Takeaways
1. 名字要 reveal intent；需要注释来解释的名字就是失败的名字，直接改名字。
2. 别误导：不是 List 就别叫 List；绝不用 `l`/`O` 作变量名；细微差名的“形状”会坑人。
3. 区分要有意义：拒绝 `a1/a2`、`ProductInfo/ProductData`、`getActiveAccount/...Accounts/...Info`。
4. 用可发音、可搜索的名字；单字母只用于短方法局部变量，魔法数字提成具名常量。
5. 弃用编码（`m_`、HN、`I` 接口前缀）；现代语言与 IDE 已记住类型。
6. 一词一义（fetch/retrieve/get 选一个），别 pun（集合插入用 insert/append 而非 add）；清晰胜过 cute（`HolyHandGrenade`→`DeleteItems`）。
7. 用类/函数提供语境，而非前缀；别给全应用加 `GSD` 这类冗余前缀。

## Connects To
- **Ch 1 (Clean Code)**: Dave Thomas / Ron Jeffries 把 meaningful names 列为整洁代码的基石；童子军规则最便宜的动作就是改一个更好的名字。
- **Ch 3 (Functions)**: 好名字是函数的门面——`get`/`set`/`is` 与静态工厂（`Complex.FromRealNumber`）的命名约定直接服务于函数可读性。
- **Refactoring — Rename / Extract Method**: 本章几乎每个改进都可借 IDE 重命名/抽取安全完成（Ron Jeffries 强调现代工具让改名极廉价）。
- **Design Patterns (VISITOR 等)**: 用 `AccountVisitor`、`JobQueue` 等 solution-domain 名，前提是读者懂模式——命名与模式语言互通。
- **JavaBeans 规范**: 访问器/修改器/谓词用 `get`/`set`/`is` 前缀，是方法命名的事实标准。
