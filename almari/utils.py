from passlib.context import CryptContext

#bcrypt is the algorithm used to hash the password
pwd_context = CryptContext(schemes= ["bcrypt"], deprecated = "auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

