# Chapter 13: Concurrency

## Core Idea
Concurrency is a **decoupling strategy** — it separates *what* gets done from *when* it gets done. It is genuinely hard; defend against its hazards by isolating concurrency code (SRP), narrowing shared-data scope, knowing your library and execution models, and testing aggressively with jiggling.

> **Language note:** 本章所有原则（SRP+并发、限制共享数据作用域、用副本隔离、三大经典模型、jiggling 测试）都是**语言无关**的。下面出现的 `synchronized` / `ConcurrentHashMap` / `Executor` / `Servlet` 仅是 Java 示例；TS / Python / C++ / Go / Rust 的对应并发原语见 [appendix-lang-map.md](appendix-lang-map.md) §4。

## Frameworks Introduced
- **SRP + Concurrency**: Concurrency design is complex enough to be its own reason to change — keep it separate from other code.
  - When to use: Always; concurrency code has its own lifecycle, challenges, and failure modes.
  - How: Split into thread-*ignorant* POJOs (testable outside threads) and small, focused thread-*aware* controllers.

- **Corollary — Limit the Scope of Data**: Protect shared data with `synchronized` critical sections, but keep the number of such sections minimal.
  - When to use: Whenever threads mutate shared state.
  - How: Encapsulate shared data tightly; fewer update points = fewer places to forget guarding (DRY) and fewer failure sources.

- **Corollary — Use Copies of Data**: Avoid sharing by copying objects (read-only, or collect per-thread results then merge in one thread).
  - When to use: When sharing can be eliminated; savings from avoiding intrinsic locks usually beat creation/GC cost.
  - How: Partition data into independent subsets operated on by independent threads.

- **Corollary — Threads as Independent as Possible**: Each thread lives in its own world, using only local variables (Servlet `doGet`/`doPost` model).
  - When to use: Default design goal; only introduce sharing for genuine shared resources (e.g. DB connections).

- **Know Your Library (Java 5+ — illustrative; see appendix §4 for other languages)**: Use thread-safe collections, the `Executor` framework for unrelated tasks, nonblocking solutions, and beware non-thread-safe classes.
  - When to use: Any concurrent work — in Java start with `java.util.concurrent` / `.atomic` / `.locks`; in other languages use the equivalents listed in appendix-lang-map.md §4 (e.g. C++ `std::thread`/`std::mutex`, Go goroutine+channel, Rust `async`/`Mutex`/channel, Python `threading`/`asyncio`).
  - How: Prefer concurrent-safe collections/primitives (Java `ConcurrentHashMap` beats `HashMap` for concurrent R/W + composite ops) over hand-rolled locking.

- **Know Your Execution Models**: Master the vocabulary — `ReentrantLock` (lock acquired/released across methods), `Semaphore` (counted lock), `CountDownLatch` (release after N events), Bound Resources, Mutual Exclusion, Starvation, Deadlock, Livelock; and the three canonical problems: **Producer-Consumer** (bound queue, signal full/empty), **Readers-Writers** (balance throughput vs starvation), **Dining Philosophers** (resource competition → deadlock/livelock).

- **Beware Dependencies Between Synchronized Methods**: Calling more than one synchronized method on a shared object is fragile.
  - When to use: When you must chain multiple methods on a shared object.
  - How: Client-Based Locking, Server-Based Locking (server wraps the sequence), or Adapted Server (intermediary).

- **Keep Synchronized Sections Small**: Locks are expensive; guard only the minimal critical section.
  - When to use: Always — oversized sections raise contention and hurt throughput.

- **Graceful Shutdown Is Hard**: Plan shutdown early; deadlock-prone (parent waiting on a deadlocked child; producer/consumer pair where consumer can't receive the stop signal).

- **Testing Threaded Code**: Write tests that can expose problems; run with varied configs/loads/platforms; never ignore a spurious failure.
  - When to use: Continuously; use pluggable + tunable code, more threads than processors, run on all target platforms, and instrument with **jiggling** (`wait`/`sleep`/`yield`/`priority`, or a `ThreadJigglePoint` aspect) to force rare orderings.

## Key Concepts
- **Concurrency as Decoupling**: Decoupling *what* from *when* improves throughput and structure (many collaborating "computers" vs one main loop).
- **Myths**: (1) concurrency *always* improves performance (only when wait time is sharable); (2) design doesn't change (it changes fundamentally); (3) containers handle it for you (you must still guard shared state).
- **Critical Section**: Any code that must be protected from simultaneous execution for correctness.
- **Non-atomicity**: `++lastIdUsed` is not atomic — many interleavings exist across just one line.
- **Busy Waiting**: Spinning until a condition holds; prefer signaling (latches/queues) over polling.
- **ThreadJigglePoint**: A no-op method whose test impl randomly sleeps/yields to surface ordering bugs.

## Mental Models
- **Use concurrency** when *what* and *when* should be decoupled — e.g. an aggregator hitting many sites, or serving many users concurrently for throughput/response time.
- **Prefer copies of data over sharing** when you can; the lock-avoidance savings usually outweigh allocation cost.
- **Use the Servlet/local-variable model** when each task can carry its own data — threads behave as if alone in the world.
- **Use Producer-Consumer / Readers-Writers / Dining Philosophers** as the template whenever you recognize a queue, a read-heavy shared resource, or competing resources.

## Anti-patterns
- **Myth "concurrency always improves performance"**: It only helps when there is real wait time to share; otherwise it adds overhead and complexity.
- **Calling multiple synchronized methods on one shared object**: Creates subtle inter-method dependencies and breaks correctness; prefer server-based locking.
- **Oversized synchronized sections**: Extending synchronization beyond the minimal critical section increases contention and degrades performance.
- **Ignoring spurious/"one-off" failures**: Threading bugs are rarely repeatable; writing them off hides a faulty foundation.

## Code Examples
```java
// NON-ATOMIC under concurrency — two threads, three possible outcomes
public class X {
   private int lastIdUsed;
   public int getNextId() {
        return ++lastIdUsed;   // not atomic: ~12,870 paths for 2 threads (int)
   }
}
// Shared instance, lastIdUsed=42: outcomes include (43,44), (44,43), or BOTH 43.
```
- **What it demonstrates**: A single line yields many interleavings; without synchronization, two threads can both read 43 and leave `lastIdUsed=43`.

```java
// Testing via jiggling — force rare orderings
public synchronized String nextUrlOrNull() {
    if (hasNext()) {
        ThreadJigglePoint.jiggle();
        String url = urlGenerator.next();
        ThreadJigglePoint.jiggle();
        updateHasNext();
        ThreadJigglePoint.jiggle();
        return url;
    }
    return null;
}
```
- **What it demonstrates**: Instrumentation that randomly sleeps/yields surfaces hidden ordering bugs; production uses a no-op `jiggle()`.

## Worked Example
The author's `X.getNextId()` with `lastIdUsed=42` shared by two threads: correct interleavings give (43,44) or (44,43), but a collision path gives *both* threads 43 with `lastIdUsed=43` — because `++lastIdUsed` is non-atomic (~12,870 execution paths for two threads on an `int`; 2.7M on a `long`). Fix by limiting data scope (`synchronized` on the minimal section) or, better, isolating concurrency. For testing, wrap risky calls in `ThreadJigglePoint.jiggle()` and run the suite thousands of times with random sleep/yield; a failure means the code was already broken, the jiggle merely exposed it. ConTest (IBM) does this automatically.

## Key Takeaways
1. Apply SRP to concurrency — separate thread-aware code from POJOs that know nothing of threads, so each is testable alone.
2. Minimize and encapsulate shared data; prefer copies and independent threads over locking.
3. Know the library (`ConcurrentHashMap`, `Executor`, `java.util.concurrent`) and the three execution models (Producer-Consumer, Readers-Writers, Dining Philosophers).
4. Keep critical sections small, plan graceful shutdown early, and test with jiggling across platforms — never dismiss a spurious failure.

## Connects To
- **Ch 11**: POJOs decoupled from infrastructure are the same isolation idea, now applied to threads.
- **Ch 12**: SRP and "runs all the tests" are the foundations that make concurrent code testable.
- **SRP**: The single most important defense principle for concurrency.
- **Dependency Injection**: Keeps thread-ignorant POJOs injectable and testable outside threads.
