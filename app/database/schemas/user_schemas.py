from pydantic import BaseModel, EmailStr, ConfigDict

class Users(BaseModel):
    id: int = 1
    username: str = "johndoe"
    name: str = "John Doe"
    email: EmailStr = "john@example.com"
    model_config = ConfigDict(from_attributes=True)

class UserInDB(Users):
    hashed_password: str = "hashed_password"

class CreateUser(BaseModel):
    username: str = "johndoe"
    name: str = "John Doe"
    email: EmailStr = "john@example.com"
    hashed_password: str = "hashed_password"
    model_config = ConfigDict(from_attributes=True)

class UpdateUser(BaseModel):
    name: str = "John Doe"
    email: EmailStr = "john@example.com"
    hashed_password: str = "hashed_password"
    model_config = ConfigDict(from_attributes=True)