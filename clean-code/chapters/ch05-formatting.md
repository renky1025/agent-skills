# Chapter 5: Formatting

## Core Idea
代码格式化关乎沟通，是专业开发者的第一要务；可读性比功能持久，因为今天的功能很可能在下个版本就变，而你的风格与纪律会留存。格式化规则应简单、一致，且团队统一。

## Frameworks Introduced
- **Newspaper Metaphor**: 源文件应像报纸文章——顶部是高层概念与算法，向下细节递增，最底部是最低层函数。
  - When to use: 决定一个类的组织顺序时。
  - How: 文件名要简单且能解释性；文件顶部给出最抽象的概念，逐层向下展开实现细节。
- **Vertical Distance (概念就近)**: 紧密相关的概念应放在垂直距离相近的位置；距离应反比于它们的概念亲和度（conceptual affinity）。
  - When to use: 安排变量、函数、依赖函数在类中的位置时。
  - How: 变量声明靠近使用处；被调用函数在调用者下方；有概念亲和度的函数簇彼此相邻。
- **Vertical Ordering (自上而下依赖)**: 函数调用依赖应指向下方——调用者在被调用者之上，形成从高层到低层的自然流动。
  - When to use: 排列同一文件内函数的先后顺序时。
  - How: 最重要的概念（最少细节）在前，低层细节在后，便于略读抓主干。
- **Horizontal Openness/Density**: 用水平空白把强相关者聚合、弱相关者分离；赋值号两侧留白以突出左右两侧，函数名与括号间不留白。
  - When to use: 排版单行表达式（赋值、函数调用、运算符优先级）时。
  - How: 围绕 `=` 留白分隔左右；参数间用逗号留白；高优先级运算符（因子）间不加空格。
- **Team Rules**: 团队应约定单一格式化风格，全员遵守，并编码进 IDE formatter。
  - When to use: 任何团队协作项目。
  - How: 花几分钟敲定花括号位置、缩进大小、命名规范，固化为自动格式化规则。

## Key Concepts
- **Vertical Openness**: 用空行分隔不同"完整思想"，每个空行是"新概念"的视觉提示。
- **Vertical Density**: 紧密相关的代码应垂直密集，无用的注释会打破关联，迫使眼与头多动。
- **Conceptual Affinity**: 某些代码段天然想靠近（同名函数族、共享变量、直接依赖），亲和度越强垂直距离应越短。
- **Indentation**: 源文件是层级（outline）结构，按作用域层级缩进使结构可见，是可读性的基础。
- **Dummy Scopes**: while/for 的空体必须正确缩进并加花括号，否则行末分号极易被忽略而出错。
- **Horizontal Alignment 反模式**: 把变量名、rvalue 对齐反而强调错的东西，且自动格式化会抹掉它。

## Mental Models
- Use **blank lines** when you finish one complete thought and start another — each blank line signals a new, separate concept.
- Use **vertical proximity** when two concepts are tightly coupled (caller/callee, variable/usage) — keep them close so the reader never has to hop.
- Use **top-down ordering** when a function calls a helper — put the caller above the callee so the module reads like a newspaper.
- Use **short lines (≤120)** when writing Java — programmers overwhelmingly prefer lines around 45–60 chars; beyond ~120 is careless.

## Anti-patterns
- **Collapsed one-line scopes**: 把短 if/while/函数压成一行、打破缩进，几乎总会让你回头补回缩进；它隐藏了作用域边界。
- **Horizontal alignment of declarations/assignments**: 把变量名或 rvalue 对齐，诱导眼睛只看值不看类型与操作符，且自动 format 会消除它。
- **Scattered instance variables**: 把 `fName`/`fTests` 藏在类中间（如 JUnit 的 TestSuite），读者只能偶然撞见声明，违背"声明在固定已知位置"的约定。
- **Misplaced constants**: 把众所周知的常量（如 "FrontPage"）埋进底层函数，而不是从有意义的层级传下来。

## Code Examples
```java
public class CodeAnalyzer implements JavaFileAnalysis {
  private int lineCount;
  private int maxLineWidth;
  private LineWidthHistogram lineWidthHistogram;

  public void analyzeFile(File javaFile) throws Exception {
    BufferedReader br = new BufferedReader(new FileReader(javaFile));
    String line;
    while ((line = br.readLine()) != null)
      measureLine(line);
  }

  private void measureLine(String line) {
    lineCount++;
    int lineSize = line.length();
    totalChars += lineSize;
    lineWidthHistogram.addLine(lineSize, lineCount);
    recordWidestLine(lineSize);
  }
}
```
- **What it demonstrates**: 实例变量集中在顶部、短函数不折叠作用域、变量靠近使用、缩进清晰体现层级。

## Worked Example
作者对比了两个 `BoldWidget` 版本。Listing 5-1 在 package/import/各函数间用空行分隔，不同代码簇"pop out"；Listing 5-2 抽掉空行并把 `addChildWidgets(match.group(1));}` 收紧，整体变成一团糊（muddle）。差异纯粹是 vertical openness。同样，`ReporterConfig` 在字段前写无用 javadoc 注释，打断了 `m_className` 与 `m_properties` 的紧密关联（Listing 5-3）；去掉注释后两个字段和一个方法刚好装进"一眼"（Listing 5-4）更易懂。结论：空行分离概念、密集表达关联。

## Key Takeaways
1. 把格式化当作沟通工具，而非信仰；固定的风格比"你偏好"更重要。
2. 文件通常 200 行、上限 500 行最易理解；小文件优于大文件。
3. 垂直上：变量近用、被调在下、亲和簇相邻、自上而下流动；水平上：短行、按优先级留白、勿做对齐。
4. 团队统一规则并交给工具自动执行，比个人英雄主义更重要。

## Connects To
- **Ch 2 (Meaningful Names)**: 命名与格式化同为"可读即沟通"的体现。
- **Ch 6 (Objects and Data Structures)**: 实例变量位置约定影响封装与可读性。
- **Uncle Bob's Formatting Rules (Listing 5-6)**: 本章标准即"代码本身是最好的编码规范文档"。
