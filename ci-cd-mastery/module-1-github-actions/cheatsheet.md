# Module 1: The "Swiss Army Knife" GHA Cheatsheet
## Quick Reference for Building and Troubleshooting

As you work through your projects, use this file as your "cheat code." It contains the most common YAML snippets you'll need in 2026.

---

## 📋 1. Common Triggers (`on:`)

| Trigger | Description | Code Snippet |
| :--- | :--- | :--- |
| **All Pushes** | Runs on every single push. | `on: [push]` |
| **Target Branch** | Runs only when pushing to `main`. | `on: push: branches: [main]` |
| **Pull Requests** | Runs only when a PR is opened. | `on: [pull_request]` |
| **Manual** | Adds a "Run Workflow" button. | `on: workflow_dispatch` |
| **Scheduled** | Runs every day at midnight. | `on: schedule: - cron: '0 0 * * *'` |

---

## 🛠️ 2. Essential "Robot Parts" (Common Actions)

| Task | Action to Use | Why? |
| :--- | :--- | :--- |
| **Get Code** | `actions/checkout@v4` | You start with 0 files. This downloads your repo. |
| **Install Node** | `actions/setup-node@v4` | Sets up the specific version of Node/NPM you want. |
| **Install Python** | `actions/setup-python@v5` | Sets up Python and pip. |
| **Upload Files** | `actions/upload-artifact@v4` | Saves a build file (like a PDF or Zip) for you to download later. |
| **Cache Stuff** | `actions/cache@v4` | Speeds up builds by remembering `node_modules`. |

---

## 🧪 3. Logical Operators (The "If/Then" logic)

Want your robot to skip a step? Use `if`.

```yaml
steps:
  - name: Only run on Main
    if: github.ref == 'refs/heads/main'
    run: echo "I am on the main branch!"

  - name: Run even if previous step failed
    if: siempre() # Always (Spanish: siempre) - Oops, in GHA it's actually:
    # if: always()
    run: echo "I will run no matter what happens before me."
```

---

## 🚨 4. Troubleshooting: "The Robot is Breaking!"

If your pipeline turns **RED**, check these 3 things first:

1.  **Indentation:** YAML is *extremely* picky about spaces. Use 2 spaces, never tabs.
2.  **Permissions:** Did you give the robot permission to write to the repo? (Check `permissions:` block).
3.  **Secrets:** Did you spell the secret name exactly right in the GitHub settings? (Case sensitive!).

---

## 🎤 5. Interview "Killer" Question

**Interviewer:** *"Can a Job use the files created by a previous Job?"*
**You:** *"By default, NO. Each Job starts on a clean, new computer with a fresh disk. If Job A builds a file and Job B needs to test it, Job A must 'Upload' that file as an **Artifact**, and Job B must 'Download' it. This is a core part of keeping CI/CD environments isolated and clean."*

---

> **Tip for 2026:** If you get stuck, use **GitHub Copilot** or a modern AI tool to "Explain this YAML." It's now standard practice for DevOps engineers to use AI for debugging complex workflow logic.
