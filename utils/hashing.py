from passlib.context import CryptContext

class Hashing:
    pwd_ctx=CryptContext(schemes=["bcrypt"],deprecated="auto")

    def hash(self,inputString):
        hashedInput=self.pwd_ctx.hash(inputString)
        return hashedInput

    def verify(self,plain_str,hashed_str):
        return self.pwd_ctx.verify(plain_str,hashed_str)