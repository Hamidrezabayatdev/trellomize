import argparse
import json
import bcrypt
import sys
import logging
import base64
#logging:
logger2 = logging.getLogger("manager.py")

logging.basicConfig(filename="user_actions.log",
                    filemode='a',
                    format='%(asctime)s, %(name)s %(levelname)s %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)


def get_hashed_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) 
    encoded_hashed_password = base64.b64encode(hashed_password).decode('utf-8')
    return encoded_hashed_password

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
            loggingMessage = "Manager created!...Name: "+ Manager["name"]
            logger2.info(loggingMessage)
            
        
    else:
        loggingMessage = "The output of (createAdmin) function was: "+ "A manager already exists! you can't create a new one."
        print("A manager already exists! you can't create a new one.")
        logger2.warning(loggingMessage)

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
    loggingMessage = "These arguments were passed to the (createAdmin) function : "+ args.username +" , "+ args.password 
    logger2.info(loggingMessage)
elif sys.argv[1]=="purge-data":
    print("all datas will be deleted! (including information regarding users, projects, tasks and etc)... Do you wish to proceed?")
    print("(enter 1 for YES and any other key for NO)")
    managerchoice = input()
    if managerchoice == '1':
        PurgeData()
    else:
        pass
        


    