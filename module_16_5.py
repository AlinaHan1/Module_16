from fastapi import FastAPI, Path, status, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, List
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory='templates')

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/")
def get_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get(path='/user/{user_id}')
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse('users.html', {'request': request, 'user': users[user_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail='User not found')


@app.post('/user/{username}/{age}')
async def create_user(
        username: Annotated[str, Path(min_length=4, max_length=20, description='Enter username', example='Capybara')],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]):
    if users:
        user_id = max(users, key=lambda u: u.id).id + 1
    else:
        user_id = 1
    users.append(User(id=user_id, username=username, age=age))
    return f'User id {user_id} username {username} age {age} is registered'


@app.put('/user/{user_id}/{username}/{age}')
async def put_users(user_id: int,
                    username: Annotated[
                        str, Path(min_length=5, max_length=20, description='Enter username', example='Capybara')],
                    age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> str:
    try:
        edit_user = users[user_id]
        edit_user.username = username
        edit_user.age = age
        return f'The User {user_id} has been updated'
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[str, Path(description='Enter id for delete', example='1')]) -> str:
    users.pop(user_id)
    return f'The User {user_id} has been deleted'
