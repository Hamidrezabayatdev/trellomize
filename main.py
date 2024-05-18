from rich.console import Console
console = Console()
from datetime import datetime
import json
with open("users.json", 'r') as usersFR:
    users = json.load(usersFR)
with open("projects.json", 'r') as projectsFR:
    projects = json.load(projectsFR)

inUser = 1000

def checkInUser(val, checkType):
    for i in users:
        if i[checkType] == val:
            return False
    return True

def signUp ():
    console.print('Please enter needed values to continue...', style='magenta')
    console.print('Username: ', end='')
    inpUsername = input()
    while checkInUser(inpUsername, 'username') == False:
        console.print('Username already exists, please enter another username...', style='red bold')
        inpUsername = input()
    console.print('Email address: ', end='')
    inpEmail = input()
    while checkInUser(inpEmail, 'email') == False:
        console.print('Email already exists, please enter another email...', style='red bold')
        inpEmail = input()
    checkInUser(inpEmail, 'email')
    console.print('Password: ', end='')
    inpPassword = input()
    #push in data

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
    global users
    users.append(user)
    with open("users.json", 'w') as usersFW:
        json.dump(users, usersFW)

def usernameCheck (usernameC):
    global users
    for i in range(len(users)):
        if users[i]['username'] == usernameC:
            return i
    return False

def login():
    console.print('Please enter expected values...', style='magenta')
    console.print('Username: ', end='')
    while True:
        username = input()
        if usernameCheck(username) != False or str(usernameCheck(username)) == '0':
            break
        else:
            console.print('Username does not exist, please enter another usename...', style='red bold')
    console.print('Password: ', end='')
    while True:
        password = input()
        if password == users[usernameCheck(username)]['password']:
            global inUser
            inUser = usernameCheck(username)
            break
        else:
            console.print('Password does not match, please enter another password...', style='red bold')

def newTask():
    task = {
        'id' : '',
        'title' : '',
        'description' : '',
        'time' : '',
        'date' : '',
        'assigness' : [],
        'priority' : 'LOW',
        'status' : 'BACKLOG',
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
        priority = input()
        if priority == '1':
            task['priority'] = 'CRITICAL'
            break
        elif priority == '2':
            task['priority'] = 'HIGH'
            break
        elif priority == '3':
            task['priority'] = 'MEDIUM'
            break
        elif priority == '':
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
    console.print('Task has been successfully added', style='green')
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
    users[inUser]['leaderOf'].append(project['name'])
    project['collaborators'].append(users[inUser]['username'])
    console.print('Project collaborators username: ', end=' ', style='')
    console.print('press enter to continue', style='yellow')
    collaborator = input()
    while collaborator != '':
        if checkInUser(collaborator, 'username'):
            console.print('This username doesn\'t exist! Please enter an existing username', style='red bold')
            console.print('Project collaborators username: ', end=' ', style='')
            console.print('press enter to continue', style='yellow')
        else:
            if collaborator not in project['collaborators']:
                project['collaborators'].append(collaborator)
                console.print(collaborator, 'has been successfully added to task\'s collaborators', style='green')
                console.print('Project collaborators username: ', end=' ', style='')
                console.print('press enter to continue', style='yellow')
            else:
                console.print('Already added! Please add another username', end=' ', style='red bold')
                console.print('or press enter to continue', style='yellow')
        collaborator = input()
    project['leader'] = users[inUser]['username']
    console.print('Press \'1\' to add a new task to your project', end=' ', style='magenta')
    console.print('press enter to continue', style='yellow')
    while input() != '':
        project['tasks'].append(newTask())
        console.print('Press \'1\' to add a new task to your project', end=' ', style='magenta')
        console.print('press enter to continue', style='yellow')
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
        console.print(users)
        console.print("\t1. Login \n\t2. sign up", style='magenta')
    else:
        console.print('Please enter 1 or 2', style='red bold')
console.print('Here is your panel', style='magenta')
console.print('\t1. new project\n\t2. show existing projects\n\t3. edit your projects', style='magenta')
panelJob = input()
if panelJob == '1':
    project = newProject()
    # users[inUser]['leaderOf'].append(project['name'])
    projects.append(project)






with open("users.json", 'w') as usersFW:
    json.dump(users, usersFW)
with open("projects.json", 'w') as projectsFW:
    json.dump(projects, projectsFW)