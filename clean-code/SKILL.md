---
name: clean-code
description: >
  Knowledge base distilled from "Clean Code: A Handbook of Agile Software
  Craftsmanship" by Robert C. Martin (Uncle Bob). Use when applying Uncle Bob's
  frameworks for meaningful names, small functions, comments, formatting,
  objects vs data structures, error handling, boundaries, unit tests / TDD,
  class design (SRP), systems, concurrency, refactoring, and code smells;
  studying the book; or referencing its concepts during code review, cleanup,
  or TDD work.
triggers:
  - clean code: 整洁代码/代码整洁/clean code/refactor/重构/代码质量
  - naming: 命名/meaningful names/变量名/函数名/类名/命名规范
  - functions: 函数设计/小函数/do one thing/参数/函数拆分
  - comments: 注释/comments/该不该写注释
  - tdd: TDD/单元测试/unit test/测试驱动/clean tests
  - error handling: 异常处理/error handling/异常设计
  - code smell: 代码味道/code smell/坏味道/反模式/review
  - design: SRP/面向对象/类设计/对象与数据结构/并发
---

# Clean Code
**Author**: Robert C. Martin (Uncle Bob) | **Pages**: ~462 | **Chapters**: 17 | **Generated**: 2026-08-24

## How to Use This Skill

- **No arguments** — load core frameworks for reference (this file's Core Frameworks section).
- **With a topic** — ask about `naming`, `functions`, `comments`, `TDD`, `error handling`, `code smells`, etc.; I find and read the relevant chapter.
- **With a chapter** — ask for `ch03` (functions) or `ch17` (smells); I load that specific chapter file.
- **Browse** — ask "what chapters do you have?" to see the full index.

When you ask about a topic not covered in the Core Frameworks below, I will read
the relevant chapter file before answering, grounded in the book's actual content.

**Language-agnostic:** The principles in this skill are universal software-engineering
truths, not Java rules. The book happens to use Java for its code examples, but naming,
functions, comments, SRP, TDD, error handling, concurrency, and code smells apply to
every language. When you name a language (e.g. "in Rust", "in Go"), I will translate
the advice to that language using [appendix-lang-map.md](appendix-lang-map.md) instead
of quoting Java syntax.

---

## Core Frameworks & Mental Models

Clean Code is a discipline of *care*: code is read far more than it is written
(reading:writing ≈ 10:1), so optimize for the reader. Below are the author's
named, reusable frameworks — apply them, don't just recall them.

**Professionalism & attitude**
- **The Boy Scout Rule** — Leave the campground cleaner than you found it. Every check-in makes one small, safe improvement (rename, extract, de-dupe). Cumulatively this prevents rot; you never need a "Grand Redesign in the Sky".
- **LeBlanc's law** — "Later equals never." Refactoring deferred to "later" is refactoring never done. Fix it where you stand.
- **The Primal Conundrum** — Making a mess to hit a deadline *guarantees* you miss it; the only way to go fast is to keep the code clean. Refuse requirements that force chaos (Semmelweis hand-washing analogy).

**Naming (Ch 2)**
- **Use Intention-Revealing Names** — a name should answer why it exists, what it does, how it is used. `int daysSinceCreation` > `int d`.
- **Avoid Disinformation / Encodings** — no `aix`/`sz` noise, no Hungarian `m_`, no type encodings (`strName`) — the language/IDE already knows types.
- **Make Meaningful Distinctions / Pronounceable / Searchable names** — `source` vs `destination`, not `a1`/`a2`; `Customer` not `Cust`.
- **One word per concept** — don't mix `fetch`/`get`/`retrieve` for the same idea.

**Functions (Ch 3)**
- **Small! + Do One Thing** — a function does one thing, does it well, does it only. Steps inside it are one level of abstraction below its name.
- **The Step-down Rule** — code reads top-down like a narrative; each function is followed by the next level of detail.
- **Few arguments (≤ 3)** — niladic > monadic > dyadic > triadic; avoid output arguments (mutate the receiver, not a param); **no flag arguments** (a boolean means the function does two things — split it).
- **Command-Query Separation** — either do something or answer something, not both.
- **Don't repeat yourself** — duplication is a missed abstraction; DRY at function level first.

**Comments (Ch 4)**
- **Comments do not make up for bad code** — express intent in code, not in commentary.
- **Good comments only**: legal/license, informative, explanation of intent, clarification, warning of consequences, TODO (with discipline), amplification of importance, javadoc for public APIs.
- **Bad comments**: mumbling, redundant, misleading, mandated noise, journal/change-history, position markers, commented-out code (delete it — VCS remembers).

**Formatting (Ch 5)**
- **The Newspaper Metaphor** — a source file reads like a newspaper: headline (name) first, high-level concepts, details downward.
- **Vertical Distance / Ordering** — declare variables and private helpers close to where they are used; callable functions sit above the functions that call them.

**Objects vs Data Structures (Ch 6)**
- **Data/Object Anti-Symmetry** — objects hide data and expose behavior; data structures expose data and have no meaningful behavior. Don't force one into the other.
- **The Law of Demeter (shy code)** — a method should talk only to its friends, not friends-of-friends: avoid `a.getB().getC().doX()`. Use adapters/helpers to expose needed services.

**Error Handling (Ch 7)**
- **Use Exceptions, not return codes** — write `try-catch-finally` first; wrap third-party APIs so you control the boundary.
- **Special Case Pattern** — return a special object (e.g. a null-safe implementation) instead of `null`.
- **Never return null; never pass null** — both are an Open Invitation to a null-reference crash.

**Boundaries (Ch 8)**
- **Learning Tests** — write tests against third-party APIs you adopt to lock in behavior and detect version drift.
- **Adapter at the boundary** — hide foreign interfaces (e.g. `Map`) behind your own small types.

**Unit Tests (Ch 9)**
- **The Three Laws of TDD** — (1) write no production code until a failing test exists; (2) write only enough test to fail; (3) write only enough production code to pass.
- **F.I.R.S.T.** — tests are Fast, Independent, Repeatable, Self-Validating, Timely.
- **Tests are as clean as production** — no duplication, one concept per test; messy tests rot the suite and kill the safety net.

**Classes (Ch 10)**
- **Single Responsibility Principle (SRP)** — a class has one reason to change; small classes with high cohesion.
- **Organize for change** — isolate likely-varying parts behind interfaces/factories.

**Systems (Ch 11)**
- **Separate constructing a system from using it** — `main` builds, the rest runs; use Dependency Injection / Abstract Factory so modules don't know how their collaborators are made.

**Emergence / Simple Design (Ch 12)**
- **The Four Rules of Simple Design** (in priority order): (1) passes all tests; (2) contains no duplication; (3) expresses intent (small, well-named); (4) minimizes classes/methods. Test-driven emergence: keep the system running green while refining.

**Concurrency (Ch 13)**
- **SRP + Concurrency** — keep concurrent code and non-concurrent code in separate classes.
- **Limit the scope of data / Use copies / Threads move data** — share as little mutable state as possible; confine data to single threads or use immutable copies.

**Smells & Heuristics (Ch 17)**
- **DRY [G5]**, **ONE SWITCH rule [G23]** (at most one switch per type, producing polymorphic objects), **Feature Envy [G14]** (a method reaches into another object's data — move it), **Magic Numbers [G25]**, **Selector Arguments [G15]**. Use the C/E/F/G/J/N/T taxonomy as a review checklist.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-clean-code.md) | Clean Code | Boy Scout Rule, LeBlanc's law, code-sense |
| [ch02](chapters/ch02-meaningful-names.md) | Meaningful Names | Intention-Revealing, Avoid Encoding, One Word/Concept |
| [ch03](chapters/ch03-functions.md) | Functions | Small/Do One Thing, Step-down Rule, CQS, ≤3 args |
| [ch04](chapters/ch04-comments.md) | Comments | Comments ≠ bad code, Good vs Bad comments |
| [ch05](chapters/ch05-formatting.md) | Formatting | Newspaper Metaphor, Vertical Distance/Ordering |
| [ch06](chapters/ch06-objects-and-data-structures.md) | Objects and Data Structures | Data/Object Anti-Symmetry, Law of Demeter |
| [ch07](chapters/ch07-error-handling.md) | Error Handling | Exceptions > return codes, Special Case, no null |
| [ch08](chapters/ch08-boundaries.md) | Boundaries | Learning Tests, Adapter Pattern |
| [ch09](chapters/ch09-unit-tests.md) | Unit Tests | Three Laws of TDD, F.I.R.S.T., BUILD-OPERATE-CHECK |
| [ch10](chapters/ch10-classes.md) | Classes | SRP, Cohesion, Organize for Change |
| [ch11](chapters/ch11-systems.md) | Systems | Separate Construct/Use, DI, Abstract Factory |
| [ch12](chapters/ch12-emergence.md) | Emergence | Four Rules of Simple Design, TCR |
| [ch13](chapters/ch13-concurrency.md) | Concurrency | SRP+Concurrency, Limit Scope of Data, Copies |
| [ch14](chapters/ch14-successive-refinement.md) | Successive Refinement | Args case study, incremental refactoring |
| [ch15](chapters/ch15-junit-internals.md) | JUnit Internals | Boy Scout Rule, Extract Method, Collecting Parameter |
| [ch16](chapters/ch16-refactoring-serialdate.md) | Refactoring SerialDate | enum over int, Abstract Factory, Feature Envy fix |
| [ch17](chapters/ch17-smells-and-heuristics.md) | Smells and Heuristics | C/E/F/G/J/N/T taxonomy, DRY, ONE SWITCH |

## Topic Index

- **Naming** → ch02
- **Functions / Do One Thing / CQS** → ch03
- **Comments** → ch04
- **Formatting** → ch05
- **Objects / Data Structures / Demeter** → ch06, ch17
- **Error Handling / Exceptions / null** → ch07
- **Boundaries / Learning Tests** → ch08
- **TDD / Unit Tests / F.I.R.S.T.** → ch09
- **Classes / SRP / Cohesion** → ch10
- **Systems / DI / Factory** → ch11
- **Simple Design** → ch12
- **Concurrency** → ch13
- **Refactoring** → ch14, ch16
- **Code Smells / Heuristics** → ch17
- **Boy Scout Rule** → ch01, ch15
- **DRY** → ch12, ch17
- **Cross-language (TS/Python/C++/Go/Rust)** → appendix-lang-map

## Supporting Files

- [glossary.md](glossary.md) — key terms with definitions and chapter references
- [patterns.md](patterns.md) — techniques and design patterns from the book
- [cheatsheet.md](cheatsheet.md) — decision rules, trade-off matrices, and smell quick-reference
- [appendix-lang-map.md](appendix-lang-map.md) — how to apply the principles in any language (TS/Python/C++/Go/Rust) and which heuristics are Java-specific

---

## Scope & Limits

This skill covers the content of *Clean Code* only. It is a synthesized study
aid (frameworks, principles, anti-patterns, worked examples), not the book text.
For hands-on implementation in your own codebase, combine it with project-specific
tools and your language's conventions. For topics beyond this book (e.g. broader
design patterns, architecture, or language-specific idioms), consult related
skills or ask the agent directly.
