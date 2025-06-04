from pydantic import BaseModel, Field, EmailStr

class PostSchema(BaseModel):
    id = Field(default=None)
    title = Field(...)
    content = Field(...)
    
    class Config:
        json_schema_extra = {
            "example":{
                "title":"Securing FastAPI applications with JWT.",
                "content":"In this tutorial, you'll learn how to secure your application by enabling authentication using JWT. We'll be using PyJWT to sign, encode and decode JWT tokens...."
            }
        }