from pydantic import BaseModel

class ItemBase(BaseModel):
    product_name: str
    description: str|None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id:int
    
    class Config:
        orm_mode = True
        

class UserBase(BaseModel):
    email:str
    
class UserCreate(UserBase):
    password: str
    
class User(UserBase):
    id:int
    items: list[Item] = []
    
    class Config: 
        orm_mode = True