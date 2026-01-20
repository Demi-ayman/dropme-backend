# DropMe Backend - Core Recycling Flow

## 1. Architecture Overview

- **Framework:** FastAPI
- **Database:** SQLite (SQLAlchemy ORM)
- **Modules:**
  - `users`: User registration & retrieval
  - `recycling`: Recycling transactions & points calculation
- **Key Features:**
  - User registration
  - Create recycling transaction
  - Automatic points calculation per material
  - Transaction persistence
  - Input validation & error handling
- **Design Principles:**
  - API-based architecture
  - Clear separation of concerns (routers, services, models, schemas)
  - Environment-based configuration

---

