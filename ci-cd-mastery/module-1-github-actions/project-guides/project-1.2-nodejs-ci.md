# Project 1.2 Guide: The Node.js Automated Guard
## Goal: Build, Test, and Lint a Real App

In this project, you are going to set up a pipeline that acts as a **Guard**. It will prevent any "bad code" from being merged by automatically running checks.

---

## 🛠️ Step 1: Prepare the "App" (Local Setup)

Before the pipeline can run, we need a simple application to test. 

1.  **Create your project folder:** `mkdir -p projects/02-nodejs-app`
2.  **Initialize a Node project:**
    *   Create a `package.json`.
    *   Add `jest` (for testing) and `eslint` (for checking code style) to your `devDependencies`.
3.  **Create a simple source file:** (e.g., `src/index.js` with a `sum` function).
4.  **Create a test file:** (e.g., `test/index.test.js` to test your `sum` function).

---

## 🤖 Step 2: The "Guard" Workflow

Now, create the YAML file: `.github/workflows/node-ci.yml`.

### 📋 What this workflow must do:
1.  **Trigger:** Run on `push` and `pull_request` to the `main` branch.
2.  **Setup:** Use the latest Ubuntu runner and the `actions/checkout` action.
3.  **The Brains:** Use the `actions/setup-node` action to install Node.js (Version 20).
4.  **The Work:** 
    *   `npm ci`: (Clean Install) This installs your dependencies exactly as they are in your lockfile.
    *   `npm run lint`: Checks if your code is "pretty" and follows rules.
    *   `npm test`: Runs your Jest tests.
    *   `npm run build`: Simulates building the app for production.

---

## 🔍 Deep Dive: Why `npm ci` instead of `npm install`?

This is a common interview question for junior/mid-level DevOps:
*   `npm install` can update your `package-lock.json` if it finds newer compatible versions. **We don't want this in CI.** 
*   `npm ci` is faster, cleaner, and **fails immediately** if the lockfile and package.json don't match. It ensures the environment in GitHub is *identical* to your local machine.

---

## 🚀 2026 Optimization: Caching

Building an app can be slow if you have to download 500MB of `node_modules` every time.
**Your Challenge:** Try to use the `cache` option in `actions/setup-node`. It looks like this:

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm' # This one line saves minutes of build time!
```

---

## ✅ Success Criteria
1.  Push your code and the workflow.
2.  Go to the **Actions** tab.
3.  **Watch it fail!** (I recommend making a typo in your code on purpose first to see the pipeline catch it).
4.  Fix the code and see the "Green Checkmark."

---

> **Once this is done:** You will have built a "Continuous Integration" pipeline that is production-ready.
