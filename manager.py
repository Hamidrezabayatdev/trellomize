import argparse
import json
def createAdmin(name, password):
    Manager = {
        "name": name,
        "password": password
    } 
    with open("managerInfo.json", 'w') as maFile:
        json.dump(Manager, maFile)

     
parser = argparse.ArgumentParser()
parser.add_argument("creat-admin")
parser.add_argument("--username")
parser.add_argument("--password")
args= parser.parse_args()
if args.create_admin:
    createAdmin(args.username, args.password )