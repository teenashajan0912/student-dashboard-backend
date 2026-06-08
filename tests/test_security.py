from security import hash_password, verify_password

def test_hash_password():
    password = "admin123"
    hashed = hash_password(password)

    assert hashed != password

def test_verify_password():
    password = "admin123"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True

def test_verify_password_invalid():
    password = "admin123"
    hashed = hash_password(password)

    assert verify_password("wrongpass", hashed) is False