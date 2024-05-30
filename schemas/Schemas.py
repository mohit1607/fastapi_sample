# here we will do what is called serialize the things  or basically way 
# to identify object by mongodb

def individual_serial(user) -> dict :
    return {
        "id": str(user["_id"]),
        "name": str(user["name"]),
        "email": str(user["email"]),
        "password": str(user["password"]),
    }

def list_serial(users) -> list:
    return[individual_serial(user) for user in users]