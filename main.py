from rich.console import Console
console = Console()
from datetime import datetime
import json

inUser = []

def signUp ():
    console.print('Please enter needed values to continue...', style='magenta')
    console.print('Username: ', end='')
    inpUsername = input()
    console.print('Email address: ', end='')
    inpEmail = input()
    console.print('Password: ', end='')
    inpPassword = input()
    #push in data
    # check for repeated username or email
    checkForValidSignup = True
    creationTime = 0
    if checkForValidSignup:
        console.log("Your account was successfully made", style='green bold')
        creationTime = datetime.now()
    user = {
        'email' : inpEmail,
        'username' : inpUsername,
        'password' : inpPassword,
        # 'time' : creationTime,
        'isActive' : True,
        'leaderOf' : [],
        'memberOf' : [],
    }
    users.append(user)
    with open("users.json", 'w') as usersFW:
        json.dump(users, usersFW)


def usernameCheck (users, usernameC):
    for user in users:
        if user['username'] == usernameC:
            return user
    return False

def login():
    console.print('Please enter expected values...', style='magenta')
    console.print('Username: ', end='')
    while True:
        username = input()
        if usernameCheck(users, username) != False:
            break
        else:
            console.print('Username does not exist, please enter another usename...', style='red bold')
    console.print('Password: ', end='')
    while True:
        password = input()
        if password == usernameCheck(users, username)['password']:
            inUser.append(usernameCheck(users, username))
            break
        else:
            console.print('Password does not match, please enter another password...', style='red bold')
with open("users.json", 'r') as usersFR:
    users = json.load(usersFR)

def newTask(project):
    task = {
        'id' : '',
        'title' : '',
        'description' : '',
        'time' : '',
        'date' : '',
        'assigness' : [],
        'priority' : '',
        'status' : '',
        'history' : [],
        'comments' : []
    }
    # console.print('Alright!\nPlease enter expected values... ', style='magenta')
    # console.print('Project title: ', end='')
    # task['title'] = input()
    # console.print('Project description: ', end='')
    # task['description'] = input()
    # # assigness left here

    # console.print('Project title: ', end='')
    # console.print('Project title: ', end='')
    # console.print('Project title: ', end='')

# -------------- main code starts from here ---------------------
# -------------- main code starts from here ---------------------
# -------------- main code starts from here ---------------------
# -------------- main code starts from here ---------------------
console.print("\t1. Login \n\t2. sign up", style='magenta')
while True:
    signInType = input()
    if signInType == '1':
        login()
        break
    elif signInType == '2':
        signUp()
        console.print("\t1. Login \n\t2. sign up", style='magenta')
    else:
        console.print('Please enter 1 or 2', style='red bold')
console.print('Here is your panel', style='magenta')
console.print('\t1. new project\n\t2. show existing projects\n\t3. edit your projects', style='magenta')
panelJob = input()
if panelJob == '1':
    project = {
        'id' : '',
        'name' : '',
        'leader' : '',
        'collaborators' : [],
        'tasks' : []
    }
    console.print('Alright!\nPlease enter expected values... ', style='magenta')
    console.print('Project name: ', end='', style='')
    project['name'] = input()
    console.print('Project collaborators: ', end='', style='')
    while True:
        collaborator = input()
        if collaborator == 'end':
            break
        else:
            project['collaborators'].append(collaborator)
    project['leader'] = inUser['username']
    while True:
        project['tasks'].append(newTask(project))
        if collaborator == 'end':
            break
        else:
            project['tasks'].append(newTask(project))