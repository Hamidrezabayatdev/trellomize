import os
from rich.console import Console
console = Console()
from rich.table import Table
from datetime import datetime, timedelta
from rich.progress import track
import json
import re
import time
import bcrypt
import uuid
import logging
from enum import Enum
import base64
# convert the time in seconds since the epoch to a readable format
# local_time = time.ctime(seconds)

#logging :
logger = logging.getLogger("main.py")

logging.basicConfig(filename="user_actions.log",
                    filemode='a',
                    format='%(asctime)s, %(name)s %(levelname)s %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)

#enumeration class for task status:
class TaskStatus(Enum):
    TODO = 1
    DOING = 2
    DONE = 3
    ARCHIVED = 4
    BACKLOG = 5   

#enumeration class for task priority:
class TaskPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

#cls func:
def clear_terminal(seconds=0.01):
    '''
    takes seconds and clears terminal after that
    '''
    time.sleep(seconds)
    os.system('cls' if os.name == 'nt' else 'clear')
    

with open("users.json", 'r') as usersFR:
    users = json.load(usersFR)
with open("projects.json", 'r') as projectsFR:
    projects = json.load(projectsFR)

inUser = 1000

def get_hashed_password(password):
    '''
    Takes password
    Returns hashed password
    '''
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) 
    encoded_hashed_password = base64.b64encode(hashed_password).decode('utf-8')
    return encoded_hashed_password

def check_password(password, encoded_hashed_password):
    '''
    Takes password
    Returns True if hash check was true
    '''
    hashed_password = base64.b64decode(encoded_hashed_password)
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def timeValidate(dt_string):
    '''
    Takes a string for time
    Returns True if time format was right
    '''
    try:
        time.strptime(dt_string, "%d-%m-%Y %H:%M")
    except ValueError:
        return False
    return True

def checkEmail(email):
    '''
    Takes email string
    Returns True if email format was right
    '''
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.match(pat,email)):
        return True
    else:
        return False
    
def filesWrite():
    '''
    Dumps datas to json files
    '''
    with open("users.json", 'w') as usersFW:
        json.dump(users, usersFW ,indent=4)
    with open("projects.json", 'w') as projectsFW:
        json.dump(projects, projectsFW, indent=4)

def checkInUsers(val, checkType,Users=users):
    '''
    Takes a value and a key to check in users
    Returns user's index in users json file - False for not found
    '''
    for i in range(len(Users)):
        if Users[i][checkType] == val:
            return i
    return False

def checkInProjects(val, checkType,Projects=projects):
    '''
    Takes a value and a key to check in projects
    Returns project's index in projects json file - False for not found
    '''
    for i in range(len(Projects)):
        if Projects[i][checkType] == val:
            return i
    return False

# def editAsigness(assigness):



def signUp ():
    '''
    Sign up an account
    '''
    console.print('(you can press enter to return to main manu)', style='yellow')
    console.print('Username:', end=' ')
    
    inpUsername = input()
    if inpUsername == '':
        clear_terminal()
        return
    while checkInUsers(inpUsername, 'username') != False or str(checkInUsers(inpUsername, 'username')) == '0':
        console.print('Username already exists, please enter another username...', style='red bold')
        clear_terminal(2)
        inpUsername = input()
        if inpUsername == '':
            clear_terminal()
            return
    console.print('(you can press enter to return to main manu)', style='yellow')
    console.print('Email address:', end=' ')
    
    inpEmail = input()
    if inpEmail == '':
        clear_terminal()
        return
    while True:
        if checkEmail(inpEmail):
            if checkInUsers(inpEmail, 'email') != False or str(checkInUsers(inpEmail, 'email')) == '0':
                console.print('Email already exists, please enter another email...', style='red bold')
                clear_terminal(2)
            else:
                break
        else:
            console.print('Incorrect email format, please enter another email...', style='red bold')
            clear_terminal(2)
        inpEmail = input()
        if inpEmail == '':
            clear_terminal()
            return
    console.print('(you can press enter to return to main manu)', style='yellow')
    console.print('Password:', end=' ')
    
    inpPassword = input()
    if inpPassword == '':
        clear_terminal()
        return
    
    #push in data

    checkForValidSignup = True
    if checkForValidSignup:
        console.log("Your account was successfully made", style='green bold')
        clear_terminal(1.5)
    user = {
        'email' : inpEmail,
        'username' : inpUsername,
        'password' : get_hashed_password(inpPassword),
        # 'password' : inpPassword,
        # 'time' : creationTime,
        'isActive' : True,
        'leaderOf' : [],
        'memberOf' : [],
    }
    global users
    users.append(user)
    filesWrite()
    

def usernameCheck (usernameC):
    '''
    Takes a username string
    Returns return user's index in users json file if existed - False for not found
    '''
    global users
    for i in range(len(users)):
        if users[i]['username'] == usernameC:
            return i
    return False

def login():
    '''
    login an account
    '''
    console.print('Please enter expected values', style='magenta')
    console.print('(or press enter to return and start over)', style='yellow')
    console.print('Username: ', end=' ')
    
    while True:
        username = input()
        if username == '':
            clear_terminal()
            return
        elif usernameCheck(username) != False or str(usernameCheck(username)) == '0':
            break
        else:
            console.print('Username does not exist, please enter another username...', style='red bold')
            clear_terminal(2)
            console.print('Username: ', end=' ')
    console.print('(you can press enter to return and start over)', style='yellow')
    console.print('Password: ', end=' ')
    
    while True:
        password = input()
        if password == '':
            clear_terminal()
            return
        elif check_password(password, users[usernameCheck(username)]['password']) and users[usernameCheck(username)]["isActive"]==True:
        # elif password == users[usernameCheck(username)]['password'] and users[usernameCheck(username)]["isActive"]==True:
            global inUser
            inUser = usernameCheck(username)
            loggingMessage = "User logged in to account "+ username
            logger.info(loggingMessage) 
            break
        else:
            if not check_password(password, users[usernameCheck(username)]['password']):
            # if password != users[usernameCheck(username)]['password']:
                console.print('Password does not match, please enter another password...', style='red bold')
                clear_terminal(1)
                console.print('Password: ', end=' ')
                
            elif users[usernameCheck(username)]["isActive"] == False:
                console.print("Your account has been suspended by the manager! You can't sign in!", style="red bold")
                clear_terminal(2)
                
                return False
    return True
def EnterAsManager():
    '''
    login as a manager
    '''
    def validating():
        '''
        validates if a user is manager
        '''
        global checkingIfuserIsManager  
        checkingIfuserIsManager=True
        console.print("Confirm that you are the manager:", style="magenta")
        console.print("Enter your username:", end=" ")
        enteredUsername = input()
        console.print("\nEnter your password:", end=" ")
        enteredPass=input()
        with open("managerInfo.json", 'r') as h:
            jj=json.load(h)
            
            if enteredUsername != jj["name"] or not check_password(enteredPass, jj['password']) :
                checkingIfuserIsManager = False
        
    validating() 
    while checkingIfuserIsManager == False :
        console.print("Wrong username/password! Try Again!", style="red bold")
        clear_terminal(1.5)
        validating()        
    global inUser
    inUser = -25
    #-25 represents manager's id. it's been picked randomly :)
    
def checkIDuniquness(myid):
    '''
    Takes an ID
    Returns False if ID was repeated in projects - True if ID was unique
    '''
    for i in projects:
        if i["id"]==myid:
            return False
    return True
def newTask(collaborators):
    '''
    Takes project's collaborators
    Returns created task
    '''
    task = {
        'id' : '',
        'title' : '',
        'description' : '',
        'time' : '',
        'assigness' : [users[inUser]['username']],
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
    task['id']=uuid.uuid4().int
    # assigness left here
    #time&date and endtime&enddate
    
    console.print('Choose task status', end=' ')
    console.print('(press enter if you want to continue with default value (BACKLOG))', style='yellow')
    console.print('\t1. TODO\n\t2. DOING\n\t3. DONE\n\t4. ARCHIVED', style='magenta')

    StatusEnumValues = [e.value for e in TaskStatus]
    while True:
        status = input()
        if status == '':
            break
        elif not status.isdigit():
            console.print('Please enter between 1 to 4', style='red bold')
            clear_terminal(1.5)
        elif int(status) in StatusEnumValues:
            task['status']= TaskStatus(int(status)).name
            break
        else:
            console.print('Please enter between 1 to 4', style='red bold')
            clear_terminal(1.5)
    console.print('Task priority: ', end='')
    console.print('press enter if you want to continue with default value(LOW)', style='yellow')
    console.print('\t1. CRITICAL\n\t2. HIGH\n\t3. MEDIUM', style='magenta')
    PriorityEnumValues = [e.value for e in TaskPriority]
    while True:
        priority = input()
        if priority == '':
            break
        elif not priority.isdigit():
            console.print('Please enter between 1 to 3', style='red bold')
            clear_terminal(1.5)
        elif int(priority) in PriorityEnumValues:
            task['priority'] = TaskPriority(int(priority)).name
            break
        else:
            console.print('Please enter between 1 to 3', style='red bold')
            clear_terminal(1.5)
    clear_terminal()
    console.print('If you want to assign this task to a collaborator, please type their name', end=' ', style='magenta')
    console.print('press enter to continue', style='yellow')
    console.print("Collaborators:", collaborators)
    assignName = input()
    while assignName != '':
        if usernameCheck(assignName) == False and str(usernameCheck(assignName)) != '0':
            console.print('Username does not exist, please enter another usename...', style='red bold')
            clear_terminal(1.5)
        elif assignName in task['assigness']:
            console.print("Already added!", style='red bold')
            clear_terminal(1)
        elif assignName not in collaborators:
            console.print('This user is not in the project\'s collaborators', style='red bold')
            clear_terminal(1.5)
        else:
            task['assigness'].append(assignName)
            console.print("Task has been successfully assigned to", assignName, style='green')
            clear_terminal(1.5)
        console.print('If you want to assign this task to another collaborator, please type their name', end=' ', style='magenta')
        console.print('press enter to continue', style='yellow')
        console.print("Collaborators:", collaborators)
        assignName = input()
        clear_terminal()
    console.print('If you want to add comments, please type them here...', end=' ', style='magenta')
    console.print('press enter to continue', style='yellow')
    comment = input()
    while comment != '':
        commentList = [(datetime.now()).strftime('%d-%m-%Y %H:%M'), users[inUser]['username'], comment]
        task['comments'].append(commentList)
        console.print('Comment added!', end=' ', style='green')
        clear_terminal(1)
        console.print('If you want to add another comment, please type it...', end=' ', style='magenta')
        console.print('press enter to continue', style='yellow')
        comment = input()
    clear_terminal()
    tomorrow = datetime.now() + timedelta(1)
    task['time'] = tomorrow.strftime('%d-%m-%Y %H:%M')
    console.print('If you want to edit task\'s ending time, type it in this format (DAY-MONTH-YEAR H:M)', style='magenta')
    console.print('Press enter to continue with default value (tommorow)', style='yellow')
    editTime = input()
    clear_terminal()
    while timeValidate(editTime) == False and editTime != '':
        console.print('Please enter in this format (DAY-MONTH-YEAR H:M)', style='red bold')
        clear_terminal(1.5)
        editTime = input()
    if editTime != '':
        task['time'] = editTime
        console.print('Task time has been set', style='green')
        clear_terminal(1.2)
    console.print('Task has been successfully added', style='green')
    clear_terminal(1.2)
    return task
def newProject():
    '''
    makes a new project
    Returns project list
    '''
    project = {
        'id' : '',
        'name' : '',
        'leader' : '',
        'collaborators' : [],
        'tasks' : []
    }
    console.print('Alright!\nPlease enter expected values...', style='magenta')
    console.print('Project ID: ', end='', style='')
    enteredID=input()
    while not checkIDuniquness(enteredID) or not enteredID.isdigit():
        if not enteredID.isdigit():
            console.print("Project ID should be a number!", style='red bold')
            clear_terminal(1.5)
        else:
            console.print("this ID is used for another project existing in the system! try another one!", style="red bold")
            clear_terminal(1.5)
        enteredID=input()
    project['id']=enteredID
    console.print('Project name: ', end='', style='')
    project['name'] = input()
    users[inUser]['leaderOf'].append(project['name'])
    project['collaborators'].append(users[inUser]['username'])
    console.print('(you can press enter to continue)', style='yellow')
    console.print('Project collaborators usernames: ', end=' ', style='')
    
    collaborator = input()
    clear_terminal()
    while collaborator != '':
        if checkInUsers(collaborator, 'username') == False and str(checkInUsers(collaborator, 'username')) != '0':
            console.print('This username doesn\'t exist! Please enter an existing username', style='red bold')
            clear_terminal(1.5)
            console.print('Project collaborators username: ', end=' ', style='')
            console.print('press enter to continue', style='yellow')
        else:
            if collaborator not in project['collaborators']:
                project['collaborators'].append(collaborator)
                users[checkInUsers(collaborator, 'username')]['memberOf'].append(project['name'])
                ## collab memberOf
                console.print(collaborator, 'has been successfully added to task\'s collaborators', style='green')
                clear_terminal(1.5)
                console.print('Project collaborators username: ', end=' ', style='')
                console.print('press enter to continue', style='yellow')
            else:
                console.print('Already added! Please add another username', end=' ', style='red bold')
                console.print('or press enter to continue', style='yellow')
        collaborator = input()
        clear_terminal()
        
    project['leader'] = users[inUser]['username']
    console.print('Type in anything to add a new task to your project', end=' ', style='magenta')
    console.print('press enter to continue', style='yellow')
    while input() != '':
        clear_terminal()
        project['tasks'].append(newTask(project['collaborators']))
        console.print('Type in anything to add a new task to your project', end=' ', style='magenta')
        console.print('press enter to continue', style='yellow')
    return project
def showLeaderProjects():
    '''
    shows projects that the member is their leader
    '''
    if len(users[inUser]['leaderOf'])!=0:
        console.print('Projects that you are leader of them:', style='magenta')
        for projs in users[inUser]['leaderOf']:
            console.log('\t', projs)
def showMemberProjects():
    '''
    shows projects that the member is their ordinary member
    '''
    if len(users[inUser]["memberOf"])!=0:
        console.print('Projects that you are an ordinary member of them:', style='magenta')
        for projs in users[inUser]['memberOf']:
            console.log('\t', projs)
def taskIndex(val, checkType, projectIndex):
    '''
    Takes a value and a key to check in tasks
    Returns task's index in tasks list - False if task was not found
    '''
    for i in range(len(projects[projectIndex]['tasks'])):
        if projects[projectIndex]['tasks'][i][checkType] == val:
            return i
    return False



def editTasknew(editProjIndex, editTaskIndex):
    '''
    Takes project index and task index
    Returns edited task
    '''
    # console.print("edit new ID:", projects[editProjIndex]['tasks'][editTaskIndex]['id'])
    if len(projects[editProjIndex]['tasks']) == 0:
        console.print("This project has no tasks!", style="red bold")
        return
    task = {
        'id' : projects[editProjIndex]['tasks'][editTaskIndex]['id'],
        'title' : projects[editProjIndex]['tasks'][editTaskIndex]['title'],
        'description' : projects[editProjIndex]['tasks'][editTaskIndex]['description'],
        'time' : projects[editProjIndex]['tasks'][editTaskIndex]['time'],
        'assigness' : projects[editProjIndex]['tasks'][editTaskIndex]['assigness'],
        'priority' : projects[editProjIndex]['tasks'][editTaskIndex]['priority'],
        'status' : projects[editProjIndex]['tasks'][editTaskIndex]['status'],
        'history' : projects[editProjIndex]['tasks'][editTaskIndex]['history'],
        'comments' : projects[editProjIndex]['tasks'][editTaskIndex]['comments']
    }

    console.print('Enter the task item that you want to edit', end=' ', style='magenta')
    console.print('press enter to continue', style='yellow')
    console.print('Valid choices:\n\t1. title\n\t2. description\n\t3. comments\n\t4. priority\n\t5. status\n\t6. time', style='magenta')
    taskItemEdit = input()
    clear_terminal()
    while taskItemEdit != '':
        if taskItemEdit == '1':
            console.print('Ok, Enter the title that you want to replace', style='magenta')
            newTitle = input()
            task['title'] = newTitle
            historyMessage = datetime.now().strftime('%d-%m-%Y %H:%M') + " : the title of task has been replaced with " + '('+newTitle+') by '+ users[inUser]['username']
            loggingMessage = users[inUser]['username']+" changed the title of task number "+ str(editTaskIndex+1)+ " of Project "+ projects[editProjIndex]['name'] 
            logger.info(loggingMessage)
            console.log("Title has been successfully changed", style='green bold')
            clear_terminal(1)
            task["history"].append(historyMessage)
        elif taskItemEdit == '2':
            console.print('Ok, Enter the description that you want to replace', style='magenta')
            newDescription = input()
            task['description'] = newDescription
            historyMessage = datetime.now().strftime('%d-%m-%Y %H:%M') + " : the description of task has been replaced with " + '('+newDescription+') by '+ users[inUser]['username']
            loggingMessage = users[inUser]['username']+" changed the description of task number "+ str(editTaskIndex+1)+ " of Project "+ projects[editProjIndex]['name']
            logger.info(loggingMessage)
            console.log("Description has been successfully changed", style='green bold')
            clear_terminal(1)
            task["history"].append(historyMessage)
        elif taskItemEdit == '4':
            console.print('press enter to continue', style='yellow')
            console.print('\t1. CRITICAL\n\t2. HIGH\n\t3. MEDIUM\n\t4. LOW', style='magenta')
            PriorityEnumValues = [e.value for e in TaskPriority]
            while True:
                priority = input()
                clear_terminal()
                if priority == '':
                    break
                elif int(priority) in PriorityEnumValues:
                    task['priority'] = TaskPriority(int(priority)).name 
                    historyMessage = datetime.now().strftime('%d-%m-%Y %H:%M') + " : the priority of task has been changed into "+task['priority']+" by "+ users[inUser]['username'] 
                    task['history'].append(historyMessage)
                    loggingMessage = users[inUser]['username'] + " changed the priority of task number "+ str(editProjIndex+1)+ " of project "+projects[editProjIndex]['name'] +" to "+task['priority']
                    logger.info(loggingMessage)
                    console.log("Priotity has been successfully changed", style='green bold')
                    clear_terminal(1.2)
                    break
                else:
                    console.print('Please enter between 1 to 4', style='red bold')
                    clear_terminal(1.5)
        elif taskItemEdit == '5':
                console.print('press enter to continue', style='yellow')
                console.print('\t1. TODO\n\t2. DOING\n\t3. DONE\n\t4. ARCHIVED\n\t5. BACKLOG', style='magenta')
                StatusEnumValues = [e.value for e in TaskStatus]
                while True:
                    status = input()
                    clear_terminal()
                    if status == '':
                        break
                    elif int(status) in StatusEnumValues:
                        task['status'] = TaskStatus(int(status)).name
                        historyMessage = datetime.now().strftime('%d-%m-%Y %H:%M') + " : the status of task has been changed into "+task['status']+" by "+ users[inUser]['username']
                        task['history'].append(historyMessage)
                        loggingMessage = users[inUser]['username'] + " changed the Status of task number "+ str(editProjIndex+1)+ " of project "+projects[editProjIndex]['name'] +" to "+task['status']
                        logger.info(loggingMessage)
                        console.log("Status has been successfully changed", style='green bold')
                        clear_terminal(1.2)
                        break
                    else:
                        console.print('Please enter between 1 to 5', style='red bold')
        elif taskItemEdit == '3':
            console.print('Enter the comment that you want to add', style='magenta')
            commentedTxt = input()
            while commentedTxt != '':
                comment = [(datetime.now()).strftime('%d-%m-%Y %H:%M'), users[inUser]['username'], commentedTxt]
                task['comments'].append(comment)
                historyMessage = datetime.now().strftime('%d-%m-%Y %H:%M') + " : the comment: "+ '('+commentedTxt+')'+" has been added to the task by "+ users[inUser]['username']
                task['history'].append(historyMessage)
                loggingMessage = users[inUser]['username'] + " added a comment to task number "+ str(editProjIndex+1)+ " of project "+projects[editProjIndex]['name'] 
                logger.info(loggingMessage)
                console.print('Comment added!', end=' ', style='green')
                clear_terminal(1)
                console.print('If you want to add another comment, please type it...', end=' ', style='magenta')
                console.print('press enter to continue', style='yellow')
                commentedTxt = input()
            clear_terminal()
        elif taskItemEdit == '6':
            console.print("Type the expiration time in this format (D-M-Y H:M)",end=' ', style='magenta')
            console.print("press enter to continue", style='yellow')
            editTime = input()
            clear_terminal()
            while timeValidate(editTime) == False and editTime != '':
                console.print('Please enter in this format (DAY-MONTH-YEAR H:M)', style='red bold')
                editTime = input()
            if editTime != '':
                task['time'] = editTime
                historyMessage = datetime.now().strftime('%d-%m-%Y %H:%M') + " : the expiration time of the task has be set to: " + editTime+" by "+ users[inUser]['username']
                task['history'].append(historyMessage)
                console.log("Expiration time has been successfully added", style='green bold')
                clear_terminal(1.5)
        elif taskItemEdit == '':
            break
        else:
            clear_terminal()
            console.print('Please enter between 1 to 6', style='red bold')
            clear_terminal(1.2)
        console.print('Enter the task item that you want to edit', end=' ', style='magenta')
        console.print('press enter to continue', style='yellow')
        console.print('Valid choices:\n\t1. title\n\t2. description\n\t3. comments\n\t4. priority\n\t5. status\n\t6. time', style='magenta')
        taskItemEdit = input()
        clear_terminal()

    return task

def editAtask():
    '''
    shows a proper menu to edit a task
    '''
    showLeaderProjects()
    showMemberProjects()
    if len(users[inUser]['leaderOf']) == 0 and len(users[inUser]['memberOf']) == 0:
        console.print("You are not a collaborator of any project!", style='red bold')
        clear_terminal(1.5)
        return
    console.print("If you want to see/edit a task in these project, enter the project name:", end=' ', style="magenta")
    console.print("press enter to continue", style="yellow")
    editProjName = input()
    clear_terminal()
    while editProjName != '':
        if editProjName in users[inUser]['leaderOf'] or editProjName in users[inUser]['memberOf']:
            break
        else:
            console.print('You can only edit the projects that you are a member of them!', style='red bold')
            clear_terminal(1.5)
            console.print('enter the project name', end=' ', style='magenta')
            console.print("press enter to continue", style="yellow")
            showLeaderProjects()
            showMemberProjects()
            editProjName = input()
            clear_terminal()
    if editProjName != '':
        editProjIndex = checkInProjects(editProjName, 'name')
        while editProjIndex == False and str(editProjIndex) != '0':
            console.print('Project not found', style='red bold')
            clear_terminal(1)
            showLeaderProjects()
            showMemberProjects()
            console.print("If you want to see/edit a task in these project, enter the project name:", end=' ', style="magenta")
            console.print("press enter to continue", style="yellow")
            editProjName = input()
            editProjIndex = checkInProjects(editProjName, 'name')
        console.print('All tasks in this project:', style='magenta')
        for task in projects[editProjIndex]['tasks']:
            console.print(task['title'], end=', ')
        console.print()
        console.print('Tasks which are assigned to you:', style='magenta')
        for task in projects[editProjIndex]['tasks']:
            if users[inUser]['username'] in task['assigness']:
                console.print(task['title'], end=', ')
        console.print()
        console.print('Enter the task name that you want to see/edit', end=' ', style='magenta')
        console.print('press enter to continue', style='yellow')
        editTaskName = input()
        clear_terminal()
        if editTaskName != '':
            while taskIndex(editTaskName, 'title', editProjIndex) == False and str(taskIndex(editTaskName, 'title', editProjIndex)) != '0':
                console.print('This task doesn\'t exist!', style='red bold')
                clear_terminal(1)
                console.print('All tasks in this project:', style='magenta')
                for task in projects[editProjIndex]['tasks']:
                    console.print(task['title'], end=', ')
                console.print()
                for task in projects[editProjIndex]['tasks']:
                    if users[inUser]['username'] in task['assigness']:
                        console.print(task['title'], end=', ')
                console.print()
                console.print('Enter the task name that you want to see/edit', end=' ', style='magenta')
                console.print('press enter to continue', style='yellow')
                editTaskName = input()
                clear_terminal()
                if editTaskName == '':
                    break
        editTaskIndex = taskIndex(editTaskName, 'title', editProjIndex)
        # new task assigness
        # new task assigness
        if users[inUser]['username'] == projects[editProjIndex]['leader']:
            console.print("You are the project leader; you can edit the assigness", style='green')
            console.print('Task assigness:', projects[editProjIndex]['tasks'][editTaskIndex]['assigness'], style='magenta')
            console.print('collaborators:', projects[editProjIndex]['collaborators'], style='magenta')
            console.print('If you want to assign this task to a collaborator/remove a collaborator from assigness, please type their name', end=' ', style='magenta')
            console.print('press enter to continue', style='yellow')
            assignName = input()
            clear_terminal()
            while assignName != '':
                if usernameCheck(assignName) == False and str(usernameCheck(assignName)) != '0':
                    console.print('Username does not exist, please enter another usename...', style='red bold')
                    clear_terminal(1.5)
                elif assignName not in projects[editProjIndex]['collaborators']:
                    console.print('This user is not in the project\'s collaborators', style='red bold')
                    clear_terminal(1.5)
                elif assignName == users[inUser]['username']:
                    console.print('You can not remove the project leader from assigness!', style='red bold')
                    clear_terminal(1.5)
                elif assignName in projects[editProjIndex]['tasks'][editTaskIndex]['assigness']:
                    projects[editProjIndex]['tasks'][editTaskIndex]['assigness'].remove(assignName)
                    console.print(assignName, 'has been successfully removed', style='green')
                    clear_terminal(1.2)
                else:
                    projects[editProjIndex]['tasks'][editTaskIndex]['assigness'].append(assignName)
                    console.print("Task has been successfully assigned to", assignName, style='green')
                    clear_terminal(1.2)
                console.print('Task assigness:', projects[editProjIndex]['tasks'][editTaskIndex]['assigness'], style='magenta')
                console.print('collaborators:', projects[editProjIndex]['collaborators'], style='magenta')
                console.print('If you want to assign this task to a collaborator/remove a collaborator from assigness, please type their name', end=' ', style='magenta')
                console.print('press enter to continue', style='yellow')
                assignName = input()
                clear_terminal()
        
        task = projects[editProjIndex]['tasks'][editTaskIndex]
        #table = Table(show_header=False)
        table = Table(title=task['title'])
        table.add_column('', justify='center', style='bold blue')
        table.add_column('', justify='center')
        table.add_row('title', task['title'])
        table.add_row('description', task['description'])
        table.add_row('priority', task['priority'])
        table.add_row('deadline', task['time'])
        table.add_row('status', task['status'])
        # table.add_row('history', ' '.join(task['history']))
        commentTable = Table(title='comments')
        commentTable.add_column('time', justify='center', style='yellow')
        commentTable.add_column('user', justify='center')
        commentTable.add_column('comment', justify='center')
        console.print(table)
        for i in range(len(task['comments'])):
            commentTable.add_row(task['comments'][i][0], task['comments'][i][1], task['comments'][i][2])
        time.sleep(5)
        console.print(commentTable)
        time.sleep(3)
        if len(task['history']) != 0:
            console.print("Task history: ")
            for i in track(range(len(task['history'])), description="History shown"):
                console.print()
                console.print('------------------------------------------')
                console.print(task['history'][i])
                console.print('------------------------------------------')
                console.print()
                time.sleep(2)
        if users[inUser]['username'] in projects[editProjIndex]['tasks'][editTaskIndex]['assigness']:
            projects[editProjIndex]['tasks'][editTaskIndex] = editTasknew(editProjIndex, editTaskIndex)
            filesWrite()
        else:
            console.print('press enter to return to the main menu', style='yellow')
            continueForEditTask = input()
        # new task assigness



def showProjects():
    '''
    shows projects and tasks properly to user
    '''
    if len(users[inUser]['leaderOf']) == 0 and len(users[inUser]['memberOf']) == 0:
        console.print("You are not a collaborator of any project!", style='red bold')
        clear_terminal(1.5)
        return
    showLeaderProjects()
    showMemberProjects()
    TODO = []
    DOING = []
    DONE = []
    ARCHIVED = []
    BACKLOG = []
    lens = []
    console.print("Enter the project name that you want to see it\'s tasks", style='magenta')
    console.print('press enter to continue', style='yellow')
    projName = input()
    clear_terminal()
    while projName != '':
        if checkInProjects(projName, 'name') == False and str(checkInProjects(projName, 'name')) != '0':
            console.print("This project doesn\'t exist!", style='red bold')
            clear_terminal(1.2)
        elif projName not in users[inUser]['leaderOf'] and projName not in users[inUser]['memberOf']:
            console.print("You are not a member of this project", style='red bold')
            clear_terminal(1.2)
        else:
            projectIndex = checkInProjects(projName, 'name')
            for i in range(len(projects[projectIndex]['tasks'])):
                if projects[projectIndex]['tasks'][i]['status'] == 'TODO':
                    TODO.append(projects[projectIndex]['tasks'][i]['title'])
                elif projects[projectIndex]['tasks'][i]['status'] == 'DOING':
                    DOING.append(projects[projectIndex]['tasks'][i]['title'])
                elif projects[projectIndex]['tasks'][i]['status'] == 'DONE':
                    DONE.append(projects[projectIndex]['tasks'][i]['title'])
                elif projects[projectIndex]['tasks'][i]['status'] == 'ARCHIVED':
                    ARCHIVED.append(projects[projectIndex]['tasks'][i]['title'])
                elif projects[projectIndex]['tasks'][i]['status'] == 'BACKLOG':
                    BACKLOG.append(projects[projectIndex]['tasks'][i]['title'])
            lens = [len(TODO), len(DOING), len(DONE), len(ARCHIVED), len(BACKLOG)]
            maxlen = max(lens)
            for i in range(maxlen - len(TODO)):
                TODO.append(' ')
            for i in range(maxlen - len(DOING)):
                DOING.append(' ')
            for i in range(maxlen - len(DONE)):
                DONE.append(' ')
            for i in range(maxlen - len(ARCHIVED)):
                ARCHIVED.append(' ')
            for i in range(maxlen - len(BACKLOG)):
                BACKLOG.append(' ')
            table = Table(title='' + projName + ' tasks')
            table.add_column('TODO', justify='center')
            table.add_column('DOING', justify='center', style='yellow')
            table.add_column('DONE', justify='center', style='red')
            table.add_column('ARCHIVED', justify='center')
            table.add_column('BACKLOG', justify='center')
            for i in range(maxlen):
                table.add_row(TODO[i], DOING[i], DONE[i], ARCHIVED[i], BACKLOG[i])
            console.print(table)
            TODO = []
            DOING = []
            DONE = []
            ARCHIVED = []
            BACKLOG = []
            lens = []
            console.print("\n----------------------------------------------")
        time.sleep(3)
        showLeaderProjects()
        showMemberProjects()
        console.print("Enter the project name that you want to see it\'s tasks", style='magenta')
        console.print('press enter to continue', style='yellow')
        projName = input()
        clear_terminal()

def editProject():
    '''
    edits a project and saves it
    '''
    if len(users[inUser]['leaderOf']) == 0:
        console.print("You have no projects!", style='red bold')
        clear_terminal(1.2)
        return
    showLeaderProjects()
    console.print('Enter the name of the project that you want to edit:', end=' ', style='magenta')
    console.print('press enter to continue', style='yellow')
    editProjName = input()
    clear_terminal()
    if editProjName == '':
        return
    # If editProjName in users[inUser]['leaderOf]
    while True:
        if editProjName in users[inUser]['leaderOf']:
            break
        else:
            console.print('You can only edit the projects that you are the leader of them!', style='red bold')
            clear_terminal(1.5)
            console.print('Enter the name of the project that you want to edit:', end=' ', style='magenta')
            editProjName = input()
    editProjIndex = checkInProjects(editProjName, 'name')
    while editProjIndex == False and str(editProjIndex) != '0':
        console.print('Project not found', style='red bold')
        clear_terminal(1.2)
        showLeaderProjects()
        console.print('Enter the name of the project that you want to edit:', end=' ', style='magenta')
        editProjName = input()
        clear_terminal()
        editProjIndex = checkInProjects(editProjName, 'name')
    table = Table(title=projects[editProjIndex]['name'])
    table.add_column('key', justify='center', style='bold blue')
    table.add_column('value', justify='center')
    table.add_row('id', projects[editProjIndex]['id'])
    table.add_row('name', projects[editProjIndex]['name'])
    table.add_row('leader', projects[editProjIndex]['leader'])
    table.add_row('collaborators', ', '.join(projects[editProjIndex]['collaborators']))
    console.print(table)
    # table.add_row('tasks', projects[editProjIndex]['tasks'])
    # console.print('your projects specifications:', projects[editProjIndex])
    console.print('If you want to add/remove a collaborator, type the name', end=' ', style='magenta')
    console.print('press enter to continue', style='yellow')
    # console.print('collaborators: ', projects[editProjIndex]['collaborators'], end=' ')
    collabEdit = input()
    clear_terminal()
    while collabEdit != '':
        if collabEdit in projects[editProjIndex]['collaborators']:
            if collabEdit == projects[editProjIndex]['leader']:
                console.print('You can not remove the project leader from collaborators!', style='red bold')
                clear_terminal(1.5)
                
            else:
                loggingMessage = users[inUser]['username'] + " removed "+ collabEdit + " from project "+ projects[editProjIndex]['name']
                projects[editProjIndex]['collaborators'].remove(collabEdit)
                users[checkInUsers(collabEdit, 'username')]['memberOf'].remove(projects[editProjIndex]['name'])
                for i in range(len(projects[editProjIndex]['tasks'])):
                    if collabEdit in projects[editProjIndex]['tasks'][i]['assigness']:
                        projects[editProjIndex]['tasks'][i]['assigness'].remove(collabEdit)
                console.print(collabEdit, 'has been successfully removed from this task\'s collaborators', style='green')
                clear_terminal(1.5)
                logger.info(loggingMessage)
        else:
            if checkInUsers(collabEdit, 'username') == False and str(checkInUsers(collabEdit, 'username')) != '0':
                console.print('This username doesn\'t exist! Please enter an existing username', style='red bold')
                clear_terminal(1.5)
            else:
                projects[editProjIndex]['collaborators'].append(collabEdit)
                users[checkInUsers(collabEdit, 'username')]['memberOf'].append(projects[editProjIndex]['name'])
                # debug: console.print('checkIn: ', checkInUsers(collabEdit, 'username'), projects[editProjIndex]['name'], style='blue', end=' ')
                console.print(collabEdit, 'has been successfully added to task\'s collaborators', style='green')
                clear_terminal(1.5)
        table = Table(title=projects[editProjIndex]['name'])
        table.add_column('key', justify='center', style='bold blue')
        table.add_column('value', justify='center')
        table.add_row('id', projects[editProjIndex]['id'])
        table.add_row('name', projects[editProjIndex]['name'])
        table.add_row('leader', projects[editProjIndex]['leader'])
        table.add_row('collaborators', ', '.join(projects[editProjIndex]['collaborators']))
        console.print(table)
        console.print('If you want to add/remove a collaborator, type the name', end=' ', style='magenta')
        console.print('press enter to continue', style='yellow')
        # console.print('collaborators: ', projects[editProjIndex]['collaborators'], end=' ')
        collabEdit = input()
        clear_terminal()
    # console.print(projects, style='blue')
    console.print('Type in anything to add a new task to your project', end=' ', style='magenta')
    console.print('press enter to continue', style='yellow')
    while input() != '':
        clear_terminal()
        projects[editProjIndex]['tasks'].append(newTask(projects[editProjIndex]['collaborators']))
        loggingMessage = users[inUser]['username']+ " added a new task to the project "+ projects[editProjIndex]['name']
        logger.info(loggingMessage)
        filesWrite()
        console.print('Enter anything to add a new task to your project', end=' ', style='magenta')
        console.print('press enter to continue', style='yellow')
    clear_terminal()
    console.print("Project updated!", style="green")
    filesWrite()
    clear_terminal(1.5)
    # console.print('If you want to edit an existing task, type it\'s name', end=' ', style='magenta')
    # console.print('press enter to continue', style='yellow')
    # console.print('Existing tasks: ')
    # for i in projects[editProjIndex]['tasks']:
    #     console.print(i['title'], end=', ')
    # console.print()
    # editTaskFunc(editProjIndex)
# -------------- main code starts from here ---------------------
# -------------- main code starts from here ---------------------
# -------------- main code starts from here ---------------------
# -------------- main code starts from here ---------------------
while True:
    console.print("\t1. Login \n\t2. sign up \n\t3. Enter as manager", style='magenta')
    console.print("press enter to exit", style="yellow")
    signInType = input()
    clear_terminal()
    if signInType == '1':
        
        t = login()
        while not t:
            t = login()
        clear_terminal()
        console.print('Here is your panel', end=' ', style='magenta')
        console.print("press enter to log out", style="yellow")
        console.print('\t1. new project\n\t2. show existing projects and tasks\n\t3. edit your projects / add tasks\n\t4. see/edit a task', style='magenta')
        panelJob = input()
        clear_terminal()
        while panelJob != '':
            if panelJob == '1':
                clear_terminal()
                project = newProject()
                projects.append(project)
                filesWrite()
                logger.info("user created a new project")
            elif panelJob == '2':
                showProjects()
            elif panelJob == '3':
                editProject()
            elif panelJob == '4':
                editAtask()
            else:
                console.print('Please enter 1, 2, 3 or 4', style='red bold')
            clear_terminal()
            console.print('Here is your panel', end=' ', style='magenta')
            console.print("press enter to log out", style="yellow")
            console.print('\t1. new project\n\t2. show existing projects and tasks\n\t3. edit your projects / add tasks\n\t4. see/edit a task', style='magenta')
            panelJob = input()
            clear_terminal()
    elif signInType == '2':
        signUp()
        logger.info("user created a new account")
        # console.print(users)
    elif signInType =="3":
        EnterAsManager()
        logger.info("user entered as manager")
        clear_terminal()
        console.print("Here are active members of this system:", style="magenta")
        table = Table(title="Users")
        table.add_column('user', justify='center', style='blue')
        table.add_column('activity status', justify='center')
        usersManage = []
        for i in users:
            usersManage.append(i['username'])
            if i['isActive']:
                status = 'Active'
            else:
                status = 'Deactive'
            table.add_row(i['username'], status)
        console.print(table)
        console.print("Enter the name of who ever you'd like to active/deactivate:", end="  ", style="magenta")
        console.print("press enter to continue", style="yellow")
        command = input()
        clear_terminal()
        while command != "":
            if usernameCheck(command) == False and str(usernameCheck(command)) != '0':
                console.print('Username doesn\'t exist, please enter another username...', style='red bold')
                clear_terminal(2)
            elif users[usernameCheck(command)]["isActive"] == False:
                users[usernameCheck(command)]["isActive"] = True
                loggingMessage = "user activated "+ command+" as the manager"
                logger.info(loggingMessage)
                filesWrite()
            else:
                users[usernameCheck(command)]["isActive"] = False
                loggingMessage = "user deactivated "+ command+" as the manager"
                logger.info(loggingMessage)
                filesWrite()
            console.print("Here are active members of this system:", style="magenta")
            table = Table(title="Users")
            table.add_column('user', justify='center', style='blue')
            table.add_column('activity status', justify='center')
            for i in users:
                if i['isActive']:
                    status = 'Active'
                else:
                    status = 'Deactive'
                table.add_row(i['username'], status)
            console.print(table)
            console.print("Enter the name of who ever you'd like to deactivate:", end=" ", style="magenta")
            console.print("press enter to continue", style="yellow")
            command=input()
            clear_terminal()
        clear_terminal()
    elif signInType == '':
        break
    else:
        console.print('Please enter 1, 2 or 3', style='red bold')
        clear_terminal(1.5)
        





filesWrite()