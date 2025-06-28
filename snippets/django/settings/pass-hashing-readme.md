Ось переписаний файл як покрокову інструкцію англійською мовою для junior Django developer, з короткими, практичними коментарями:

---

# 🔐 Django Password Hashing – Developer Guide

This guide explains how to configure password hashing in a Django project using modern secure algorithms.

---

## ✅ Step 1: Understand Password Hashing in Django

Django automatically hashes user passwords before saving them to the database.

🔍 Default method: `PBKDF2` with SHA256.

### Example:

```python
user.set_password('my_secure_password')
# Result will look like: pbkdf2_sha256$260000$<salt>$<hash>
```

---

## ✅ Step 2: Install Stronger Hashing Algorithms

Django supports several hashing algorithms. Some of them require extra packages.

### Recommended algorithms:

| Algorithm    | Strength     | Package       | Install Command           |
| ------------ | ------------ | ------------- | ------------------------- |
| Argon2       | ⭐ Best       | `argon2-cffi` | `pip install argon2-cffi` |
| PBKDF2       | OK (default) | built-in      | *(already available)*     |
| BCryptSHA256 | Good         | `bcrypt`      | `pip install bcrypt`      |

Avoid: `SHA1`, `MD5`, `Crypt` – these are unsafe.

---

## ✅ Step 3: Add to `settings.py`

Update your `PASSWORD_HASHERS` to include strong options.

### Example:

```python
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]
```

> 🔁 Django uses the **first** hasher in the list for new passwords. Others are for compatibility.

---

## ✅ Step 4: Create User – Password is Automatically Hashed

```python
from django.contrib.auth.models import User

user = User.objects.create_user(username='andrii', password='super_secret')
```

> The password is hashed before saving – you don’t need to hash it manually.

---

## ✅ Step 5: Verify Password During Login

Use this in login logic or authentication views:

```python
user.check_password('super_secret')  # returns True or False
```

---

## ✅ Step 6: Optional – Test Hashing Manually

```python
from django.contrib.auth.hashers import make_password

print(make_password('demo123'))
# Output example: argon2$argon2id$v=19$m=512,t=2,p=2$...
```

---

## ✅ Bonus: Use Custom User Model (Optional)

If you want to extend the default User model:

### 1. `models.py`

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    display_name = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
```

### 2. `settings.py`

```python
AUTH_USER_MODEL = 'yourapp.CustomUser'
```

### 3. Migrate database

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## ✅ Wagtail Compatibility

Wagtail uses Django’s default `User` model unless you override it.

* Password hashing works the same way as in Django.
* Admin users in `/admin/` are authenticated using Django logic.
* `PASSWORD_HASHERS` applies to all users, including Wagtail editors.

---

## ✅ Summary

| Task                     | Action                                      |
| ------------------------ | ------------------------------------------- |
| Use Argon2 (recommended) | Install `argon2-cffi`, update settings      |
| Support older passwords  | Include PBKDF2 + SHA1 in `PASSWORD_HASHERS` |
| Create custom user       | Inherit from `AbstractUser`                 |
| Use in Wagtail           | Wagtail uses Django auth automatically      |

---

