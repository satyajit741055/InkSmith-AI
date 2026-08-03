from pydantic import BaseModel, Field ,EmailStr, ConfigDict



class UserBase(BaseModel):
    username : str = Field(...,min_length=1,max_length=50)
    email : EmailStr


class UserCreate(UserBase):
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class UserResponse(UserBase):
    id : int
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token : str
    token_type : str
    
    model_config = ConfigDict(from_attributes=True)

class UserPrompt(BaseModel):
    prompt : str
    
    model_config = ConfigDict(from_attributes=True)


class BlogGenerationId(BaseModel):
    thread_id : str
    
    model_config = ConfigDict(from_attributes=True)

class BlogGenerationResponse(BaseModel):
    thread_id : str
    status : str
    pdf_url : str | None = None
    error_message : str | None = None
    
    model_config = ConfigDict(from_attributes=True)

