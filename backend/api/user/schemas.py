"""DTO for user management"""

from pydantic import BaseModel, ConfigDict, EmailStr


class UserForm(BaseModel):
    """Schema for create new user"""

    username: str
    password: str
    email: EmailStr


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    password: str
    email: EmailStr
