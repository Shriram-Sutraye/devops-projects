# Docker Installation on Ubuntu

This guide covers installing Docker and configuring it for Jenkins.

---

## 📋 Prerequisites

- EC2 instance running Ubuntu 24.04
- Jenkins already installed
- SSH access to the instance

---

## 🤔 Why Docker?

Jenkins uses Docker for:
1. **Containerized build agents** - Each build runs in a clean container
2. **Building Docker images** - Package your app as a container
3. **Consistency** - Same environment locally and in production

---

## 🔧 Step 1: Install Docker

```bash
# Update package list
sudo apt update

# Install Docker
sudo apt install docker.io -y
```

This installs:
- Docker Engine (the container runtime)
- Docker CLI (command-line tools)
- containerd (container runtime)

---

## 🔧 Step 2: Add Users to Docker Group

By default, only `root` can run Docker. We need to give permission to:
- `jenkins` user (so Jenkins can build Docker images)
- `ubuntu` user (so you can run Docker commands)

```bash
# Add jenkins user to docker group
sudo usermod -aG docker jenkins

# Add ubuntu user to docker group
sudo usermod -aG docker ubuntu
```

---

## 🔧 Step 3: Restart Services

For the group changes to take effect:

```bash
# Restart Docker
sudo systemctl restart docker

# Restart Jenkins (so it picks up the new permissions)
sudo systemctl restart jenkins
```

---

## ✅ Step 4: Verify Installation

### Test Docker CLI

```bash
# Check Docker version
docker --version
```

**Expected Output:**
```
Docker version 28.x.x, build xxxxxxx
```

### Test Docker is Running

```bash
# List containers (will be empty, that's fine)
docker ps
```

**Expected Output:**
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

### Test Jenkins Can Use Docker

This is the **critical test** - if this fails, your pipeline will fail!

```bash
# Run docker as jenkins user
sudo su - jenkins -c 'docker ps'
```

**Expected Output:**
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

If you see "permission denied", the group membership didn't take effect. Try:
```bash
# Restart everything
sudo systemctl restart docker
sudo systemctl restart jenkins

# Wait 10 seconds, then test again
sudo su - jenkins -c 'docker ps'
```

---

## 🐳 Step 5: Test with Hello World

Run a test container to make sure everything works:

```bash
docker run hello-world
```

**Expected Output:**
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

---

## 🔧 Useful Docker Commands

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# List images
docker images

# Remove a container
docker rm <container-id>

# Remove an image
docker rmi <image-name>

# Stop all containers
docker stop $(docker ps -q)

# Remove all stopped containers
docker container prune

# Pull an image
docker pull <image-name>

# Build an image from Dockerfile
docker build -t <image-name> .

# Run a container
docker run -d --name <name> -p <host-port>:<container-port> <image>
```

---

## 🛑 Common Issues

### "permission denied while trying to connect to Docker daemon"

**Cause:** User not in docker group

**Fix:**
```bash
sudo usermod -aG docker $USER
# Then log out and back in, or run:
newgrp docker
```

### "Cannot connect to the Docker daemon"

**Cause:** Docker service not running

**Fix:**
```bash
sudo systemctl start docker
sudo systemctl enable docker  # Start on boot
```

### Docker commands hang

**Cause:** Docker daemon crashed

**Fix:**
```bash
sudo systemctl restart docker
```

---

## 📝 Your Docker Details

| Field | Value |
|-------|-------|
| **Version** | 28.2.2 |
| **Users with access** | `jenkins`, `ubuntu` |
| **Status** | Active and running |
