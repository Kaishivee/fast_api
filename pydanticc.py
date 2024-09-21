from fastapi import FastAPI, Path
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/users")
async def get_users():
    return users


@app.post("/user/{username}/{age}")
async def add_user(username: Annotated[str, Path(min_length=5, max_length=20)],
                   age: Annotated[int, Path(ge=18, le=120)]):
    current_index = max((user.id for user in users), default=0) + 1
    new_user = User(id=current_index, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(ge=1)],
                      username: Annotated[str, Path(min_length=5, max_length=20)],
                      age: Annotated[int, Path(ge=18, le=120)]):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path(ge=1)]):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")