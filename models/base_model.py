from pydantic import BaseModel
from typing import Optional

# Payload for POST /api/users
class UserCreateRequest(BaseModel):
    name: str
    job: str

# Response for POST /api/users
class UserCreateResponse(BaseModel):
    name: str
    job: str
    id: str
    createdAt: str

# The individual user profile object    
class UserProfile(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str

# The outer container returned by GET /api/users/{id}
class SingleUserResponse(BaseModel):
    data:UserProfile

# What we need in login
class UserLoginRequest(BaseModel):
    email: str
    password: str

# what we send to login
class UserLoginResponse(BaseModel):
    token: str

# when the server response on client error (HTTP 400)
class ErrorResponse(BaseModel):
    error: str

#Existing Model remain above...
class UserUpdateResponse(BaseModel):
    name:str
    job: str
    updatedAt: Optional[str] = None

    