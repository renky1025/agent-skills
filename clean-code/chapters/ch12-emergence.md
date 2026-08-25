# Chapter 12: Emergence

## Core Idea
Good design can *emerge* from following Kent Beck's **four rules of Simple Design** in priority order: a system is "simple" when it runs all its tests, contains no duplication, expresses the programmer's intent, and minimizes the number of classes and methods.

## Frameworks Introduced
- **The Four Rules of Simple Design** (in strict priority order):
  1. **Runs all the tests** — the system must be verifiably correct; a non-testable system is not verifiable and arguably should not ship.
  2. **No duplication** — duplication is the primary enemy of good design.
  3. **Expressive** — code clearly states the author's intent.
  4. **Minimal classes and methods** — keep counts low (lowest priority).
  - When to use: Continuously, as the litmus test for every change you make.
  - How: Pass tests first; then refactor to eliminate duplication, increase expressiveness, and trim excess structure — in that order.

- **Test-Driven Emergence (TCR)**: Continuously running all tests is what *empowers* refactoring without fear.
  - When to use: Always — it is rule 1 and the precondition for the other three.
  - How: Write tests; the pressure to test pushes classes toward SRP and low coupling, and toward DIP / DI / interfaces to break tight coupling. "Writing tests leads to better designs."

- **Refactoring Step**: After each few lines, pause and reflect — did this degrade the design? Clean it up and re-run tests to prove nothing broke.
  - When to use: Incrementally, after every small addition.
  - How: Apply the whole body of design knowledge — raise cohesion, lower coupling, separate concerns, shrink functions/classes, rename.

- **Template Method** (GoF): Remove higher-level duplication by fixing the invariant algorithm in a base class and leaving variant steps abstract for subclasses.
  - When to use: Several methods share the same flow but differ in a few steps (e.g. per-region rules).
  - How: Put the skeleton in the base `accrueVacation()`; subclasses fill only `alterForLegalMinimums()`.

- **Reuse in the Small**: Extracting tiny common helpers and elevating them can trigger large-scale reuse — understanding small-scale reuse is prerequisite to large-scale reuse.

## Key Concepts
- **Four Rules of Simple Design**: The prioritized checklist (tests → no dup → expressive → minimal) that lets good design emerge.
- **Duplication**: Not just identical lines — similar code massaged to look alike, or duplicated *implementation* (two methods tracking the same fact differently).
- **Expressive**: Code that makes the author's intent obvious — via good names, small functions/classes, standard pattern names (COMMAND, VISITOR), and expressive tests that double as documentation.
- **Reuse in the Small**: Extracting and elevating a tiny common method so others can discover and reuse it elsewhere.

## Mental Models
- **Use "run all tests" as the gate** when you're about to refactor — it is the only thing that removes the fear of breaking working code, and it pulls the design toward SRP/low coupling.
- **Prefer eliminating duplication over adding abstraction** — but when two methods share a flow with one variant, reach for Template Method rather than copy-paste.
- **Use expressive names and pattern names** when you want the next reader (often future-you) to understand intent fast and ship fewer defects.
- **Keep classes/methods minimal, but treat it as the lowest-priority rule** — tests, no-dup, and expressiveness always win.

## Anti-patterns
- **Pointless dogmatism**: Insisting on an interface for every class, or always splitting fields from behavior into data/behavior classes. This inflates class counts for no benefit and violates the "minimal" rule.
- **Over-extracting into tiny classes/methods**: Taking SRP/expressiveness too far creates needless micro-structure; balance with the minimal-classes rule.

## Code Examples
```java
// BEFORE: duplication between scale and rotate
public void scaleToOneDimension(float desired, float imageDim) {
  if (Math.abs(desired - imageDim) < errorThreshold) return;
  float sf = desired / imageDim;
  sf = (float)(Math.floor(sf * 100) * 0.01f);
  RenderedOp newImage = ImageUtilities.getScaledImage(image, sf, sf);
  image.dispose(); System.gc(); image = newImage;
}
public synchronized void rotate(int degrees) {
  RenderedOp newImage = ImageUtilities.getRotatedImage(image, degrees);
  image.dispose(); System.gc(); image = newImage;
}
// AFTER: extract the common disposal/replace
private void replaceImage(RenderedOp newImage) {
  image.dispose(); System.gc(); image = newImage;
}
```
- **What it demonstrates**: Eliminating small duplication (here the dispose/GC/reassign block) reveals SRP violations and enables "reuse in the small."

## Worked Example
The author shows `scaleToOneDimension` and `rotate` each repeating `image.dispose(); System.gc(); image = newImage;`. Extract that into a private `replaceImage(RenderedOp)` helper called by both; `rotate` and `scaleToOneDimension` shrink to a single operation each. This tiny extraction surfaces that `replaceImage` might belong in another class (SRP), and elevating it lets a teammate reuse it elsewhere — complexity shrinks from the bottom up. The higher-level analog is `VacationPolicy`: `accrueUSDivisionVacation` and `accrueEUDivisionVacation` share the calc→minimums→payroll flow; Template Method moves the skeleton to `accrueVacation()` and leaves only `alterForLegalMinimums()` abstract, so subclasses supply just the non-duplicated part.

## Key Takeaways
1. Treat "runs all the tests" as the top-priority rule — it is what makes safe, continuous refactoring possible.
2. Hunt duplication relentlessly, including duplicated *implementation*; extraction at the smallest scale compounds into large-scale reuse.
3. Buy expressiveness with good names, small units, and standard pattern names; expressive tests are documentation.
4. Respect "minimal classes/methods" last — never let dogmatic micro-structure override tests, no-dup, and clarity.

## Connects To
- **Ch 11**: Test-driving the architecture depends on the same "runs all the tests" discipline at the system level.
- **Ch 13**: Concurrency code defended by SRP is the same principle — isolate the hard-to-change concern.
- **SRP / DIP / DI**: Forced upon you by the need to keep code testable and duplication-free.
- **Template Method**: The canonical tool for removing higher-level duplication.
