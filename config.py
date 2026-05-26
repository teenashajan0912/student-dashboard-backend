DATABASE_URL = "sqlite:///./students.db"
SECRET_KEY = "secret"
ALGORITHM = "HS256"
PASSWORD_HASH_SCHEME = "sha256_crypt"
PASSWORD_HASH_DEPRECATED = "auto"
DEFAULT_ADMIN = {
    "username": "admin",
    "email": "admin@test.com",
    "password": "password123",
    "role": "admin"
}
ALLOW_ORIGINS = ["http://localhost:3000","http://localhost:5173"]