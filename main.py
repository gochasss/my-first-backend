

def load_tasks():
    tasks = []
    try:
        with open("tasks.txt", "r") as file:
            for line in file:
                tasks.append(line.strip())
    except:
        pass
    return tasks


def save_task(task):
    with open("tasks.txt", "a") as file:
        file.write(task + "\n")


def show_tasks(tasks):
    print("Your tasks:")
    for t in tasks:
        print("-", t)


def main():
    user = {}
    tasks = load_tasks()

    print("Personal Assistant")
    print("Commands: setname, info, time, addtask, showtasks, exit")

    while True:
        command = input("> ")

        if command == "setname":
            name = input("Your name: ")
            user["name"] = name
            print("Saved.")

        elif command == "time":
            print("It's always time for tea ☕")

        elif command == "info":
            if "name" in user:
                print("Your name is", user["name"])
            else:
                print("I don't know your name yet.")

        elif command == "addtask":
            task = input("New task: ")
            tasks.append(task)
            save_task(task)
            print("Task added.")

        elif command == "showtasks":
            show_tasks(tasks)

        elif command == "exit":
            print("Goodbye 👋")
            break

        else:
            print("Unknown command")


main()



