---
name: llm-aiops
description: Use when working on AIOps (AI for IT Operations) tasks — incident management, root cause analysis, log parsing/anomaly detection, cloud infrastructure management, or applying LLMs to IT operations. Also use when researching LLM-based solutions for incident response, fault localization, or infrastructure-as-code.
---

# LLM AIOps Reference

## Overview
Curated reference applying Large Language Models to AIOps, based on the [awesome-LLM-AIOps](https://github.com/Jun-jie-Huang/awesome-LLM-AIOps) research taxonomy. Covers incident management, log analysis, and infrastructure management.

## When to Use
- **Incidents**: triaging, diagnosing, mitigating cloud incidents
- **RCA**: root cause analysis of system failures
- **Logs**: parsing, anomaly detection, logging statement generation
- **Infrastructure**: IaC, performance diagnosis, LLM training platforms
- **AIOps QA**: domain-specific question answering for operations

## Taxonomy & Key Approaches

### 1. LLM for Incident Management

| Area | Key Approaches | Notable Systems |
|------|---------------|-----------------|
| **Surveys & Benchmarks** | Evaluation frameworks for AIOps agents | AIOpsLab (MLSys 2025), ITBench (ICML 2025) |
| **Incident Diagnosis** | LLM agents + diagnostic tools | D-Bot (VLDB 2024), NetAssistant (NSDI 2024), FLASH (Preprint 2024) |
| **Incident Reporting** | Fine-tuning, CoT prompting for summarization | Oasis (FSE 2023), COLA (ICSE-SEIP 2024), MonitorAssistant (FSE 2024) |
| **Root Cause Analysis** | Agents with tool augmentation, CoT, ICL, multi-agent | RCAgent (CIKM 2024), mABC (EMNLP 2024), Flow-of-Action (WWW 2025), OpenRCA (ICLR 2025), COCA (ICSE 2025), RCACopilot (EuroSys 2024) |
| **Incident Mitigation** | Agent-based with troubleshooting guides, RAG | Nissist (ECAI 2024), LLexus (SIGOPS 2024), STRATUS (NeurIPS 2025) |
| **Postmortem Analysis** | Fine-tuning for fault profiling | FaultProfIT (ICSE-SEIP 2024), FAIL (ASE 2024) |
| **AIOps Q&A** | Instruction tuning, RAG, domain-specialized LLMs | OWL (ICLR 2024), iKnow (ASE 2025), OpsEval (Preprint 2023), MSQA (EMNLP 2023) |

### 2. LLM for Log Analysis

| Area | Key Approaches | Notable Systems |
|------|---------------|-----------------|
| **Log Parsing** | ICL prompting, adaptive caching, entropy + CoT merging | DivLog (ICSE 2024), LILAC (FSE 2024), LogBatcher (ASE 2024), LUNAR (FSE 2025), LibreLog (ICSE 2025) |
| **Log Anomaly Detection** | Prompting, RAG, fine-tuning | LogGPT (Preprint 2023), LogPrompt (ICPC 2024), RAGLog (Preprint 2024), CodeAD (2025) |
| **Logging Statement Generation** | ICL, fine-tuning, static context analysis | UniLog (ICSE 2024), SCLogger (FSE 2024), FastLog (ISSTA 2024) |

### 3. LLM for Infrastructure Management

| Area | Key Approaches | Notable Systems |
|------|---------------|-----------------|
| **Infrastructure-as-Code** | Agent-based bug discovery, semantic checking | Unearthing IaC Checks (SOSP 2024) |
| **LLM Training Platform** | Black-box performance diagnosis | LLMPrism (DSN 2025) |
| **Benchmarks** | IaC code generation | IaC-Eval (NeurIPS D&B 2024) |

## Common LLM Techniques Used

- **Prompting**: ICL (In-Context Learning), CoT (Chain-of-Thought), ToT (Tree-of-Thought)
- **Fine-tuning**: Instruction tuning, domain-specific adaptation (e.g., OWL for IT ops)
- **Agent-based**: Tool-augmented LLMs, multi-agent collaboration, SOP-guided agents
- **RAG**: Retrieval-Augmented Generation for incident resolution recommendations
- **Code Synthesis**: LLM generates rule code for anomaly detection (CodeAD)

## Key Benchmarks

- **ITBench** (ICML 2025) — Diverse real-world IT automation tasks
- **AIOpsLab** (MLSys 2025) — Holistic autonomous cloud agent evaluation
- **OpsEval** — Comprehensive AIOps task benchmark
- **OpenRCA** (ICLR 2025) — RCA benchmark with fault propagation awareness
- **IaC-Eval** (NeurIPS 2024) — Infrastructure-as-Code generation benchmark

## Common Mistakes

- ❌ Treating log parsing as a solved problem — LLM-based parsers still struggle with unseen log formats; use adaptive caching (LILAC pattern)
- ❌ Applying generic LLMs to ops without domain tuning — Domain-specific models (OWL) or RAG significantly outperform general-purpose prompting for AIOps Q&A
- ❌ Single-agent RCA for complex microservice failures — Multi-agent systems (mABC, Flow-of-Action) with SOP guidance outperform single-agent approaches
- ❌ Ignoring confidence estimation in RCA — Use PACE-LM style confidence calibration before acting on LLM-generated RCA results

## Real-World Impact

The field has rapidly evolved from basic prompting (2023) to sophisticated multi-agent systems with tool augmentation (2024-2025), with production-grade systems like Nissist, STRATUS, and iKnow deployed in real cloud environments. Key trend: moving from single LLM calls to autonomous agent loops with verification.
