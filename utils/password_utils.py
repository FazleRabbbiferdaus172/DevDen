import bcrypt


def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(user, password: str) -> bool:
    return bcrypt.checkpw(password, user.pwd.encode('utf-8'))