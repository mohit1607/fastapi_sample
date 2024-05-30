from fastapi import APIRouter, status, HTTPException, Depends, Header
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from models.users import User, LogUser
from connection.connectdb import client
from schemas.Schemas import individual_serial, list_serial
from bson import ObjectId
from utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_hashed_password,
    verify_token
)
from models.users import Token


# Dependency function
def check_login(data: Annotated[str, Header()]):
    try:
        # Check if the token is provided
        if not data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Authentication token is missing"
            )

        # Validate the access token
        email = verify_token(data)
        if email == "No email":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )

        # Check if the user exists in the database
        found = individual_serial(usersCollection.find_one({"email": email}))
        if not found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return {'email': email, "status_authenticated": True}

    except HTTPException as e:
        # Re-raise HTTP exceptions to be handled by FastAPI
        raise e
    except Exception as e:
        # Catch any other exceptions and return a generic error message
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        ) from e


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


@router.post('/login', summary="Check user")
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
    
@router.post('/items')
async def list_items(authenticated_user: Annotated[str, Depends(check_login)] ): #this is called dependency injection
    # here this funciton depends on the function check_login which will check if the token is valid or not 
    # and then validate the user to perform certian operations.
    if not authenticated_user['status_authenticated']: 
           raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Not Authorized"
        )
    information = list_serial(usersCollection.find())
    # here now it is accessible to the users who are subscribed
       
    return {"data": authenticated_user, "items": information}
    