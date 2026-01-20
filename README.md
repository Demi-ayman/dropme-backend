# 🚀 DropMe Recycling Backend

A FastAPI backend service for recycling machines that enables users to **Scan → Recycle → Earn Points**.

## 📋 Quick Start

### **Prerequisites**
- Python 3.11+
- pip package manager

### **Installation**
```bash
# Clone repository
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

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **Access API Documentation**
**👉 Open browser:** [http://localhost:8000/docs](http://localhost:8000/docs)

## 📁 Project Structure
```
dropme-backend/
├── app/
│   ├── common/           # Shared utilities
│   │   ├── exceptions.py # BusinessRuleException
│   │   └── responses.py  # success_response, error_response
│   ├── core/             # Core configuration
│   │   ├── config.py     # Settings class
│   │   └── database.py   # SQLAlchemy setup
│   ├── recycling/        # Recycling module
│   │   ├── models.py     # Recycling model
│   │   ├── schemas.py    # Pydantic schemas
│   │   ├── services.py   # Business logic
│   │   └── router.py     # API endpoints
│   └── users/            # User module
│       ├── models.py     # User model
│       ├── schemas.py    # Pydantic schemas
│       └── router.py     # API endpoints
├── main.py              # FastAPI app entry point
├── dropme.db           # SQLite database (auto-created)
├── .env                # Environment variables
└── requirements.txt    # Python dependencies
```

## 🌐 API Endpoints

### **Base URL:** `http://localhost:8000`

### **User Endpoints**
| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| POST | `/users/register` | Register new user | 201, 400, 409 |
| GET | `/users/{user_id}` | Get user details | 200, 404 |

### **Recycling Endpoints**
| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| POST | `/recycling/` | Create recycling transaction | 201, 400, 404 |
| GET | `/recycling/user/{user_id}` | Get user's recycling history | 200, 404 |
| GET | `/recycling/{recycling_id}` | Get specific transaction | 200, 404 |
| DELETE | `/recycling/{recycling_id}` | ⛔ Blocked (audit integrity) | 400 |

## 📤 Sample API Requests

### **Register User**
```bash
curl -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

**Response (201 Created):**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "points": 0
  }
}
```

### **Create Recycling Transaction**
```bash
curl -X POST "http://localhost:8000/recycling/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "material_type": "plastic",
    "weight_kg": 2.5
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user_id": 1,
  "material_type": "plastic",
  "weight_kg": 2.5,
  "points_earned": 25,
  "created_at": "2024-01-20T10:30:00Z"
}
```

### **Get User Details**
```bash
curl "http://localhost:8000/users/1"
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Success",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "points": 25
  }
}
```

## 🎯 Implemented Features

### ✅ **Task 1: Core Recycling Flow**
- User registration with email identification
- Recycling transaction creation with points calculation
- Points automatically added to user balance
- SQLite database persistence
- Complete "Scan → Recycle → Earn Points" workflow

### ✅ **Task 2: API Design & Validation**
- Input validation using Pydantic schemas
- Consistent response format (`success_response`, `error_response`)
- Custom `BusinessRuleException` for business logic errors
- Meaningful HTTP status codes (201, 400, 404, 409, 500)

## 🛡 Business Rules & Validation

### **1. Input Validation**
- Email validation using Pydantic's `EmailStr`
- Material type restricted to: `plastic`, `glass`, `metal`, `paper`
- Weight must be greater than 0
- User must exist before creating recycling transaction

### **2. Business Rule Enforcement**

**🚫 Daily Limit:** Maximum 10 recycling transactions per user per day
```json
{
  "status": "error",
  "message": "Daily recycling limit exceeded"
}
```

**🚫 Duplicate Prevention:** Same user + same material + same weight within 5 minutes
```json
{
  "status": "error",
  "message": "Duplicate recycling detected"
}
```

**🚫 No Deletion Policy:** Transactions cannot be deleted for audit integrity
```json
{
  "status": "error",
  "message": "Deleting recycling records is not allowed"
}
```

**🚫 Invalid Material:** Only supported materials accepted
```json
{
  "status": "error",
  "message": "Unsupported material type"
}
```

**🚫 Duplicate Email:** Email must be unique
```json
{
  "status": "error",
  "message": "Email already registered"
}
```

## 📊 Points Calculation

**Points = Weight (kg) × Rate (points/kg)**

| Material | Points per kg | Example |
|----------|--------------|---------|
| Plastic  | 10 points | 2.5 kg = 25 points |
| Glass    | 8 points  | 1.0 kg = 8 points  |
| Metal    | 15 points | 0.5 kg = 8 points  |
| Paper    | 5 points  | 3.0 kg = 15 points |

## 🔧 Technical Details

### **Database Schema**
**Users Table:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    points INTEGER DEFAULT 0
);
```

**Recycling Table:**
```sql
CREATE TABLE recycling (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    material_type TEXT NOT NULL,
    weight_kg REAL NOT NULL,
    points_earned INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### **Environment Configuration**
Create `.env` file:
```env
DATABASE_URL=sqlite:///./dropme.db
MAX_RECYCLES_PER_DAY=10
```

### **Dependencies**
```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
```

## 📦 Postman Collection

Import the provided `DropMe Backend.postman_collection.json` file which includes:
- User registration requests
- Recycling transaction creation
- Error scenario testing
- All implemented endpoints

## 🚨 Error Handling Examples

### **400 Bad Request (Business Rule Violation)**
```json
{
  "status": "error",
  "message": "Daily recycling limit exceeded"
}
```

### **404 Not Found (User Not Found)**
```json
{
  "status": "error",
  "message": "User not found"
}
```

### **409 Conflict (Duplicate Email)**
```json
{
  "status": "error",
  "message": "Email already registered"
}
```

## 🎨 API Documentation

### **Interactive Documentation**
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### **Features:**
- Try API endpoints directly from browser
- View request/response schemas
- See example requests
- View HTTP status codes

## 🔄 Database Operations

### **Automatic Table Creation**
```python
# Tables are created automatically on startup
Base.metadata.create_all(bind=engine)
```

### **Relationships**
- One User → Many Recycling transactions
- Cascade delete: When user is deleted, all their recycling records are deleted

## ⚙️ Configuration

### **Settings Class**
```python
class Settings(BaseSettings):
    APP_NAME: str = "Drop Me Backend"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./dropme.db"
    MAX_RECYCLES_PER_DAY: int = 10
```

### **Database Connection**
```python
# SQLite with SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

## 📝 Assumptions & Design Decisions

### **Assumptions**
1. Email is sufficient for user identification (no passwords)
2. Recycling machines are trusted devices
3. Weight measurements are accurate
4. Four material types cover most recycling needs
5. Points system is linear (weight × rate)

### **Design Decisions**
1. **SQLite**: Chosen for simplicity and easy setup
2. **FastAPI**: Modern, fast, with built-in OpenAPI docs
3. **Service Layer**: Business logic separated from API routes
4. **No Delete Policy**: Transactions are permanent for audit trail
5. **Custom Exceptions**: Clear separation of business logic errors

## 🧪 Testing the Flow

### **Complete Workflow Example**
```bash
# 1. Register a user
curl -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'

# Response: User created with id=1

# 2. Create recycling transaction
curl -X POST "http://localhost:8000/recycling/" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "material_type": "metal", "weight_kg": 1.2}'

# Response: 1.2kg metal = 18 points earned

# 3. Check user points
curl "http://localhost:8000/users/1"

# Response: User now has 18 points
```

## 📄 License

Developed for DropMe technical assessment.

## 🤝 Support

For issues or questions:
1. Check API documentation at `http://localhost:8000/docs`
2. Review the business rules section above
3. Test with the provided Postman collection

---

**✅ Ready for Production!**  
Start the server and test the complete recycling flow.
