import json

class Main:

    task_path = 'Tasks.json'
    help = '\nCommand List :\n' \
    'add    -> add tasks to the tracker.\n' \
    'update -> update tasks from the tracker.\n' \
    'mark   -> mark your task done.\n' \
    'list   -> list of all your tasks.\n' \
    'break  -> end this program.\n' \
    
    def add(task):
        json_task = {
        "Task": task,
        "Status": False
        }

        with open(Main.task_path, 'r') as f:
            data = json.load(f)
        data["Tasks"].append(json_task)
        with open(Main.task_path, 'w') as f:
            json.dump(data, f, indent=2)
        task_id = len(data["Tasks"])
        return task_id
    
    def action(commands):
        if commands == 'help':
            return Main.help
        elif commands == 'add':
            task_input = input('Add Your Task: ')
            task_id = Main.add(task_input)
            return f'"{task_input}" has been added to your task list! (ID:{task_id})'
        elif commands == 'break':
            return 'exit'
        
print('> Welcome to Task Tracker CLI by Prince14!\n> Type "help" for more Informations')
while True:
    user_input = input("> ")
    output = Main.action(user_input)
    if output == 'exit':
        print('Exiting Program!')
        break
    else:
        print(output)