# 🧠 AutoScheduler — Intelligent Weekly Planner

## Overview
**AutoScheduler** is a personal automation project designed to enhance productivity and life improvement through intelligent scheduling.  
It runs entirely on a **Raspberry Pi 4**, utilizing the **Notion API** to automatically generate and manage a weekly schedule—completely hands-free.

This project is part of my workflow for my new **IT Support Specialist** role, and it's built to continuously evolve with my personal and professional growth goals.

---

## 🎯 Core Purpose
AutoScheduler creates a **smart weekly plan** inside Notion, powered by automation and AI.  
It determines:
- **When** to schedule tasks for the upcoming week.
- **What** to prioritize (work goals, personal projects, skill growth, or rest).
- **How** to adapt based on my habits, time availability, and recent activity.

The idea is simple:  
> *Let the system think, plan, and optimize my week before I even wake up Monday.*

---

## 🧩 Key Features
- **🗓 Automatic Weekly Planning**  
  Every week, the system runs in the background to generate a new Notion schedule.

- **🤖 AI-driven Recommendations**  
  Uses lightweight AI models to suggest what to do on weekends — whether it’s self-improvement, studying, or creative rest.

- **⚙️ Background Execution**  
  Runs silently on a Raspberry Pi 4, triggered automatically at optimal times during the week.

- **📡 Notion API Integration**  
  Seamlessly creates, updates, and organizes tasks and pages in my Notion workspace.

- **📈 Goal-Oriented Design**  
  Prioritizes long-term growth — balancing IT skill development, health, relationships, and financial goals.

---

## 🛠️ Tech Stack
- **Hardware:** Raspberry Pi 4 (4GB)
- **Language:** Python 3
- **APIs:** Notion API
- **Libraries:**  
  - `requests` — for API calls  
  - `schedule` — for time-based task execution  
  - `openai` — for AI logic & suggestions *(optional)*  
  - `dotenv` — for environment variables  
  - `logging` — for tracking task execution  

---

## 🔧 How It Works
1. **Runs automatically** once per week (Sunday night or Monday morning).
2. **Fetches goals and context** from a Notion database.
3. **Analyzes** current tasks, habits, and available hours.
4. **Generates a new schedule** block-by-block for the week.
5. **Adds AI insights** for weekend improvement opportunities.
6. **Syncs results** back into Notion for review and manual adjustments.

---

## 🚀 Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/autoscheduler.git
   cd autoscheduler
