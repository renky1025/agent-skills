# Chapter 11: Systems

## Core Idea
A system must be clean at every level of abstraction: separate the concern of *constructing* objects from the concern of *using* them, and keep domain logic as decoupled POJOs wrapped noninvasively by aspects. An invasive architecture overwhelms the domain and kills agility.

## Frameworks Introduced
- **Separation of Constructing from Using**: The startup process (object construction + dependency wiring) is a distinct concern from runtime logic. Modularize it separately with a global, consistent strategy.
  - When to use: Any application past a few classes. Construction logic mixed into runtime breaks SRP and scatters the global setup strategy.
  - How: Move construction to `main` (or modules called by `main`); the application assumes everything is already built and wired.

- **Separation of Main**: Push all construction into `main`; the application side has zero knowledge of `main` or the construction process. Dependency arrows point one way, away from `main`.
  - When to use: You want the runtime code free of "how was this built" knowledge.
  - How: `main` builds objects, then passes them to the application.

- **Abstract Factory**: Gives the application control of *when* to build, while keeping *how* separate on the `main` side.
  - When to use: The app must decide timing/arguments of creation (e.g. `LineItem` in an `Order`), but shouldn't know construction details.
  - How: Inject a factory; app calls `factory.create(...)`, implementation lives on the main side.

- **Dependency Injection (DI) / Inversion of Control (IoC)**: An object takes no direct steps to resolve its dependencies — it is passive, receiving them via constructor args or setters; a container wires them during construction.
  - When to use: An object should not instantiate its own dependencies (supports SRP). True DI > JNDI lookup (which is "partial" — the caller still actively resolves).
  - How: Declare deps as constructor args/setters; a DI container (e.g. Spring) instantiates and wires via config file or construction module. Lazy-init is still an available optimization inside DI.

- **Aspect-Oriented Programming (AOP)**: Modular constructs called *aspects* specify system-wide behavior modifications (persistence, transactions, security) noninvasively — i.e. without editing target source.
  - When to use: A concern *cuts across* natural object boundaries and would otherwise be duplicated in many objects (cross-cutting concern).
  - How (three Java mechanisms, escalating power):
    1. **Java Proxies** (JDK `Proxy`/`InvocationHandler`): only wrap interfaces; verbose, no system-wide pointcut spec. Use bytecode libs (CGLIB/ASM/Javassist) for classes.
    2. **Pure Java AOP** (Spring AOP, JBoss AOP): auto-generate the proxy boilerplate; you write POJOs + declarative XML/annotations. The client sees a "Russian doll" of nested Decorators (Bank → DAO → DataSource).
    3. **AspectJ**: first-class aspect language, richest toolset, needs new tools/idioms; annotation form lowers the barrier.

- **Test Drive the System Architecture**: POJOs decoupled from architecture let you evolve architecture via TDD from simple → sophisticated; **avoid BDUF** (Big Design Up Front).
  - When to use: Starting a project — begin "naively simple" but decoupled, add infrastructure as you scale.
  - How: Keep domain logic in POJOs; adopt technologies on demand.

- **Optimize Decision Making**: Postpone decisions to the last responsible moment — premature decisions are made with suboptimal knowledge.
- **Use Standards Wisely**: Adopt a standard only when it adds demonstrable value; don't let hype override customer value.
- **Domain-Specific Languages (DSLs)**: Small languages/APIs that read like domain-expert prose; minimize the communication gap between concept and code.

## Key Concepts
- **Cross-Cutting Concern**: A concern (persistence, transactions, security) that applies across many objects and can't be cleanly isolated without AOP.
- **POJO**: Plain Old Java Object — focused purely on its domain, no dependency on enterprise frameworks; easy to test-drive and reuse.
- **Lazy Initialization / Evaluation**: Defer construction until first use; reduces startup cost but is just an *optimization* (and a premature one if used by default).
- **BDUF**: Big Design Up Front — designing everything before implementing anything; harmful, inhibits adapting to change.
- **Walking Skeleton**: A minimally coupled end-to-end slice that grows infrastructure as needed (vs. building the whole highway up front).

## Mental Models
- **Use Separation of Main** when you want the application code to never know *how* its collaborators were built — construction lives entirely outside runtime.
- **Use Dependency Injection** when an object shouldn't know or instantiate its dependencies; prefer it over JNDI lookup because the class stays completely passive.
- **Use AOP / pure-Java aspects** when a behavior (transactions, caching, persistence) must apply system-wide without invading every class — prefer Spring AOP for 80–90% of cases, AspectJ only when you need real pointcuts.
- **Use a walking skeleton + sprints** when scaling a system from simple to complex; never assume you can "get it right the first time."

## Anti-patterns
- **Scattered Lazy Initialization**: Ad-hoc `if (x == null) x = new Impl()` mixes construction into runtime, hard-codes dependencies (can't compile without them even if unused), breaks SRP, and scatters the global setup strategy with duplication. Worse as an optimization when premature.
- **EJB2 heavyweight container coupling**: Subclassing container types + boilerplate lifecycle methods makes isolated unit testing nearly impossible, blocks reuse outside EJB, and undermines OOP (no bean inheritance, DTO "structs"). Over-engineered.
- **BDUF**: Pre-plans everything; psychological resistance to discarding effort and architecture choices that box in later thinking.

## Code Examples
```java
// LAZY INITIALIZATION — mixes construction with use
public Service getService() {
  if (service == null)
    service = new MyServiceImpl(...);  // Good enough default for most cases?
  return service;
}
```
- **What it demonstrates**: The convenient idiom that hard-codes a dependency, breaks SRP, and scatters setup logic — the very thing Separation of Main / DI is meant to eliminate.

## Worked Example
Reproduce the author's Bank persistence concern. With **EJB2**, `Bank` must implement `EntityBean`, subclass container types, provide empty lifecycle methods (`ejbActivate`, `ejbLoad`, …), do JNDI lookups inside business methods, and ship XML deployment descriptors — business logic is welded to the container, untestable in isolation. Rewritten as a **POJO + Spring AOP**, the domain `Bank` is a plain object; persistence/transactions are added via declarative config, so the client calls `getAccounts()` on what is actually a nested Decorator (Bank → DAO → DataSource) assembled by the DI container. With **EJB3** the same collapses to annotations (`@Entity`, `@Table`, `@OneToMany`) on a clean POJO. The win: identical behavior, but the EJB3/POJO version is test-driveable, reusable, and decoupled.

## Key Takeaways
1. Always separate construction from use — via Separation of Main, Abstract Factory, or Dependency Injection — so runtime code stays single-purpose.
2. Express cross-cutting concerns (persistence, transactions, security) as noninvasive aspects, not duplicated code in every class.
3. Keep domain logic in POJOs so the architecture itself can be test-driven; avoid BDUF.
4. Postpone decisions to the last responsible moment; adopt standards and DSLs only for demonstrable value.

## Connects To
- **Ch 12**: Simple Design's "runs all the tests" is what makes a POJO system test-driveable.
- **Ch 13**: POJOs that know nothing of threading are the same decoupling principle applied to concurrency.
- **Dependency Injection**: A concrete IoC mechanism reinforcing SRP at the system level.
- **AOP**: The tool that restores modularity for cross-cutting concerns.
