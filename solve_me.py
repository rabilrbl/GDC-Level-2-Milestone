class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics"""
        )

    def add(self, args):
        self.read_current()
        if len(args) < 2:
            print("Error: Missing tasks string. Nothing added!")
            return
        priority = int(args[0])
        name = " ".join(args[1:])
        if priority in self.current_items.keys():
            newPriority  = priority+1
            while newPriority in self.current_items.keys():
                newPriority += 1
            self.current_items[newPriority] = self.current_items.get(priority)
        self.current_items[priority] = name
        self.write_current()
        print(f"Added task: \"{name}\" with priority {priority}",end="")
            

    def done(self, args):
        if len(args) < 1:
            print("Error: Missing priority number. Nothing done!")
            return
        priority = int(args[0])
        if priority in self.current_items.keys():
            self.completed_items.append(self.current_items.get(priority))
            del self.current_items[priority]
            self.write_current()
            self.write_completed()
            print("Marked item as done.")
        else:
            print(f"Error: no incomplete item with priority {priority} exists.",end="")

    def delete(self, args):
        if len(args) < 1:
            print("Error: Missing priority number. Nothing deleted!")
            return
        priority = int(args[0])
        if priority in self.current_items.keys():
            del self.current_items[priority]
            self.write_current()
            print(f"Deleted item with priority {priority}.")
        else:
            print(f"Error: item with priority {args[0]} does not exist. Nothing deleted.")

    def ls(self):
        if len(self.current_items) == 0:
            print("No items in the list!")
            return
        for index,key in enumerate(sorted(self.current_items.keys()),1):
            print(f"{index}. {self.current_items[key]} [{key}]")

    def report(self):
        if len(self.current_items) == 0:
            print("No items in the list!")
            return
        print(f"Pending : {len(self.current_items)}")
        for index,key in enumerate(sorted(self.current_items.keys()),1):
            print(f"{index}. {self.current_items[key]} [{key}]")
        print(f"\nCompleted : {len(self.completed_items)}")
        for index,item in enumerate(self.completed_items,1):
            print(f"{index}. {item}")
