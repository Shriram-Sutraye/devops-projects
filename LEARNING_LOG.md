# 📔 DevOps Learning Log
> **Start Date:** January 24, 2026  
> **Goal:** Zero to Hero in DevOps (CI/CD, AWS, Kubernetes)

---

## 📅 January 24, 2026

### ⏰ 07:40 AM EST - First Jenkins Pipeline Success!
**Activity:** Ran the `first-jenkins` pipeline from the *Jenkins Zero to Hero* repo.
**Key Learnings:**
*   **Containerized Agents:** Jenkins didn't use the server's tools. It pulled a `node:16-alpine` Docker image on the fly.
*   **Isolation:** The job ran inside a temporary container and destroyed it afterwards. This keeps the EC2 server clean.
*   **Volume Mounting:** Jenkins automatically "mounted" the code from the workspace into the Docker container so it could run `node --version`.

### ⏰ 07:20 AM EST - Installing Docker on EC2
**Activity:** Installed Docker Engine on the Ubuntu 22.04 instance.
**Key Learnings:**
*   **Prerequisites:** Needed `ca-certificates` and `curl` before installation.
*   **Repository Setup:** Had to add the official Docker GPG key and stable repository (standard security practice on Linux).
*   **Permissions:** Added `jenkins` and `ubuntu` users to the `docker` group.
    *   *Why?* So they can run `docker run` without needing `sudo` (crucial for automation).

### ⏰ 07:10 AM EST - Securing the Instance
**Activity:** Configured AWS Security Groups.
**Key Learnings:**
*   Opened ports **8080** (Jenkins), **80** (HTTP), and **22** (SSH).
*   Changed ingress to `0.0.0.0/0` (Allow All) for learning purposes, though in production, we would lock this down to specific IP addresses.

### ⏰ 06:45 AM EST - Installing Jenkins (The Challenge)
**Activity:** Installed OpenJDK 17 and Jenkins on AWS EC2.
**Key Learnings:**
*   **GPG Key Issue:** Encountered a `NO_PUBKEY` error because the official Jenkins documentation had a key mismatch with the Ubuntu 22.04 keyserver.
*   **Solution:** Manually fetched the keys (`5BA31D57EF5975CA` and `7198F4B714ABFC68`) from `keyserver.ubuntu.com`.
*   **Java Compatibility:** Learned that while Java 25 is the latest, Jenkins is most stable on **Java 17 (LTS)**.

### ⏰ 02:45 AM EST - GitHub Actions (Module 1)
**Activity:** Created the "Hello World" Workflow.
**Key Learnings:**
*   **Workflow Location:** Files *must* live in `.github/workflows/`.
*   **Structure:** Trigger (`on`) -> Runner (`runs-on`) -> Jobs -> Steps.
*   **Runners:** GitHub provides free `ubuntu-latest` runners (virtual machines) to execute code.
*   **Actions:** Used `actions/checkout@v4` to pull code before running usage.

### ⏰ 08:20 AM EST - Multi-Stage, Multi-Agent Pipeline (Calculator App)
**Activity:** Built and successfully ran a full CI/CD pipeline for a Python Calculator app.
**Project Structure:**
*   **App:** Simple Python calculator (`src/calculator.py`).
*   **Tests:** 9 unit tests using `pytest` (`tests/test_calculator.py`).
*   **Pipeline:** 4 Stages (Lint, Test, Build, Deploy).

**Real-World Challenges & Fixes:**
1.  **Repo Visibility:** Jenkins couldn't clone the private repo without credentials.
    *   *Fix:* Temporarily made repo public (simpler for learning) vs. adding PAT to Jenkins (best practice).
2.  **Docker Permissions:** `pip install` failed inside the container because Jenkins runs as non-root user `115:122`.
    *   *Fix:* Added `environment { HOME = '/tmp' }` to Jenkinsfile so pip has a writable cache.
    *   *Fix:* Used `pip install --user` to install packages in the local user directory instead of system-wide.
3.  **Context Issues:** Pipeline ran commands from the root, but the app was in a subfolder.
    *   *Fix:* Wrapped steps in `dir('jenkins-demos/calculator-app')` block.

**Key Learnings (The "Aha!" Moments):**
*   **Agent `none`:** Defining `agent none` at the top level allowed us to use *different* Docker containers for each stage (Python for testing, Ubuntu for deploy).
*   **Environment Isolation:** The `pytest` installed in Stage 2 didn't exist in Stage 3. Each stage started with a fresh, clean container.
*   **Workspace persistence:** Even though containers were destroyed, the code in the Jenkins workspace (`/var/lib/jenkins/workspace/...`) persisted and was shared across stages via volume mounts.
