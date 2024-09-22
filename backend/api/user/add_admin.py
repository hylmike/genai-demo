import asyncio

from fastapi.encoders import jsonable_encoder

from api.user.services import create_user
from api.user.schemas import UserForm
from api.database.db import get_session


async def add_admin():
    username = input("Please input admin username: ")
    password = input("Please input admin password: ")
    email = input("Please input admin email: ")
    user_input = {
        "username": username,
        "password": password,
        "email": email,
    }

    async_session = get_session()
    try:
        user = await create_user(async_session, UserForm.model_validate(user_input))
        print(f"Following is created admin user:\n{jsonable_encoder(user)}")
        await async_session.commit()
    except Exception:
        print("Failed to create admin user")
        await async_session.rollback()
    finally:
        await async_session.close()


if __name__ == "__main__":
    asyncio.run(add_admin())
