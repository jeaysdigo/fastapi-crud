from app.models.user import UserCreate
from app.core.security import SecurityManager
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi import HTTPException
from app.core.constants import UserConstants

class UserService:
    def __init__(self, db: AsyncIOMotorClient):
        self.collection = db["users"]

    async def create_user(self, user_data: UserCreate):
        hashed_password = SecurityManager.hash_password(user_data.password)
        user_dict = {
            "username": user_data.username,
            "password": hashed_password,
            "email": user_data.email,
            "role": user_data.role,
        }
        
        try:
            result = await self.collection.insert_one(user_dict)
            user_dict['id'] = str(result.inserted_id)
            return user_dict
        except Exception as e:
            raise HTTPException(status_code=500, detail=UserConstants.ERROR_CREATING_USER) from e

    async def get_user_by_email(self, email: str):
        user = await self.collection.find_one({"email": email})
        if not user:
            raise self._user_not_found_error()
        return user

    async def get_user_by_id(self, user_id: str):
        try:
            user = await self.collection.find_one({"_id": ObjectId(user_id)})
            if user:
                user['id'] = str(user['_id'])
                del user['_id']
                return user
            else:
                raise self._user_not_found_error()
        except Exception:
            raise HTTPException(status_code=400, detail=UserConstants.INVALID_USER_ID_ERROR)

    async def update_user(self, user_id: str, user_data: dict):
        try:
            update_result = await self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": user_data})
            if update_result.modified_count == 0:
                raise self._user_not_found_error()
            return {"msg": UserConstants.SUCCESS_UPDATING_USER}
        except Exception as e:
            raise HTTPException(status_code=500, detail=UserConstants.ERROR_UPDATING_USER) from e

    async def delete_user(self, user_id: str):
        try:
            result = await self.collection.delete_one({"_id": ObjectId(user_id)})
            if result.deleted_count == 0:
                raise self._user_not_found_error()
            return {"msg": UserConstants.SUCCESS_DELETING_USER}
        except Exception as e:
            raise HTTPException(status_code=500, detail=UserConstants.ERROR_DELETING_USER) from e

    def _user_not_found_error(self):
        return HTTPException(status_code=404, detail=UserConstants.USER_NOT_FOUND_ERROR)
