import argparse
import json
import os
import bcrypt
def get_hashed_password(plain_text_password):

    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def createAdmin(name, password):
    Manager = {
        "name": name,
        "password": get_hashed_password(password)
    }
    p=True
    with open("managerInfo.json", 'r') as exFile:
        managerInfodict = json.load(exFile)
        if managerInfodict['name']!="" or managerInfodict['password']!='' :
            p=False
    if p:
        with open("managerInfo.json", 'w') as maFile:
            json.dump(Manager, maFile)
    else:
        print("A manager already exists! you can't create a new one.")

     
parser = argparse.ArgumentParser()
parser.add_argument("create-admin")
parser.add_argument("--username")
parser.add_argument("--password")
#parser.add_argument("purge-data")
args= parser.parse_args()

createAdmin(args.username, args.password )
#if args.purge:
    #with open("users.json", "w") as Ufile:
        #Ufile.truncate()
    #with open("projects.json", "w") as Pfile:
        #Pfile.truncate()        
    