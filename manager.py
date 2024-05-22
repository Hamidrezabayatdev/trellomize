import argparse
import json
def createAdmin(name, password):
    Manager = {
        "name": name,
        "password": password
    }
    p=True
    with open("managerInfo.json", 'r') as exFile:
        if exFile["name"] !="" :
            p=False
    if p:
        with open("managerInfo.json", 'w') as maFile:
            json.dump(Manager, maFile)

     
parser = argparse.ArgumentParser()
parser.add_argument("create-admin")
parser.add_argument("--username")
parser.add_argument("--password")
args= parser.parse_args()

createAdmin(args.username, args.password )