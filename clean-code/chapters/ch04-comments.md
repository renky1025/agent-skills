# Chapter 4: Comments

## Core Idea
Comments are, at best, a necessary evil—they compensate for our failure to express intent in code, and they lie because code changes while comments drift. Express yourself in code; minimize comments.

## Frameworks Introduced
- **Comments Do Not Make Up for Bad Code**: When you feel the urge to comment a confusing module, clean the code instead. Clear, expressive code with few comments beats cluttered code with many comments.
  - When to use: Whenever you reach for a comment to explain a mess.
  - How: Refactor the mess first; spend the energy cleaning, not documenting.
- **Explain Yourself in Code**: Replace explanatory comments with code that says the same thing—usually by extracting a well-named function or variable.
  - When to use: When a comment describes what the code computes.
  - How: `if (employee.isEligibleForFullBenefits())` instead of `// Check to see if the employee is eligible for full benefits` plus a flag bitwise check.
- **Good Comments (the acceptable set)**: legal, informative, explanation of intent, clarification, warning of consequences, TODO, amplification, Javadocs for public APIs. Even these should be minimal; the best comment is the one you found a way not to write.
  - When to use: Only when code genuinely cannot carry the information.
  - How: Use them sparingly and keep them accurate and local.
- **Bad Comments (the default category)**: mumbling, redundant, misleading, mandated, journal, noise, position markers, closing-brace comments, attributions, commented-out code, HTML, nonlocal info, too much info, inobvious connection. Most comments fall here.
  - When to use: Never.
  - How: Delete or refactor them away; if a comment is needed, prefer a function or variable.

## Key Concepts
- **Legal Comments**: Copyright/authorship headers required by corporate standards; keep them short and point to an external license rather than embedding terms.
- **Informative Comments**: Basic info a function returns (e.g., what an abstract method yields); often better replaced by a better name (responderBeingTested).
- **Explanation of Intent**: A comment documenting why a decision was made, not just what—e.g., `return 1; // we are greater because we are the right type`.
- **Clarification**: Translating an obscure library argument/return value into something readable when you cannot alter the code; risky because it can be wrong—verify accuracy.
- **Warning of Consequences**: Alerting others to a costly or unsafe behavior (e.g., SimpleDateFormat is not thread safe; don't use a static instance).
- **TODO Comments**: Notes for work the programmer intends but cannot do now; not an excuse to leave bad code. Scan and delete them regularly.
- **Amplification**: Emphasizing the importance of something inconsequential (the `trim()` prevents an item being misread as a list).
- **Javadocs in Public APIs**: Worth writing for public APIs, but they can mislead/be nonlocal just like any other comment.
- **Noise Comments**: Restate the obvious (`/** Default constructor. */`, `/** The day of the month. */`) and eventually lie as code changes.

## Mental Models
- Use a function or variable instead of a comment when the comment merely restates logic—`if (moduleDependees.contains(ourSubSystem))` removes the need to explain the condition.
- Prefer explaining intent in code via a descriptively named function over a comment that will drift from the code it describes.
- Keep any necessary comment local and accurate; a comment describing distant systemwide behavior (the default port) is nonlocal and will rot.
- Treat TODOs as a tracked backlog, not as permission to leave a mess; prune them on a regular pass.

## Anti-patterns
- **Mumbling**: A comment written in a hurry that obscures meaning (`// No properties files means all defaults are loaded`—who loads them, and when?). Forces the reader to hunt in other modules.
- **Redundant Comments**: A header that is less precise than the code and slower to read (Listing 4-1 waitForClose); the legion of useless Javadocs in Tomcat's ContainerBase.
- **Misleading Comments**: A comment that is subtly wrong—waitForClose "returns when this.closed is true" but actually waits a blind timeout then throws; another dev will misuse it.
- **Mandated Comments**: Rules forcing a Javadoc on every function/variable produce abominations (Listing 4-3 addCD) that clutter and invite lies.
- **Journal Comments**: Per-edit change logs at the top of a module; obsolete since source control tracks history.
- **Noise Comments**: `/** Default constructor. */`, `/** The name. */`, and copy-paste errors (`/** The version. */` on the info field).
- **Position Markers / Closing-Brace Comments**: `// Actions //////////////////` and `} //while` clutter; shorten functions instead.
- **Attributions / Bylines**: `/* Added by Rick */`—source control already knows; they rot.
- **Commented-Out Code**: Dead code left in place gathers like dregs; delete it, source control remembers.
- **HTML Comments**: Embedding HTML in source comments is unreadable in the editor; let doc tools add markup.
- **Nonlocal / Too Much Info / Inobvious Connection**: A Javadoc stating the default port (which the function can't control); pasting the full RFC 2045 Base64 spec; a comment about "filter bytes" with no clear tie to the +1 or *3.

## Code Examples
```java
// Check to see if the employee is eligible for full benefits
if ((employee.flags & HOURLY_FLAG) &&
    (employee.age > 65))
```
versus the code-only rewrite:
```java
if (employee.isEligibleForFullBenefits())
```
- **What it demonstrates**: A comment explaining intent is better expressed as a function whose name carries the intent—no comment needed.

## Worked Example
Kernighan & Plauger: "Don't comment bad code—rewrite it." The GeneratePrimes module (Listing 4-7) was once considered "well documented"; now it reads as a small mess:

BEFORE (Listing 4-7, comment-heavy):
```java
/**
 * This class Generates prime numbers up to a user specified
 * maximum.  The algorithm used is the Sieve of Eratosthenes.
 * <p> Eratosthenes of Cyrene, b. c. 276 BC ... calculated the
 * circumference of the Earth ...
 * @author Alphonse  @version 13 Feb 2002 atp
 */
public static int[] generatePrimes(int maxValue) {
  if (maxValue >= 2) { // the only valid case
    // declarations
    int s = maxValue + 1;
    boolean[] f = new boolean[s];
    // initialize array to true.
    for (int i = 0; i < s; i++) f[i] = true;
    // get rid of known non-primes
    f[0] = f[1] = false;
    // sieve
    for (int i = 2; i < Math.sqrt(s) + 1; i++) {
      if (f[i]) { // if i is uncrossed, cross its multiples.
        for (int j = 2 * i; j < s; j += i)
          f[j] = false; // multiple is not prime
      }
    }
    // how many primes are there?  ...  // move the primes into the result
    // ...
    return primes;  // return the primes
  } else return new int[0]; // return null array if bad input.
}
```

AFTER (Listing 4-8, refactored—only two explanatory comments remain, the code tells the story):
```java
public class PrimeGenerator {
  private static boolean[] crossedOut;
  private static int[] result;
  public static int[] generatePrimes(int maxValue) {
    if (maxValue < 2) return new int[0];
    uncrossIntegersUpTo(maxValue);
    crossOutMultiples();
    putUncrossedIntegersIntoResult();
    return result;
  }
  private static int determineIterationLimit() {
    // Every multiple in the array has a prime factor that
    // is less than or equal to the root of the array size,
    // so we don't have to cross out multiples of numbers
    // larger than that root.
    return (int) Math.sqrt(crossedOut.length);
  }
  // ... each step extracted into a one-thing function ...
}
```
The refactor deletes the biography, the journal-style header, the per-line narration, and the redundant trailing comments; only the square-root rationale survives because no name or structure made it clear.

## Key Takeaways
1. Comments are failures of expression—first try to say it in code (extract a function/variable) before writing a comment.
2. Good comments are rare and limited to legal, informative, intent, clarification, warning, TODO, amplification, and public-API Javadocs; the best comment is the one omitted.
3. Avoid bad comments wholesale: mumbling, redundancy, misleading text, mandated Javadocs, journals, noise, position markers, bylines, and commented-out code.
4. Keep any necessary comment local and accurate; nonlocal info (default port), too much info (RFC dumps), and inobvious connections rot fastest.
5. Don't comment bad code—rewrite it; let small named functions replace explanatory comments.

## Connects To
- **Ch 3 (Functions)**: Small, well-named functions express intent in code, eliminating the need for explanatory comments.
- **Ch 5 (Formatting)**: Vertical density and ordering keep code readable so comments aren't needed as crutches.
- **DRY**: Commented-out code and journal comments are duplication/rot that source control already handles.
- **SRP**: Mandated comment rules and noisy Javadocs violate the spirit of clean, single-purpose modules.
