import argparse
import json
import bcrypt
import sys
def get_hashed_password(plain_text_password):

    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def createAdmin(name, password):
    Manager = {
        "name": name,
        "password": password
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

def PurgeData():
    with open("users.json", 'w') as usersToPurge:
        usersToPurge.truncate()   
    with open("projects.json", 'w') as projectsToPurge:
        projectsToPurge.truncate()
parser = argparse.ArgumentParser()
parser.add_argument("create-admin")
parser.add_argument("--username")
parser.add_argument("--password")
args= parser.parse_args()

if sys.argv[1]=="create-admin" :
    createAdmin(args.username, args.password )
elif sys.argv[1]=="purge-data":
    print("all datas will be deleted! (including information regarding users, projects, tasks and etc)... Do you wish to proceed?")
    print("(enter 1 for YES and any other key for NO)")
    managerchoice = input()
    if managerchoice == '1':
        PurgeData()
    else:
        pass
        


    