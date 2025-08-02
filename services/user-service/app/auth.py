from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email : str
    password : str
    
@router.post("/login")
def login(data: LoginRequest):
    if data.email == "admin@documind.local" and data.password == "admin":
        return {"access_token": "mock-jwt-token"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

