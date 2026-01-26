# 09 - Kubernetes Setup (EKS)

This guide covers provisioning a production-grade AWS EKS cluster.

---

## 📋 What We Built

- **Cluster Name:** `spring-boot-cluster`
- **Region:** `us-east-1`
- **Kubernetes Version:** v1.33
- **Nodes:** 2x `t3.large` instances (8GB RAM each)

---

## 🚀 Step 1: Install Tools (Already Done)

Ensure you have:
- `kubectl`
- `eksctl`
- `aws` CLI

---

## 🏗️ Step 2: Create Cluster

We used this command to provision the infrastructure:

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

This process takes ~15-20 minutes and creates:
1. VPC & Subnets
2. IAM Roles
3. Control Plane
4. Worker Nodes (EC2)

---

## ✅ Step 3: Verify Access

### Check Nodes
```bash
kubectl get nodes
```
**Expected Output:**
```
NAME                             STATUS   ROLES    AGE   VERSION
ip-192-168-16-86.ec2.internal    Ready    <none>   5m    v1.33...
ip-192-168-40-218.ec2.internal   Ready    <none>   5m    v1.33...
```

### Check System Pods
```bash
kubectl get pods -A
```
**Expected Output:**
All pods in `kube-system` should be `Running`.

---

## 🛑 Troubleshooting

### "Error: cannot find map config"
Update your kubeconfig:
```bash
aws eks update-kubeconfig --region us-east-1 --name spring-boot-cluster
```

### "Unauthorized"
Ensure your AWS CLI credentials are correct:
```bash
aws sts get-caller-identity
```

---

## 💰 Cost Alert
This cluster costs approximately **$0.26/hour** ($6/day).
**Remember to delete it if you stop working for a long time!**

### Delete Cluster
```bash
eksctl delete cluster --name spring-boot-cluster --region us-east-1
```
