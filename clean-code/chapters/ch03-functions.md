# Chapter 3: Functions

## Core Idea
Functions should be very small, do one thing, and stay at one level of abstraction so the code reads like a top-down narrative. Small functions with good names are the verbs of the domain-specific language your system speaks.

## Frameworks Introduced
- **Small! (size rule)**: The first rule of functions is that they should be small; the second is that they should be smaller than that. Functions should hardly ever be 20 lines long; blocks within if/else/while should be one line (often a function call); indent level should not exceed one or two.
  - When to use: Always. This is the default shape for every function you write.
  - How: When a block grows beyond one line, extract the line into a descriptively named function; when the function nests structures, split it.
- **Do One Thing**: A function does one thing if it only performs steps that are one level of abstraction below its stated name. If you can extract another function whose name is not merely a restatement of the implementation, the original was doing more than one thing.
  - When to use: When judging whether a function is cohesive.
  - How: Write the function as a brief TO paragraph; each step should sit one level below the function's name. A function divided into "sections" (declarations, initializations, sieve) is a symptom of doing more than one thing.
- **One Level of Abstraction per Function**: All statements in a function must sit at the same level of abstraction. Mixing high-level concepts (getHtml()) with low-level details (.append("\n")) confuses readers and invites more detail to accrete.
  - When to use: When reviewing a function for readability.
  - How: Push details down into callees; keep the function at a single conceptual altitude.
- **The Step-down Rule**: Code should read top-to-bottom like a set of TO paragraphs; each function is followed by those at the next level of abstraction, descending one level at a time as you read down.
  - When to use: When ordering functions within a module.
  - How: Make each function introduce the next, staying at a consistent level of abstraction—this is the key technique for keeping functions short and doing one thing.
- **Switch buried in an Abstract Factory**: Switch statements naturally do N things and are hard to keep small; tolerate a switch only if it appears once, is used to create polymorphic objects, and is hidden behind an inheritance relationship that the rest of the system cannot see.
  - When to use: When you cannot avoid a switch on type.
  - How: Put the switch in the basement of an ABSTRACT FACTORY; dispatch calculatePay/isPayday/deliverPay polymorphically through the interface. This respects SRP and OCP.
- **Function Arguments (niladic > monadic > dyadic > triadic)**: Ideal argument count is zero, then one, then two; three should be avoided, and more than three requires special justification. Arguments are costly to comprehend and combinatorially hard to test.
  - When to use: When designing a function signature.
  - How: Prefer instance methods (report.appendFooter()) over output args; wrap related args into an object (makeCircle(Point center, double radius)); use keyword form to encode argument order (assertExpectedEqualsActual(expected, actual)).
- **Command Query Separation**: A function should either do something (change state) or answer something (return info), but not both. Doing both leads to verb/adjective confusion (if (set("username","unclebob"))).
  - When to use: When a function both mutates and returns a status.
  - How: Split into a query (attributeExists("username")) plus a command (setAttribute("username","unclebob")).
- **Prefer Exceptions to Returning Error Codes**: Returning error codes subtly violates Command Query Separation and forces nested, immediate error handling. Exceptions separate the happy path from error processing and avoid the Error dependency magnet (an enum that forces recompile/redeploy on change).
  - When to use: When a command can fail.
  - How: Throw exceptions; extract try/catch bodies into their own functions so the try is the first word and there is nothing after the catch/finally. Error handling is itself "one thing."
- **Don't Repeat Yourself (DRY)**: Duplication is the root of much evil; repeated algorithms bloat code and create four-fold opportunities for errors of omission. Many paradigms (normalization, OOP base classes, AOP) exist to eliminate it.
  - When to use: When you spot the same algorithm repeated (e.g., four setup/teardown cases).
  - How: Extract the shared algorithm into one function and call it from each site.

## Key Concepts
- **niladic / monadic / dyadic / triadic / polyadic**: Function arity of 0 / 1 / 2 / 3 / >3 arguments.
- **Output argument**: An argument used to return information (appendFooter(StringBuffer report)); confusing because readers expect data to flow out via return value.
- **Flag argument**: A boolean passed into a function (render(boolean isSuite)) that loudly proclaims the function does more than one thing; split instead.
- **Side effect**: A function that promises one thing but also changes class state, parameters, or globals—a lie that creates temporal couplings and order dependencies.
- **Temporal coupling**: A hidden ordering requirement created by a side effect (e.g., checkPassword also calls Session.initialize(), so it must be called only when safe to reinitialize the session).
- **Structured Programming**: Dijkstra's one-entry/one-exit rule (single return, no break/continue/goto); harmless to relax in very small functions.
- **The Step-down Rule**: Reading code as a top-down narrative, one level of abstraction per descent.

## Mental Models
- Use a function name as the topic sentence, and let each callee be the next paragraph down—read the module like a story, not a program.
- Prefer niladic functions and instance methods over dyadic functions and output arguments because every extra argument multiplies comprehension and test cost.
- Use polymorphism to bury switch statements behind an Abstract Factory so the rest of the system never sees the type dispatch.
- Split a command/query hybrid into two functions rather than returning a status from a mutator, to kill verb/adjective ambiguity.

## Anti-patterns
- **Large functions with mixed abstraction levels**: Listing 3-1 (testableHtml) mixes buffers, string appends, PathParser.render, and getHtml()—unreadable; the fix is extraction and renaming, not comments.
- **Switch statements in the open**: calculatePay(Employee e) with a switch on e.type violates SRP and OCP and gets repeated across isPayday/deliverPay; bury it in a factory.
- **Flag arguments**: render(true) is confusing; better to split into renderForSuite() and renderForSingleTest().
- **Output arguments**: appendFooter(s) forces a double-take on whether s is input or output; prefer report.appendFooter().
- **Command-query confusion**: set("username","unclebob") returns boolean, making if (set(...)) ambiguous about intent.
- **Returning error codes**: deletePage(page) == E_OK produces deeply nested error handling and creates an Error dependency magnet.
- **Hidden side effects**: checkPassword also calls Session.initialize(), creating a dangerous temporal coupling.
- **Sectioned functions**: A function split into "declarations / initializations / sieve" sections is doing more than one thing.

## Code Examples
```java
public static String renderPageWithSetupsAndTeardowns(
  PageData pageData, boolean isSuite) throws Exception {
  if (isTestPage(pageData))
    includeSetupAndTeardownPages(pageData, isSuite);
  return pageData.getHtml();
}
```
- **What it demonstrates**: A function doing one thing at a single level of abstraction; each step is a descriptively named call one level below the name.

## Worked Example
Refactoring FitNesse's `testableHtml` (Listing 3-1 → Listing 3-2 → Listing 3-3):

BEFORE (Listing 3-1, excerpt — long, mixed levels, duplicated 4×):
```java
public static String testableHtml(
  PageData pageData, boolean includeSuiteSetup) throws Exception {
  WikiPage wikiPage = pageData.getWikiPage();
  StringBuffer buffer = new StringBuffer();
  if (pageData.hasAttribute("Test")) {
    if (includeSuiteSetup) {
      WikiPage suiteSetup =
        PageCrawlerImpl.getInheritedPage(
          SuiteResponder.SUITE_SETUP_NAME, wikiPage);
      if (suiteSetup != null) {
        WikiPagePath pagePath =
          suiteSetup.getPageCrawler().getFullPath(suiteSetup);
        String pagePathName = PathParser.render(pagePath);
        buffer.append("!include -setup .")
              .append(pagePathName).append("\n");
      }
    }
    // ... repeated for SetUp, TearDown, SuiteTeardown ...
  }
  buffer.append(pageData.getContent());
  // ... teardown blocks ...
  pageData.setContent(buffer.toString());
  return pageData.getHtml();
}
```

AFTER (Listing 3-7, the whole module refactors to one-liners at consistent abstraction):
```java
public class SetupTeardownIncluder {
  private PageData pageData;
  private boolean isSuite;
  private WikiPage testPage;
  private StringBuffer newPageContent;
  private PageCrawler pageCrawler;

  public static String render(PageData pageData) throws Exception {
    return render(pageData, false);
  }
  public static String render(PageData pageData, boolean isSuite)
    throws Exception {
    return new SetupTeardownIncluder(pageData).render(isSuite);
  }
  private String render(boolean isSuite) throws Exception {
    this.isSuite = isSuite;
    if (isTestPage())
      includeSetupAndTeardownPages();
    return pageData.getHtml();
  }
  private boolean isTestPage() throws Exception {
    return pageData.hasAttribute("Test");
  }
  private void includeSetupAndTeardownPages() throws Exception {
    includeSetupPages();
    includePageContent();
    includeTeardownPages();
    updatePageContent();
  }
  private void includeSetupPages() throws Exception {
    if (isSuite) includeSuiteSetupPage();
    includeSetupPage();
  }
  // ... each helper one or two lines, one level down ...
}
```
The duplication (the include algorithm repeated for SetUp / SuiteSetUp / TearDown / SuiteTearDown) is eliminated by a single `include(String pageName, String arg)` helper, satisfying DRY.

## Key Takeaways
1. Keep functions tiny (rarely >20 lines); make every block a one-line function call to stay small and self-documenting.
2. Make a function do one thing by ensuring all steps are one level of abstraction below its name; if you can extract a non-restating function, it was doing more than one thing.
3. Order functions to obey The Step-down Rule so the module reads top-down as a narrative.
4. Minimize arguments (niladic > monadic > dyadic); wrap related args into objects and use keyword/verb-noun names.
5. Separate commands from queries, prefer exceptions over error codes, and bury switch statements behind an Abstract Factory.

## Connects To
- **Ch 2 (Names)**: Descriptive names are half the battle for functions that read "pretty much what you expected."
- **Ch 4 (Comments)**: Express intent in code (small named functions) instead of commenting a messy function.
- **Ch 5 (Formatting)**: Vertical density and ordering support the step-down narrative.
- **SRP / OCP**: Switch-in-the-open violates both; polymorphism restores them.
