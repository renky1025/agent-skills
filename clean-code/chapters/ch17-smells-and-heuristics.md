# Chapter 17: Smells and Heuristics

## Core Idea
作者把多年重构中"读了就觉得臭"的征兆编成一份可当参考用的启发式清单：大部分源自 Fowler 的 Code Smells，并补充大量个人条目，按 Comments / Environment / Functions / General / Java / Names / Tests 分类组织。

## Frameworks Introduced
- **Smell Taxonomy (C/E/F/G/J/N/T)**: 用前缀把味道分七类——Comments、Environment、Functions、General、Java、Names、Tests，便于检索与对照。
- **DRY (Don't Repeat Yourself) [G5]**: 重复是"错失抽象"的信号；重复的 switch/if-else 链 → 多态，相似算法 → TEMPLATE METHOD / STRATEGY。
- **ONE SWITCH rule [G23]**: 对某类选择，全系统至多一个 switch，其 case 必须产出多态对象以取代其它 switch。
- **Law of Demeter / "Shy Code" [G36]**: 模块只应认识直接协作者，避免 `a.getB().getC()` 的传递导航。
- **Principle of Least Surprise**: 贯穿 G2 / G11 / G17 / N2——代码行为应符合读者合理预期。

## Key Concepts
- **Code Smell (Fowler)**: 暗示更深层设计问题的表面征兆，不是 bug 但值得修。
- **Heuristic**: 经验法则，不是铁律；用来判断"这里味道不对"。
- **Selector Argument**: 用标志参数在一个函数里选多种行为（应拆函数）。
- **Feature Envy**: 方法伸进别的对象操作其数据，说明它属于那个对象。
- **Logical vs Physical dependency [G22]**: 逻辑依赖（假设）必须变成物理依赖（显式询问）。
- **Magic Number [G25]**: 任何值不自解释、意义不明显的字面量（含字符串如 `"John Doe"`）。

## Mental Models
- Use **polymorphism** when you catch yourself writing a switch/if-else that repeats across modules (G23).
- Use **enums** when a set of constants is currently `public static final int` (J3).
- Use **explanatory variables** when a single expression packs two or more computations (G19).
- Use **descriptive / long names** when a variable lives in a wide scope (N1, N5).
- Use **`plusX` not `addX`** when the method returns a new instance instead of mutating `this` (G20).
- Use **static import, not constant inheritance** when you want constants from another type (J2).

## Anti-patterns
（按书中分类；每条给英文标签 + 一句为何是味道。）

### Comments
- **C1 Inappropriate Information**: 变更历史/作者/SPR 号属于版本控制或 issue 系统，塞进注释只是噪音。例：文件头 CHANGE HISTORY。
- **C2 Obsolete Comment**: 过期注释会漂离原代码，变成误导性的"浮岛"。例：描述已删除行为的注释。
- **C3 Redundant Comment**: 注释复述代码自身能说明的事（`i++; // increment i`）。例：只重复方法签名的 Javadoc。
- **C4 Poorly Written Comment**: 值得写的注释值得写好——语法、标点、别啰嗦。
- **C5 Commented-Out Code**: 注释掉的代码会腐烂、调用已不存在的函数；删它，版本控制记得它。

### Environment
- **E1 Build Requires More Than One Step**: 构建应一条命令完成（`svn get` + `ant all`）；多步=摩擦。
- **E2 Tests Require More Than One Step**: 一条命令跑全部测试，能跑测试是基本且重要的能力。

### Functions
- **F1 Too Many Arguments**: 参数越少越好，超过三个应极力避免。
- **F2 Output Arguments**: 读者默认参数是输入；要改状态就改调用对象自己。
- **F3 Flag Arguments**: 布尔参数宣告"我做了不止一件事"，应拆成独立函数。
- **F4 Dead Function**: 从不被调用的函数直接删，版本控制记得它。

### General
- **G1 Multiple Languages in One Source File**: 一个源文件应只有一种语言；混入 HTML/Javadoc/XML 难维护。
- **G2 Obvious Behavior Is Unimplemented**: 违反最小惊讶——函数没实现读者合理期待的行为（如 Day 解析不忽略大小写）。
- **G3 Incorrect Behavior at the Boundaries**: 别信直觉，每个边界/角落条件都要测（SerialDate 跨年 bug）。
- **G4 Overridden Safeties**: 手动控制 serialVersionUID、关警告、跳过失败测试都是覆盖安全机制，危险。
- **G5 Duplication (DRY)**: 每处重复都是错失的抽象；switch 链→多态，相似算法→TEMPLATE METHOD/STRATEGY。
- **G6 Code at Wrong Level of Abstraction**: 实现细节的常量/工具不该出现在基类。例：`Stack.percentFull()` 应在 `BoundedStack`。
- **G7 Base Classes Depending on Their Derivatives**: 基类不应知道派生类名；用工厂解耦（见 Ch16）。
- **G8 Too Much Information**: 接口越小越好——少方法、少变量=低耦合。
- **G9 Dead Code**: 永不执行的死代码会变质、不再遵循新约定，删掉。
- **G10 Vertical Separation**: 变量/私有函数应紧邻使用处定义，缩小纵向距离。
- **G11 Inconsistency**: 相似的事用相似方式做（同变量名、同名风格），否则违反最小惊讶。
- **G12 Clutter**: 空默认构造器、未用变量、无信息注释都是 clutter，清理。
- **G13 Artificial Coupling**: 互不依赖的东西不该被硬性耦合；通用 enum 别塞进更具体的类。
- **G14 Feature Envy**: 方法通过别人 accessor 操作别的对象数据，应搬进那个对象。例：`HourlyPayCalculator.calculateWeeklyPay(e)` 伸进 `HourlyEmployee`。
- **G15 Selector Arguments**: 末尾标志参数选行为（`calculateWeeklyPay(boolean overtime)`）是懒惰，应拆 `straightPay()`/`overTimePay()`。
- **G16 Obscured Intent**: 长表达式、匈牙利命名、魔法数掩盖意图。例：`m_otCalc()` 不如 `overTimePay()`。
- **G17 Misplaced Responsibility**: 代码放哪遵循最小惊讶——PI 该和三角函数在一起。
- **G18 Inappropriate Static**: 偏好非静态；除非确定永不想要多态（如 `Math.max`）。
- **G19 Use Explanatory Variables**: 把计算拆成带含义的中间变量（Kent Beck），几乎不会过度。
- **G20 Function Names Should Say What They Do**: `date.add(5)` 看不出加几天/是否改原对象；叫 `plusDays`/`daysLater`。
- **G21 Understand the Algorithm**: 别靠堆 if/flag 蒙混，真正理解算法再收工。
- **G22 Make Logical Dependencies Physical**: 逻辑依赖要变成物理依赖——显式向依赖方要信息。例：`PAGE_SIZE` 应来自 `HourlyReportFormatter.getMaxPageSize()`。
- **G23 Prefer Polymorphism to If/Else or Switch/Case**: 每个 switch 都可疑；遵守 ONE SWITCH rule。
- **G24 Follow Standard Conventions**: 团队统一编码标准，代码即文档。
- **G25 Replace Magic Numbers with Named Constants**: `86400`→`SECONDS_PER_DAY`；但 5280、Math.PI 等广为人知的保留（Math.PI 已被定义好）。
- **G26 Be Precise**: 浮点表示货币近乎犯罪；声明 ArrayList 而 List 就够是过度约束；该判 null 就判。
- **G27 Structure over Convention**: 用结构强制合规（抽象方法）优于靠命名约定（switch/case）。
- **G28 Encapsulate Conditionals**: 把 `if (timer.hasExpired() && !timer.isRecurrent())` 抽成 `shouldBeDeleted(timer)`。
- **G29 Avoid Negative Conditionals**: 偏好 `shouldCompact()` 而非 `!shouldNotCompact()`。
- **G30 Functions Should Do One Thing**: 多段式函数拆成多个只做一件事的小函数。例：`pay()`→`payIfNecessary`/`calculateAndDeliverPay`。
- **G31 Hidden Temporal Couplings**: 调用顺序的耦合要显式——用"桶 brigade"（上一函数产出作下一函数入参）暴露时序。
- **G32 Don't Be Arbitrary**: 结构要有理由且被结构本身传达；公共类不该随意嵌套进别的类。
- **G33 Encapsulate Boundary Conditions**: 边界处理集中一处，别让 `+1`/`-1` 散落。例：`int nextLevel = level + 1;`。
- **G34 Functions Should Descend Only One Level of Abstraction**: 函数体内语句同处一层抽象，比函数名低一级。
- **G35 Keep Configurable Data at High Levels**: 默认/配置常量放高层，作入参传下，别埋在低层函数。
- **G36 Avoid Transitive Navigation (Law of Demeter)**: 避免 `a.getB().getC().doSomething()`；让直接协作者提供所需服务。

### Java（专属示例，通用原则见下；跨语言转译见 [appendix-lang-map.md](appendix-lang-map.md) §3）
> 以下 J 类是 Uncle Bob 针对 Java 的具体写法；其**通用原则**在所有语言成立，只是语法不同。

- **J1 Avoid Long Import Lists by Using Wildcards → 通用原则：最小化导入面**：同包用两个类以上就 `import pkg.*`（Java）；非 Java 用模块 / 命名空间导入，避免隐式耦合。
- **J2 Don't Inherit Constants → 通用原则：别把常量耦合进继承**：通过实现接口继承常量很丑（藏在继承链顶端）；用 `static import` / 模块 / 命名空间承载常量。
- **J3 Constants versus Enums → 通用原则：用类型安全枚举替魔法 int 常量**：Java 5 起用 `enum` 而非 `public static final int`；其他语言见 §3（TS union、Python Enum、C++ enum class、Go iota、Rust enum）。例：`HourlyPayGrade` enum 带 `rate()`。

### Names
- **N1 Choose Descriptive Names**: 名字占可读性 90%，慎重选、随演化重估。
- **N2 Choose Names at the Appropriate Level of Abstraction**: 别用暴露实现的名字；`dial(phoneNumber)`→`connect(connectionLocator)`。
- **N3 Use Standard Nomenclature Where Possible**: 用 DECORATOR、`toString` 等既定命名/项目通用语言（ubiquitous language）。
- **N4 Unambiguous Names**: 名字要无歧义；`doRename` 不如 `renamePageAndOptionallyAllReferences`。
- **N5 Use Long Names for Long Scopes**: 作用域越长名字越长；5 行循环里的 `i` 没问题。
- **N6 Avoid Encodings (Type Encodings)**: 别用 `m_`/`f`/`vis_` 等匈牙利式类型编码，环境已提供这些信息。
- **N7 Names Should Describe Side-Effects**: 名字要描述副作用；`getOos()` 实际会创建，应叫 `createOrReturnOos`。

### Tests
- **T1 Insufficient Tests**: 测试套件要覆盖一切可能出错之处，而非"看起来够多"。
- **T2 Use a Coverage Tool!**: 覆盖率工具暴露测试空白（绿/红行）。
- **T3 Don't Skip Trivial Tests**: 琐碎测试易写，文档价值高于成本。
- **T4 An Ignored Test Is a Question about an Ambiguity**: 注释掉或 `@Ignore` 的测试表达对需求歧义的提问。
- **T5 Test Boundary Conditions**: 算法中段常对、边界常错，重点测边界。
- **T6 Exhaustively Test Near Bugs**: bug 爱扎堆，找到 bug 就穷举测该函数。
- **T7 Patterns of Failure Are Revealing**: 失败用例模式（如输入>5 字符全失败）能定位根因。
- **T8 Test Coverage Patterns Can Be Revealing**: 看通过测试执行/未执行的代码，能推断失败原因。
- **T9 Tests Should Be Fast**: 慢测试会被丢弃，保持测试快。

## Code Examples
```java
// G14 Feature Envy — 方法伸进 HourlyEmployee 操作其数据
public Money calculateWeeklyPay(HourlyEmployee e) {
  int tenthRate = e.getTenthRate().getPennies();
  int tenthsWorked = e.getTenthsWorked();
  ...
}
// 修复：把行为搬进 HourlyEmployee（或让该方法成为其成员）

// G15 Selector Argument — 用布尔选行为
public int calculateWeeklyPay(boolean overtime) {
  double overtimeRate = overtime ? 1.5 : 1.0 * tenthRate;
  ...
}
// 修复：拆成 straightPay() / overTimePay()
```
- **What it demonstrates**: Feature Envy 暴露了别的对象内部；Selector Argument 用一个懒惰的标志把多个函数揉成一团。

## Worked Example
以 **G14 Feature Envy → 修复** 为例（书中 `HourlyEmployeeReport`）：

```java
// 坏味道：reportHours 羡慕 HourlyEmployee 的 scope
String reportHours() {
  return String.format("Name: %s\tHours:%d.%1d\n",
    employee.getName(),
    employee.getTenthsWorked()/10,
    employee.getTenthsWorked()%10);
}
```
担心把报表格式耦合进 `HourlyEmployee` 会违反 SRP/OCP/CCP，所以这里 Feature Envy 是"必要的恶"——格式字符串留在报告类。反之，`SerialDate.monthCodeToQuarter` 对 `Month` 数据的羡慕毫无理由，应搬进 `Month.quarter()`（见 Ch16）。判断标准：被羡慕的对象是否因此被迫知道本不属于它的概念。

## Key Takeaways
1. 把这份清单当**参考手册**：读代码时逐条问"这里有没有 Gxx / Nx / Tx 的味道"。
2. 重复（G5/DRY）是头号信号——看见重复就抽象；switch 重复就上多态（G23）。
3. 命名（N1–N7）占可读性九成：描述性、无编码、无歧义、长作用域用长名。
4. 测试（T1–T9）不是附属品：覆盖率工具 + 边界测试 + 穷举邻近 bug 是质量底线。
5. 味道不是铁律——G14 Feature Envy 有时是必要妥协，判断靠"是否强加不该知道的概念"。

## Connects To
- **Ch 16**: 本章每条 smell 在 SerialDate 重构中都有对应落地（G5/G7/G13/G14/G18/G22/G25 等）。
- **Ch 6 (Objects & Data Structures)**: G23/G36 与"对象 vs 数据结构"的选择互补。
- **Ch 9 (Unit Tests)**: T1–T9 是本章 Tests 类的展开。
- **Refactoring (Fowler)**: C/G 多条味道直接源自 Fowler 的 Code Smells 目录。
