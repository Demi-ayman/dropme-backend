from fastapi import FastAPI, Request
from app.common.exceptions import BusinessRuleException
from app.common.responses import error_response
from fastapi.responses import JSONResponse
from app.users.router import router as user_router
from app.core.database import Base, engine
from app.recycling.router import router as recycling_router
# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DropMe Backend")

@app.exception_handler(BusinessRuleException)
async def business_rule_exception_handler(
    request: Request,
    exc: BusinessRuleException
):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.message)
    )
# Include routers
app.include_router(user_router)
app.include_router(recycling_router)