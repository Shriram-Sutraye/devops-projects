# Jenkins Installation on Ubuntu

This guide covers installing Jenkins on Ubuntu 24.04 LTS.

---

## 📋 Prerequisites

- EC2 instance running Ubuntu 24.04
- SSH access to the instance
- At least 2GB RAM (4GB+ recommended)

---

## 🔧 Step 1: Install Java

Jenkins is a Java application. It requires Java 17 or 21.

```bash
# Update package list
sudo apt update

# Install Java 17
sudo apt install fontconfig openjdk-17-jre -y

# Verify installation
java -version
```

**Expected Output:**
```
openjdk version "17.0.x" 2024-xx-xx
OpenJDK Runtime Environment (build 17.0.x...)
OpenJDK 64-Bit Server VM (build 17.0.x...)
```

---

## 🔧 Step 2: Add Jenkins Repository

Jenkins isn't in Ubuntu's default repositories. We need to add the official Jenkins repo.

### Add the GPG Key

On **Ubuntu 24.04**, there's a known issue with the standard method. Use this approach:

```bash
# Import the key via keyserver (this worked for us!)
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7198F4B714ABFC68
```

> ⚠️ You'll see a warning about `apt-key` being deprecated. Ignore it for now - it still works.

### Add the Repository

```bash
# Add Jenkins repo to sources list
echo "deb https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
```

---

## 🔧 Step 3: Install Jenkins

```bash
# Update package list (now includes Jenkins repo)
sudo apt-get update

# Install Jenkins
sudo apt-get install jenkins -y
```

This will:
- Download Jenkins (~95MB)
- Install it as a system service
- Start Jenkins automatically
- Enable it to start on boot

---

## 🔧 Step 4: Verify Installation

```bash
# Check Jenkins service status
sudo systemctl status jenkins
```

**Expected Output:**
```
● jenkins.service - Jenkins Continuous Integration Server
     Loaded: loaded (/usr/lib/systemd/system/jenkins.service; enabled; ...)
     Active: active (running) since Sun 2026-01-25 16:xx:xx UTC; ...
```

Press `q` to exit the status view.

---

## 🔓 Step 5: Get Initial Admin Password

Jenkins generates a random password on first install:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

**Example Output:**
```
7cb9e2f91bd8463a80d022f77441bfd2
```

**COPY THIS PASSWORD** - you'll need it in the next step!

---

## 🌐 Step 6: Access Jenkins Web UI

1. Open your browser
2. Go to: `http://<YOUR-EC2-PUBLIC-IP>:8080`
3. Paste the initial admin password
4. Click **"Continue"**

---

## 🔌 Step 7: Install Plugins

When prompted, choose: **"Install suggested plugins"**

This installs common plugins automatically. Wait for completion (2-5 minutes).

---

## 👤 Step 8: Create Admin User

Fill in:
| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | (your choice, e.g., `Admin123.#`) |
| Full name | Your Name |
| Email | your@email.com |

Click **"Save and Continue"**.

---

## 🎉 Step 9: Jenkins is Ready!

You should see the Jenkins dashboard.

---

## 📦 Additional Plugins to Install

For this CI/CD project, install these plugins:

1. Go to **Manage Jenkins** → **Plugins** → **Available plugins**
2. Search and install:
   - `Docker Pipeline`
   - `SonarQube Scanner`
   - `Maven Integration`
3. Restart Jenkins when prompted

---

## 🛑 Common Issues

### "Package jenkins has no installation candidate"

**Cause:** GPG key not properly imported

**Solution:**
```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7198F4B714ABFC68
sudo apt-get update
sudo apt-get install jenkins -y
```

### Jenkins won't start

**Check logs:**
```bash
sudo journalctl -u jenkins -f
```

**Common fix - not enough memory:**
```bash
# Edit Jenkins defaults
sudo nano /etc/default/jenkins

# Reduce memory if needed (change -Xmx to 512m)
JAVA_ARGS="-Xmx512m"

# Restart
sudo systemctl restart jenkins
```

### Can't access port 8080

**Check if Jenkins is listening:**
```bash
sudo netstat -tlnp | grep 8080
```

**Check security group** in AWS console - port 8080 must be open!

---

## 🔧 Useful Commands

```bash
# Start Jenkins
sudo systemctl start jenkins

# Stop Jenkins
sudo systemctl stop jenkins

# Restart Jenkins
sudo systemctl restart jenkins

# Check status
sudo systemctl status jenkins

# View logs
sudo journalctl -u jenkins -f

# Reset admin password (if locked out)
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

---

## 📝 Your Jenkins Details

| Field | Value |
|-------|-------|
| **URL** | http://34.205.16.151:8080 |
| **Username** | `admin` |
| **Password** | `Admin123.#` |
| **Version** | 2.541.1 LTS |
