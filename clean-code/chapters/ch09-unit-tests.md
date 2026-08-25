# Chapter 9: Unit Tests

## Core Idea
测试代码与生产代码同等重要，绝不是二等公民。脏测试等于（甚至不如）没有测试——它们会腐烂生产代码。测试的真正价值在于：它让改变不再可怕，从而支撑所有 -ilities（灵活性、可维护性、可复用性）。

## Frameworks Introduced
- **The Three Laws of TDD**: 锁定"测试仅比生产代码早几秒"的短循环。
  - Law 1: 不允许写生产代码，除非先写了失败的单元测试。
  - Law 2: 不允许写多于"足以失败"的单元测试（编译不过也算失败）。
  - Law 3: 不允许写多于"足以通过当前失败测试"的生产代码。
- **F.I.R.S.T.**: 干净测试的五条规则。
  - Fast：慢测试没人跑，问题发现晚，代码开始腐烂。
  - Independent：测试间不互相依赖，可任意顺序独立运行。
  - Repeatable：任何环境（生产/QA/笔记本）都能重复运行。
  - Self-Validating：输出布尔值（通过/失败），不需读日志或人工比对。
  - Timely：单元测试应在使其通过的生产代码之前写。
- **BUILD-OPERATE-CHECK Pattern**: 每个测试分三段——构建数据、操作数据、校验结果。
- **Domain-Specific Testing Language**: 从重构测试代码中演化出一套专用 API，让测试更易写更易读。
- **Single Concept per Test**: 每个测试函数只测一个概念，而非把多个不相关断言堆在一起。

## Key Concepts
- **Three Laws of TDD**: 先写失败测试、最小化测试、最小化通过的生产的强制循环。
- **Dual Standard**: 测试环境代码可牺牲效率（内存/CPU），但绝不牺牲整洁度。
- **Learning Tests**: 见 Ch 8，边界处验证第三方代码行为的测试。
- **One Assert per Test**: 理想准则——尽量把断言数降到最低，但单概念优先于单断言。

## Mental Models
- Keep **tests as clean as production code** when 任何测试开始变脏，因为脏测试比没测试更糟：最终被丢弃，随后生产代码腐烂。
- Use **a domain-specific testing language** when 测试被无关 API 细节淹没（如 `PathParser`、`makeResponse` 强转），用 `makePage`/`submitRequest`/`assertResponseContains` 抽出表达力。
- Prefer **single concept per test over one-assert-per-test** because 真正的问题是"测了多个概念"，多个断言服务于同一概念是合理的（如校验 XML 且含子串）。
- Write **tests first (Timely)** when 生产代码已存在，否则它会变得难以测试、你也不再会设计成可测的。

## Anti-patterns
- **Dirty / "quick and dirty" tests**: 命名差、重复多、不设计；维护成本超过写新功能，最终整套被丢弃，缺陷率上升，生产代码随之腐化。
- **Multiple concepts in one test**: 如 `testAddMonths` 把三种日期边界规则混在一起，读者需费力分辨"每段在测什么"。
- **Non-self-validating / non-repeatable tests**: 需要读日志或人工比对才算通过，失败变主观，环境一缺就成借口。

## Code Examples
```java
@Test
public void turnOnLoTempAlarmAtThreshold() throws Exception {
  wayTooCold();
  assertEquals("HBchL", hw.getState());
}
```
- **What it demonstrates**: Refactored 测试——`tic()` 细节被藏进 `wayTooCold()`，状态用约定字符串表达（大写=开，小写=关，顺序为 heater/blower/cooler/hi-temp-alarm/lo-temp-alarm），一眼可读结果。注意这是 dual standard：测试里的 `getState` 用字符串拼接而非 `StringBuffer`（效率差但测试环境无所谓）。

## Worked Example
FitNesse 的 `SerializedPageResponderTest` 重构对比。原始版本（Listing 9-1）满是 `PathParser.parse(...)`、`new FitNesseContext(root)`、`(SimpleResponse) responder.makeResponse(...)` 等杂音，每个测试重复大量 setup。重构后（Listing 9-2）抽出 `makePages`、`submitRequest`、`assertResponseIsXML`、`assertResponseContains`，清晰呈现 BUILD-OPERATE-CHECK：
```java
public void testGetPageHierarchyAsXml() throws Exception {
  makePages("PageOne", "PageOne.ChildOne", "PageTwo");
  submitRequest("root", "type:pages");
  assertResponseIsXML();
  assertResponseContains(
    "<name>PageOne</name>", "<name>PageTwo</name>", "<name>ChildOne</name>"
  );
}
```
进一步可用 given-when-then 命名（Listing 9-7），但拆得太碎会带来重复；作者偏好 Listing 9-2 的多断言、单概念形式。

## Key Takeaways
1. 测试代码必须和生产代码一样整洁——脏测试会让你失去测试，进而失去改代码的勇气。
2. 干净测试的三要素：可读性、可读性、可读性；靠 BUILD-OPERATE-CHECK 与领域测试语言达成。
3. 遵循 F.I.R.S.T.；测试慢、互相依赖、不可重复、需人工判定，都会让套件被弃用。
4. 优先"每个测试单概念"，断言数最小化即可，不必机械执行单断言。
5. 测试是双标准环境：可牺牲效率，但永不牺牲整洁。

## Connects To
- **Ch 8**: learning tests 就是边界处的干净测试，验证第三方行为。
- **Ch 10**: 把大函数拆小会产生更多小类；同样，重构测试会演化出测试专用 API。
- **-ilities**: 测试使能变化，变化使能灵活性/可维护性/可复用性。
