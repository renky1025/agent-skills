# Chapter 6: Objects and Data Structures

## Core Idea
Objects 暴露行为、隐藏数据；data structures 暴露数据、没有有意义的行为。两者是虚拟相反（anti-symmetric）的：OO 易加新类型难加新函数，过程式易加新函数难加新类型。成熟程序员知道"一切皆对象"是神话，按需选择。

## Frameworks Introduced
- **Data Abstraction**: 隐藏实现不是简单地在变量外包一层函数，而是暴露能操作数据本质的抽象接口。
  - When to use: 设计代表数据的类/接口时。
  - How: 用 `setCartesian(x,y)` 这类原子接口表达访问策略，而不是暴露 `x`/`y` 让调用方独立操纵；用 `getPercentFuelRemaining()` 抽象掉燃料量的具体存储形式。
- **Data/Object Anti-Symmetry**: objects 与 data structures 互补且对立；决定系统某部分是偏向加类型还是加行为，据此选 OO 或过程式。
  - When to use: 架构某模块、预判未来变化方向时。
  - How: 要频繁加新数据类型 → 用 objects（多态）；要频繁加新函数而类型稳定 → 用 data structures + procedures。
- **Law of Demeter**: 方法 f 只应调用其自身类 C、f 创建的对象、作为参数传入的对象、以及 C 的实例变量所持有对象的方法；不应对"被允许调用所返回的对象"再调用方法。即 talk to friends, not strangers。
  - When to use: 判断链式调用 `a.b().c().d()` 是否越界时。
  - How: 若 ctxt/options/scratchDir 是 objects（有行为），链式导航其内部结构即违规；若是纯 data structures（无行为），暴露内部结构 Demeter 不适用。
- **Special Case Pattern / wrap third-party**: 见 Ch 7（此处引子：用对象封装特殊情形与第三方内部结构）。
  - When to use: 需要 ctxt 隐藏内部而不暴露路径时，问它"去做某事"而非"问它的内部"。
  - How: `ctxt.createScratchFileStream(className)` 让对象隐藏内部，调用方不违反 Demeter。
- **Data Transfer Objects (DTO)**: 典型 data structure = 只有 public 变量、无函数的类；bean 形式（private + getters/setters）是常见变体，准封装并无其他收益。
  - When to use: 与数据库、socket 消息通信、翻译原始数据时。
  - How: DTO 常作为数据库行→应用对象的第一个翻译阶段；Active Record 是带 save/find 导航方法的 DTO。

## Key Concepts
- **Object**: 把数据隐藏在抽象之后，暴露操作数据的函数（多态 `area()`）。
- **Data Structure**: 暴露其数据、没有有意义的函数（如 `Square` 只有 `topLeft`/`side` 公有字段）。
- **Procedural Shape**: 形状是裸 data structures，所有行为在 `Geometry` 类里（用 `instanceof` 分发）；加函数不影响形状，加形状要改所有函数。
- **Polymorphic Shape**: 每个形状自己实现 `area()`；加形状不影响现有函数，加函数要改所有形状（可用 VISITOR/dual-dispatch 绕过，但代价是把结构拉回过程式）。
- **Train Wrecks**: `ctxt.getOptions().getScratchDir().getAbsolutePath()` 这类耦合调用链，风格潦草应拆分。
- **Hybrids (Feature Envy)**: 半对象半 data structure——既有实质函数又有 public/公开访问器，把私有变量实际变 public，最难加函数也最难加类型，是 design muddle 的标志。

## Mental Models
- Use **objects with behavior** when you expect to add new data types — polymorphism keeps existing functions untouched.
- Use **data structures + procedures** when you expect to add new functions — existing structures stay untouched.
- Use **short local variables** — sorry, wrong chapter. → Use **Demeter-compliant calls** when navigating: talk to friends, not strangers; chain only across data structures, never across objects.
- Use **DTO/bean** when moving raw data between database/socket and your domain — keep them dumb, push business rules into separate objects.

## Anti-patterns
- **Blithely adding getters/setters**: 机械给每个私有变量加 getter/setter，等于把实现暴露成 public，仍未隐藏实现；最糟选项。
- **Train wrecks on objects**: 对具有真实行为的 objects 做 `a.b().c()` 导航，暴露其内部 = 违反 Law of Demeter。
- **Hybrids**: 同时有行为函数又公开访问器，导致加函数难、加类型也难，是"对是否需要保护"犹豫不决的产物。
- **Putting business rules in Active Record**: 把业务规则塞进本应只是 data structure 的 Active Record，制造 hybrid。

## Code Examples
```java
// Procedural: data structures + external behavior
public class Square { public Point topLeft; public double side; }
public class Geometry {
  public double area(Object shape) throws NoSuchShapeException {
    if (shape instanceof Square) {
      Square s = (Square)shape; return s.side * s.side;
    }
    // ... Rectangle, Circle branches ...
    throw new NoSuchShapeException();
  }
}

// OO: behavior hidden in objects
public class Square implements Shape {
  private Point topLeft; private double side;
  public double area() { return side*side; }
}
```
- **What it demonstrates**: 同一 `area` 语义，过程式把行为集中在 Geometry（加类型要改它），OO 把行为分散到各形状（加类型不改现有代码）。

## Worked Example
作者用 Point 对比：Listing 6-1 `public double x; public double y;` 明确是直角坐标、暴露实现；Listing 6-2 用接口 `getX/getY/setCartesian/setPolar`，你根本不知道底层是直角还是极坐标，且强制"坐标必须原子地一起设置"的访问策略——这是抽象而非简单加壳。Vehicle 同理：`getFuelTankCapacityInGallons()` 暴露存储细节，而 `getPercentFuelRemaining()` 抽象掉数据形态。结论：隐藏实现关乎 abstraction，而非 getter/setter 这一层函数。

## Key Takeaways
1. 不要盲目给对象加 getter/setter；思考真正要暴露的抽象接口（如原子 setCartesian）。
2. 预判变化方向：要加类型用 objects，要加函数用 data structures/过程式——两者都正当。
3. 遵守 Law of Demeter：对象间"告诉它去做"，对 data structures 才允许导航；出现 train wreck 先判断对方是 object 还是 structure。
4. 杜绝 hybrids；DTO/bean/Active Record 应保持"哑"数据，业务规则放进独立对象。

## Connects To
- **Ch 3 (Functions)**: 过程式把行为写成独立函数，与 data structures 配合。
- **Ch 5 (Formatting)**: 实例变量声明位置约定（顶部）支撑此处封装。
- **Ch 7 (Error Handling)**: 第三方 API 用 wrapper 隐藏（呼应 hybrid/Active Record 处理）。
- **Law of Demeter / Feature Envy**: 与 [Refactoring] (Fowler) 直接关联。
