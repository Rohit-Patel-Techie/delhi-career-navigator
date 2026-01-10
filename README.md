📘 GITHUB COLLABORATION GUIDE

(Delhi AI Grind Hackathon – Team Workflow)

🧩 1. ONE-TIME SETUP (EVERY TEAM MEMBER)
Step 1: Install Git

👉 Download & install: https://git-scm.com

Verify:

git --version

Step 2: Configure Git (Do this once)
git config --global user.name "Your Name"
git config --global user.email "your-email@gmail.com"

Step 3: Clone the Project Repository
git clone https://github.com/<username>/delhi-career-navigator.git
cd delhi-career-navigator

🌳 2. BRANCH STRUCTURE (IMPORTANT)
Branch	Purpose
main	Final demo-ready code
frontend	Frontend development
backend	Backend development
🏗️ 3. CREATE YOUR OWN WORKING BRANCH
Frontend Developer
git checkout -b frontend
git push origin frontend

Backend Developer
git checkout -b backend
git push origin backend

🔁 4. DAILY WORKFLOW (DO THIS EVERY DAY)
Step 1: Switch to your branch
git checkout frontend   # or backend

Step 2: Pull latest updates
git pull origin main

Step 3: Work ONLY on your folder

Frontend → /frontend

Backend → /backend

Step 4: Save, Commit, Push
git add .
git commit -m "Clear message describing your work"
git push origin frontend   # or backend

👀 5. HOW TO SEE TEAMMATE’S CODE
On GitHub Website

Open repository

Change branch from dropdown

Select frontend or backend

View code and commits

On Local Machine
git checkout backend
git pull origin backend

🔄 6. WHEN SOMEONE NEEDS TO CHANGE OTHER BRANCH CODE
Small change:
git checkout frontend
git pull origin frontend
# make change
git commit -m "Small frontend fix"
git push origin frontend


Inform the branch owner.

Big change (recommended):

Create new branch:

git checkout -b frontend-fix


Push & open Pull Request

Owner reviews and merges

🔀 7. MERGING INTO MAIN (ONLY WHEN READY)
Only Team Lead / Owner should do this
git checkout main
git pull origin main
git merge frontend
git merge backend
git push origin main

🚫 8. WHAT NOT TO DO (VERY IMPORTANT)

❌ Do NOT code directly on main
❌ Do NOT mix frontend + backend in one commit
❌ Do NOT push broken code
❌ Do NOT force push
❌ Do NOT delete branches without discussion

🧯 9. IF SOMETHING GOES WRONG
Check status
git status

Abort merge
git merge --abort

Ask before force actions
🧠 10. GOLDEN RULES (MEMORISE)

✔ Pull before you push
✔ Commit often with clear messages
✔ One branch = one responsibility
✔ main must always be demo-ready
✔ If it’s not pushed → it doesn’t exist