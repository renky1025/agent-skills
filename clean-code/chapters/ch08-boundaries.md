# Chapter 8: Boundaries

## Core Idea
边界（boundary）是我们自己的代码与"我们无法控制"的代码相遇之处——第三方包、或尚未存在的 API。保持边界清洁的关键是：清晰的隔离，加上一组定义期望的测试。

## Frameworks Introduced
- **Learning Tests**: 用测试去探索第三方 API，把你对它的理解编码成可运行的实验。
  - When to use: 集成不熟悉的第三方库、需要确认其行为符合预期时。
  - How: 像在生产代码中那样调用该 API，写"受控实验"验证你的理解；每次升级该库时重跑，立刻发现行为差异。
- **Adapter Pattern**: 把我们理想的接口翻译成第三方提供的接口，桥接双方。
  - When to use: 真实 API 尚未定义，或第三方接口与我们的领域模型不匹配时。
  - How: 先定义自己想要的接口；待真实 API 就绪后，写一个 Adapter 实现桥接，把所有交互封进一处。
- **Boundary Interface Encapsulation（如 Sensors 包装 Map）**: 把边界接口藏进一个类，对外只暴露裁剪过的、符合应用需求的方法。
  - When to use: 当 `Map` 或任何边界接口要在系统里被到处传递时。
  - How: 在类内部持有 `Map`，提供 `getById` 之类的方法；不要从 public API 返回或接收它。

## Key Concepts
- **Boundary**: 自有代码与受控外部代码之间的接缝；变化在此发生。
- **Learning Tests**: 检验第三方包是否按预期工作的受控测试，升级时即"免费的回归测试"。
- **Adapter**: 隔离对外 API 依赖、提供单一变更点的设计模式（见 GOF）。
- **Seam**: 代码中便于替换实现的接缝，可用 Fake 对象在测试时注入。

## Mental Models
- Use **learning tests** when 集成陌生第三方代码，因为它让你在隔离环境中学会 API，并在每次发布时暴露破坏性变更。
- Use **你自己的接口 + Adapter** when 真实 API 尚不存在，让客户端代码保持可读、且始终掌握在你能控制的范围。
- Wrap **Map** inside a class when 你在系统里到处传递集合，把"接口一旦变化需要修改多少处"降到最低。
- Depend on **something you control** rather than something you don't control, lest it end up controlling you.

## Anti-patterns
- **Passing Maps (or any boundary interface) around the system**: 暴露了比需要更多的能力（如 `clear()`），且一旦接口变动（如 Java 5 加入泛型）有海量调用点要改。
- **Skipping learning tests for third-party code**: 把学习与集成混在 production 代码里，导致漫长的调试拉锯，升级时被动踩坑。
- **Letting too much code know third-party particulars**: 边界代码散落各处，迁移成本高、维护点增多。

## Code Examples
```java
public class Sensors {
  private Map sensors = new HashMap();
  public Sensor getById(String id) {
    return (Sensor) sensors.get(id);
  }
  //snip
}
```
- **What it demonstrates**: 把 `Map` 边界接口藏进类内部；泛型/类型转换成为实现细节，外部调用方不再关心，接口可自由演化。

## Worked Example
以 log4j 为例演示 learning tests。最初写下：
```java
@Test
public void testLogCreate() {
  Logger logger = Logger.getLogger("MyLogger");
  logger.info("hello");
}
```
运行报错：需要一个 `Appender`。读文档后加 `ConsoleAppender`，又报"无 output stream"；最终发现默认构造器是"unconfigured"的怪异行为，写成：
```java
@Test
public void addAppenderWithStream() {
  logger.addAppender(new ConsoleAppender(
    new PatternLayout("%p %t %m%n"),
    ConsoleAppender.SYSTEM_OUT));
  logger.info("addAppenderWithStream");
}
```
整套实验把 log4j 的初始化知识编码进 `LogTest`，随后封装进我们自己的 logger 类，使应用其余部分与 log4j 边界隔离。另一例：Transmitter API 未定义时，先写自己想要的 `Transmitter.transmit(frequency, stream)` 接口，真实 API 就绪后用 `TransmitterAdapter` 桥接，并用 `FakeTransmitter` 在接缝处测试。

## Key Takeaways
1. 不要在整个系统里传递 `Map` 等边界接口——把它关进一个类或紧密相关的家族里。
2. 用 learning tests 探索第三方代码；它们免费，且在新版本发布时帮你发现不兼容。
3. 对尚不存在的 API，先定义自己想要的接口，再用 Adapter 桥接，制造可测试的 seam。
4. 边界处要"少引用"：要么包装（如 Map），要么适配（Adapter），两者都减少维护点。

## Connects To
- **Ch 9**: learning tests 本质就是单元测试，是边界处的 outbound 测试。
- **Ch 10**: Adapter 与抽象依赖是隔离变化、遵循 DIP 的具体手段。
- **Dependency Inversion Principle**: 边界处优先依赖你能控制的抽象，而非具体实现。
