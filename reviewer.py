import os
import requests
from google import genai

# ── Config ────────────────────────────────────────────────────
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
GITHUB_TOKEN   = os.environ["GITHUB_TOKEN"]
REPO           = os.environ["GITHUB_REPOSITORY"]
PR_NUMBER      = os.environ["PR_NUMBER"]

client = genai.Client(api_key=GEMINI_API_KEY)

# ── Fetch PR diff ─────────────────────────────────────────────
def get_pr_diff():
    url     = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept":        "application/vnd.github.v3.diff"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

# ── Review diff with Gemini ───────────────────────────────────
def review_code(diff):
    prompt = f"""You are an expert code reviewer. Review the following pull request diff and provide:

1. **Summary** — what this PR does in 1-2 lines
2. **Issues** — bugs, security vulnerabilities, or logic errors (if any)
3. **Suggestions** — improvements for readability, performance, or best practices
4. **Verdict** — Approve / Request Changes / Needs Discussion

Be concise, specific, and actionable. Reference line numbers where possible.

```diff
{diff[:8000]}
```
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text

# ── Post comment on PR ────────────────────────────────────────
def post_comment(review):
    url     = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept":        "application/vnd.github+json"
    }
    body = f"## 🤖 AI Code Review\n\n{review}"
    response = requests.post(url, headers=headers, json={"body": body})
    response.raise_for_status()
    print("Review posted successfully")

# ── Main ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Fetching PR diff...")
    diff = get_pr_diff()

    if not diff.strip():
        print("No diff found — skipping review")
        exit(0)

    print("Sending to Gemini for review...")
    review = review_code(diff)

    print("Posting comment...")
    post_comment(review)