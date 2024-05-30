from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str | None = 'anyname'
    email: EmailStr  = 'example@email.com'
    password: str

class LogUser(BaseModel):
    email: str
    password: str
    
    
class Token(BaseModel):
    access_token: str | None