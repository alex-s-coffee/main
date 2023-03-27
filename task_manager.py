import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

class Task:
    def __init__(self, username = None, title = None, description = None, due_date = None, assigned_date = None, completed = None):
        '''
        Inputs:
        username: String
        title: String
        description: String
        due_date: DateTime
        assigned_date: DateTime
        completed: Boolean
        '''
        self.username = username
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_date = assigned_date
        self.completed = completed
    
    def from_string(self, task_str):
        '''
        Convert from string in tasks.txt to object
        '''
        tasks = task_str.split(",")
        username = tasks[0]
        title = tasks[1]
        description = tasks[2]
        due_date = datetime.strptime(tasks[3], DATETIME_STRING_FORMAT)
        assigned_date = datetime.strptime(tasks[4], DATETIME_STRING_FORMAT)
        completed = True if tasks[5] == "Yes" else False
        self.__init__(username, title, description, due_date, assigned_date, completed)

        
    def to_string(self):
        '''
        Convert to string for storage in tasks.txt
        '''
        str_attrs = [
            self.username,
            self.title,
            self.description,
            self.due_date.strftime(DATETIME_STRING_FORMAT),
            self.assigned_date.strftime(DATETIME_STRING_FORMAT),
            "Yes" if self.completed else "No"
        ]
        return ",".join(str_attrs)
    
    def display(self):
        '''
        Display object in readable format
        '''
        disp_str = f"Task: \t\t {self.title}\n"
        disp_str += f"Assigned to: \t {self.username}\n"
        disp_str += f"Date Assigned: \t {self.assigned_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {self.due_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {self.description}\n"
        return disp_str

# Functions:

def validate_string(input_str):
    '''
    Function for ensuring that string is safe to store
    '''
    if ";" in input_str:
        print("\nYour input cannot contain a ';' character")
        return False
    return True

def check_username_and_password(username, password):
    '''
    Ensures that usernames and passwords can't break the system
    '''
    # ';' character cannot be in the username or password
    if ";" in username or ";" in password:
        print("\nUsername or password cannot contain ';'.")
        return False
    return True

def write_usernames_to_file(username_dict):
    '''
    Function to write username to file

    Input: dictionary of username-password key-value pairs
    '''
    with open("user.txt", "w") as out_file:
        user_data = []
        for k in username_dict:
            user_data.append(f"{k};{username_dict[k]}")
        out_file.write("\n".join(user_data))

def reg_user():
    """
    Function to register a new user if current user is admin
    It checks for duplicates and only allows unique users
    Saves user-password into the dict as key-value pairs
    Writes to user.txt
    """
    while True:

        if curr_user != 'admin':
            print("Registering new users requires admin privileges")
            break

        new_username = input("New Username: ")
        
        for u in username_password_list.keys():
            if new_username == u:
                print("This username is already taken, please choose a different one\n")
                duplicate_username = True
        
                if duplicate_username:
                    continue
                
        new_password = input("New Password: ")

        if not check_username_and_password(new_username, new_password):
            continue

        confirm_password = input("Confirm Password: ")

        if new_password == confirm_password:
            print("New user added")

            username_password_list[new_username] = new_password
            write_usernames_to_file(username_password_list)
            break

        else:
            print("Passwords do no match")        
            break

def add_task():
    """
    Function to create a new object Task() with correct syntax
    Appends new object to task_list and writes to tasks.txt 
    """
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password_list.keys():
            print("User does not exist. Please enter a valid username")
            continue
        else:
            break

    while True:
        task_title = input("Title of Task: ")
        if validate_string(task_title):
            break
        
    while True:
        task_description = input("Description of Task: ")
        if validate_string(task_description):
            break
    
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = date.today()
        
    new_task = Task(task_username, task_title, task_description, due_date_time,curr_date, False)
    task_list.append(new_task)

    with open("tasks.txt", "w") as task_file:
        task_file.write("\n".join([t.to_string() for t in task_list]))
    print("Task successfully added.")

def view_all():
    """
    Prints all tasks in task_list
    """
    
    print("-----------------------------------") 

    if len(task_list) == 0:
        print("There are no tasks.")
        print("-----------------------------------")

    for t in task_list:
        print(t.display())
        print("-----------------------------------")

def view_mine():
    """
    Prints all tasks assigned to current user
    Allows user to edit some properties of a selected task through modify_task()
    """

    print("-----------------------------------")
    has_task = False
    count_task = 1
    for t in task_list:
        if t.username == curr_user:
            has_task = True
            print(f"Task number {count_task}")
            print(t.display())
            print("-----------------------------------")
        count_task += 1


    if not has_task:
        print("You have no tasks.")
        print("-----------------------------------")


    chosen_task_number = int(input("\nIf you'd like to edit a task select the appropriate number or return to menu by typing '-1': "))
    
    if chosen_task_number == -1:
        print()
    
    else:
        modify_task(chosen_task_number)
        
def modify_task(selected_task_number):
    """
    Allows user to mark task as completed, or change assigned user or due date

    :param selected_task_number: the number of the task we want to edit
    """
    print(f"\nYou have selected task number {selected_task_number} \n")
    print("-----------------------------------")

    action_required = input("""
    Select one of the following options

    edu - edit username
    edd - edit due date
    com - mark task as complete 
    """).lower()
        
    selected_task = task_list[selected_task_number -1]

    if selected_task.completed == True:
        print("\nThis task has been completed and it cannot be edited.")
        print("-----------------------------------")

    elif action_required == 'com':
        selected_task.completed = True 
        print(f"\nThe task number {selected_task_number} has been marked as completed. \nIt can be no longer edited!")
        print("-----------------------------------")
        replace_modified_task(selected_task_number, selected_task)
        
    elif action_required == 'edu':
        while True:
            task_username = input("\nName of the new person assigned to task: ")
            if task_username not in username_password_list.keys():
                print("\nUser does not exist. Please enter a valid username")
                print("-----------------------------------")
                continue
            else:
                selected_task.username = task_username
                print(f"\nTask number {selected_task_number} is now assigned to {task_username}.")
                print("-----------------------------------")
                replace_modified_task(selected_task_number, selected_task)
                break
    
    elif action_required == 'edd':
        while True:
            try:
                task_due_date = input("\nThe new due date of the task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                selected_task.due_date = due_date_time
                print("The due date of this task has been modified.")
                print("-----------------------------------")
                replace_modified_task(selected_task_number, selected_task)
                break

            except ValueError:
                print("\nInvalid datetime format. Please use the format specified")
                print("-----------------------------------") 

def replace_modified_task(line_to_replace, new_replacing_task):
    """
    Updates task_list with the new_replacing_task and writes it on tasks.txt

    :param line_to_replace: indicates the position in task_list and the line in tasks.txt that will be replaced
    :param new_replacing_task: new task that will be written in the appropriate position  
    """

    task_list[line_to_replace -1] = new_replacing_task

    with open('tasks.txt','r',encoding='utf-8') as file:
        data = file.readlines()
    
    data[line_to_replace - 1] = new_replacing_task.to_string() + '\n'

    with open('tasks.txt', 'w', encoding='utf-8') as file:
        file.writelines(data)

def generate_reports():
    """
    Defines and calculates variables needed for the two reports task_overview and user_overview
    Writes all data to task_overview.txt and user_overview.txt
    """
    total_n_tasks = len(task_list)
    n_completed_tasks = len([t for t in task_list if t.completed == True])
    n_uncompleted_tasks = len([t for t in task_list if t.completed == False]) 
    n_overdue_tasks = len([t for t in task_list if t.due_date < datetime.now()]) - n_completed_tasks
    percent_overdue_tasks = round(n_overdue_tasks / total_n_tasks * 100, 2)
    percent_uncompleted_tasks = round(n_uncompleted_tasks / total_n_tasks * 100, 2) 

    task_overview_to_file = f"""
    \t\tTasks overview report:
    -----------------------------------
    Number of tasks:            {total_n_tasks} 
    Completed:                  {n_completed_tasks}
    Uncompleted:                {n_uncompleted_tasks}
    Overdue:                    {n_overdue_tasks}
    Uncompleted /total:         {percent_uncompleted_tasks}%
    Overdue /total:             {percent_overdue_tasks}%
    -----------------------------------
"""

    total_n_users = len(username_password_list)

    user_overview_to_file = f"""
    \t\tUsers overview report:
    -----------------------------------
    Number of users:          {total_n_users}
    Number of tasks:          {total_n_tasks}
    -----------------------------------

    \n\n\t\tBreakdown user by user:
    """


    for user in username_password_list.keys():
        count_tasks = 0
        for t in task_list:
            if t.username == user:
                count_tasks +=1
        
        if count_tasks == 0:
            user_overview_to_file +=f"""
    -----------------------------------
    Tasks for user: {user}
    -----------------------------------
    Assigned to user:          {count_tasks}
    User /total:               {count_tasks}
    Completed:                 {count_tasks}
    Uncompleted:               {count_tasks}
    Overdue:                   {count_tasks}
    """
        else:
            user_overview_to_file +=f"""
    -----------------------------------
    Tasks for user: {user}
    -----------------------------------
    Assigned to user:          {count_tasks}
    User /total:               {round(count_tasks/total_n_tasks *100, 2)} %
    Completed:                 {round(len([task for task in task_list if task.username == user and task.completed == True]) /count_tasks*100, 2)} %
    Uncompleted:               {round(len([task for task in task_list if task.username == user and task.completed == False]) /count_tasks*100, 2)} %
    Overdue:                   {round(len([task for task in task_list if task.username == user and task.completed == False and task.due_date < datetime.now()]) /count_tasks*100, 2)} %
    """
    # Write task_overview.txt and user_overview.txt

    with open("task_overview.txt", 'w') as task_file:
        task_file.write(task_overview_to_file)

    with open("user_overview.txt", 'w') as user_file:
        user_file.write(user_overview_to_file)
    
    print("\nUser_overview and task_overview reports have been generated.")
    print("-----------------------------------")


# Read and parse tasks.txt
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = Task()
    curr_t.from_string(t_str)
    task_list.append(curr_t)

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin, password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password_list = {}
for user in user_data:
    username, password = user.split(';')
    username_password_list[username] = password


# Keep trying until a successful login
logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password_list.keys():
        print("\nUser does not exist")
        continue
    elif username_password_list[curr_user] != curr_pass:
        print("\nWrong password")
        continue
    else:
        print("\nLogin Successful!")
        logged_in = True

#########################
# Main Program
######################### 

while True:
    # Get input from user
    if curr_user == 'admin':
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my tasks
    gr - generate reports
    ds - display statistics
    e - Exit
    : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    e - Exit
    : ''').lower()
# Register new user (if admin)
    if menu == 'r':     
        reg_user()
# adding a new task
    elif menu == 'a': 
        add_task()
# View all tasks       
    elif menu == 'va':       
        view_all()
# View my tasks
    elif menu == 'vm':    
       view_mine()
# Generate reports regarding users and tasks
    elif menu == 'gr' and curr_user == 'admin': 
        generate_reports()
        
        
# If admin, display statistics       
    elif menu == 'ds' and curr_user == 'admin': 
        if not os.path.exists("task_overview.txt"):
            with open("task_overview.txt", "w") as default_file:
                pass

        if not os.path.exists("user_overview.txt"):
            with open("user_overview.txt", "w") as default_file:
                pass

        with open("task_overview.txt", 'r') as task_file:
            task_overview = task_file.read()
            print(task_overview+"\n\n")

        with open("user_overview.txt", 'r') as user_file:
            user_overview = user_file.read()
            print(user_overview)
# Exit program
    elif menu == 'e': 
        print('Goodbye!!!')
        exit()
# Default case
    else: 
        print("You have made a wrong choice, Please Try again")

    
    """
This programme adds functionality to the already existing task_manager. 
I have refactored the code and isolated the 4 functions that were requested in the task. 
view_mine() now allows the user to edit their own tasks, thanks to the function modify_task().
The function modify_task() edits username, due_date or completed. 
I have created the function replace_modified_task() to then replace the modified_tasks in task_list, my working variable, and in tasks.txt
Finally the function generate_reports calculates statistics about users and tasks and writes them into user_overview and tasks_overview.
The admin can display the reports from the txt files through ds - display statistics. 
"""