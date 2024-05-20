from rich.console import Console
console = Console()
from datetime import datetime
import json
with open("users.json", 'r') as usersFR:
    users = json.load(usersFR)
with open("projects.json", 'r') as projectsFR:
    projects = json.load(projectsFR)

inUser = 1000

def filesWrite():
    with open("users.json", 'w') as usersFW:
        json.dump(users, usersFW)
    with open("projects.json", 'w') as projectsFW:
        json.dump(projects, projectsFW)

def checkInUsers(val, checkType):
    for i in range(len(users)):
        if users[i][checkType] == val:
            return i
    return False

def checkInProjects(val, checkType):
    for i in range(len(projects)):
        if projects[i][checkType] == val:
            return i
    return False


def signUp ():
    console.print('Please enter needed values to continue...', style='magenta')
    console.print('Username: ', end='')
    inpUsername = input()
    while checkInUsers(inpUsername, 'username') != False or str(checkInUsers(inpUsername, 'username')) == '0':
        console.print('Username already exists, please enter another username...', style='red bold')
        inpUsername = input()
    console.print('Email address: ', end='')
    inpEmail = input()
    while checkInUsers(inpEmail, 'email') != False or str(checkInUsers(inpEmail, 'email')) == '0':
        console.print('Email already exists, please enter another email...', style='red bold')
        inpEmail = input()
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
    filesWrite()

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
    console.print('Choose task status', end=' ')
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
    console.print('Project collaborators usernames: ', end=' ', style='')
    console.print('press enter to continue', style='yellow')
    collaborator = input()
    while collaborator != '':
        if checkInUsers(collaborator, 'username') == False and str(checkInUsers(collaborator, 'username')) != '0':
            console.print('This username doesn\'t exist! Please enter an existing username', style='red bold')
            console.print('Project collaborators username: ', end=' ', style='')
            console.print('press enter to continue', style='yellow')
        else:
            if collaborator not in project['collaborators']:
                project['collaborators'].append(collaborator)
                users[checkInUsers(collaborator, 'username')]['memberOf'].append(project['name'])
                ## collab memberOf
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
def showLeaderProjects():
    console.print('Projects that you are leader of them:', style='magenta')
    for projs in users[inUser]['leaderOf']:
        console.log('\t', projs)
def showMemberProjects():
    console.print('Projects that you are member of them:', style='magenta')
    for projs in users[inUser]['memberOf']:
        console.log('\t', projs)
def taskIndex(val, checkType, projectIndex):
    for i in range(len(projects[projectIndex]['tasks'])):
        if projects[projectIndex]['tasks'][i][checkType] == val:
            return i
    return False
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
        # console.print(users)
        console.print("\t1. Login \n\t2. sign up", style='magenta')
    else:
        console.print('Please enter 1 or 2', style='red bold')
console.print('Here is your panel', style='magenta')
console.print('\t1. new project\n\t2. show existing projects\n\t3. edit your projects', style='magenta')
panelJob = input()
while panelJob != '':
    if panelJob == '1':
        project = newProject()
        projects.append(project)
        filesWrite()
    elif panelJob == '2':
        showLeaderProjects()
        showMemberProjects()
    elif panelJob == '3':
        showLeaderProjects()
        console.print('Enter the name of the project that you want to edit:', end=' ', style='magenta')
        editProjName = input()
        editProjIndex = checkInProjects(editProjName, 'name')
        while editProjIndex == False and str(editProjIndex) != '0':
            console.print('You can only edit the projects that you are the leader of them!', end=' ', style='red bold')
            console.print('Projects that you are leader of them:', style='magenta')
            showLeaderProjects()
            console.print('Enter the name of the project that you want to edit:', end=' ', style='magenta')
            editProjName = input()
            editProjIndex = checkInProjects(editProjName, 'name')

        console.log('your projects specifications:', projects[editProjIndex])
        console.print('If you want to add/remove a collaborator, type the name', end=' ', style='magenta')
        console.print('press enter to continue', style='yellow')
        collabEdit = input()
        while collabEdit != '':
            if collabEdit in projects[editProjIndex]['collaborators']:
                if collabEdit == projects[editProjIndex]['leader']:
                    console.print('You can not remove the project leader from collaborators!', style='red bold')
                else:
                    projects[editProjIndex]['collaborators'].remove(collabEdit)
                    users[checkInUsers(collabEdit, 'username')]['memberOf'].remove(projects[editProjIndex]['name'])
                    console.print(collabEdit, 'has been successfully removed from this task\'s collaborators', style='green')
            else:
                if checkInUsers(collabEdit, 'username') == False and str(checkInUsers(collabEdit, 'username')) != '0':
                    console.print('This username doesn\'t exist! Please enter an existing username', style='red bold')
                else:
                    if collabEdit not in projects[editProjIndex]['collaborators']:
                        projects[editProjIndex]['collaborators'].append(collabEdit)
                        users[checkInUsers(collabEdit, 'username')]['memberOf'].append(projects[editProjIndex]['name'])
                        ## collab memberOf
                        console.print(collabEdit, 'has been successfully added to task\'s collaborators', style='green')
                    else:
                        console.print('Already added! Please add another username', end=' ', style='red bold')
                        console.print('or press enter to continue', style='yellow')
            console.print('If you want to add/remove a collaborator, type the name', end=' ', style='magenta')
            console.print('press enter to continue', style='yellow')
            collabEdit = input()
        # console.print(projects, style='blue')
        console.print('If you want to edit an existing task, type it\'s name', end=' ', style='magenta')
        console.print('press enter to continue', style='yellow')
        editTaskName = input()
        while editTaskName != '':
            ediTaskIndex = taskIndex(editTaskName, 'title', editProjIndex)
            console.print('Enter the task item that you want to edit', end=' ', style='magenta')
            console.print('press enter to continue', style='yellow')
            taskItemEdit = input()
            while taskItemEdit != '':
                if taskItemEdit == 'title' or taskItemEdit == 'description':
                    console.print('Ok, Enter the text that you want to replace in', taskItemEdit, end=' ', style='magenta')
                    projects[editProjIndex]['tasks'][ediTaskIndex][taskItemEdit] = input()
                elif taskItemEdit == 'priority':
                    console.print('press enter to continue', style='yellow')
                    console.print('\t1. CRITICAL\n\t2. HIGH\n\t3. MEDIUM\n\t4. LOW', style='magenta')
                    while True:
                        priority = input()
                        if priority == '1':
                            projects[editProjIndex]['tasks'][ediTaskIndex]['priority'] = 'CRITICAL'
                            break
                        elif priority == '2':
                            projects[editProjIndex]['tasks'][ediTaskIndex]['priority'] = 'HIGH'
                            break
                        elif priority == '3':
                            projects[editProjIndex]['tasks'][ediTaskIndex]['priority'] = 'MEDIUM'
                            break
                        elif priority == '4':
                            projects[editProjIndex]['tasks'][ediTaskIndex]['priority'] = 'LOW'
                            break
                        elif priority == '':
                            break
                        else:
                            console.print('Please enter between 1 to 3', style='red bold')
                elif taskItemEdit == 'status':
                    console.print('press enter to continue', style='yellow')
                    console.print('\t1. TODO\n\t2. DOING\n\t3. DONE\n\t4. ARCHIVED\n\t5. BACKLOG', style='magenta')
                    while True:
                        status = input()
                        if status == '1':
                            projects[editProjIndex]['tasks'][ediTaskIndex]['status'] = 'TODO'
                            break
                        elif status == '2':
                            projects[editProjIndex]['tasks'][ediTaskIndex]['status'] = 'DOING'
                            break
                        elif status == '3':
                            projects[editProjIndex]['tasks'][ediTaskIndex]['status'] = 'DONE'
                            break
                        elif status == '4':
                            projects[editProjIndex]['tasks'][ediTaskIndex]['status'] = 'ARCHIVED'
                            break
                        elif status == '5':
                            projects[editProjIndex]['tasks'][ediTaskIndex]['status'] = 'BACKLOG'
                            break
                        elif status == '':
                            break
                        else:
                            console.print('Please enter between 1 to 4', style='red bold')
                elif taskItemEdit == 'comments':
                    console.print('Enter the comment that you want to add', style='magenta')
                    projects[editProjIndex]['tasks'][ediTaskIndex]['comments'].append(input())
                elif taskItemEdit == '':
                    break
                else:
                    console.print('This task does not have this item!', style='red bold')
                console.print('Enter the task item that you want to edit', end=' ', style='magenta')
                console.print('press enter to continue', style='yellow')
                taskItemEdit = input()
            console.print('If you want to edit an existing task, type it\'s name', end=' ', style='magenta')
            console.print('press enter to continue', style='yellow')
            editTaskName = input()
    console.print('\t1. new project\n\t2. show existing projects\n\t3. edit your projects', style='magenta')
    panelJob = input()


print("pouri joon, barat olvie doros kadam")

filesWrite()