# 🎯 Delhi Career Navigator

An **AI-powered career guidance platform** that helps **Delhi & NCR students** discover the most suitable career paths based on their skills, interests, constraints, and local job-market demand.

Built for **Delhi AI Grind Hackathon 2026 🚀**

---

## 🌐 Project Overview

Choosing the right career is difficult due to:
- Limited access to quality guidance
- Confusion between multiple career options
- Budget, time, and skill constraints
- Lack of local (Delhi-specific) job awareness

**Delhi Career Navigator** solves this problem using AI-driven insights combined with **Delhi NCR job market data** to provide **realistic, personalized career pathways**.

---

## 🖼️ UI Preview

### 🏠 Homepage
![Homepage UI](\frontend\src\assets\image-01.png)

### 📝 Career Input Form
![Form UI](\frontend\src\assets\image-02.png)

### 📊 Career Recommendations Pages
![Dashboard UI](\frontend\src\assets\image-03.png)

> 📌 *Images show the actual UI flow: homepage → input form → AI recommendations.*

---

## 🧠 How It Works

1. User fills a short career assessment form
2. Inputs include skills, stream, availability, budget & preferences
3. Backend AI engine analyzes the profile
4. Career paths are matched with **Delhi NCR demand**
5. Top 3 career pathways are generated
6. Each career includes:
   - Why it fits the user
   - Effort & trade-offs
   - Local relevance
   - 30-day action plan

---

## ✨ Key Features

- 🤖 AI-powered career recommendations
- 🏙️ Delhi & NCR context-aware analysis
- 📋 Skill, time & budget-based matching
- ⭐ Primary + backup career options
- 📅 Actionable 30-day starter plan
- 🌐 Language-ready (English / Hindi)
- 🎨 Clean, student-friendly UI

---

## 🧩 Example Career Output

Each recommendation includes:

- **Career Title** (Primary / Backup)
- **Match value**
- **Expected Salary (Delhi NCR)**
- **Job Locations**
- **Why it fits the user**
- **Delhi-specific opportunities**

---

## 🛠️ Tech Stack

### Frontend
- React (Vite)
- TypeScript
- Tailwind CSS
- Component-based UI

### Backend
- Django
- Django REST Framework
- AI logic module (LLM-based, Rules Based AI)
- Delhi job-market dataset (JSON)
---

## 🚀 Getting Started

### Clone the Repository
```bash
git clone https://github.com/Rohit-Patel-Techie/delhi-career-navigator.git
cd delhi-career-navigator

### Frontend Setup
- cd frontend
- npm install
- npm run dev

### Backend Setup
- cd backend
- python -m venv venv
- source venv/bin/activate      # Windows: venv\Scripts\activate
- pip install -r requirements.txt
- python manage.py runserver

- This project is developed for educational and hackathon purposes only.