from pydantic import BaseModel, EmailStr, Field

from app.core.constants import RoleConstants

class UserCreate(BaseModel):
    username: str = Field(..., description="The username of the user")
    password: str = Field(..., description="The password of the user")
    email: EmailStr = Field(..., description="The email address of the user")
    role: str = Field(default=RoleConstants.USER_ROLE, description="The role of the user")

class UserResponse(BaseModel):
    id: str = Field(..., description="The unique identifier of the user")
    username: str = Field(..., description="The username of the user")
    email: EmailStr = Field(..., description="The email address of the user")
    role: str = Field(..., description="The role of the user")

class UserUpdate(BaseModel):
    username: str = Field(None, description="The new username of the user")
    email: EmailStr = Field(None, description="The new email address of the user")
    role: str = Field(None, description="The new role of the user")

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="The email address of the user")
    password: str = Field(..., description="The password of the user")
