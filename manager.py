import argparse
import json
import os
def createAdmin(name, password):
    Manager = {
        "name": name,
        "password": password
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
args= parser.parse_args()

createAdmin(args.username, args.password )