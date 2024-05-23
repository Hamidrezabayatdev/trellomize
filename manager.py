import argparse
import json
import os
import argon2
def createAdmin(name, password):
    passBytes = password.encode('utf-8')
    hashed = argon2.PasswordHasher().hash(passBytes)
    Manager = {
        "name": name,
        "password": hashed
    }
    p=True
    with open("managerInfo.json", 'r') as exFile:
        if os.path.getsize("managerInfo.json") !=0 :
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
    