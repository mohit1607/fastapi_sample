from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.users import User, LogUser
from connection.connectdb import client
from schemas.Schemas import individual_serial, list_serial
from bson import ObjectId
from utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_hashed_password
)



router = APIRouter()

db = client['Simple_database']
usersCollection = db['users']

@router.get('/')
async def getUsers():
    userslist = list_serial(usersCollection.find())
    return userslist

@router.get('/singleUser')
async def getSingleUser(name: str ):
    user = individual_serial(usersCollection.find_one({"name": name}))
    return user

# @router.post('/')
# async def createUser(user: User):
#     user = usersCollection.insert_one(dict(user)) #remember this step you passing object as dictionary
#     # successfully creating
    
@router.put('/{id}')
async def updateUser(id:str, user:User):
    updatedUser = usersCollection.update_one({"_id": ObjectId(id)}, {"$set": dict(user)}) #remember this special method
    #successfylly updating user
    
@router.delete('/{id}')
async def deleteUser(id:str):
    deleteUser = usersCollection.delete_one({"_id": ObjectId(id)})

#successfully made a crud application with fastapi.


@router.post('/signup', summary="Create new user")
async def create_user(data: User):
    # first check if there is user in the db
    user = usersCollection.find_one({"name": data.email})
    if user is not None:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    user = {
        "name": data.name,
        'email': data.email,
        'password': get_hashed_password(data.password),
    }
    user = usersCollection.insert_one(dict(user))
    return {"message": "created user"}

@router.post('/lgoin', summary="Check user")
async def login_user(details: LogUser):
    user =  individual_serial(usersCollection.find_one({"email": details.email}))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    hashed_pass = user['password']
    if not verify_hashed_password(details.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password" # be aware here not to messup
        )
        
    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }
    