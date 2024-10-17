from fastapi import APIRouter, HTTPException
from app.models.user import UserCreate, UserResponse, UserUpdate, LoginRequest
from app.services.user_service import UserService
from app.core.security import JWTManager, SecurityManager
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import Config
from app.core.constants import UserConstants

router = APIRouter()
client = AsyncIOMotorClient(Config.MONGO_URI)
db = client.user_management
user_service = UserService(db)

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    """
    Register a new user.

    - **user**: UserCreate model containing the user's details (username, password, email, role).

    Returns the created user details.
    """
    existing_user = await user_service.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail=UserConstants.ERROR_CREATING_USER)
    new_user = await user_service.create_user(user)
    return UserResponse(**new_user)

@router.post("/login")
async def login(login_request: LoginRequest):
    """
    Log in a user and return an access token.

    - **login_request**: LoginRequest model containing the user's email and password.

    Returns an access token and token type if successful.
    """
    user = await user_service.get_user_by_email(login_request.email)
    if not user or not SecurityManager.verify_password(login_request.password, user['password']):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = JWTManager.create_access_token({"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_profile(user_id: str):
    """
    Retrieve a user's profile by their user ID.

    - **user_id**: The ID of the user to retrieve.

    Returns the user details if found.
    """
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=UserConstants.USER_NOT_FOUND_ERROR)
    return UserResponse(**user)

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user_profile(user_id: str, user_data: UserUpdate):
    """
    Update a user's profile by their user ID.

    - **user_id**: The ID of the user to update.
    - **user_data**: UserUpdate model containing the updated user details.

    Returns the updated user details.
    """
    updated_user = await user_service.update_user(user_id, user_data.dict(exclude_unset=True))
    
    if updated_user.matched_count == 0:
        raise HTTPException(status_code=404, detail=UserConstants.ERROR_UPDATING_USER)

    user = await user_service.get_user_by_id(user_id)
    return UserResponse(**user)

@router.delete("/users/{user_id}")
async def delete_user_profile(user_id: str):
    """
    Delete a user's profile by their user ID.

    - **user_id**: The ID of the user to delete.

    Returns a success message if the user was deleted.
    """
    result = await user_service.delete_user(user_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=UserConstants.ERROR_DELETING_USER)
    return {"msg": UserConstants.SUCCESS_DELETING_USER}
