# Windows Local Validation Setup

## Requirements

Use the Main Windows account where the self-hosted runner is installed.

Required local tools:

```text
Git
GitHub CLI
Ollama
Codex CLI authenticated through ChatGPT local auth
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe
```

Required Ollama models:

```text
qwen2.5-coder:7b
llama3.1:latest
```

Do not set `OPENAI_API_KEY` or any paid API key for validation.

Runner labels must include:

```text
self-hosted
Windows
X64
codie-local
codex
ollama
```

## Local Smoke Check

```powershell
& "C:\Users\Main\.venvs\codie-py312\Scripts\python.exe" scripts/codie_validation_gate.py --phase-id Phase35A --phase-part outside-validation --gate-scope INTERMEDIATE_PACKET --target-sha <sha>
```
