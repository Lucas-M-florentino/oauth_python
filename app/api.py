from fastapi import FastAPI, Body, Depends, Header
from fastapi.responses import JSONResponse

from app.model import PostSchema, UserLoginSchema, UserSchema
from app.auth.auth_handler import sign_jwt
from app.auth.auth_bearer import JWTBearer

app = FastAPI()


posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    }
]

users = []

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return JSONResponse(status_code=307, headers={"Location": "/docs"},content={"message":"Simple Blog page!"})

@app.get("/posts", tags=["posts"])
async def get_posts() -> dict:
    return {"data": posts}

@app.get("/posts/{id}", tags=["posts"])
async def get_single_post(id: int) -> dict:
    if id > len(posts):
        return {
            "error": "No such post with the suplied ID."
        }
    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }

@app.post("/posts",dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(post: PostSchema) -> dict:
    post.id = len(posts) + 1
    posts.append(post.model_dump())
    return {
        "data": "post added."
    }
    
@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user)
    return sign_jwt(user.email)

@app.post("/user/login",tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return sign_jwt(user.email)
    return {
        "error": "wrong login details!"
    }