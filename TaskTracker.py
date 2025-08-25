from datetime import datetime
import json
import os

class Config: #Default configuration
    task_path = 'Tasks.json'
    help = '\nCommand List :\n' \
    'add            -> add tasks to track\n' \
    'del            -> delete task from the list\n' \
    'delall         -> delete all task in the list\n' \
    'edit           -> edit tasks from the list\n' \
    'mark-done      -> mark your task done\n' \
    'mark-doing     -> mark your task ongoing\n' \
    'list [status]  -> list tasks (status: pending, done, doing)\n' \
    'break          -> end this program\n'
    now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    valid_statuses = ['pending', 'done', 'doing']

    if not os.path.exists(task_path): #Add Tasks.JSON when not already available
        with open(task_path, 'w') as f:
            json.dump({"Tasks": []},f,indent=2)


class Main:
    def get_task_id(): #ID for new task
        with open(Config.task_path, 'r') as f:
            data = json.load(f)
        task_id = len(data["Tasks"])
        return task_id
    

    def add(task, description): #Add new task and description
        json_task = {
        "Id": Main.get_task_id(),
        "Task": task,
        "Status": "Pending",
        "Description": description,
        "CreatedAt": Config.now,
        "EditedAt": Config.now
        }

        with open(Config.task_path, 'r') as f:
            data = json.load(f)
        data["Tasks"].append(json_task)
        with open(Config.task_path, 'w') as f:
            json.dump(data, f, indent=2)
        return json_task["Id"]
    
    
    def delete(delete_id): #Delete task per ID
        with open(Config.task_path, 'r') as f:    
            data = json.load(f)

        index = delete_id
        if 0 <= index < len(data["Tasks"]): #Check if ID is inside length
            data["Tasks"].pop(index)
        else:
            return f"Task ID {delete_id} not found."
        
        for i, task in enumerate(data["Tasks"]): #re-ID the tasks to fill lowest number
            task["Id"] = i
        
        with open(Config.task_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        delete_check = True
        deleted_output = "Deleted!\n" + Main.list(None, delete_check)
        return deleted_output
    
    
    def delall(): #Delete all task with confirmation
        confirm = input('Are you sure? (Y/N): ')
        if confirm.lower() == 'y':
            with open(Config.task_path, 'r') as f:
                data = json.load(f)
            data["Tasks"] = []
            with open(Config.task_path, 'w') as f:
                json.dump(data, f)
            return "All tasks has been cleared!"
        elif confirm.lower() == 'n':
            return "Your task was not cleared!"
        else:
            return "Invalid answer."
        

    def edit(task_id): #Edit file name and description
        with open(Config.task_path, 'r') as f:
            data = json.load(f)
        
        found = False
        for task in data["Tasks"]: #Find the correct task by the ID
            if task["Id"] == int(task_id):
                found = True
                new_name = input(f'Enter a new task name (current: {task["Task"]}): ')
                task["Task"] = new_name
                new_description = input(f'Enter new task description (current: {task["Description"]}): ')
                task["Description"] = new_description
                task["EditedAt"] = Config.now
                break

        if not found:
            return f'Task ID {task_id} not found.'
        
        with open(Config.task_path, 'w') as f:
            json.dump(data, f, indent=2)

        return f'Task {task_id} has been updated!'
    

    def mark_done(task_id): #Mark task as done
        with open(Config.task_path, 'r') as f:
            data = json.load(f)
        
        found = False
        for task in data["Tasks"]:
            if task["Id"] == int(task_id):
                found = True
                if task["Status"] == "Done":
                    return 'Task is already marked "done"!'
                else:
                    task["Status"] = "Done"
                break
        
        if not found:
            return f'Task ID {task_id} not found.'
        
        with open(Config.task_path, 'w') as f:
            json.dump(data, f, indent=2)

        return f'Task {task_id} has been marked done!'
    

    def mark_doing(task_id): #Mark task as doing
        with open(Config.task_path, 'r') as f:
            data = json.load(f)
        
        found = False
        for task in data["Tasks"]:
            if task["Id"] == int(task_id):
                found = True
                if task["Status"] == "Doing":
                    return 'Task is already marked "Doing"!'
                else:
                    task["Status"] = "Doing"
                break
        
        if not found:
            return f'Task ID {task_id} not found.'
        
        with open(Config.task_path, 'w') as f:
            json.dump(data, f, indent=2)

        return f'Task {task_id} has been marked doing!'
        
        
    def list(status_filter=None,delete_check=False): #List with args filter and different message when deletion
        with open(Config.task_path, 'r') as f:
            data = json.load(f)

        def task_list(): 
            tasks = data["Tasks"]
            if not tasks:
                return "Yout task list is empty!"
            
            lines = ['ID | Task | Status | Description', '-'*50]

            for task in tasks: #Check if theres a filter
                if status_filter is not None and task["Status"].lower() != str(status_filter).lower():
                    continue
                lines.append(f'{task["Id"]} | {task["Task"]} | {task["Status"]} | {task["Description"]}')
            
            if status_filter and len(lines) == 2: #Check if theres any tasks in filtered list
                return f'No task with status {status_filter}'
            
            return "\n".join(lines)

        if delete_check:
            return 'Here is your updated task list!\n' + task_list()
        else:
            return task_list()
        
    
    def action(command_input): #All command config
        parts = command_input.strip().split()
        if not parts:
            return 'No command inputted.'
        
        commands = parts[0]
        args = parts[1:]

        task_list = Main.list()

        if commands == 'help':
            return Config.help
        
        elif commands == 'add':
            task_input = input('Add a task: ')
            task_description = input('Add an optional description: ')
            task_id = Main.add(task_input, task_description)
            return f'"{task_input}" has been added to your task list! (ID:{task_id})'
        
        elif commands == 'del':
            delete_id = int(input(f'{task_list}\nEnter Task ID to delete: '))
            return Main.delete(delete_id)
        
        elif commands == 'delall':
            return Main.delall()
        
        elif commands == 'edit':
            input_id = input(f'{task_list}\nEnter Task ID to edit: ')
            return Main.edit(input_id)
        
        elif commands == 'mark-done':
            input_id = input(f'{task_list}\nEnter Task ID to mark done: ')
            return Main.mark_done(input_id)
        
        elif commands == 'mark-doing':  
            input_id = input(f'{task_list}\nEnter Task ID to mark doing: ')
            return Main.mark_doing(input_id)
        
        elif commands == 'list':
            if args:
                status = args[0].lower()
                if status in Config.valid_statuses:
                    return Main.list(status_filter = status.capitalize())
                else:
                    return f'Unknown status: {args}. Valid statuses: {", ".join(Config.valid_statuses)}'
            else:
                return Main.list()

        elif commands == 'break':
            return 'exit'
        
        else:
            return f'Unknown command: {commands}'
        

class RunCLI: #Run the program
    print('Welcome to Task Tracker CLI by Prince14!\nType "help" for more Information.')

    while True:
        user_input = input("> ")
        output = Main.action(user_input)
        if output == 'exit':
            print('Exiting Program!')
            break
        else:
            print(output)
