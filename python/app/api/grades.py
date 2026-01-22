#trigger grading
from fastapi import APIRouter

router = APIRouter()

@router.get("")
def get_all_stock():
    return {"stocks":[]}

#might not be useful
