from fastapi import FastAPI, Path, status, Body, HTTPException
from typing import Annotated, List
from pydantic import BaseModel

app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/users')
async def get_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def create_user(
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]):
    user_id = len(users) + 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return f'User id {user_id} username {username} age {age} is registered'


@app.put('/user/{user_id}/{username}/{age}')
async def put_users(user_id: int,
                    username: Annotated[
                        str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
                    age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]):
    for i in users:
        if i.id == user_id:
            i.username = username
            i.age = age
            return users
    raise HTTPException(status_code=404, detail="User not found")


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter id for delete', example='1')]):
    try:
        for i, user in enumerate(users):
            if user.id == user_id:
                return users.pop(i)
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")
