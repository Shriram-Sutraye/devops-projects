# SonarQube Setup

This guide covers running SonarQube as a Docker container and integrating it with Jenkins.

---

## 📋 Prerequisites

- EC2 instance with Docker installed
- Jenkins running with SonarQube Scanner plugin installed
- At least 4GB RAM available (SonarQube is memory-hungry!)

---

## 🤔 What is SonarQube?

SonarQube is a **code quality and security scanner**. It analyzes your code and reports:

| Check | What it Finds |
|-------|---------------|
| **Bugs** | Code that will likely cause errors |
| **Vulnerabilities** | Security risks (SQL injection, XSS, etc.) |
| **Code Smells** | Maintainability issues |
| **Coverage** | How much code is tested |
| **Duplications** | Copy-pasted code |

---

## 🐳 Step 1: Run SonarQube Container

The easiest way to run SonarQube is via Docker:

```bash
docker run -d --name sonarqube -p 9000:9000 sonarqube:lts-community
```

**Breakdown:**
| Flag | Meaning |
|------|---------|
| `-d` | Run in background (detached mode) |
| `--name sonarqube` | Name the container "sonarqube" |
| `-p 9000:9000` | Map port 9000 on host to 9000 in container |
| `sonarqube:lts-community` | Official free SonarQube image (LTS = Long Term Support) |

---

## ⏳ Step 2: Wait for Startup

SonarQube takes **1-2 minutes** to start. Check the logs:

```bash
docker logs -f sonarqube
```

Wait until you see:
```
SonarQube is operational
```

Press `Ctrl+C` to exit the log view.

---

## 🌐 Step 3: Access SonarQube UI

1. Open browser: `http://<YOUR-EC2-IP>:9000`
2. Wait for the loading screen to finish
3. Login with default credentials:
   - **Username:** `admin`
   - **Password:** `admin`
4. You'll be prompted to change the password - do it!

---

## 🔑 Step 4: Generate Access Token

Jenkins needs a **token** (not your password) to authenticate with SonarQube.

### In SonarQube UI:

1. Click your **profile icon** (top-right) → **My Account**
2. Click **"Security"** tab
3. Under **"Generate Tokens"**:
   | Field | Value |
   |-------|-------|
   | Name | `jenkins` |
   | Type | Global Analysis Token |
   | Expires in | No expiration (for learning) |
4. Click **"Generate"**
5. **COPY THE TOKEN IMMEDIATELY** - it won't show again!

Token format: `sqa_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## 🔧 Step 5: Configure Jenkins → SonarQube

### Part A: Add Token as Jenkins Credential

1. Go to Jenkins → **Manage Jenkins** → **Credentials**
2. Click **(global)** under "Stores scoped to Jenkins"
3. Click **"Add Credentials"**
4. Fill in:
   | Field | Value |
   |-------|-------|
   | Kind | Secret text |
   | Secret | (paste your SonarQube token) |
   | ID | `sonarqube-token` |
   | Description | SonarQube Token |
5. Click **Create**

### Part B: Configure SonarQube Server

1. Go to **Manage Jenkins** → **System**
2. Scroll to **"SonarQube servers"** section
3. Check **"Environment variables"**
4. Click **"Add SonarQube"**
5. Fill in:
   | Field | Value |
   |-------|-------|
   | Name | `sonarqube` |
   | Server URL | `http://<YOUR-EC2-IP>:9000` |
   | Server authentication token | (select `sonarqube-token`) |
6. Click **Save**

---

## ✅ Step 6: Verify Integration

You can test the connection by running a simple pipeline:

```groovy
pipeline {
    agent any
    stages {
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh 'echo "SonarQube is connected!"'
                }
            }
        }
    }
}
```

If it runs without errors, the integration is working!

---

## 🐳 Useful Docker Commands for SonarQube

```bash
# Check if SonarQube is running
docker ps | grep sonarqube

# View logs
docker logs -f sonarqube

# Stop SonarQube
docker stop sonarqube

# Start SonarQube
docker start sonarqube

# Restart SonarQube
docker restart sonarqube

# Remove container (deletes all data!)
docker rm -f sonarqube

# Check container resource usage
docker stats sonarqube
```

---

## 🛑 Common Issues

### "SonarQube is starting..." hangs forever

**Cause:** Not enough memory (SonarQube needs ~2GB)

**Check memory:**
```bash
free -h
```

**Fix:** Use a larger EC2 instance type (t3.large or bigger).

### "max virtual memory areas vm.max_map_count is too low"

**Cause:** Linux kernel setting too restrictive

**Fix:**
```bash
sudo sysctl -w vm.max_map_count=262144
```

To make permanent:
```bash
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
```

### Container keeps restarting

**Check logs:**
```bash
docker logs sonarqube
```

**Common causes:**
- Out of memory → Use bigger instance
- Port 9000 in use → Stop other container using that port
- Database issues → Remove and recreate container

### "Upgrade immediately" warning

This is just informational. It means a newer version exists. **You can safely ignore it for learning purposes.**

---

## 📝 Your SonarQube Details

| Field | Value |
|-------|-------|
| **URL** | http://13.222.248.55:9000 |
| **Username** | `admin` |
| **Password** | `Admin123.#` |
| **Token** | `sqa_4b03602474d2a964e7265b77440f47a90adc9426` |
| **Container Name** | `sonarqube` |
| **Image** | `sonarqube:lts-community` |
