import json

class Main:

    task_path = 'Tasks.json'
    help = '\nCommand List :\n' \
    'add            -> add tasks to track.\n' \
    'del            -> delete task from the list.\n' \
    'delall         -> delete all task in the list.\n' \
    'edit           -> edit tasks from the list.\n' \
    'mark-done      -> mark your task done.\n' \
    'mark-doing     -> mark your task ongoing.\n' \
    'list           -> list of all your tasks.\n' \
    'break          -> end this program.\n' \
    
    
    def get_task_id():
        with open(Main.task_path, 'r') as f:
            data = json.load(f)
        task_id = len(data["Tasks"])
        return task_id
    

    def add(task, description):                
        json_task = {
        "Id": Main.get_task_id(),
        "Task": task,
        "Status": "pending",
        "Description": description
        }

        with open(Main.task_path, 'r') as f:
            data = json.load(f)
        data["Tasks"].append(json_task)
        with open(Main.task_path, 'w') as f:
            json.dump(data, f, indent=2)
        return json_task["Id"]
    
    
    def delete(delete_id):
        with open(Main.task_path, 'r') as f:    
            data = json.load(f)

        index = delete_id
        if 0 <= index < len(data["Tasks"]):
            data["Tasks"].pop(index)
        else:
            return f"Task ID {delete_id} not found."
        
        for i, task in enumerate(data["Tasks"]):
            task["Id"] = i
        
        with open(Main.task_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        delete_check = True
        deleted_output = "Deleted!\n" + Main.list(delete_check)
        return deleted_output
    
    
    def delall():
        confirm = input('Are you sure? (Y/N): ')
        if confirm.lower() == 'y':
            with open(Main.task_path, 'r') as f:
                data = json.load(f)
            data["Tasks"] = []
            with open(Main.task_path, 'w') as f:
                json.dump(data, f)
            return "All tasks has been cleared!"
        elif confirm.lower() == 'n':
            return "Your task was not cleared!"
        else:
            return "Invalid answer."
        

    def edit(task_id):
        with open(Main.task_path, 'r') as f:
            data = json.load(f)
        
        found = False
        for task in data["Tasks"]:
            if task["Id"] == int(task_id):
                found = True
                print(f'Task: {task["Task"]}\nDescription: {task["Description"]}')
                new_name = input('Enter a new task name: ')
                task["Task"] = new_name
                new_description = input('Enter new task description: ')
                task["Description"] = new_description
                break

        if not found:
            return f'Task ID {task_id} not found.'
        
        with open(Main.task_path, 'w') as f:
            json.dump(data, f, indent=2)

        return f'Task {task_id} has been updated!'
        
        
    def list(delete_check=False):
        with open(Main.task_path, 'r') as f:
            data = json.load(f)

        def task_list():
            tasks = data["Tasks"]
            if not tasks:
                return "Yout task list is empty!"
            lines = ['ID | Task | Status | Description', '-'*50]
            for task in tasks:
                if task["Status"]:
                    status = 'Done'
                else:
                    status = 'Pending'
                lines.append(f'{task["Id"]} | {task["Task"]} | {status} | {task["Description"]}')
            return "\n".join(lines)

        if delete_check:
            return 'Here is your updated task list!\n' + task_list()
        else:
            return task_list()
        
    
    def action(commands):
        task_list = Main.list()

        if commands == 'help':
            return Main.help
        
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
        
        elif commands == 'list':
            return Main.list()

        elif commands == 'break':
            return 'exit'
        
        
print('Welcome to Task Tracker CLI by Prince14!\nType "help" for more Information.')
while True:
    user_input = input("> ")
    output = Main.action(user_input)
    if output == 'exit':
        print('Exiting Program!')
        break
    else:
        print(output)