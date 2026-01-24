# Module 1: GitHub Actions (The Modern Standard)
## Deep Dive: Building Your First Automation Engine

In Module 0, we talked about the Car Factory. Now, we are going to build the **Robot Instructions** for that factory. In the world of GitHub, those instructions are called **Workflows**.

---

## 🤖 1.1 What is GitHub Actions? (Analogy Time)

Imagine GitHub is a massive **Library** where everyone stores their books (Code). 
*   **GitHub Actions** is a team of **Library Robots** that wait for you to do something.
*   When you "Return a Book" (Push Code), the robot springs into action.
*   It can scan the book for typos (Linting), check if the pages are in order (Testing), or even make a copy of the book to send to a bookstore (Deployment).

### Why is it the "Modern Standard" in 2026?
1.  **Zero Setup:** You don't need to buy a server. GitHub gives you the robots for free.
2.  **YAML Power:** You write instructions in a simple format called YAML.
3.  **The Marketplace:** There are thousands of pre-made robots you can "borrow" to do things like "Send a Slack message" or "Deploy to AWS."

---

## 🏗️ 1.2 The Anatomy of a Workflow (The Recipe)

Every GitHub Action instruction manual (Workflow) has four main parts:

### 1. The Trigger (The "Starter Pistol")
**Code:** `on: push`
This tells the robot *when* to start. "Start whenever I push new code to the `main` branch."

### 2. The Runner (The "Robot Body")
**Code:** `runs-on: ubuntu-latest`
This tells GitHub what kind of computer the robot should use. Linux (Ubuntu) is the most common because it's fast and cheap.

### 3. Jobs (The "Departments")
A workflow can have multiple jobs. 
*   **Job A:** Build the car engine.
*   **Job B:** Paint the car doors.
Jobs usually run at the same time (in parallel) to save time!

### 4. Steps (The "Individual Actions")
Inside a Job, you have Steps. These happen one-by-one.
*   Step 1: Get the parts.
*   Step 2: Screw the bolts.
*   Step 3: Test the engine.

---

## 🛡️ 1.3 2026 Best Practices: The "Pro" Level

To shine in an interview, you shouldn't just write "a script." You should write a **Secure, Professional Pipeline**.

1.  **Secret Management:** Never put passwords in your code. Use `${{ secrets.MY_PASSWORD }}`. GitHub has a "Vault" where these are kept safe.
2.  **Version Pinning:** Don't just say "Use the latest robot." Say "Use version 4.1.0." This prevents your pipeline from breaking if the robot manufacturer changes something.
3.  **The Checkout Action:** This is the most important step. Your robot starts in an empty room. `actions/checkout` is the command that tells the robot: "Go to the library and fetch my code so you can work on it."

---

## 🚀 1.4 Your First Project: Project 01 - Hello World

We are going to build a workflow that simply says "Hello" to you whenever you push code.

### The "Recipe" (YAML)
We will create a file at `.github/workflows/hello.yml`. 

> **Crucial Rule:** GitHub Actions ONLY works if the file is in the `.github/workflows/` folder. If you put it anywhere else, the robots won't see it!

---

## 📝 Check Your Understanding

*   **Q:** "Where must I store my GitHub Action files?"
*   **A:** In the `.github/workflows/` folder at the root of my repository.
*   **Q:** "What is a 'Runner'?"
*   **A:** It's the virtual machine/computer that actually executes your commands.

---

> **Next Step:** We are going to code **Project 01**. I will set up the folder structure and create your first real working YAML file!
