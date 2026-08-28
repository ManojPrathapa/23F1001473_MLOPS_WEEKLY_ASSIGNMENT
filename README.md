# 🛡️ MLOps Week 11: Governing the Fine-Tuned LLM Guardrails on the IRIS Pipeline

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![LLMOps](https://img.shields.io/badge/Governance-LLMOps-blueviolet)
![Vertex AI](https://img.shields.io/badge/Platform-Google%20Vertex%20AI-4285F4?logo=googlecloud&logoColor=white)
![Guardrails](https://img.shields.io/badge/Defense-Input%20%26%20Output%20Guardrails-00C853)

**Author:** Manoj Prathapa  
**Course:** IIT Madras BS in Data Science & Applications — MLOps  
**Repository:** `23F1001473_MLOPS_WEEKLY_ASSIGNMENT`  
**Target Branch:** `week_11`  

---

## 📌 Executive Summary

While standard ML evaluation tests whether a model produces correct outputs on well-formed inputs, it fails to account for adversarial threats unique to the text-in/text-out interfaces of Large Language Models.

This repository implements **Runtime LLM Governance and Guardrails** for the IRIS classification pipeline, defending against **Prompt Injection** and **Prompt Leakage** across both raw-feature (`v1`) and natural language description (`v2`) models.

```text
[User Input]
     │
     ▼
[Input Guardrails] ──(Matches Blocklist / Schema Violation?)──► [Return {"blocked": true}]
     │ (Clean)
     ▼
[Fine-Tuned LLM Endpoint (v1 / v2)]
     │
     ▼
[Output Guardrails] ──(Detects Secret Tokens / Off-topic?)────► [Return Fallback Safe Message]
     │ (Safe)
     ▼
[Verified Response: setosa / versicolor / virginica]

🔬 Benchmark & Governance EvaluationGovernance MetricBefore GuardrailsAfter GuardrailsOperational InterpretationPrompt Injection Block Rate0.0% (Vulnerable)100.0% (Guarded)100% of instruction overrides and roleplay attacks intercepted.Prompt Leakage Block Rate0.0% (Vulnerable)100.0% (Guarded)System keys and context window extraction attempts neutralized.False Positive RateN/A0.0% (Optimal)Zero legitimate IRIS feature inputs were incorrectly blocked.Clean Input Accuracy100.0%100.0%Normal classification performance preserved.Accuracy DeltaN/A0.0%Guardrail validation layer introduces zero performance penalty.

📂 Repository Structure
23F1001473_MLOPS_WEEKLY_ASSIGNMENT/
├── run_llm_guardrails_evaluation.py  # Master evaluation & guardrails execution script
├── evidence/
│   ├── RUBRIC_00_SETUP.md            # Environment setup verification
│   └── guardrails_evaluation_report.txt # Full benchmark tables & raw red-team logs
├── AI_USAGE_DOC.md                   # Mandatory AI tool usage transparency document
├── VIDEO_SCRIPT.md                   # Complete 15-minute video screencast transcript
└── README.md                         # Project documentation