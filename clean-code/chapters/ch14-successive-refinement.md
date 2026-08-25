# Chapter 14: Successive Refinement

## Core Idea
写干净代码的第一遍一定是"脏代码"——先让它跑起来（getting it working），再通过 successive refinement（逐步精炼）把它清理成结构干净的程序。专业程序员不会把初稿留给下一个维护者。

## Frameworks Introduced
- **Successive Refinement（逐步精炼）**: 把"让程序工作"和"让程序干净"拆成两个正交阶段。初稿只求行为正确，精炼阶段在测试保护下反复小步改写。
  - When to use: 任何无法一眼看出最优设计的模块（如命令行解析、协议解析、多种类型分支）。
  - How: ① 先写 rough draft 让测试通过；② 停止加功能，转入重构；③ 每次只做最小改动且保持测试绿；④ 重复直到结构满意。
- **ArgumentMarshaler 抽象（类型分派封装）**: 把"每种参数类型需要的三处代码（parse schema / parse argument string / getXXX）"收敛到一个类层次中。
  - When to use: 当同一类概念有 N 种变体，且每加一种变体都要在 M 个地方复制代码时。
  - How: 定义 `interface ArgumentMarshaler { void set(Iterator<String>) throws ArgsException; }`，每种类型为它的派生类；`Args` 只持有一张 `Map<Character, ArgumentMarshaler>`。
- **TDD 纪律（保持系统一直运行）**: 每个改动都必须让既有测试继续通过，绝不允许系统处于"broken"状态。
  - When to use: 进行结构性重构、准备删除/迁移大块代码时。
  - How: 备好 unit tests（JUnit）+ acceptance tests（FitNesse），每次小改后立刻跑；测试挂了先恢复绿，再继续下一步。
- **Incrementalism（小步前进）**: 避免一次性大规模结构重写——那种"改进"常让程序再也回不到原行为。
  - When to use: 要替换核心数据结构或继承体系时。
  - How: 先并行引入新结构（如新增 `marshalers` map），再一处一处把旧调用迁过去，最后删除旧结构。

## Key Concepts
- **Rough Draft（初稿）**: 第一版只为工作的代码，允许混乱、变量多、分支脏。
- **Festering Pile（化脓的垃圾堆）**: 每增量加一个功能就变丑一点的代码，靠"两三个同类 map + type-case"堆叠而成。
- **Marshalling（编组）**: 把命令行字符串参数解析并转换成目标类型（boolean/int/String…）的过程。
- **Type-case（类型分支）**: 用 `instanceof` 在 `setArgument` 里对每种 Marshal 分派，是待消除的坏味道。
- **Iterator 传递（Collecting via Iterator）**: 把 `String[]` 包成 `List` 传 `ListIterator<String>` 给 `set`，避免给每个 Marshal 传两个散参（`args` + `currentArg`）。
- **Deploy to derivative（向派生类下沉）**: 先把行为堆在基类，再逐步把 `set`/`get` 推到各具体派生类，并删除基类里的空方法。

## Mental Models
- Use **rough draft first** when 你还没想清最优结构——先求行为正确，再求干净。
- Use **TDD + 小步提交** when 你要改动核心结构——每次改动保持测试绿，才能无恐惧重构。
- Use **ArgumentMarshaler 抽象** when 同类功能有 N 种变体且每加一种都要改 M 个地方——把"类型分支"换成"对象多态"。
- Use **Iterator 而非多散参** when 派生类需要访问遍历状态——传一个 `Iterator<String>` 比传 `args` + `index` 两个参数更干净 ([F1])。

## Anti-patterns
- **留下 rough draft 当成品**: 别人读你的初稿也会觉得"幸亏他没留成这样"。初稿=专业自杀。
- **大规模一次性结构重写（big-bang refactor）**: 很难让系统恢复原有行为，很多程序就此无法恢复。
- **为每种类型维护独立 Map（booleanArgs / stringArgs / intArgs）**: 三个 map 同步脆弱，加类型要改四处；应合并为单一 `marshalers` map。
- **type-case 分派 + 散落异常管理**: `setArgument` 里 `instanceof` 链加 try/catch 既丑又重复，应把异常埋进各 Marshal 的 `set`。
- **把迭代状态作为两个独立成员变量传参**: `args[]` + `currentArgument` 下推到派生类很脏，应改为传单一 `Iterator`。

## Code Examples
```java
public class Args {
  private Map<Character, ArgumentMarshaler> marshalers;
  private Set<Character> argsFound;
  private ListIterator<String> currentArgument;

  public Args(String schema, String[] args) throws ArgsException {
    marshalers = new HashMap<>();
    argsFound = new HashSet<>();
    parseSchema(schema);
    parseArgumentStrings(Arrays.asList(args));
  }
  private void parseSchemaElement(String element) throws ArgsException {
    char id = element.charAt(0);
    String tail = element.substring(1);
    if (tail.length() == 0)      marshalers.put(id, new BooleanArgumentMarshaler());
    else if (tail.equals("*"))   marshalers.put(id, new StringArgumentMarshaler());
    else if (tail.equals("#"))   marshalers.put(id, new IntegerArgumentMarshaler());
    else throw new ArgsException(INVALID_ARGUMENT_FORMAT, id, tail);
  }
  public boolean getBoolean(char arg) {
    return BooleanArgumentMarshaler.getValue(marshalers.get(arg));
  }
}
```
- **What it demonstrates**: 精炼后的 `Args`——单一 `marshalers` map、`parseSchemaElement` 只是选择 Marshal 子类、getter 委托给各 Marshal 的静态 `getValue`，无 type-case。

```java
public interface ArgumentMarshaler {
  void set(Iterator<String> currentArgument) throws ArgsException;
}
public class IntegerArgumentMarshaler implements ArgumentMarshaler {
  private int intValue = 0;
  public void set(Iterator<String> currentArgument) throws ArgsException {
    String parameter = currentArgument.next();
    try { intValue = Integer.parseInt(parameter); }
    catch (NoSuchElementException e) { throw new ArgsException(MISSING_INTEGER); }
    catch (NumberFormatException e)  { throw new ArgsException(INVALID_INTEGER, parameter); }
  }
  public static int getValue(ArgumentMarshaler am) {
    return (am instanceof IntegerArgumentMarshaler) ? ((IntegerArgumentMarshaler)am).intValue : 0;
  }
}
```
- **What it demonstrates**: `NumberFormatException` 被埋进 `IntegerArgumentMarshaler` 内部，调用方永远看不到类型转换细节。

## Worked Example
**Args 工具的逐步重构（Uncle Bob 的真实演进）**

1. **初稿（Listing 14-8）**：`booleanArgs/stringArgs/intArgs` 三张独立 `Map`，外加 `valid`、`errorArgumentId`、`unexpectedArguments` 等一堆成员变量；`setArgument` 用 `isBooleanArg/isStringArg/isIntArg` + `instanceof` 风格分支；`parseArguments` 用裸 `ArrayIndexOutOfBoundsException` 兜错。能工作，但是 festering pile。
2. **只支持 Boolean 的更早版本（Listing 14-9）**说明：脏只源于增量——只多加了 String 和 Integer 两种类型，代码就从"还行"塌成"难维护"。
3. **转折点 "So I Stopped"**：再加两种类型会让堆更大无法收拾，于是停加功能、开始重构。观察到"每加一种类型要在 parse / set / get 三处加代码"→ 这呼唤一个类 → **ArgumentMarshaler 概念诞生**。
4. **小步重构序列（每次保持测试绿）**：
   - 先在 `Args` 末尾挂 `ArgumentMarshaler` 骨架（含 `Boolean/Integer/String` 内部派生类），不破坏任何东西。
   - 把 `booleanArgs` 的 value 类型从 `Boolean` 改为 `ArgumentMarshaler`，修几处报错；发现 `getBoolean` 在 key 不存在时 `NullPointerException` → 把 null 检查从"boolean 是否为 null"改为"Marshaler 是否为 null"。
   - 同样把 String、Integer 的 map 改掉，把 `setString/setInteger` 行为先堆进基类。
   - **向派生类下沉**：把 `set` 做成 `abstract`，在 `BooleanArgumentMarshaler` 实现 `set("true")`；再把 `get` 做成 `abstract`（返回 `Object`），各自实现；删除基类里被取代的 `setBoolean/getBoolean` 等，把 `booleanValue` 等字段下移到派生类并改 `private`。
   - **合并三张 map**：新增 `marshalers` map，逐个方法把 `booleanArgs.get` 换成 `marshalers.get`，并把 `isBooleanArg` 改为 `m instanceof BooleanArgumentMarshaler`；逐步 inline 掉 `isXxxArg` 辅助方法，最后删掉三张旧 map。
   - **消除 type-case**：把 `args` 数组转 `List`、传 `ListIterator<String>` 给 `set`（`args` + `currentArg` 两个散参 → 一个 Iterator，[F1]）；把 `setIntArg/setStringArg/setBooleanArg` 整段下推进各自 `ArgumentMarshaler.set`，`Args` 的 `setArgument` 只剩 `m.set(currentArgument)` + 一层 try/catch。
   - 顺带：FitNesse acceptance test 暴露了 `getBoolean` 在错误类型上应返回 `false` 的需求（unit test 没覆盖），于是加 `ClassCastException` 兜底，并补一个跑全部 FitNesse 的 unit test。
5. **最终形态（Listing 14-2）**：`Args` 持单一张 `marshalers` map；`parseSchemaElement` 只做"按 tail 选 Marshal 子类"；每个 `getXXX` 委托 `XxxArgumentMarshaler.getValue(am)`；类型转换与异常全埋进各 Marshal。加新类型只需：新派生类 + 新 `getXXX` + `parseSchemaElement` 里一个 `else if` + 新 `ErrorCode`。

**重构纪律要点**：小步到像解 Rubik's cube——先把东西放进去（`set(String)` 与 `set(Iterator)` 并存）再拿出来；每一步都跑测试；靠"系统一直能跑"消除对大改的恐惧。

## Key Takeaways
1. 干净代码不是一次写成的：先写 dirty code，再 successive refinement。
2. 用 TDD + 小步提交把"重构风险"降到零：每步都保持测试绿，broken 状态绝不留。
3. 当"加一种变体要改 M 个地方"时，抽象出一个类层次（如 ArgumentMarshaler）替代 type-case。
4. 合并平行的同类数据结构（多张 map）为单一多态容器，是消除散落分支的利器。
5. 把遍历状态包成 `Iterator` 下推，比传多个散参更干净；把异常埋进最具体的类。
6. 别留下 rough draft——你讨厌别人留的初稿，别人也讨厌你留的。

## Connects To
- **Ch 1 (Clean Code)**: rough draft → clean code 是全书主旨的实操化。
- **Ch 5 (Formatting) / Ch 2 (Meaningful Names)**: 精炼时重命名（`fExpected`→`expected`、消除 `this.` 歧义）是每一步的伴随动作。
- **Ch 6 (Objects & Data Structures)**: ArgumentMarshaler 用多态取代 `instanceof` 类型分支。
- **Ch 15 (JUnit Internals)**: 同一套 successive refinement + Boy Scout Rule 用于 ComparisonCompactor。
