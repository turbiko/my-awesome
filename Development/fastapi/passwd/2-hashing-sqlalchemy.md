
---

# 🔐 Password Management in FastAPI + SQLAlchemy

### ✅ Technologies used:

* FastAPI
* SQLAlchemy (declarative style)
* Pydantic
* Passlib (`argon2` or `bcrypt`)

---

## 📦 Step 1: Install required packages

```bash
pip install fastapi sqlalchemy passlib[argon2] argon2-cffi uvicorn psycopg2-binary
```

> Use `passlib[bcrypt]` instead of `argon2` if you prefer bcrypt.

---

## 🧱 Step 2: Project Structure (minimal)

```
.
├── main.py
├── models.py
├── database.py
├── hashing.py
├── schemas.py
```

---

## 🛠️ Step 3: `hashing.py` — Password hashing utility

```python
# hashing.py

from passlib.context import CryptContext

# Password hashing context with argon2 (recommended) or bcrypt
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    default="argon2",
    deprecated="auto"
)

def hash_password(password: str) -> str:
    """Hash plain password using selected algorithm"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed one"""
    return pwd_context.verify(plain_password, hashed_password)
```

---

## 🧩 Step 4: `database.py` — SQLAlchemy engine & session

```python
# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:password@localhost/mydb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

---

## 🧾 Step 5: `models.py` — User model

```python
# models.py

from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
```

---

## 📦 Step 6: `schemas.py` — Pydantic models

```python
# schemas.py

from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
```

---

## 🚀 Step 7: `main.py` — FastAPI app with register/login

```python
# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine
from hashing import hash_password, verify_password

app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 🔐 Register endpoint

```python
@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = models.User(
        username=user.username,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
```

### 🔐 Login endpoint

```python
@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")

    return {"message": "Login successful"}
```

---

## ✅ Security Summary

| Feature              | Status               |
| -------------------- | -------------------- |
| Password hashing     | ✅ Argon2 / bcrypt    |
| Password comparison  | ✅ `passlib.verify()` |
| No plain-text stored | ✅                    |
| SQLAlchemy ORM       | ✅                    |
| Ready for JWT?       | 🔜 (Easy to extend)  |

---

## 🧪 To test:

1. Start server:

   ```bash
   uvicorn main:app --reload
   ```

2. Open Swagger docs at:
   [http://localhost:8000/docs](http://localhost:8000/docs)

---

Would you like an extended version with **JWT tokens** for login/session or **Docker** setup?
