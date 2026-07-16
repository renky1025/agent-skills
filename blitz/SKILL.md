---
name: blitz
description: Use when the user wants to learn a new topic quickly, understand a complex subject, study for an exam, prepare a learning plan, or use accelerated learning techniques. Trigger phrases: "learn fast", "blitz", "understand quickly", "study guide", "learning roadmap", "master [topic]", "spaced repetition", "active recall", "Feynman technique", "first principles".
---

# Blitz — Universal Accelerated Learning Protocol

A 7-phase interactive protocol for learning any topic with maximum efficiency. Based on validated learning science: Feynman Technique, First-Principles Thinking, Active Recall, and Spaced Repetition.

The user invokes: `/blitz <topic> [--phase=N]`

- Without `--phase`, run phases 1→7 in sequence.
- With `--phase=3`, jump directly to Phase 3 (Active Recall Training).
- With `--phase=all`, do a full pass through all phases.

Run each phase **one at a time**. Complete the phase, get user feedback, then proceed.

---

## Phase 1 — Feynman Technique (Understand First)

**Goal:** Establish foundational understanding by explaining in simple terms.

1. **Teach** the topic in simple language as if explaining to a complete beginner.
   - Use analogies, avoid jargon, keep it conversational.
   - Cover: What is it? Why does it matter? How does it work at a high level?

2. **Ask the user to explain it back** in their own words.
   - Prompt: "Now explain this back to me in your own words. I'll point out gaps."

3. **Diagnose gaps.** After their explanation, identify:
   - What they got right — reinforce it.
   - What they got wrong or omitted — clarify simply.
   - Areas where their explanation revealed confusion — re-teach those parts.

4. **Confirm understanding** before moving on.

> **Sign off:** "Phase 1 complete. Ready for first-principles breakdown? (y/n)"

---

## Phase 2 — First-Principles Breakdown

**Goal:** Decompose the topic into irreducible components so the user understands essential logic instead of memorizing surface facts.

1. **Break it down:**
   - What are the fundamental building blocks?
   - What axioms or invariants are true regardless of context?
   - Strip away conventions, tools, and implementation details — what's the core essence?

2. **Show the chain of reasoning** — build up from first principles to the full topic, step by step.

3. **Ask: "Does any link in this chain feel unclear or unmotivated?"**
   - Address each confusion by decomposing further.

4. **Cross-check understanding** — ask one re-framing question that forces the user to reason from first principles:
   - "Based on these fundamentals, what do you think happens when X changes?"

> **Sign off:** "Phase 2 complete. Ready for active recall training? (y/n)"

---

## Phase 3 — Active Recall Training

**Goal:** Force retrieval of information without notes, then evaluate and correct.

1. **Warn the user:** "This is retrieval practice — answer without looking at notes. Being wrong is productive."

2. **Ask 3–5 hard questions** that force the user to retrieve and apply knowledge:
   - Mix of: factual recall, application, synthesis, "what if" scenarios.
   - Questions increase in difficulty.

3. **For each answer:**
   - Praise what's correct.
   - Correct errors with specific, constructive feedback.
   - If partially correct, identify the missing piece and explain why it matters.

4. **Final score summary:**
   - Areas of strength.
   - Areas needing review (link these to Phase 2 first principles).
   - Suggested re-study focus.

> **Sign off:** "Phase 3 complete. Want a spaced repetition schedule? (y/n)"

---

## Phase 4 — Spaced Repetition Table

**Goal:** Generate a concrete review schedule to move information to long-term memory.

1. **Categorize the material** into:
   - **Core concepts** — must internalize permanently
   - **Supporting details** — useful context, less critical
   - **Nitpicks / trivia** — recall when needed, not priority

2. **Build the table:**

   | Cadence | What to Review | Method |
   |---|---|---|
   | **Daily (first 3 days)** | Core concepts | Active recall (Phase 3 style) |
   | **Weekly (first month)** | Core + supporting | Explain from memory + connect to first principles |
   | **Monthly (quarter 1)** | Core concepts only | Teach someone else or write a summary |
   | **Quarterly (year 1)** | Full map + any gaps | Diagnostic quiz (Phase 7 style) |

3. **Customize:** Adjust cadence based on user's deadline, depth goal, and prior knowledge.

4. **Export suggestion:** "Copy this table to a note app or flashcard system (Anki, RemNote, etc.)."

> **Sign off:** "Phase 4 complete. Want a distilled knowledge summary? (y/n)"

---

## Phase 5 — Knowledge Summary (Frameworks & Mental Models)

**Goal:** Distill the topic into clear frameworks, mental models, and simplified structures for easy retention and application.

1. **Extract the core frameworks:**
   - What are the 2–3 mental models that capture the essence?
   - Can the topic be visualized as a map, tree, flowchart, or spectrum?

2. **Create a one-page cheat sheet** (can be markdown, mermaid diagram, or conceptual map):
   - Core principles (3–5 bullet points max)
   - Relationships between concepts
   - Common pitfalls / anti-patterns

3. **Memorable hook:** A one-sentence summary. "If you remember only one thing about this topic, it's _."

4. **Ask:** "Does this summary match your mental model? What would you add or change?"

> **Sign off:** "Phase 5 complete. Want a learning roadmap for deeper mastery? (y/n)"

---

## Phase 6 — Learning Roadmap (Acceleration Plan)

**Goal:** Create a staged plan for going from current level to mastery, with clear milestones.

1. **Assess current level:**
   - Rate 1–10: How well does the user understand the topic after Phase 1–5?
   - Identify the next logical growth area.

2. **Build the roadmap:**

   | Stage | Goal | Activities | Checkpoint |
   |---|---|---|---|
   | **Foundation** | Solid understanding of basics | Review Phases 1–5, spaced repetition | Can explain core concepts without notes |
   | **Application** | Use knowledge in real scenarios | Projects, exercises, real-world application | Completed 3 practical exercises |
   | **Integration** | Connect to adjacent domains | Cross-domain reading, teach others | Created a guide or tutorial for others |
   | **Mastery** | Push boundaries, contribute | Advanced resources, community participation, original work | Published analysis, contribution, or project |

3. **Resources:** Recommend 1–2 books, courses, or projects per stage. Not overwhelm — specific, actionable picks.

4. **Time estimate:** Realistic hours per stage based on topic complexity.

> **Sign off:** "Phase 6 complete. Want a weak-point diagnosis to close remaining gaps? (y/n)"

---

## Phase 7 — Weak Point Diagnosis

**Goal:** Identify remaining blind spots, misunderstandings, and suggest targeted fixes.

1. **Ask 5 diagnostic questions** — designed to expose:
   - Common misconceptions about the topic
   - Edge cases the user hasn't considered
   - Connections between sub-topics they may have missed
   - Practical application nuances

2. **Analyze responses:**
   - Pattern: are errors in one specific area?
   - Root cause: is the gap conceptual (didn't understand) or memory-based (forgot)?

3. **Prescribe targeted improvements:**
   - For conceptual gaps → re-teach from first principles (Phase 2)
   - For memory gaps → spaced repetition (Phase 4)
   - For application gaps → practical exercise (Phase 6)
   - For blind spots → specific reading or exercise

4. **Final diagnosis summary:**
   ```
   Strengths: [what they know well]
   Weak spots: [specific gaps]
   Root causes: [why those gaps exist]
   Rx: [targeted Phase references + one concrete next action]
   ```

> **Sign off:** "Phase 7 complete. Run `/blitz <topic>` again in a week for reinforcement."

---

## Quick Reference

| Phase | Name | Core Question | Duration |
|---|---|---|---|
| 1 | Feynman Technique | "Can you explain it simply?" | 5–10 min |
| 2 | First-Principles Breakdown | "What are the irreducible truths?" | 5–10 min |
| 3 | Active Recall Training | "Can you retrieve it under pressure?" | 10–15 min |
| 4 | Spaced Repetition Table | "What to review, when?" | 5 min |
| 5 | Knowledge Summary | "What's the one-page cheat sheet?" | 5–10 min |
| 6 | Learning Roadmap | "What's the path to mastery?" | 5–10 min |
| 7 | Weak Point Diagnosis | "What am I missing?" | 10 min |

## Common Mistakes

- **Skipping Phase 1** — "I already know this." Feynman reveals hidden gaps. Run it anyway.
- **Rushing active recall** — struggle is productive. Let the user sit with a hard question.
- **Overloading the roadmap** — recommend 1–2 resources per stage, not a book list.
- **Too many diagnostic questions** — 5 sharp questions > 20 shallow ones.

## When NOT to Use

- The user needs a quick fact, not deep understanding (use search / direct answer).
- The topic is purely procedural / muscle memory (use practice drills, not this protocol).
- The user explicitly wants just one thing (references, a roadmap, etc.) — use `--phase=N`.
