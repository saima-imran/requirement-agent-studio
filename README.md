# Requirement Agent Studio

A modular, human-in-the-loop prototype for AI-assisted requirements engineering.

Requirement Agent Studio demonstrates how a multi-agent architecture can support the analysis of software requirements by combining rule-based reasoning, software engineering principles, and future AI integration.

---

# Overview

Software requirements often contain ambiguity, security concerns, and compliance issues that are difficult to identify manually.

This project explores how specialised software agents can automatically analyse requirements and produce structured findings that support engineers during the requirements engineering process.

The current implementation provides a rule-based foundation designed for future integration with Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG).

---

# Features

- Requirement extraction from text documents
- Multi-agent analysis pipeline
- Requirement quality analysis
- Security requirement analysis
- Compliance analysis
- Markdown report generation
- Automated unit testing with pytest
- Modular and extensible architecture

---

# Current Architecture

```
Requirement Document
        │
        ▼
RequirementExtractionAgent
        │
        ▼
Requirement Objects
        │
        ▼
AnalysisPipeline
        │
 ┌──────┼──────────────┐
 ▼      ▼              ▼
Quality Security   Compliance
 Agent    Agent        Agent
        │
        ▼
 Findings
        │
        ▼
Markdown Report
```

---

# Project Structure

```
requirement-agent-studio/
│
├── data/
├── output/
├── src/
│   └── requirement_agent_studio/
│       ├── analysis_pipeline.py
│       ├── base_agent.py
│       ├── compliance_agent.py
│       ├── extractor_agent.py
│       ├── models.py
│       ├── quality_agent.py
│       ├── report_generator.py
│       └── security_agent.py
│
├── tests/
├── main.py
└── README.md
```

---

# Running the Project

Clone the repository:

```bash
git clone https://github.com/saima-imran/requirement-agent-studio.git
```

Install the dependencies:

```bash
pip install pytest
```

Run the project:

```bash
$env:PYTHONPATH="src"
py main.py
```

---

# Running the Tests

```bash
py -m pytest
```

---

# Example Analysis

The system analyses each requirement independently using specialised agents.

Example findings include:

- Ambiguous requirements
- Security-related requirements
- Compliance-related requirements
- Human oversight requirements
- Transparency requirements

The analysis is exported as a Markdown report.

---

# Future Work

The current version provides a rule-based implementation.

Future work includes:

- Configuration-driven agents
- LLM integration
- Retrieval-Augmented Generation (RAG)
- Traceability analysis
- Explainable AI support
- EU AI Act compliance assistance
- ISO/IEC 42001 support

---

# Technologies

- Python
- Object-Oriented Programming
- Dataclasses
- pytest
- Markdown
- Git
- GitHub

---

# Research Motivation

This project is part of an ongoing exploration into AI-assisted requirements engineering and trustworthy AI.

The long-term objective is to investigate how specialised AI agents can support requirements analysis while maintaining human oversight, explainability, and compliance with emerging AI regulations.

---

# Author

**Saima Imran**

Software Engineer | Requirements Engineering | AI-Assisted Software Engineering
