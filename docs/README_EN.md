# Bildmind-LernenWorte – Vocabulary Learning through AI

This repository contains the **public module** of the **BuildMind** project,
designed for **efficient foreign language vocabulary learning**
through an adaptive system of spaced repetition, examples, tests, and statistics.

---

## 🎯 Purpose

The `LernenWorte` module implements an MVP system for:

- adding custom words to a personal dictionary
- personalized repetition based on intervals
- taking daily vocabulary tests
- tracking personal progress and performance

> The user adds a word → the system schedules repetitions → the user takes tests → long-term memory is formed.

---

## 🧩 Key Components

- `main.py` — entry point of the FastAPI application
- `alembic/` — database migration system
- `api/` — HTTP endpoints for user interaction
- `config/` — environment variables and global settings
- `core/` — basic business services (without AI)
- `crud/` — database operations (create/read/update/delete)
- `db/` — database structure:
- `models/` — SQLAlchemy ORM models
- `schemas/` — Pydantic request/response schemas
- `database.py` — DB connection logic
- `init_data.py` — initial data loader
- `sdk/` — SDK/client interface for mobile applications

---

## 💾 Entities

- **User** – basic user data
- **Word** – global vocabulary
- **UserWord** – personalized word study records
- **TestSession** – test history
- **UserStats / DailyProgress / LevelProgress** – progress & motivation tracking

---

## 🔐 Features

- Adaptive Spaced Repetition System
- Soft-delete for hiding words without deleting
- Support for multiple languages and levels
- JWT-based authentication
- Compatible with FastAPI, SQLAlchemy, Alembic

---

## 🚀 Deployment

### 1. Clone the repository

```bash
git clone https://github.com/your-org/BuildMind-LernenWorte.git
cd BuildMind-LernenWorte
```
## 👤 Author

Project initiated and maintained by:
**Dmytro Movchan | [bildmind.com](https://bildmind.com)**

## 📜 License

This repository is published under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)** license.

You are free to:
- View and study the code
- Use it in **non-commercial projects**
- Share the original version **with proper attribution**

## ❗️Prohibited:

- Using the code for **commercial purposes** without **written permission** from the author
- Modifying or creating derivative works based on this code

## 💡 Special Condition

All legal rights to this code are retained by **Dmytro Movchan**.
Use of this public code in **commercial products** is only permitted under the following conditions:

- As part of **direct collaboration** with the author,
- Or through an **official agreement** with a **non-profit organization (Verein)** that has been granted a license by Dmytro Movchan.

Trigger test — 2025-05-31 22:45
