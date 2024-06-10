# from fastapi import APIRouter, status, HTTPException, Depends, Header, File, UploadFile
# from typing import Annotated
# from fastapi.security import OAuth2PasswordRequestForm
# from models.users import User, LogUser
# from connection.connectdb import client
# from schemas.Schemas import individual_serial, list_serial
# from bson import ObjectId
# from utils import (
#     get_hashed_password,
#     create_access_token,
#     create_refresh_token,
#     verify_hashed_password,
#     verify_token
# )
# from models.users import Token
# import shutil
# from fastapi.staticfiles import StaticFiles
# import json
# import yaml
# import time
# from fastapi.responses import FileResponse, Response, StreamingResponse
# import os
# import uuid
# from random import randint


# local_db = []

# # Remember Annotated is used to provide the metadat to the query param if it goes wrong

# # Dependency function
# def check_login(data: str = Header()):
#     try:
#         # Check if the token is provided
#         if not data:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Authentication token is missing"
#             )

#         # Validate the access token
#         email = verify_token(data)
#         if email == "No email":
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid authentication token"
#             )

#         # Check if the user exists in the database
#         found = individual_serial(usersCollection.find_one({"email": email}))
#         if not found:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="User not found"
#             )

#         return {'email': email, "status_authenticated": True}

#     except HTTPException as e:
#         # Re-raise HTTP exceptions to be handled by FastAPI
#         raise e
#     except Exception as e:
#         # Catch any other exceptions and return a generic error message
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="An unexpected error occurred"
#         ) from e


# router = APIRouter()

# db = client['Simple_database']
# usersCollection = db['users']



# @router.get('/')
# async def getUsers():
#     userslist = list_serial(usersCollection.find())
#     return userslist

# @router.get('/singleUser')
# async def getSingleUser(name: str ):
#     user = individual_serial(usersCollection.find_one({"name": name}))
#     return user

# # @router.post('/')
# # async def createUser(user: User):
# #     user = usersCollection.insert_one(dict(user)) #remember this step you passing object as dictionary
# #     # successfully creating
    
# @router.put('/{id}')
# async def updateUser(id:str, user:User):
#     updatedUser = usersCollection.update_one({"_id": ObjectId(id)}, {"$set": dict(user)}) #remember this special method
#     #successfylly updating user
    
# @router.delete('/{id}')
# async def deleteUser(id:str):
#     deleteUser = usersCollection.delete_one({"_id": ObjectId(id)})

# #successfully made a crud application with fastapi.


# @router.post('/signup', summary="Create new user")
# async def create_user(data: User):
#     # first check if there is user in the db
#     user = usersCollection.find_one({"name": data.email})
#     if user is not None:
#         raise HTTPException(
#             status_code= status.HTTP_400_BAD_REQUEST,
#             detail="User with this email already exists"
#         )
#     user = {
#         "name": data.name,
#         'email': data.email,
#         'password': get_hashed_password(data.password),
#     }
#     user = usersCollection.insert_one(dict(user))
#     return {"message": "created user"}


# @router.post('/login', summary="Check user")
# async def login_user(details: LogUser):
#     user =  individual_serial(usersCollection.find_one({"email": details.email}))
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect email or password"
#         )
    
#     hashed_pass = user['password']
#     if not verify_hashed_password(details.password, hashed_pass):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect email or password" # be aware here not to messup
#         )
        
#     return {
#         "access_token": create_access_token(user['email']),
#         "refresh_token": create_refresh_token(user['email']),
#     }
    
# @router.post('/items')
# async def list_items(authenticated_user: str =  Depends(check_login) ): #this is called dependency injection
#     # here this funciton depends on the function check_login which will check if the token is valid or not 
#     # and then validate the user to perform certian operations.
#     if not authenticated_user['status_authenticated']: 
#            raise HTTPException(
#             status_code= status.HTTP_400_BAD_REQUEST,
#             detail="Not Authorized"
#         )
#     information = list_serial(usersCollection.find())
#     # here now it is accessible to the users who are subscribed
       
#     return {"data": authenticated_user, "items": information}

# @router.post('/fileupload')
# async def upload_file(file: Annotated[UploadFile, File(description="This is where user will upload file nothing else")]):
#     # You can perform any operations here on file the file objcect is spooled thing
#     # I have to know more about this thing
#     # content = file.decode('utf-8')
#     # lines = content.split('\n')
#     # if not lines:
#     #     raise HTTPException(status_code=401, detail='The file was unable to decode')
#     return {"filename": file.filename, "type": file.content_type}

# # @router.post('/files')
# # def get_file(file: bytes = File(...)):
# #     content = file.decode('utf-8')
# #     lines = content.split('\n')
# #     return {"content": lines}


# @router.post('/upload')
# def upload_file(uploaded_file: UploadFile = File(...)):
#     try:
#         path = f"files/{uploaded_file.filename}"
#         with open(path, 'w+b') as file:
#             try:
#                 shutil.copyfileobj(uploaded_file.file, file)
#             except Exception as e:
#                 raise HTTPException(status_code=500, detail=f"Error saving file: {e}")

#         return {
#             'file': uploaded_file.filename,
#             'content': uploaded_file.content_type,
#             'path': path,
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing file: {e}")
    
# @router.post('/upload/file')
# def upload_json(file:UploadFile = File(...)):
#     if file.content_type != 'application/json':
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wow, That's not allowed")
#     data = json.loads(file.file.read())
#     return {
#         "filename":file.filename,
#         "content":data
#     }
    
    
# # time_str = time.strftime('%Y-%m%d - %H%M%S')
# # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# # UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


# # @router.post('/upload/download')
# # def upload_download(file: UploadFile):
# #     print(f"Received file: {file.filename} with content type: {file.content_type}")
# #     if file.content_type != 'application/json':
# #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wow, that's not allowed")
    
# #     try:
# #         data = json.loads(file.file.read())
# #     except Exception as e:
# #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid JSON file: {e}")
    
# #     new_filename = "{}_{}.yaml".format(os.path.splitext(file.filename)[0], time_str)
# #     SAVE_F = os.path.join(UPLOAD_DIR, new_filename)
# #     print(f"Saving file to: {SAVE_F}")  # Debugging statement

# #     try:
# #         with open(SAVE_F, "w") as f:
# #             yaml.safe_dump(data, f)
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=f"Error saving YAML file: {e}")
    
# #     return FileResponse(path=SAVE_F, media_type="application/octet-stream", filename=new_filename)



# # Success ultimate able to download and upload images.
# @router.post('/image/upload')
# async def image_upload(file: Annotated[UploadFile, File(description="upload image here")]):
#     try:
#         file.filename = f"{uuid.uuid4()}.jpg"
#         contents = await file.read()  # <-- Important!
        
#         local_db.append(contents)
        
#         return {"filename": file.filename}
#     except Exception as e:
#         return {"error": str(e)}


# # An ultimately successful thing I made
# @router.get('/image/download')
# async def image_download():
#     try:
#         random_index = randint(0, len(local_db) - 1)
#         headers = {
#             'Content-Disposition': 'attachment; filename=image.jpg',
#             'Content-Type': 'image/jpeg'  # Change the content type accordingly if your image is in a different format
#         }
#         response = Response(content=local_db[random_index], headers=headers)
#         return response
#     except Exception as e:
#         return {"error": str(e)}
    
# # Success ultimate able to download and upload images.
# @router.post('/video/upload')
# async def video_upload(file: Annotated[UploadFile, File(description="upload image here")]):
#     try:
#         file.filename = f"{uuid.uuid4()}.mp4"
#         contents = await file.read()  # <-- Important!
        
#         local_db.append(contents)
        
#         return {"filename": file.filename}
#     except Exception as e:
#         return {"error": str(e)}


# # An ultimately successful thing I made
# @router.get('/video/download')
# async def video_download():
#     try:
#         random_index = randint(0, len(local_db) - 1)
#         headers = {
#             'Content-Disposition': 'attachment; filename=filename.mp4',
#             'Content-Type': 'video/mp4'
#         }
#         response = Response(content=local_db[random_index], headers=headers)
#         return response
#     except Exception as e:
#         return {"error": str(e)}
    
    
    
    
# # Success ultimate able to download and upload images.
# @router.post('/ppt/upload')
# async def ppt_upload(file: Annotated[UploadFile, File(description="upload image here")]):
#     try:
#         file.filename = f"{uuid.uuid4()}.pptx"
#         contents = await file.read()  # <-- Important!
        
#         local_db.append(contents)
        
#         return {"filename": file.filename}
#     except Exception as e:
#         return {"error": str(e)}


# # An ultimately successful thing I made
# @router.get('/ppt/download')
# async def ppt_download():
#     try:
#         random_index = randint(0, len(local_db) - 1)
#         headers = {
#             'Content-Disposition': 'attachment; filename=filename.pptx',
#             'Content-Type': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
#         }
#         response = Response(content=local_db[random_index], headers=headers) #this is important step
#         return response
#     except Exception as e:
#         return {"error": str(e)}
    