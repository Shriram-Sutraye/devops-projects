# 10 - Argo CD & GitOps Setup

This guide takes you through installing Argo CD and verifying the "GitOps" magic where your code automatically deploys to the cluster.

---

## 🎯 Goal
Install Argo CD on your cluster, expose it to the internet, and verify that it automatically synced your Spring Boot application.

---

## 📋 Prerequisites
- You must have a running EKS cluster (from Doc #09).
- You must have `kubectl` configured.

---

## 🚀 Step 1: Install Argo CD

Run these commands one by one in your terminal:

### 1. Create a Namespace
Think of this as creating a "folder" for Argo CD applications.
```bash
kubectl create namespace argocd
```

### 2. Install the Software
This downloads and installs Argo CD official components.
```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 3. Expose to the Internet
By default, Argo CD is hidden. We need to attach a "Load Balancer" to make it accessible.
```bash
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
```

---

## 🔓 Step 2: Get Access Credentials

### 1. Get the URL
Run this command to find the website address (Load Balancer URL):
```bash
kubectl get svc argocd-server -n argocd
```
> **Look for the `EXTERNAL-IP` column.**
> It will look like: `a1b2c3d4...us-east-1.elb.amazonaws.com`
>
> **Copy that address.**

### 2. Get the Password
Argo CD generates a random initial password. Run this **exact** command to retrieve and decode it:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```
> **Output:** It will print a long random string (e.g., `s8X9...`). 
> **Copy it carefully.** There is no newline at the end, so be careful not to copy your username prompt by mistake!

---

## 🔗 Step 3: Connect GitHub to Argo CD

We need to tell Argo CD **what** to deploy. We do this by creating a simple file.

### 1. Create the File
Run this command to create the file `argocd-app.yaml`:

```bash
cat <<EOF > argocd-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: spring-boot-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/<YOUR-GITHUB-USERNAME>/devops-projects.git
    targetRevision: master
    path: Jenkins-Zero-To-Hero/java-maven-sonar-argocd-helm-k8s/spring-boot-app-manifests
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
EOF
```

> ⚠️ **Important:** Replace `<YOUR-GITHUB-USERNAME>` with your actual GitHub username!

### 2. Apply the File
Send this instruction to the cluster:
```bash
kubectl apply -f argocd-app.yaml
```
> **Expected Output:** `application.argoproj.io/spring-boot-app created`

---

## ✅ Step 4: Verify in Browser (The "Wow" Moment)

1. Open your web browser.
2. Paste the **EXTERNAL-IP** you copied in Step 2.1.
   - *Note: You might see a "Privacy Warning" (SSL error). This is normal. Click "Advanced" -> "Proceed".*
3. **Login:**
   - **Username:** `admin`
   - **Password:** (The string you copied in Step 2.2)
4. **Look at the Dashboard:**
   - You should see a card named `spring-boot-app`.
   - It should have a green heart 💚 (**Healthy**) and green checkmark ✅ (**Synced**).

---

## ✅ Step 5: Verify on CLI

Check if your actual application pods are running:

```bash
kubectl get pods
```

**Expected Output:**
```
NAME                               READY   STATUS    RESTARTS   AGE
spring-boot-app-54848f6854-abcde   1/1     Running   0          2m
spring-boot-app-54848f6854-fghij   1/1     Running   0          2m
```

If you see `Running`, **CONGRATULATIONS!** 
You have successfully deployed a Java app to Kubernetes using GitOps! 🚀

---

## 🛑 Troubleshooting

### Issue: "Pending" External IP
**Fix:** Run `kubectl get svc argocd-server -n argocd` again after 1-2 minutes. AWS takes a moment to create the Load Balancer.

### Issue: Login Failed
**Fix:** 
- Ensure you copied the FULL password.
- Ensure you are using username `admin`.

### Issue: App status "Broken" / "Degraded"
**Fix:**
- Click on the Broken heart icon in Argo CD.
- Read the error message.
- Common cause: `ImagePullBackOff` (means Docker image name is wrong in `deployment.yml`).
