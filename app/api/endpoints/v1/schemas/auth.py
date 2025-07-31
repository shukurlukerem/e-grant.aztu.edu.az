
from pydantic import BaseModel

class AuthBase(BaseModel):
    fin_kod: str
    email: str
    user_type: int
    project_role: int

class SignUp(AuthBase):
    password: str
    pass

class SignIn(BaseModel):
    fin_kod: str
    password: str