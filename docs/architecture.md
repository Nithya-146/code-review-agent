# System Architecture & Multi-Agent Design

## 1. System Overview
The Smart Code Inspection Platform is a multi-agent system designed to analyze Python and Java source code for quality issues, design anti-patterns, and OWASP Top 10:2025 security vulnerabilities.

## 2. Multi-Agent Pipeline Flow
1. **Code Submission Module:** Ingests raw code via direct paste or file upload (.py / .java).
2. **Deterministic AST Validator:** Validates syntax using Python `ast` and Java `javalang`. Halts execution on syntax errors to save computational resources.
3. **Multi-Agent Orchestration:**
   - **Code Analysis Agent:** Identifies code smells (long methods, magic numbers, deep nesting) and computes complexity metrics.
   - **Security Vulnerability Agent:** Evaluates code against OWASP Top 10 (2025/2026) standards (A01-A10) and maps findings to CWE IDs with severity ratings.
4. **Remediation Agent:** Generates production-ready replacement snippets and explains the mechanical rationale for fixes.
5. **PR Summary Agent:** Combines all agent findings into a structured Pull Request style Markdown summary.
6. **Conversational Code Assistant:** RAG-powered chatbot grounded in ChromaDB vector store using `sentence-transformers/all-MiniLM-L6-v2`.

## 3. Core Agent Responsibilities Matrix
| Agent Name | Primary Responsibility | Input | Output |
|---|---|---|---|
| AST Validator | Syntax check & metadata extraction | Raw Source Code | AST Metadata / Syntax Errors |
| Code Analysis Agent | Code smells, complexity, anti-patterns | Valid AST & Code | Code Smell Findings List |
| Security Vulnerability Agent | OWASP 2025 scanning & CWE mapping | Code & RAG Context | Security Findings List |
| Remediation Agent | Concrete diffs & patch generation | Security & Smell Findings | Remediation List |
| PR Summary Agent | Human-readable executive summary | All Agent Findings | Markdown PR Report |