🚀 DropMe Recycling Backend
A complete backend API for recycling machines that enables users to Scan → Recycle → Earn Points.

📋 Quick Start
1. Clone & Setup
bash
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
2. Run the Server
bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
3. Test API
Open browser: http://localhost:8000/docs

📁 Project Structure
text
dropme-backend/
├── app/
│   ├── common/           # Shared utilities
│   ├── core/             # Configuration & DB
│   ├── recycling/        # Recycling transactions
│   └── users/            # User management
├── main.py              # FastAPI app entry
├── dropme.db            # SQLite database
├── requirements.txt     # Python dependencies
└── README.md           # This file
🌐 API Endpoints
Base URL: http://localhost:8000
1. User Management
POST /users/register - Register new user

GET /users/{user_id} - Get user details & points

2. Recycling Transactions
POST /recycling/ - Create recycling transaction

GET /recycling/user/{user_id} - Get user's recycling history

GET /recycling/{recycling_id} - Get specific transaction

DELETE /recycling/{recycling_id} - Blocked for audit integrity

📤 Sample API Requests
1. Register User
bash
curl -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
2. Recycle Items
bash
curl -X POST "http://localhost:8000/recycling/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "material_type": "plastic",
    "weight_kg": 2.5
  }'
3. Check User Points
bash
curl "http://localhost:8000/users/1"
🎯 Features Implemented
✅ Task 1: Core Recycling Flow
User registration with email identification

Recycling transaction creation

Points calculation: Plastic(10/kg), Glass(8/kg), Metal(15/kg), Paper(5/kg)

Real-time points updating

SQLite database persistence

✅ Task 2: API Design & Validation
Pydantic validation for all inputs

Consistent error response format

Business rule enforcement:

Daily recycling limit (10 transactions/day)

Duplicate transaction prevention (5-minute window)

Transaction immutability (no deletions allowed)

Proper HTTP status codes (201, 400, 404, 409, 500)

🛡 Business Rules
Daily Limit: Max 10 recycling transactions per user per day

No Duplicates: Same user + same material + same weight within 5 minutes = blocked

No Deletion: Transactions are permanent for audit trail

Valid Materials: Only "plastic", "glass", "metal", "paper" accepted

📊 Points System
Material	Points per kg
Plastic	10 points
Glass	8 points
Metal	15 points
Paper	5 points
Example: 2kg plastic = 20 points

🔧 Technical Details
Framework: FastAPI (Python)

Database: SQLite with SQLAlchemy ORM

Validation: Pydantic v2

Architecture: Clean separation (Models, Schemas, Services, Routers)

Documentation: Auto-generated OpenAPI at /docs

🚨 Error Examples
Daily Limit Exceeded
json
{
  "status": "error",
  "message": "Daily recycling limit exceeded"
}
Duplicate Transaction
json
{
  "status": "error",
  "message": "Duplicate recycling detected"
}
Invalid Material
json
{
  "status": "error",
  "message": "Unsupported material type"
}
📦 Postman Collection
Import DropMe Backend.postman_collection.json for ready-to-use API requests.

🔄 Database
File: dropme.db (auto-created on first run)

Tables:

users (id, email, points)

recycling (id, user_id, material_type, weight_kg, points_earned, created_at)

Relations: One user → Many recycling transactions

🎨 API Documentation
Interactive documentation available at:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

⚙️ Configuration
Environment variables (in .env):

env
DATABASE_URL=sqlite:///./dropme.db
MAX_RECYCLES_PER_DAY=10
ENVIRONMENT=development
🏗 Architecture Decisions
SQLite over NoSQL: Chosen for ACID compliance and transaction integrity

FastAPI: Modern, fast, with built-in OpenAPI docs

Service Layer: Business logic separated from API routes

No Delete Policy: Transactions are permanent to prevent fraud

Email-only Auth: Simplified for MVP (can add JWT later)

📝 Assumptions Made
Email is unique identifier for users

No authentication required for MVP

Machines are trusted devices

Weight measurements are accurate

Four material types cover most recycling needs

🔮 Future Improvements
Add JWT authentication

Implement webhooks for machine integration

Add admin dashboard endpoints

Migrate to PostgreSQL for production

Add Redis caching for frequent queries

🚀 Quick Test Script
bash
# Test the full flow
./test_flow.sh
📄 License
Developed for DropMe technical assessment.
