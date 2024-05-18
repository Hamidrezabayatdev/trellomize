from rich.console import Console
console = Console()
from datetime import datetime
import json

inUser = {}

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
            global inUser
            inUser = usernameCheck(users, username)
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
    console.print('Alright!\nPlease enter expected values... ', style='magenta')
    console.print('Task title: ', end='')
    task['title'] = input()
    console.print('Task description: ', end='')
    task['description'] = input()
    # assigness left here
    #time&date and endtime&enddate
    console.print('Choose ask status', end=' ')
    console.print('(press enter if you want to continue with default value (BACKLOG))', style='yellow')
    console.print('\t1. TODO\n\t2. DOING\n\t3. DONE\n\t4. ARCHIVED', style='magenta')
    while True:
        status = input()
        if status == '1':
            task['status'] = 'TODO'
            break
        elif status == '2':
            task['status'] = 'DOING'
            break
        elif status == '3':
            task['status'] = 'DONE'
            break
        elif status == '4':
            task['status'] = 'ARCHIVED'
            break
        elif status == '':
            break
        else:
            console.print('Please enter between 1 to 4', style='red bold')
    console.print('Task priority: ', end='')
    console.print('press enter if you want to continue with default value(LOW)', style='yellow')
    console.print('\t1. CRITICAL\n\t2. HIGH\n\t3. MEDIUM', style='magenta')
    while True:
        prioritry = input()
        if prioritry == '1':
            task['prioritry'] = 'CRITICAL'
            break
        elif status == '2':
            task['prioritry'] = 'HIGH'
            break
        elif prioritry == '3':
            task['prioritry'] = 'MEDIUM'
            break
        elif prioritry == '':
            break
        else:
            console.print('Please enter between 1 to 3', style='red bold')
    console.print('If you want to add comments, please type here...', end=' ', style='magenta')
    console.print('press enter to continue', style='yellow')
    comment = input()
    while True:
        if comment == '':
            break
        else:
            task['comments'].append(comment)
            console.print('Comment added; If you want to add another comment, please type it...', end=' ', style='green')
            console.print('press enter to continue', style='yellow')
            comment = input()
    console.print('Task has been successfully added', end=' ', style='green')
    return task
def newProject():
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
    return project
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
    newProject()