from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api import stocks, grades
from app.core.auth import require_auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stocks.router, prefix="/stocks", dependencies=[Depends(require_auth)])
app.include_router(grades.router, prefix="/grades", dependencies=[Depends(require_auth)])


