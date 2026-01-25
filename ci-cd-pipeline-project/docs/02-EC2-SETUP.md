# EC2 Instance Setup

This guide covers launching and configuring an AWS EC2 instance for running Jenkins, Docker, and SonarQube.

---

## 📋 Prerequisites

- AWS Account with EC2 access
- AWS CLI configured locally (optional but helpful)
- SSH client (built into Linux/Mac, use Git Bash or WSL on Windows)

---

## 🖥️ Instance Specifications

| Setting | Value | Why |
|---------|-------|-----|
| **Instance Type** | `t2.large` or `t3.large` | 8GB RAM needed for Jenkins + SonarQube |
| **OS** | Ubuntu 22.04 or 24.04 LTS | Most tutorials use Ubuntu |
| **Storage** | 30-50 GB | Docker images take space |
| **Region** | `us-east-1` (or your preference) | Pick one close to you |

---

## 🚀 Step-by-Step: Launch EC2 Instance

### 1. Open EC2 Console
- Go to: https://console.aws.amazon.com/ec2
- Click **"Launch Instance"**

### 2. Configure Instance

| Field | Value |
|-------|-------|
| **Name** | `jenkins` (or `Jenkins-Zero-To-Hero`) |
| **AMI** | Ubuntu Server 24.04 LTS (64-bit x86) |
| **Instance type** | `t3.large` |
| **Key pair** | Create new → Name: `jenkins` → Download `.pem` file |

### 3. Network Settings

Click **"Edit"** and configure:

| Setting | Value |
|---------|-------|
| **VPC** | Default VPC |
| **Subnet** | No preference |
| **Auto-assign public IP** | Enable |

### 4. Security Group Rules

Create a new security group with these inbound rules:

| Type | Port | Source | Purpose |
|------|------|--------|---------|
| SSH | 22 | My IP (or 0.0.0.0/0) | SSH access |
| Custom TCP | 8080 | 0.0.0.0/0 | Jenkins UI |
| Custom TCP | 9000 | 0.0.0.0/0 | SonarQube UI |

> ⚠️ **Security Note:** Using `0.0.0.0/0` (anywhere) is fine for learning but NOT for production!

### 5. Storage
- Change root volume to **30 GB** (or more)

### 6. Launch
- Click **"Launch Instance"**
- Wait for status: **Running**

---

## 🔐 SSH Connection

### 1. Move the Key File to Your Project
```bash
mv ~/Downloads/jenkins.pem ~/Projects/devops-projects/
```

### 2. Fix Key Permissions (CRITICAL!)
```bash
chmod 400 ~/Projects/devops-projects/jenkins.pem
```
> Without this step, SSH will reject the connection with "permissions too open" error.

### 3. Connect to Your Instance
```bash
ssh -i "/home/axonritts/Projects/devops-projects/jenkins.pem" ubuntu@<YOUR-PUBLIC-IP>
```

Replace `<YOUR-PUBLIC-IP>` with your instance's public IP from the EC2 console.

---

## ✅ Verification

Once connected, you should see:
```
Welcome to Ubuntu 24.04.3 LTS (GNU/Linux 6.14.0-1018-aws x86_64)
...
ubuntu@ip-172-31-xx-xx:~$
```

You're in! 🎉

---

## 🔧 AWS CLI Commands (Optional)

If you prefer CLI over console:

### List Running Instances
```bash
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" \
  --query "Reservations[*].Instances[*].[InstanceId,PublicIpAddress,Tags[?Key=='Name'].Value|[0]]" \
  --output table
```

### Open All Traffic (for learning only!)
```bash
aws ec2 authorize-security-group-ingress \
  --group-id <SECURITY-GROUP-ID> \
  --protocol -1 --port -1 --cidr 0.0.0.0/0
```

### Stop Instance (save money when not using)
```bash
aws ec2 stop-instances --instance-ids <INSTANCE-ID>
```

### Start Instance
```bash
aws ec2 start-instances --instance-ids <INSTANCE-ID>
```

---

## 🛑 Common Issues

### "Permission denied (publickey)"
- **Cause:** Wrong key file, or key file not found
- **Fix:** Check the path to your `.pem` file and run `chmod 400` on it

### "Connection timed out"
- **Cause:** Security group doesn't allow SSH
- **Fix:** Add inbound rule for port 22 from your IP

### Instance shows "Running" but can't connect
- **Cause:** Public IP not assigned
- **Fix:** Enable "Auto-assign Public IP" or allocate an Elastic IP

---

## 📝 Your Instance Details

| Field | Value |
|-------|-------|
| **Instance ID** | `i-0860e0e7ffe609373` |
| **Public IP** | `34.205.16.151` |
| **Instance Type** | `t3.large` |
| **Region** | `us-east-1` |
| **Key File** | `jenkins.pem` |
| **SSH Command** | `ssh -i "/home/axonritts/Projects/devops-projects/jenkins.pem" ubuntu@ec2-34-205-16-151.compute-1.amazonaws.com` |
