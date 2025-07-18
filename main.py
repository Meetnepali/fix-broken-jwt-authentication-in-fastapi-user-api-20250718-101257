import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Load secret and algorithm from config (simulating an error in the config/change)
JWT_SECRET = os.environ.get("JWT_SECRET", "BROKEN_SECRET")  # Should match token generator
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")

class User(BaseModel):
    username: str
    role: str

# Dummy user database
users_db = {
    "alice": {"username": "alice", "role": "admin"},
    "bob": {"username": "bob", "role": "user"},
}

def decode_jwt(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_jwt(token)
    if not payload or "username" not in payload or "role" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = users_db.get(payload["username"])
    if not user or user["role"] != payload["role"]:
        raise HTTPException(status_code=401, detail="Invalid user or role")
    return User(**user)

def require_role(role: str):
    def role_dependency(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_dependency

@app.post("/token")
def issue_token(form_data: dict):
    username = form_data.get("username")
    role = form_data.get("role")
    if username not in users_db or users_db[username]["role"] != role:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    payload = {"username": username, "role": role}
    # Token might be issued with a different secret/algorithm in real world
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/public")
def public():
    return {"msg": "public endpoint"}

@app.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return {"msg": f"Hello {user.username}, role: {user.role}"}

@app.get("/admin")
def admin_endpoint(user: User = Depends(require_role("admin"))):
    return {"msg": f"Hello admin {user.username}"}

