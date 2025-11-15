**step-by-step guide**  how to **securely hash passwords in FastAPI**, using both `bcrypt` and `argon2` as alternatives.

---

## 🔐 How to Hash Passwords in FastAPI (with `bcrypt` and `argon2`)

---

### ✅ Step 1: Install the required libraries

#### 🔹 If you want to use **bcrypt**:

```bash
pip install passlib[bcrypt]
```

#### 🔹 If you want to use **argon2**:

```bash
pip install passlib[argon2] argon2-cffi
```

---

### ✅ Step 2: Create a hashing utility module

```python
# hashing.py

from passlib.context import CryptContext

# Choose your desired algorithm: bcrypt or argon2
# bcrypt — stable, fast, widely supported
# argon2 — more secure, modern, recommended by OWASP

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],  # Priority order
    default="argon2",              # You can change to "bcrypt" if needed
    deprecated="auto"
)

def hash_password(password: str) -> str:
    """Hash plain text password using the configured algorithm"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare a plain password with a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)
```

> 🛠 Tip: You can switch between `argon2` and `bcrypt` by changing the `default` value in the context.

---

### ✅ Step 3: Hash the password when registering a user

```python
# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from hashing import hash_password

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    password: str

@app.post("/register")
def register_user(user: UserCreate):
    hashed_pwd = hash_password(user.password)
    
    # Normally you would store the user in the database here
    return {
        "username": user.username,
        "hashed_password": hashed_pwd
    }
```

---

### ✅ Step 4: Verify password on login

```python
from fastapi import HTTPException
from hashing import verify_password

@app.post("/login")
def login(user: UserCreate):
    # Simulated stored user with hashed password
    stored_user = {
        "username": "admin",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$..."  # Example hash
    }

    if not verify_password(user.password, stored_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid password")

    return {"message": "Login successful"}
```

---

## 🔍 Which algorithm should you use?

| Algorithm  | Security      | Performance | OWASP Recommended | Passlib Support |
| ---------- | ------------- | ----------- | ----------------- | --------------- |
| **bcrypt** | ✅ High        | ⚡ Fast      | ✅ Yes             | ✅ Yes           |
| **argon2** | ✅🔒 Very High | 🐢 Slower   | ✅ Yes             | ✅ Yes           |

> ✅ Use **`bcrypt`** if you need something simple and secure.
> 🔐 Use **`argon2`** if you want the strongest protection and don't mind a bit more setup.

---

## 📚 Resources

* 🔗 [bcrypt (Wikipedia)](https://en.wikipedia.org/wiki/Bcrypt)
* 🔗 [argon2 (OWASP Cheat Sheet)](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#argon2id)
* 🔗 [Passlib documentation](https://passlib.readthedocs.io/en/stable/)

---

