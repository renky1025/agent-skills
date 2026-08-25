# Chapter 1: Clean Code

## Core Idea
代码是我们最终表达需求的语言——它永远不会消失，只能是“更高级”的代码；而保持代码整洁（clean）不是锦上添花，而是专业主义（professionalism）的底线：唯一能让你走得快的方式，就是始终让它保持干净。

## Frameworks Introduced
- **LeBlanc's law**: "Later equals never."
  - When to use: 当你想把“清理/重构”推迟到以后时，用它作为警示。
  - How: 任何“我以后回来收拾”的承诺在经验上都等于永不执行；把麻烦就地解决，而非记入待办。
- **The Boy Scout Rule**: "Leave the campground cleaner than you found it."
  - When to use: 每次 checkout/checkin 一段代码时，无论改动大小。
  - How: 不做大动作，只做微小且确定有益的改进——改一个更好的变量名、拆一个略大的函数、消除一处小重复、理清一个复合 if。累积效应使代码无法腐坏。
- **code-sense**: 识别好/坏代码、并能规划一连串“保持行为不变（behavior-preserving）的变换”把脏代码改写成干净代码的判断力。
  - When to use: 面对一个混乱模块，不知道“从哪下手”时。
  - How: 没有 code-sense 的人只看到“乱”；有 code-sense 的人看到选项与变体，并能选择最优变体、规划变换序列。这是本书真正要传授的东西，只能通过练习获得。
- **Object Mentor School of Clean Code**: 本书立场——把推荐当作“本门派的绝对准则”来实践，但不声称自己是唯一真理。
  - When to use: 你接受“整洁代码有可传授的纪律”这一前提时。
  - How: 把各章规则当作本门派的技艺来练；同时承认存在其他同样专业的“门派”，应跨界学习。
- **The Primal Conundrum（原始困境）**: 开发者明知旧烂摊子会拖慢自己，却又感到“为了赶 deadline 必须制造烂摊子”的压力。
  - When to use: 在“赶进度 vs 写干净”之间做取舍时。
  - How: 拒绝第二部分。制造混乱不会让你赶上 deadline，只会立刻拖慢你并导致错过它；唯一赶上 deadline 的方式是始终尽量保持代码干净。

## Key Concepts
- **There Will Be Code**: 需求只要我们指定到机器可执行的精度，就是代码；抽象层级会升高、DSL 会变多，但这些“更高层规格”本身仍是代码。
- **Wading**: 在烂代码里艰难跋涉的状态——我们 slog through a morass of tangled brambles and hidden pitfalls。
- **The Grand Redesign in the Sky**: 团队被烂代码逼到造反、要求推倒重做的“天上大重设计”；常演变为新旧系统长达数年的赛跑，且新系统最终也会变成烂摊子。
- **Reading vs. Writing ratio (10:1)**: 读代码与写代码的时间比远超 10:1；你今天要写的代码，难易取决于周围代码是否易读。
- **Broken Windows（破窗效应）**: Dave Thomas & Andy Hunt 的隐喻——一处破窗让人不再在乎，导致更多破坏；坏代码“诱惑”混乱生长（Bjarne 的 "tempt"）。
- **Literate code**: 代码应写得让人类可读（Knuth 的 literate programming 的软引用）；并非所有必要信息都能仅用代码表达。

## Mental Models
- **Think of 整洁代码 as 你作为作者的作品**：Javadoc 的 `@author` 字段提醒你——你是 author，有 reader，要对沟通负责；reader 会评判你的用心。
- **Use 干净代码 when 你想“走得快”**：写的难易取决于周围代码是否易读，所以“让代码易读”反而让写更容易；想快就先让它易读。
- **Think of 烂代码 as 复利债务**：生产力随混乱累积渐近于零，管理层加人只会加速恶化——这是数学，不是管理问题。
- **Use 医生的洗手类比 when 经理要求你为赶工牺牲质量**：就像病人要求手术前别洗手，专业医生会拒绝（Semmelweis 1847 年首倡洗手曾被以“太忙”拒绝）；程序员也该拒绝不懂混乱风险的管理要求。

## Anti-patterns
- **"Later equals never" / 推迟清理**: 把重构记入“以后”，经验上永不执行（LeBlanc's law）。
- **Grand Redesign in the Sky**: 推倒重来；往往是旧债未清又欠新债，且新系统最终同样腐化。
- **靠加人拯救烂代码库**: 新人不懂设计意图，在“提产”高压下制造更多混乱，把生产力进一步推向零。
- **把脏代码归咎于需求/排期/经理**: 责任在“我们”——经理与市场依赖我们提供真相与承诺的依据； defending the code 是你的职业责任。
- **认为“能识别干净代码 = 会写干净代码”**: 像能分辨画好坏 ≠ 会画画；识别只是起点，code-sense 需通过纪律与小技巧习得。

## Code Examples
```java
// 体现 The Boy Scout Rule 的最小改动：checkout 时顺手让一处更清晰
// before:
int d; // 距创建过去的天数
// after（仅改一个名字，无需改动逻辑）:
int daysSinceCreation;
```
- **What it demonstrates**: 童子军规则不需要大动作——一次只把一个名字、一处重复改好，腐坏就无法累积。

## Worked Example
**医生的洗手类比（Attitude 一节，Semmelweis 1847）**：设想你是外科医生，病人要求“手术前别搞那些费时的洗手”。病人是“老板”，但医生应坚决拒绝——因为医生比病人更懂感染风险，屈从既不专业甚至违法。Uncle Bob 据此断言：当经理因不懂混乱风险而要求你制造烂摊子时，程序员屈从同样不专业。

**配套的前后对比（同一章逻辑链）**：
- 症状：一个本应一行改动的变更，散落在数百个模块；几周才做完本应几小时的事。
- 根因不是需求变了，而是“我们”允许代码腐坏——专业主义要求把守代码质量，像医生把守无菌。
- 行动：用 The Boy Scout Rule 把“大重设计”替换为每次 checkin 的一点点变好；想象一个代码随时间越来越好的项目，那是专业主义的应有之义。

> 说明：第 1 章以论述为主、无成段代码；本示例忠实复述书中 Attitude / Boy Scout Rule 的逻辑，并补了一个符合本章建议的最小代码片段。

## Key Takeaways
1. 代码不会消失，它只是变成“更高层/领域特定”的代码——所以“整洁”是永恒的工程专业问题。
2. 赶 deadline 的唯一办法是保持代码干净；制造混乱会立刻反噬并让你错过 deadline（The Primal Conundrum）。
3. "Later equals never"：清理必须就地做，别记到以后。
4. 每次 checkin 都比 checkout 更干净一点（The Boy Scout Rule），腐坏就无法发生。
5. 读:写 ≈ 10:1；让代码易读，反而让写更快、更容易。
6. 你是作者，代码有读者；整洁代码的本质是被“care（在乎）”过——Michael Feathers 说它“看起来像有人在乎”。

## Connects To
- **Ch 2 (Meaningful Names)**: 童子军规则最便宜的落地动作就是改一个更好的名字；Dave Thomas / Ron Jeffries 都把 meaningful names 列为整洁代码的基石。
- **Ch 3+ (Functions / Classes)**: code-sense 的具体运用对象——函数、类如何写干净，是后续章节的主题。
- **PPP (Agile Software Development: Principles, Patterns, and Practices)**: 本书是 PPP 的“前传”；SRP / OCP / DIP 等设计原则在代码层面回响。
- **Kent Beck — Implementation Patterns / Beck's rules of simple code**: Ron Jeffries 引用“runs all tests; no duplication; expresses design ideas; minimizes entities”作为简单代码的优先级。
- **Test Driven Development**: Dave Thomas 断言“无测试的代码不干净”——测试是整洁代码的先决条件。
