# 09 - Kubernetes Setup (EKS)

This section guides you through creating a professional-grade Kubernetes cluster on AWS using EKS (Elastic Kubernetes Service).

---

## 🎯 Goal
Create a cluster named `spring-boot-cluster` in `us-east-1` with 2 powerful nodes (`t3.large`) to run our Java application and DevOps tools.

---

## 📋 Prerequisites

Before starting, open your terminal (on your EC2 instance) and verify you have the tools:

### 1. Check AWS CLI
```bash
aws --version
```
> **Expected Output:** `aws-cli/2.x.x ...`

### 2. Check Permissions
Verify you are logged in as the correct user:
```bash
aws sts get-caller-identity
```
> **Expected Output:** You should see your `UserId`, `Account`, and `Arn`.

### 3. Check eksctl
```bash
eksctl version
```
> **Expected Output:** `0.210.0` (or similar)

---

## 🏗️ Step 1: Create the Cluster

This single command automates the entire setup (VPC, Subnets, IAM Roles, EC2 Nodes).

**Copy and paste this exact command:**

```bash
eksctl create cluster \
  --name spring-boot-cluster \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.large \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed
```

### ⏳ What happens now?
- You will see logs saying `building cluster stack`, `deploying stack`, etc.
- **DO NOT CLOSE THE TERMINAL.**
- This process takes **15-20 minutes**. Go grab a coffee! ☕

### ✅ How do I know it's done?
You will see this validation message at the end:
```
[✔]  EKS cluster "spring-boot-cluster" in "us-east-1" region is ready
```

---

## 🔌 Step 2: Configure kubectl

`eksctl` usually does this automatically, but let's be sure. Run this command to tell your local `kubectl` how to talk to the new cluster:

```bash
aws eks update-kubeconfig --region us-east-1 --name spring-boot-cluster
```

> **Expected Output:** `Updated context arn:aws:eks:us-east-1:xxxx:cluster/spring-boot-cluster in /home/ubuntu/.kube/config`

---

## ✅ Step 3: Verify Everything

### 1. Check the Nodes (Servers)
```bash
kubectl get nodes
```
> **Expected Output:**
> You should see **2 items** listed.
> STATUS must be **Ready**.
>
> ```
> NAME                             STATUS   ROLES    AGE   VERSION
> ip-192-168-xx-xx.ec2.internal    Ready    <none>   5m    v1.33...
> ip-192-168-xx-xx.ec2.internal    Ready    <none>   5m    v1.33...
> ```

### 2. Check System Components
```bash
kubectl get pods -A
```
> **Expected Output:**
> A list of `aws-node`, `coredns`, `kube-proxy`. All should show `Running`.

---

## 🛑 Troubleshooting

### Issue: "Error: cannot find map config"
**Fix:** Run the `aws eks update-kubeconfig` command from Step 2 again.

### Issue: Logs hang on "waiting for CloudFormation stack"
**Fix:** This is normal! It takes 20 minutes. Just wait.

### Issue: "Insufficient Capacity"
**Fix:** AWS might be out of `t3.large` instances in a specific zone. Delete the cluster and try a different region (e.g., `us-east-2`).

---

## 💰 Cost Warning (Very Important!)

This cluster runs on real AWS infrastructure.
- **Cost:** ~$6.00 per day
- **Action:** If you are done for the day/week, **DELETE IT** to save money.

### How to Delete
```bash
eksctl delete cluster --name spring-boot-cluster --region us-east-1
```
