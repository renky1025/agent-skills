# Chapter 10: Classes

## Core Idea
类也必须小——但衡量标准不是行数，而是职责（responsibilities）。用 SRP、内聚、OCP、DIP 把系统组织成许多小类，使变化风险局部化、代码更易定位与理解。

## Frameworks Introduced
- **Class Organization Convention**: 标准 Java 排列顺序。
  - Order: `public static` 常量 → `private static` 变量 → `private instance` 变量 → `public` 函数；public 函数后的私有工具方法紧随其后（stepdown 规则，像报纸一样读）。
  - How: 几乎没有理由用 public 变量；需要时再考虑 protected/包级（测试优先）。
- **Single Responsibility Principle (SRP)**: 一个类/模块只有一个、且只有一个变更理由。
  - When to use: 判断类是否过大、是否该拆分时。
  - How: 用约 25 词描述类且不出现 if/and/or/but；含 Processor/Manager/Super 等词常暗示职责过多。
- **Cohesion**: 类的实例变量应少，方法应操作其中变量；方法 manipulates 的变量越多越内聚。
  - When to use: 发现一堆函数共享少数变量时。
  - How: 内聚下降就拆类——把共享变量的函数提成新类。
- **Open-Closed Principle (OCP)**: 类对扩展开放、对修改关闭。
  - When to use: 预计要给类加新功能（如新 SQL 语句类型）时。
  - How: 抽象基类 + 子类各自实现，新功能以新子类"插入"，不动旧类。
- **Dependency Inversion Principle (DIP)**: 类应依赖抽象，而非具体细节。
  - When to use: 客户端依赖易变的具体实现（如外部 API）时。
  - How: 抽出接口，构造函数注入接口引用；具体实现与测试桩都实现该接口。
- **Factories**: 在隔离变化语境下，用工厂/构造函数注入选择具体实现，让调用方只依赖抽象。

## Key Concepts
- **SRP**: 类只有一个变更理由；既是职责定义也是类大小准则。
- **Cohesion**: 方法与变量共依赖、作为逻辑整体"挂在一起"的程度。
- **God Class**: 暴露 ~70 个 public 方法的超大类（如 `SuperDashboard`），职责爆炸。
- **OCP / DIP**: 通过抽象与子类化，让系统以"扩展"而非"修改"接纳变化。
- **Encapsulation (pragmatic)**: 变量与工具方法默认 private；仅为测试可放宽到 protected/包级，但这是最后手段。

## Mental Models
- Use **SRP** when 一个类出现多个"变更理由"（如 `SuperDashboard` 既管版本号又管 Swing 组件），把它拆成 `Version` 这样的单职责类。
- Split **a class when cohesion drops** because 几个函数想共享某些变量，本身就说明它们该成独立类。
- Prefer **abstract dependencies + constructor injection (DIP)** over concrete dependencies when 具体实现易变或难测（如 `TokyoStockExchange`），用 `StockExchange` 接口隔离细节、便于注入测试桩。
- Organize for **OCP** when 你"打开"一个类加功能会冒破坏风险，改用抽象基类 + 新子类，旧类保持关闭。

## Anti-patterns
- **God Class / too many responsibilities**: `SuperDashboard` 暴露约 70 个 public 方法，或即便只有 5 个方法却同时管版本号与 Swing 组件——仍有两个变更理由。
- **Concrete dependency in client**: `Portfolio` 直接依赖 `TokyoStockExchange`，价格每五分钟一变，测试无法写、变化会波及客户端。
- **Opening a class for every change**: `Sql` 既要为新型语句改、又要为单语句细节改，违反 SRP，每次修改都要全量重测、有破坏风险。

## Code Examples
```java
public class Stack {
  private int topOfStack = 0;
  List<Integer> elements = new LinkedList<Integer>();
  public int size() { return topOfStack; }
  public void push(int element) {
    topOfStack++;
    elements.add(element);
  }
  public int pop() throws PoppedWhenEmpty {
    if (topOfStack == 0) throw new PoppedWhenEmpty();
    int element = elements.get(--topOfStack);
    elements.remove(topOfStack);
    return element;
  }
}
```
- **What it demonstrates**: 高内聚类——变量 `topOfStack` 与 `elements` 被 `push`/`pop` 共同操作；`size()` 是唯一未用全变量的方法，仍是教科书级内聚示例。

## Worked Example
把 Knuth 的 `PrintPrimes`（一个大 `main` 函数，深嵌套、怪变量、强耦合）重构成三个职责清晰的小类，而非重写：先用测试套件锁定原行为，再一步步小改。
- `PrimePrinter`：只负责执行环境（`main` 调用生成器与打印机），改调用方式（如转 SOAP）只动它。
- `PrimeGenerator`：只负责生成素数算法，算法变更只动它（本身不被实例化，仅作作用域）。
- `RowColumnPagePrinter`：只负责把数字格式化成行列分页，输出格式变更只动它。
另一例：`Sql` 违反 SRP（既要加语句类型、又要改单语句细节）。重构成抽象 `Sql` + `CreateSql`/`SelectSql`/`InsertSql`/`Where`/`ColumnList` 等，每个类极简；加 `UpdateSql` 时旧类一行不改，满足 OCP。再例：`Portfolio` 不直接依赖 `TokyoStockExchange`，而是依赖 `StockExchange` 接口（含 `Money currentPrice(String symbol)`），构造函数注入；测试用 `FixedStockExchangeStub` 固定价格，验证"买 5 股 MSFT 总值 500"，满足 DIP 且可测。

## Key Takeaways
1. 类要小，按"职责/变更理由"而非行数衡量； naming 模糊（Manager/Super）是告警信号。
2. 遵守 SRP：一个类一个变更理由；把 `SuperDashboard` 式的混合职责拆成可复用的小类。
3. 内聚下降即拆类——共享变量的函数本就是独立类的雏形。
4. 为变化组织：用 OCP（抽象基类 + 子类）让新功能以"扩展"插入，旧代码保持关闭。
5. 隔离变化用 DIP：依赖抽象接口 + 构造函数注入（Factories 选择具体实现），既解耦又易测试。

## Connects To
- **Ch 8**: Adapter 与边界隔离正是 DIP 在第三方代码处的具体落地。
- **Ch 9**: 把大函数拆小会自然催生更多小类；重构测试演化出测试 API，同理。
- **SRP / OCP / DIP**: 三者共同构成"组织以适应变化"的面向对象设计支柱。
