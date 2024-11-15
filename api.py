from fastapi import FastAPI, HTTPException
from fastapi import Form
from pydantic import BaseModel
import uvicorn
from requests import post
from database import *
from models import *
from responce_models import *


app = FastAPI(
    title="kawarag1",
    description="Что творит этот белый?",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"

)


with DBSettings.get_session() as conn:
    users = conn.query(User).all()
    users_dict = [
        {
            'id': user.id,
            'name': user.name,
            'role':user.role_id
        }
        for user in users
    ]

with DBSettings.get_session() as conn:
    roles = conn.query(Role).all()
    roles_dict = [
        {
            'id': role.id,
            'name': role.name
        }
        for role in roles
    ]



@app.get("/")
async def root():
    return{"greeting: hello world!"}


@app.get("/users/select/{user_id}")
async def get_users(user_id:int):
    try:
        with DBSettings.get_session() as conn:
            user = conn.query(User).filter(User.id == user_id).first()
            return user
    except:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/users/add/{user_name}/{user_role}", response_model= UserCreate)
async def add_users(user_name:str, user_role:str):
    user = UserCreate(name=user_name, role = user_role)
    with DBSettings.get_session() as conn:
        roleDB = conn.query(Role).filter(Role.name == user.role).first()
        if (roleDB == None):
            raise HTTPException(status_code=404, detail="We haven't this role")
        else:
            new_user = User(name = user.name, role_id = roleDB.id)
            conn.add(new_user)
            conn.commit()
            print("Успешно")    
            return(user)
            



@app.delete("/users/delete/{user_id}", response_model=UserCreate)            
async def delete_users(user_id:int):
    with DBSettings.get_session() as conn:
        user = conn.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="We haven't this user")
        conn.delete(user)
        conn.commit()
        return(user)


@app.put("/users/update/{user_id}/{new_user_name}/{new_user_role}", response_model=UserCreate)
async def update_users(user_id:int, new_user_name:str, new_user_role:str):
    userUpdate = UserCreate(name=new_user_name, role=new_user_role)
    with DBSettings.get_session() as conn:
        user = conn.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="We haven't this user")
        roleDB = conn.query(Role).filter(userUpdate.role == Role.name).first()
        if roleDB is None:
            raise HTTPException(status_code=404, detail="We haven't this role")
        user.name = userUpdate.name
        user.role_id = roleDB.id
        conn.commit()
        conn.refresh(user)
        return (userUpdate)



uvicorn.run(app, host="127.0.0.1", port=8000)    
        



