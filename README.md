# 🤖 AI Code Reviewer Bot

An automated code review pipeline that triggers on every pull request, analyzes the diff using an LLM, and posts structured feedback directly as a PR comment — with zero manual effort.

<img width="1136" height="941" alt="image" src="https://github.com/user-attachments/assets/6f3766fe-14fa-4905-879e-e32d1f645020" />


## How It Works

```
PR opened/updated → GitHub Action triggers → Fetch PR diff via GitHub REST API → Send diff to Groq LLM (LLaMA 3.3 70B) → Post structured review as PR comment
```

## Review Output

Every review includes:
- **Summary** — what the PR does in 1-2 lines
- **Issues** — bugs, security vulnerabilities, logic errors with line references
- **Suggestions** — readability, performance, and best practice improvements
- **Verdict** — Approve / Request Changes / Needs Discussion

## Sample Detection

The bot detected the following in a test PR:
- SQL injection vulnerability (line 4)
- Hardcoded credential (line 6)
- Missing zero-division check (line 9)
- Memory inefficiency in list construction (lines 12-14)

## Tech Stack

| Tool | Purpose |
|---|---|
| GitHub Actions | Workflow trigger on pull_request events |
| Python | Core scripting |
| Groq SDK | LLM API client |
| LLaMA 3.3 70B | Code analysis and review generation |
| GitHub REST API | Fetch PR diff and post review comment |

## Setup

1. Clone this repo
2. Go to Settings → Secrets and variables → Actions → New repository secret
3. Add `GROQ_API_KEY` with your key from console.groq.com
4. Open any pull request — bot triggers automatically in 15-20 seconds

## Project Structure

```
ai-code-reviewer/
├── .github/
│   └── workflows/
│       └── code_review.yml
├── reviewer.py
├── requirements.txt
└── README.md
```

## Use In Your Own Repo

Copy `.github/workflows/code_review.yml` and `reviewer.py` into your project and add the `GROQ_API_KEY` secret. Works on any Python or non-Python repo.
