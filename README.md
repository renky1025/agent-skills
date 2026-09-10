<div align="center">

**English** | [简体中文](README.zh-CN.md)

</div>

# Agent Skills: Production-Grade AI Agent Skill Library

A production-grade, open-source collection of Agent Skills for next-generation autonomous agents and developer collaboration systems (Claude Code, Codex, Cursor, and beyond). Every module follows a standardized `SKILL.md` contract system with structured context-passing design, covering content creation, multimedia engineering, code R&D and security auditing, cognitive learning, and intelligent knowledge-base management.

---

## Core Design & Engineering Principles

1. **Contract-Based Context Passing**: Every skill defines explicit input boundaries, an Outcome Contract, and a Done-When standard. No vague blind injection — state stays deterministic in multi-agent collaboration.
2. **Zero-Garble & Pure ASCII Guarantee**: Documents and generation pipelines strictly follow an ASCII-safe structure to eliminate encoding corruption (`U+FFFD` / mojibake) caused by decorative Unicode characters.
3. **Single Source of Truth**: Generic capabilities (e.g., the `de-ai-writing` anti-AI-tone algorithm) are centralized as the single source of truth; upper-layer skills reference them instead of duplicating logic.
4. **Graceful Degradation**: Skills that depend on optional plugins or external services always ship with local fallback paths and deterministic degradation strategies.

---

## Repository Structure

```
agent-skills/
+-- README.md                         # Authoritative architecture & usage guide (EN)
+-- README.zh-CN.md                   # Architecture & usage guide (Chinese)
+-- LICENSE                           # Open-source license
+-- SKILLS-UPGRADE-AUDIT.md           # Architecture audit & governance report
|
+-- [Content Creation & Media]
|   +-- article-deconstructor/        # 10-dimension viral-article deconstruction
|   +-- black-humor-writing/          # Five-step stand-up black-humor creation method
|   +-- de-ai-writing/                # Generic AI-tone removal & human-voice calibration (single source of truth)
|   +-- novel-writing/                # LOCK-system narrative novel skeleton
|   +-- snowflake-novel-writer/       # Snowflake method 10-step long-form fiction
|   +-- wechat-article-writer/        # WeChat official-account & self-media long-form creation flow
|   +-- weitoutiao-creator/           # 300-character micro-post viral copy generator
|
+-- [Multimedia & Audio/Video Engineering]
|   +-- image-design/                 # Five-dimension photography AI image-prompt generator
|   +-- infocard/                     # High-resolution adaptive modern info-card rendering engine
|   +-- mckinsey-cover/               # McKinsey-style consulting report cover generator
|   +-- mlx-tts/                      # Apple Silicon (MLX) local low-latency speech synthesis
|   +-- spec-image/                   # Spec-driven Prompting engineering image-generation engine
|   +-- video-dubbing/                # Video translation, AI voice cloning, dubbing & subtitle burning
|   +-- video-minutes/                # Intelligent video minutes & @tags task dispatch
|
+-- [Code Engineering & DevSecOps]
|   +-- agent-coding-style/           # Deterministic Coding Agent behavior rules
|   +-- claude-simplify/              # Three-agent parallel code review & simplification pipeline
|   +-- clean-code/                   # "Clean Code" 17-chapter knowledge system & refactoring guide
|   +-- design-md-extractor/          # Web visual design-system reverse extractor (DESIGN.md)
|   +-- github-analyzer/              # Fast 5-dimension GitHub repo deconstruction reports
|   +-- jira-server-pat-cli/          # Generic Jira Server/Data Center management CLI
|   +-- llm-aiops/                    # LLM AIOps operations & root-cause-analysis research library
|   +-- prompt-enhancer/              # Weak prompt -> eight-section production-grade instruction enhancer
|   +-- skill-security-check/         # Agent Skill static vulnerability & security auditor (11 checks)
|
+-- [Cognitive Learning & Education Lab]
|   +-- curriculum-design/            # OBE outcome-based + Bloom taxonomy curriculum design
|   +-- edulab/                       # Middle/high-school math visual problem solving (3D geometry + 2D functions)
|   +-- grasp/                        # Ten-dimension cognitive framework x Feynman accelerated learning protocol
|   +-- teach-eli5/                   # Matt Pocock teaching method, beginner-friendly self-contained courseware
|
+-- [Knowledge Base & Memory Management]
    +-- claude-remember/              # Multi-layer AI Agent long-term memory review & archiving
    +-- obsidian-kb-builder/          # Karpathy LLM-Wiki local bidirectional-link Obsidian knowledge base
    +-- pdf2md/                       # High-fidelity academic & industrial PDF-to-Markdown engine
```

---

## Skill Catalog

| Skill | Category | Core Positioning | Trigger Keywords | Dependencies |
|---|---|---|---|---|
| **de-ai-writing** | Writing | 36 AI-tone pattern detectors, 3-layer vocabulary filtering, 5-step human-voice calibration | `/de-ai`, remove AI tone, humanize writing | None |
| **wechat-article-writer** | Writing | Pain-point-driven topics, three-section skeleton, emotion mapping, low-creativity compliance | write WeChat article, viral copy | None |
| **weitoutiao-creator** | Writing | 5 writing styles x 10 frameworks, 300-character high-conversion micro-post generation | micro-post, Toutiao copy | None |
| **snowflake-novel-writer** | Writing | Snowflake method 10-step long-form fiction, desire arcs, 3-pass AI-tone removal | write a novel, snowflake method | None |
| **novel-writing** | Writing | LOCK-system narrative novel skeleton with three-act / two-doorway structure | English fiction, LOCK system | None |
| **article-deconstructor** | Writing | 10-dimension viral-article reverse deconstruction, emotion curves, hook extraction | deconstruct article, viral analysis | None |
| **black-humor-writing** | Writing | Five-step black-humor method (topic / attitude / expectation violation / conflict amplification) | black humor, stand-up jokes, satire | None |
| **video-minutes** | Media | 7-type video auto-classification, Faster-Whisper int8 transcription, @tags task dispatch | `generate_minutes.py`, video minutes | Python, FFmpeg, faster-whisper |
| **video-dubbing** | Media | ASR -> AI translation -> TTS dubbing -> segment-scaled alignment -> hard-subtitle burning | `dub_segments.py`, video dubbing | Python, FFmpeg, whisper, mlx-audio |
| **mlx-tts** | Media | Apple Silicon local Qwen3-TTS / CosyVoice millisecond speech synthesis | `mlx_audio.tts`, local TTS | macOS, uv, mlx-audio |
| **image-design** | Media | Five-dimension photography model (subject / composition / lighting / lens / film) prompt generation | image prompts, Midjourney, photography | None |
| **mckinsey-cover** | Media | McKinsey/BCG-style report covers & infographic structured prompts | `/mckinsey-cover`, consulting cover | None |
| **infocard** | Media | Content-adaptive layout, 10+ editorial/dashboard-theme HD info cards | `/infocard <URL/text>`, info cards | Node.js, Canvas/Playwright |
| **spec-image** | Media | Spec-driven Prompting image generation: 4-section spec prompts, parameter decoupling, edit-protection contracts, 12 workflow templates | `/spec-image <request>`, engineering imaging, transparent cutout | Any image generation/editing model |
| **agent-coding-style** | Engineering | Deterministic reply, search, editing, Git, planning, review & frontend rules for Coding Agents | coding style, agent coding rules | None |
| **claude-simplify** | Engineering | Three-agent parallel pre-commit review (reuse / code smells / runtime efficiency) | `/simplify`, code review | Git |
| **clean-code** | Engineering | Distilled 17-chapter "Clean Code" knowledge system & refactoring guide | code smells, clean code, refactoring | None |
| **skill-security-check** | Engineering | 11 static security scans (prompt injection, code execution, credential leaks, sensitive paths) | `security-check.js`, skill audit | Node.js, TypeScript |
| **github-analyzer** | Engineering | Fast 5-dimension GitHub repo analysis (positioning / pain points / architecture / onboarding / highlights) | analyze GitHub project, review this repo | Python / Node.js, curl |
| **design-md-extractor** | Engineering | Reverse-extract typography / color / spacing specs from the web into DESIGN.md | extract design system, DESIGN.md | Browser / Node.js |
| **jira-server-pat-cli** | Engineering | Generic Jira Server/Data Center REST CLI with PAT local persistence (0600 config reuse), org CAs, metadata discovery & full issue lifecycle | Jira CLI, PAT, JQL, issue management | Python 3 stdlib |
| **llm-aiops** | Engineering | LLM-for-AIOps research knowledge base: cloud ops, root-cause analysis, log parsing | AIOps, RCA, troubleshooting KB | None |
| **prompt-enhancer** | Engineering | Weak prompts -> eight-section production-grade instructions, 6 domain templates built in | enhance prompt, strengthen prompt | None |
| **grasp** | Cognition | Ten-dimension cognitive model x Feynman interactive learning protocol | `/grasp <topic>`, deep learning | None |
| **teach-eli5** | Cognition | Matt Pocock teaching method: life analogies first, self-contained interactive HTML courseware | `/eli5 <topic>`, explain simply | Open HTML in browser |
| **curriculum-design** | Cognition | OBE outcome-based + Bloom taxonomy syllabi & lesson plans | curriculum design, lesson plan, OBE | None |
| **edulab** | Cognition | Middle/high-school math visualization: SymPy vector methods + Three.js 3D/2D interactive solutions | `/edulab`, math visualization | Python (sympy), Three.js |
| **obsidian-kb-builder** | Knowledge | Karpathy LLM-Wiki bidirectional-link vaults with graph-data export | knowledge base, Obsidian links | Python |
| **pdf2md** | Knowledge | OpenDataLoader-powered high-fidelity PDF parsing (formulas, cross-page tables) | `pdf2md.py`, pdf to markdown | Python, opendataloader-pdf |
| **claude-remember** | Knowledge | Layer 1/2/3 memory system review, distillation & dedup archiving | organize memory, archive memory | None |

---

## Detailed Guide (30 Skills)

### 1. Content Creation & Self-Media

#### 1. de-ai-writing (AI-Tone Removal & Human-Voice Calibration)
- **Features**: The library's **single source of truth** for anti-AI-tone. 36 machine-writing pattern detectors (hollow sublimation, unnecessary symmetrical parallelism, -ing superficial analysis, officialese connectors), 3-tier banned-word lists (Tier 1/2/3 absolute bans & replacements), and a 5-step human-rewrite flow.
- **Triggers**: remove AI tone, make this sound human, remove officialese.
- **Usage**:
  ```
  /de-ai <text> [--strength=light|medium|heavy]
  ```
- **Output**: Before/after comparison, traced modification list, human-voice naturalness self-check score.

#### 2. wechat-article-writer (WeChat & Self-Media Long-Form Creation Flow)
- **Features**: Pain-point-driven topic selection, the "three-section framework" (01/02/03 structure), 4 high-conversion openings and 3 strong closings. Enforces WeChat's low-creativity avoidance standards with a 4-dimension pre-publish audit (information gain, originality, content density, AI involvement; max 20 points, auto-reject below 12).
- **Triggers**: write a WeChat article, self-media long form, in-depth business story.
- **Usage**:
  ```
  Write a WeChat article: [topic/pain-point material] --platform=wechat --target-words=2500
  ```
- **Output**: 3 candidate viral titles, full publish-ready body, emotion map, embedded golden-quote list, compliance scorecard.

#### 3. weitoutiao-creator (300-Character Micro-Post Viral Generator)
- **Features**: Designed for sub-300-character high-engagement short content. 5 proven writing styles (narrative, suspense, data-driven, emotional resonance, direct address) and 10 classic structures (e.g., "shocking fact - data - analysis - interaction"). Interactive 6-step SOP with user confirmation at each step.
- **Triggers**: micro-post, Toutiao short copy, social short post.
- **Usage**:
  ```
  Generate a micro-post: [domain tag / core viewpoint]
  ```
- **Output**: 15-25 character hook title, sub-300-character body, comment-section engagement hooks.

#### 4. snowflake-novel-writer (Snowflake Method 10-Step Long-Form Fiction)
- **Features**: Classic Snowflake Method expansion from "one-sentence summary" through "structure skeleton -> theme/anti-theme -> character arcs -> relationship web & secrets -> one-page synopsis -> scene list -> narrative voice -> sample chapter & full draft". Includes fiction-specific 3-pass AI-tone removal and anti-cliche checklists.
- **Triggers**: write a long novel, web-fiction plotting, snowflake outline.
- **Usage**:
  ```
  Snowflake novel: [genre & core premise]
  ```
- **Output**: Core premise, three-layer character profiles (surface/depth/contrast), refined scene list, 1500-2500 word sample chapter & full text.

#### 5. novel-writing (LOCK-System Narrative Skeleton)
- **Features**: James Scott Bell's LOCK system (Lead, Objective, Conflict, Knockout) plus the classic three-act structure with two Doorways of No Return. Focused on rapidly building high-tension narrative mains and plot outlines.
- **Triggers**: English fiction, three-act outline, LOCK plotting.
- **Usage**:
  ```
  /novel-writing [story concept / protagonist setup]
  ```
- **Output**: LOCK four-element analysis, three-act 8-beat plotline, core turning-point design.

#### 6. article-deconstructor (10-Dimension Viral-Article Deconstructor)
- **Features**: Full-spectrum reverse engineering of top articles across 10 dimensions: topic value, title formulas, hooks, argument logic, case density, emotion curves, stinging sentence patterns, pacing, golden quotes, and reusable templates.
- **Triggers**: deconstruct this article, analyze viral logic, extract writing templates.
- **Usage**:
  ```
  Deconstruct this article: [article URL or full text]
  ```
- **Output**: 10-dimension report charts, author argument skeleton, ready-to-fill blank structure templates.

#### 7. black-humor-writing (Five-Step Black-Humor Method)
- **Features**: Based on stand-up comedy and satirical literature logic: lock a serious topic -> define the satirical stance -> set up normal expectations -> plant absurd facts to break them -> amplify conflict with self-consistent logic.
- **Triggers**: black humor, satirical jokes, stand-up scripts, ironic copy.
- **Usage**:
  ```
  Write a black-humor joke: [social phenomenon / rant topic]
  ```
- **Output**: Setup & punchline structure table, absurd-logic derivation chain, finished draft.

---

### 2. Multimedia & Audio/Video Engineering

#### 8. video-minutes (Intelligent Video Minutes & @tags Task Dispatch)
- **Features**: `faster-whisper` high-performance transcription (int8 quantization + VAD filtering, 2-4x faster). Automatic 7-type video classification (meeting, lecture, interview, talk, podcast, tutorial, screen recording) and automatic task-tag extraction (`@dev`, `@design`, `@article`, `@reminder`).
- **Triggers**: video summary, video-to-text, meeting recording notes, subtitles.
- **CLI Usage**:
  ```bash
  # Process a local meeting video into Markdown minutes
  python3 video-minutes/scripts/generate_minutes.py meeting.mp4 --type meeting --language zh

  # Batch-scan a Zoom/screen-recording directory
  python3 video-minutes/scripts/scan-and-process.py ~/Recordings/ --since-hours 24
  ```
- **Output**: Structured minutes (Markdown / Obsidian links / Notion formats), timestamped outline, decisions list, TODO list.

#### 9. video-dubbing (Full-Pipeline Video Translation, AI Voice Cloning & Subtitle Burning)
- **Features**: End-to-end video translation pipeline: audio extraction (16kHz) -> Whisper ASR -> sentence-level translation -> MLX-TTS voice generation (voice consistency anchored to the first sentence) -> segment-scaled alignment (0.88-1.20x preserving original timing) -> FFmpeg muxing & hard-subtitle burning.
- **Triggers**: video translation, auto dubbing, foreign-video localization, bilingual subtitles.
- **CLI Usage**:
  ```bash
  # 1. Extract audio and get precise SRT timestamps
  ffmpeg -y -i input.mp4 -ar 16000 -ac 1 audio16k.wav
  whisper audio16k.wav --model large-v3-turbo --output_format srt

  # 2. Generate aligned audio and burn hard subtitles
  python3 video-dubbing/scripts/dub_segments.py audio16k.srt translated.txt dubbing.wav subtitle_synced.srt --lang zh
  python3 video-dubbing/scripts/burn_subtitles.py output_temp.mp4 subtitle_synced.srt output_final.mp4
  ```
- **Output**: `output_final.mp4` (with new aligned audio track & burned subtitles), `subtitle_synced.srt`.

#### 10. mlx-tts (Apple Silicon Local Low-Latency Speech Synthesis)
- **Features**: Local TTS engine optimized for macOS M-series chips, driving Qwen3-TTS / CosyVoice models on the MLX framework. Zero-shot voice cloning, cross-lingual synthesis, and prompt-based emotion control — millisecond offline rendering without cloud APIs.
- **Triggers**: local TTS, text-to-speech, Qwen3-TTS, voice cloning.
- **CLI Usage**:
  ```bash
  # Basic text reading
  mlx_audio.tts --model mlx-community/Qwen3-TTS-12B-Instruct --text "Welcome to the open-source agent skill library." --output speech.wav

  # Reference-audio voice cloning
  mlx_audio.tts --ref_audio speaker_sample.wav --ref_text "reference audio text" --text "target speech" --output cloned.wav
  ```
- **Output**: High-fidelity WAV audio, voice-design prompt config files.

#### 11. image-design (Five-Dimension Photography AI Prompt Generator)
- **Features**: Based on real photography industry standards, deconstructs requirements across five dimensions — Subject dynamics & materials, Composition, physical Lighting logic, Lens & Angle, and Film Tone & Color — producing Midjourney v6 / Stable Diffusion industrial-grade prompts.
- **Triggers**: image prompts, Midjourney prompt, photography-grade image description.
- **Usage**:
  ```
  Design photography prompts: [scene concept / subject] --aspect-ratio=16:9 --style=cinematic
  ```
- **Output**: Bilingual (EN/ZH) prompts, negative prompts, camera-parameter recommendations (focal length / aperture / ISO / film stock).

#### 12. mckinsey-cover (McKinsey & Top-Tier Consulting Cover Generator)
- **Features**: Based on Adrian Punk's original design methodology, generates visual instructions with top-tier firm texture (minimal geometric partitions, Swiss typographic grids, desaturated business palettes, metaphorical abstract 3D shapes) for whitepapers, strategy reports, and consulting decks.
- **Triggers**: McKinsey cover, consulting report cover, pitch-deck artwork.
- **Usage**:
  ```
  /mckinsey-cover [report topic / industry]
  ```
- **Output**: Cover layout structure (ASCII grid), Midjourney/DALL-E 3 English image prompts, color schemes (HEX/CMYK).

#### 13. infocard (High-Resolution Adaptive Info-Card Rendering Engine)
- **Features**: Adaptively matches the best layout skeleton based on content density and emotion of input text or URL (Editorial, Dashboard, Slate, Guofeng, Ocean and 10+ themes), rendering high-resolution PNGs locally via Node.js + Playwright/Canvas.
- **Triggers**: generate info cards, article-to-image, visual summaries.
- **Usage**:
  ```bash
  # Extract from URL into a Slate-theme card
  /infocard https://example.com/article --theme=slate

  # Generate a bilingual card from plain text
  /infocard "your core text" --theme=editorial --lang=zh
  ```
- **Output**: High-resolution PNG files saved to `~/Downloads/infocard-img/`.

---

#### 14. spec-image (Spec-driven Prompting Engineering Image Engine)
- **Features**: Parses image requirements into engineering specifications rather than gacha gambling. Five-way task routing (text-to-image / local edit / multi-image composition / transparent cutout / consistency series), four-section structured prompts (Scene / Subject / Details / Constraints), strict system-parameter vs. semantic-prompt decoupling, "change vs. preserve" edit-protection contracts, single-variable progressive iteration protocol, and a pre-delivery checklist (in-image text quoting + frequency constraints, negative-constraint coverage, protected-attribute verification).
- **Triggers**: engineering imaging, posters/logos/UI mockups/infographics, transparent cutouts, image editing, multi-image composition, character-consistency series.
- **Usage**:
  ```bash
  # Text-to-image: a Series A pitch slide (information-dense scenes auto-suggest quality bump)
  /spec-image a Series A pitch slide: TAM/SAM/SOM concentric circles + growth bar chart --ratio=16:9

  # Edit mode: replace only the specified object, everything else strictly preserved
  /spec-image replace the white chairs with wooden chairs --edit=room.jpg

  # Transparent-background asset extraction
  /spec-image extract the product and output a transparent PNG --edit=product.jpg --transparent
  ```
- **Output**: Spec-compliant generated/edited images, versionable structured prompt specifications, checklist verification results. 12 commercial workflow templates built in (film portraits, ad typography, transparent logos, 4-panel comics, UI mockups, teaching diagrams, pitch slides, virtual try-on, multi-image composition, product cutouts, sketch-to-photo, single-object replacement).

---

### 3. Code Engineering & DevSecOps

#### 15. agent-coding-style (Deterministic Coding Agent Behavior Rules)
- **Features**: Unifies reply formatting, search strategy, precision editing, Git safety, task planning, code review, and frontend generation rules into 43 deterministic constraints, reducing over-modification, unverified delivery, dangerous Git operations, and format drift.
- **Triggers**: agent coding rules, deterministic code changes, pre-commit constraints.
- **Usage**:
  ```
  Complete the following code task per agent-coding-style: [task description]
  ```
- **Output**: Clearly bounded change plans, minimal diffs, verification results, auditable Git operation notes.

#### 16. claude-simplify (Three-Agent Parallel Code Review & Simplification Pipeline)
- **Features**: Triggered before Git commit or PR submission. Based on branch diff (`git diff`), dispatches three independent audit roles in parallel:
  - **Reuse Reviewer**: scans for reinvented wheels and existing utility functions not being reused;
  - **Quality Reviewer**: checks code smells, high cyclomatic complexity, deep nesting, naming violations, hardcoding;
  - **Efficiency Reviewer**: reviews memory leaks, unnecessary large-object copies, async deadlocks, slow queries.
- **Triggers**: `/simplify`, code review, pre-commit checks, refactoring.
- **Usage**:
  ```bash
  /simplify [commit/branch/HEAD~1]
  ```
- **Output**: Three-dimension review report, file-and-line precise suggestions, before/after code comparison patches.

#### 17. clean-code ("Clean Code" 17-Chapter Knowledge System & Refactoring Guide)
- **Features**: Systematic distillation of Robert C. Martin's "Clean Code" core principles across all 17 chapters (meaningful naming, single-responsibility functions & single abstraction layer, comment rules, objects & data structures, error handling & eliminating null, boundary isolation, TDD three laws, concurrency defense, the full Smells & Heuristics catalog), with modern-language mappings (TypeScript, Python, Go, Rust, C++).
- **Triggers**: Clean Code, clean-coding standards, code-smell checks, refactoring principles.
- **Usage**:
  ```
  Review and refactor the following code per Clean Code: [code snippet]
  ```
- **Output**: Code-smell diagnosis list (with original rule IDs like `F1`, `G14`), refactored clean code, design-principle explanations.

#### 18. skill-security-check (11-Check Static Vulnerability & Security Auditor)
- **Features**: Static security scanning before installing, importing, or running third-party Agent Skills. Covers 11 core threat classes (prompt injection, arbitrary code execution, dangerous shell commands, sensitive-path access escalation, environment variable & token theft, malicious network exfiltration) with strict risk ratings (P0 block / P1 warn / P2 safe).
- **Triggers**: check skill safety, audit a skill, scan SKILL.md.
- **CLI Usage**:
  ```bash
  node skill-security-check/scripts/security-check.js /path/to/skill-folder
  ```
- **Output**: Static code & Markdown audit report, vulnerability locations (file & line), P0/P1/P2 risk scores.

#### 19. github-analyzer (Fast 5-Dimension GitHub Repo Deconstruction Reports)
- **Features**: Given a GitHub repo link, automatically fetches `README.md`, repo metadata, directory structure, and dependencies, producing a five-chapter structured analysis report within 60 seconds (what it is, core pain points, key features, 3-minute quick start, architecture & implementation highlights).
- **Triggers**: analyze this GitHub project, review this repo.
- **Usage**:
  ```
  Analyze this open-source project: https://github.com/owner/repo
  ```
- **Output**: Standard Markdown project analysis report, tech-stack radar, applicability assessment.

#### 20. design-md-extractor (Web Visual Design-System Reverse Extractor)
- **Features**: Reads the target page's DOM, computed styles, and visual screenshots to reverse-derive a `DESIGN.md` spec conforming to Google Labs conventions — extracting color semantic tokens, type hierarchy, spacing scales, shadow grids, and component styles.
- **Triggers**: extract website design specs, generate DESIGN.md, extract design tokens.
- **Usage**:
  ```
  Extract the design system from this website: https://example.com/
  ```
- **Output**: Standard `DESIGN.md` document, CSS variable definition blocks, Tailwind color extension config.

#### 21. jira-server-pat-cli (Generic Jira Server/Data Center Management CLI)
- **Features**: Pure Python stdlib Jira REST CLI supporting PAT, Cookie, Basic Auth, organization CAs, and context paths. All issue types, custom fields, transitions, priorities, components, versions, and user identities are dynamically discovered from the target instance — no hardcoded IDs, no environment privacy leaks. A user-provided PAT can be persisted once to `~/.config/jira-cli/config.json` (directory 0700 / file 0600, merge-write without overwriting other fields); subsequent calls read it automatically with no repeated prompting.
- **Triggers**: Jira CLI, PAT management, JQL search, bulk issue operations, internal-CA Jira automation.
- **CLI Usage**:
  ```bash
  export JIRA_BASE_URL="https://jira.example.com/jira"
  export JIRA_PAT="<secret>"
  python3 jira-server-pat-cli/scripts/jira_cli.py whoami
  python3 jira-server-pat-cli/scripts/jira_cli.py search "project = PROJ ORDER BY updated DESC" --limit 100
  ```
- **Output**: Instance & permission probe results, JQL JSON data, issue CRUD, transitions, comments, worklogs, attachments, links, watchers, votes; write operations support dry-run, destructive and raw REST writes require `--yes`.

#### 22. llm-aiops (LLM AIOps & Root-Cause-Analysis Research Library)
- **Features**: An LLM-for-AIOps knowledge base distilling 78+ top-tier conference and industry papers. Covers mature deployment patterns and architectures for log anomaly detection, time-series alert convergence, microservice distributed tracing, root-cause analysis (RCA), auto-remediation, and security-compliant operations.
- **Triggers**: LLM AIOps, intelligent operations, LLM fault diagnosis, RCA algorithms.
- **Usage**:
  ```
  AIOps consultation: [failure scenario / log anomaly troubleshooting approach]
  ```
- **Output**: AIOps algorithm selection matrix, microservice fault-diagnosis agent topology diagrams, academic references.

#### 23. prompt-enhancer (Weak Prompt -> Eight-Section Production-Grade Instruction Enhancer)
- **Features**: Enhances "one-line drafts" into production-grade instructions covering an eight-section skeleton (Role+Goal / Context / Restate-Align / Think-First / Execution Requirements / Explicit Exclusions / Self-Critique / Output & Acceptance). 6 domain templates built in (general dev, requirement analysis, technical architecture, repo-analysis-to-architecture-diagram, documentation writing, code review/refactoring), plus 8 guiding principles, tiered clarification gates, and anti-fabrication red lines that operationalize "ask when unclear" into a two-level clarification strategy.
- **Triggers**: enhance prompt, strengthen prompt, rewrite as production-grade instruction.
- **Usage**:
  ```
  Enhance this prompt: <raw prompt> [supplements: audience / domain / examples I like / output language]
  ```
- **Output**: Paste-ready instruction text + enhancement comparison table (weakness -> treatment) + usage notes (placeholders and trimmable gates).

---

### 4. Cognitive Learning & Education Lab

#### 24. grasp (Ten-Dimension Cognitive Framework x Feynman Accelerated Learning)
- **Features**: Based on the ten-dimension cognitive model (name, category, definition, features, structure, function, operating conditions, history, trends, risks) and the Feynman technique. Seven interactive learning stages (anchoring, exploration, structuring, Feynman output, active recall, cross-domain transfer, review) build deep conceptual understanding.
- **Triggers**: `/grasp <topic>`, deeply learn a concept, fully understand a technology.
- **Usage**:
  ```
  /grasp Transformer architecture [--phase=1]
  ```
- **Output**: Ten-dimension concept radar, ASCII concept-architecture relation diagram, active-recall self-test bank.

#### 25. teach-eli5 (Matt Pocock Method Beginner-Friendly Interactive Courseware Engine)
- **Features**: Fuses Matt Pocock's `teach` methodology (MISSION learning-goal anchoring, ZPD material selection, glossary & learning-record ADR persistence, assets reuse) with ELI5 constraints. Breaks complex topics into self-contained, polished HTML lesson pages that are image-heavy, text-light, and analogy-first.
- **Triggers**: `/eli5 <topic>`, explain in plain language, make a picture-friendly lesson page.
- **Usage**:
  ```
  /eli5 quantum entanglement --mission="explain the principle to a high-school student"
  ```
- **Output**: `./lessons/0001-<slug>.html` (self-contained printable HTML courseware with inline SVG diagrams & analogy cards), `references/glossary.md`, `learning-records/`.

#### 26. curriculum-design (OBE + Bloom Taxonomy Curriculum Design System)
- **Features**: Based on Outcome-Based Education and Bloom's six-level taxonomy (remember, understand, apply, analyze, evaluate, create), generates university- and professional-training-standard syllabi, teaching calendars, and per-lesson structured plans.
- **Triggers**: curriculum design, lesson planning, OBE teaching plans, training courses.
- **Usage**:
  ```
  Design a curriculum: [course name] --target-audience=[audience] --duration=[hours]
  ```
- **Output**: Course objective matrix (with Bloom levels), hour allocation tables, final-assessment weighting tables, per-lesson plan documents.

#### 27. edulab (Middle/High-School Math Visual Problem-Solving Lab)
- **Features**: Professional visualization and dynamic demonstration for middle/high-school geometry and function problems. Supports:
  - **3D solid geometry**: automatic coordinate-system setup and solving via Python SymPy spatial vectors, outputting Three.js interactive 3D solution pages (rotatable views, perpendicular projections, normal vectors);
  - **2D functions & analytic geometry**: parameter-slider-controlled interactive 2D charts dynamically showing how parameter changes affect intersections, extrema, and monotonic intervals.
- **Triggers**: `/edulab`, math visualization, solid-geometry setup, dynamic function plots.
- **Usage**:
  ```
  /edulab [problem text / geometric conditions] --mode=3d-geometry
  ```
- **Output**: Rigorous Python vector-algebra derivations, self-contained interactive HTML demonstration pages.

---

### 5. Knowledge Base & Memory Management

#### 28. obsidian-kb-builder (Karpathy LLM-Wiki Local Bidirectional-Link Obsidian KB)
- **Features**: Follows Andrej Karpathy's LLM-Wiki architecture pattern. Accepts local files, document directories, or web URLs; automatically extracts core entities and relations; generates a local Markdown bidirectional-link note library (`[[links]]`) conforming to a strict Wiki-Schema; exports structured graph data for graph analytics.
- **Triggers**: build a knowledge base, construct an Obsidian vault, document linking, export knowledge graphs.
- **CLI Usage**:
  ```bash
  # Scan a directory and build the knowledge-base graph
  python3 obsidian-kb-builder/scripts/build_kb.py --input ~/Documents/Papers/ --vault ~/Documents/MyVault/
  ```
- **Output**: Obsidian vault note collection (YAML frontmatter, bidirectional links, tags), `graph_data.json` knowledge-graph data.

#### 29. pdf2md (OpenDataLoader-Based High-Fidelity PDF-to-Markdown Engine)
- **Features**: Built on OpenDataLoader-PDF hybrid parsing. Designed for complex-layout PDFs — academic papers, technical reports, financial statements — with high-precision recognition of LaTeX formulas, complex cross-page tables, code blocks, two-column layouts, and embedded images, outputting extremely clean Markdown.
- **Triggers**: PDF to Markdown, extract papers, parse PDF tables & formulas.
- **CLI Usage**:
  ```bash
  python3 pdf2md/scripts/pdf2md.py input_paper.pdf --output output.md --extract-images
  ```
- **Output**: High-fidelity `output.md`, extracted illustration folder `images/`.

#### 30. claude-remember (Multi-Layer Agent Long-Term Memory Review & Archiving)
- **Features**: Manages the agent's three-layer memory architecture (Layer 1 cloud global memory, Layer 2 user-level persistent rules in `~/.claude/MEMORY.md`, Layer 3 project-level daily logs `YYYY-MM-DD.md` and distilled `MEMORY.md`). Provides memory redundancy detection, conflict resolution, and distillation/archiving of logs older than 30 days.
- **Triggers**: organize memory, review memory files, dedupe & archive memory, update long-term memory.
- **Usage**:
  ```
  Organize the current project's long-term memory and work logs
  ```
- **Output**: Updated distilled `MEMORY.md`, distilled & cleaned historical archive records.

---

## Quick Start & Environment Setup

### 1. Install Skills into a Local Agent Environment

All skills in this repository follow the common specification. You can symlink or copy the whole repo or specific skills into your global or project-level skill directory:

```bash
# Clone the repository
git clone https://github.com/renky1025/agent-skills.git ~/workspace/agent-skills

# Option A: install specific skills into the global skills directory (recommended)
mkdir -p ~/.claude/skills
cp -r ~/workspace/agent-skills/de-ai-writing ~/.claude/skills/
cp -r ~/workspace/agent-skills/infocard ~/.claude/skills/

# Option B: bulk-symlink everything
for dir in ~/workspace/agent-skills/*/; do
  skill_name=$(basename "$dir")
  if [ -f "$dir/SKILL.md" ]; then
    ln -sfn "$dir" ~/.claude/skills/"$skill_name"
  fi
done
```

### 2. Runtime Dependency Setup

Some multimedia and data-processing skills depend on specific CLI tools and Python libraries; install as needed:

```bash
# 1. Audio/video processing dependencies (macOS / Ubuntu)
brew install ffmpeg uv           # macOS
sudo apt install ffmpeg          # Ubuntu

# 2. Local TTS engine (Apple Silicon macOS)
uv tool install --force "mlx-audio" --prerelease=allow

# 3. High-precision PDF parsing
pip install "opendataloader-pdf[hybrid]"

# 4. Video transcription & minutes
pip install faster-whisper moviepy pyyaml requests
```

---

## Skill Development Standards & Contribution Guide

Community contributions of new production-grade Agent Skills are welcome! Before submitting a PR, please ensure:

1. **Directory structure**:
   ```
   my-new-skill/
   +-- SKILL.md                 # Required: full behavior spec & contract document
   +-- scripts/                 # Optional: Python/Node.js/Shell scripts
   +-- references/              # Optional: modular reference material & schemas
   +-- assets/                  # Optional: static templates, components, stylesheets
   ```
2. **Required SKILL.md structure**:
   - **YAML Frontmatter**: `name`, `description`, `version`, `argument-hint`, etc.
   - **Outcome Contract**: explicitly defines the Outcome, Done-When criteria, and Evidence.
   - **Hard Rules**: lists absolutely prohibited behaviors and hard execution boundaries.
   - **Anti-AI-tone & pure-ASCII constraint**: generated content must never use corruption-prone Unicode characters; use pure-ASCII symbols instead.
3. **Security review passed**: new skills must pass the `skill-security-check` static security audit (no P0/P1 findings).

---

## License

This project is released under the [MIT License](LICENSE). All skills have passed security review and real-world engineering verification, and are safe to integrate into enterprise and personal production environments.
