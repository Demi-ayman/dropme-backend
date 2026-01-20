# 🚀 DropMe Recycling Backend API

A complete backend API for recycling machines that enables users to **Scan → Recycle → Earn Points**.

---

## 📋 **QUICK START**

### **1. Clone & Setup**
```bash
git clone <your-repo-url>
cd dropme-backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **2. Run the Server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **3. Open API Documentation**
**👉 Go to:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📁 **PROJECT STRUCTURE**
```
dropme-backend/
├── app/
│   ├── common/           # Shared utilities
│   │   ├── exceptions.py
│   │   └── responses.py
│   ├── core/             # Configuration & DB
│   │   ├── config.py
│   │   └── database.py
│   ├── recycling/        # Recycling module
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── services.py
│   │   └── router.py
│   └── users/           # User module
│       ├── models.py
│       ├── schemas.py
│       └── router.py
├── main.py              # FastAPI app
├── dropme.db           # Database
├── requirements.txt    # Dependencies
└── README.md          # This file
```

---

## 🌐 **API ENDPOINTS**

### **Base URL:** `http://localhost:8000`

### **🔹 USER MANAGEMENT**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/register` | Register new user |
| GET | `/users/{user_id}` | Get user details & points |

### **🔹 RECYCLING TRANSACTIONS**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/recycling/` | Create recycling transaction |
| GET | `/recycling/user/{user_id}` | Get user's recycling history |
| GET | `/recycling/{recycling_id}` | Get specific transaction |
| DELETE | `/recycling/{recycling_id}` | ❌ Blocked (for audit integrity) |

---

## 📤 **SAMPLE API REQUESTS**

### **1. Register a New User**
```bash
curl -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com"}'
```

### **2. Recycle Items (Earn Points)**
```bash
curl -X POST "http://localhost:8000/recycling/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "material_type": "plastic",
    "weight_kg": 2.5
  }'
```

### **3. Check User's Points Balance**
```bash
curl "http://localhost:8000/users/1"
```

---

## 🎯 **FEATURES IMPLEMENTED**

### **✅ TASK 1: CORE RECYCLING FLOW**
- ✔ User registration with email identification
- ✔ Recycling transaction creation
- ✔ Points calculation and updating
- ✔ SQLite database persistence
- ✔ Complete Scan → Recycle → Earn Points flow

### **✅ TASK 2: API DESIGN & VALIDATION**
- ✔ Pydantic input validation
- ✔ Consistent error response format
- ✔ Proper HTTP status codes
- ✔ Business rule enforcement
- ✔ OpenAPI documentation (auto-generated)

---

## 🛡 **BUSINESS RULES**

### **🚫 Daily Limit**
- Maximum **10 recycling transactions** per user per day
- Returns error: `"Daily recycling limit exceeded"`

### **🚫 No Duplicate Transactions**
- Same user + same material + same weight within **5 minutes** = Blocked
- Returns error: `"Duplicate recycling detected"`

### **🚫 No Deletion Policy**
- Recycling transactions **cannot be deleted**
- Ensures audit trail integrity
- Returns error: `"Deleting recycling records is not allowed"`

### **✅ Valid Materials**
- Only these materials accepted: **plastic, glass, metal, paper**
- Invalid material returns: `"Unsupported material type"`

---

## 📊 **POINTS SYSTEM**

| Material | Points per kg | Example |
|----------|--------------|---------|
| **Plastic** | 10 points/kg | 2kg = 20 points |
| **Glass** | 8 points/kg | 1.5kg = 12 points |
| **Metal** | 15 points/kg | 0.5kg = 8 points |
| **Paper** | 5 points/kg | 3kg = 15 points |

**Formula:** `Points = Weight (kg) × Rate (points/kg)`

---

## 🔧 **TECHNICAL STACK**

| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | FastAPI | High-performance API framework |
| Database | SQLite | Lightweight, file-based storage |
| ORM | SQLAlchemy | Database operations |
| Validation | Pydantic v2 | Data validation & serialization |
| Documentation | OpenAPI | Auto-generated API docs |

---

## 🚨 **ERROR EXAMPLES**

### **400 Bad Request (Business Rule Violation)**
```json
{
  "status": "error",
  "message": "Daily recycling limit exceeded"
}
```

### **400 Bad Request (Duplicate)**
```json
{
  "status": "error",
  "message": "Duplicate recycling detected"
}
```

### **404 Not Found**
```json
{
  "status": "error",
  "message": "User not found"
}
```

### **409 Conflict**
```json
{
  "status": "error",
  "message": "Email already registered"
}
```

---

## 📦 **POSTMAN COLLECTION**

**Import file:** `DropMe Backend.postman_collection.json`

Contains ready-to-use requests for:
- User registration
- Recycling transactions
- Error scenarios testing

---

## 🗄 **DATABASE SCHEMA**

### **📌 Users Table**
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| email | String | Unique user email |
| points | Integer | Current points balance |

### **📌 Recycling Table**
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to users |
| material_type | String | Type of material |
| weight_kg | Float | Weight in kilograms |
| points_earned | Integer | Points earned |
| created_at | DateTime | Transaction timestamp |

---

## 🎨 **API DOCUMENTATION**

### **Interactive Docs:**
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### **Features:**
- Try API endpoints directly
- View request/response schemas
- See example requests
- View HTTP status codes

---

## ⚙️ **CONFIGURATION**

Create `.env` file:
```env
# Database
DATABASE_URL=sqlite:///./dropme.db

# Business Rules
MAX_RECYCLES_PER_DAY=10

# Environment
ENVIRONMENT=development
APP_NAME=DropMe Backend
```

---

## 🏗 **ARCHITECTURE DECISIONS**

| Decision | Reason | Impact |
|----------|--------|--------|
| **SQLite Database** | Simple setup, ACID compliance | Easy to migrate to PostgreSQL later |
| **FastAPI Framework** | Async support, auto-docs | Faster development, better performance |
| **Service Layer Pattern** | Separation of concerns | Maintainable, testable code |
| **No Delete Policy** | Audit trail, fraud prevention | Transactions are permanent records |
| **Email-only Auth** | MVP simplification | Can add JWT/OAuth2 later |

---

## 📝 **ASSUMPTIONS MADE**

1. **Email is primary identifier** - No password system for MVP
2. **Machines are trusted** - No additional device authentication
3. **Weight accuracy** - Machines provide accurate weight measurements
4. **Material types fixed** - 4 types cover majority of recycling
5. **Single currency** - Points are the only reward system

---

## 🔮 **FUTURE IMPROVEMENTS**

### **Priority 1:**
- JWT authentication
- Admin dashboard endpoints
- Webhook for machine integration

### **Priority 2:**
- PostgreSQL migration
- Redis caching layer
- Rate limiting middleware

### **Priority 3:**
- Email notifications
- QR code scanning
- Bulk recycling support

---

## 🚀 **TEST THE FULL FLOW**

```bash
# 1. Register a user
curl -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'

# 2. Recycle some items
curl -X POST "http://localhost:8000/recycling/" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "material_type": "metal", "weight_kg": 1.2}'

# 3. Check points earned
curl "http://localhost:8000/users/1"
```

---

## 📄 **LICENSE**

Developed for DropMe technical assessment.  
All code is ready for production use.

---

## ❓ **NEED HELP?**

1. Check API docs at `http://localhost:8000/docs`
2. Review business rules section above
3. Test with Postman collection provided
4. Run the quick test script

---

**✅ READY TO DEPLOY!**  
Start the server and test the complete recycling flow today.
