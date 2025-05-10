# 💪 Personal Trainer Client Management System

### Project Overview

The **Personal Trainer Client Management System (PTCMS)** is a web application built using **Python** and **Streamlit**. It helps personal trainers and admins manage clients, track progress, assign diet and workout plans, handle payment records, and communicate efficiently with clients.  

The system supports two main roles: **Admin** and **Trainer**, each with specific permissions. The application uses **SQLite databases** and **JSON files** for data storage and retrieval.

---

### Project Architecture

The system follows a **modular architecture** inspired by the **Model-View-Controller (MVC) pattern**, separating:

1. **Model (Data Storage & Business Logic)**  
2. **View (Web Interface using Streamlit)**  
3. **Controller (Business Logic & Role-Based Access)**

---

### 1. Model (Data Storage & Business Logic)

The **Model** layer manages all data, including:

- **Trainers** → stored in SQLite databases (`trainer_db.db`, `data.db`)  
- **Clients** → stored in JSON files (`client_diet.json`, `client_progress.json`, `workout_plans.json`)  
- **Payments** → stored in `payment_records.json`  
- **Phone Numbers** → stored in `phone.json`

Key operations:
- Add, update, delete trainers and clients.
- Assign diet/workout plans.
- Track client progress (weight, height).
- Manage and track payments.

---

### 2. View (Web Interface)

The **View** is built using **Streamlit**, offering:

- A **dark-themed, modern dashboard** for admins and trainers.
- Sidebar navigation to switch between tasks.
- Interactive forms, tables, and success/error messages.
- Separate menus for admin and trainer roles.

---

### 3. Controller (Business Logic & Role-Based Access)

The **Controller** handles user inputs and enforces role-based permissions:

- **Admin:**
  - Add, update, view, and delete trainer accounts.
  - Full access to manage system data.

- **Trainer:**
  - Manage client profiles.
  - Assign diet and workout plans.
  - Track client progress.
  - Monitor payment status.
  - Send WhatsApp messages to clients.

---

### User Roles and Functionalities

#### 👑 Admin
- Add Trainer
- View Trainers
- Update Trainer
- Delete Trainer
- Access full system settings

#### 🏋️ Trainer
- Add Client Details
- View Clients
- Update Client Information
- Assign Diet and Workout Plans
- Track Client Progress
- Manage Payments
- Send WhatsApp Messages

---

### Web Interface Functionalities

- **Trainer Login**
- **Admin Dashboard**
- **Sidebar Menu Navigation**
- **Interactive Forms**
- **Dynamic Tables**
- **WhatsApp Messaging (PyWhatKit)**

---

### Main Files and Data

- `client_diet.json` → Client-specific diet plans  
- `client_progress.json` → Client progress tracking  
- `workout_plans.json` → Workout routines  
- `payment_records.json` → Payment and billing data  
- `phone.json` → Client phone numbers  
- `trainer_db.db`, `data.db` → Trainer and system databases  
- `PyWhatKit_DB.txt` → WhatsApp message logs

---

### How to Use

1. **Run the application**

```bash
streamlit run Home.py
