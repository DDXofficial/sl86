import os

# parselbox current release

# CODE GRABS APP AND MACHINE PATHS FROM TEXT FILES
with open("app.txt","r") as file:
    app_path = file.read()
    file.close()

with open("machines.txt","r") as file:
    machine_path = file.read()
    file.close()

# CLEAN STATE
os.system("clear")

# BASIC DIRECTORY LISTING (APP & MACHINE)
app_dir = os.listdir(app_path)
machine_dir = os.listdir(machine_path)

# EMPTY MACHINE LIST
machines = []

# MACHINE QUANTITY
machines_count = len(next(os.walk(machine_path))[1])

# IMPORTING MACHINE NAMES TO 'machines' LIST
def machine_list_load():
    for file in machine_dir:
        machines_list = os.path.join(machine_path, file)
        if os.path.isdir(machines_list):
            machines.append(file)

# OUTPUT STARTS HERE.
print("parselbox: A text-mode 86Box machine manager for macOS, written in Python")
print("Author: Segev A. (DDX) - contact@ddxofficial.com\n")

# VIEW APP AND MACHINE PATHS
print("To set app and machine paths, edit the 'app.txt' and 'machines.txt' files respectively.")
print("")
print("86Box path:", app_path)
print("86Box machine path:", machine_path, "\n")

while True: 
    # MAIN MENU
    print("### MAIN MENU ###")
    print("")
    print("1. List machines")
    print("2. Start machine")
    print("3. Create new machine [DO NOT USE - WIP]")
    print("4. Configure machine")
    print("5. Exit")
    print("")

    main_menu_selection = int(input("Select option: "))

    print("")

    if main_menu_selection == 1:
        os.system("clear")
        print("[1] List machines")
        print("")
        # MACHINE LISTING
        machine_list_load()
        print("Machines detected in directory:", machines_count)
        for i in range(machines_count):
            print(i + 1, "-", machines[i])
        print("")

    elif main_menu_selection == 2:
        os.system("clear")
        print("[2] Start machine")
        print("")
        # MACHINE LISTING
        machine_list_load()
        print("Machines detected in directory:", machines_count)
        for i in range(machines_count):
            print(i + 1, "-", machines[i])
        print("")

        # MACHINE CHOICE
        machine_id_input = input("Which machine would you like to start? (select number) ")
        s_machine_id = int(machine_id_input) - 1

        # MACHINE EXECUTION BASED ON USER CHOICE
        print("\nStarting machine " + machine_id_input + " (" + machines[s_machine_id] + ")\n")
        os.system(app_path + "/86Box.app/Contents/MacOS/86Box -P " + "\"" + machine_path + "/" + machines[s_machine_id] + "\"")

    elif main_menu_selection == 3:
        os.system("clear")
        print("[3] Create new machine")
        print("")
        while True:
            new_machine_input = input("Please choose a name for the new machine: ")
            print("")
            print("Machine name:", new_machine_input)
            machine_name_decision = input("Is this correct? (Y/N) ")
            if machine_name_decision == "Y" or "y":
                os.system("mkdir " + machine_path + "/" + "\"" + new_machine_input + "\"")
                break
            elif machine_name_decision == "N" or "n":
                continue
            else:
                print("Invalid input - please try again.")
                print("")
    
    elif main_menu_selection == 4:
        os.system("clear")
        print("[4] Configure machine")
        print("")
        # MACHINE LISTING
        print("Machines detected in directory:", machines_count)
        for i in range(machines_count):
            print(i + 1, "-", machines[i])
        print("")

        # MACHINE CHOICE
        machine_id_input = input("Which machine would you like to configure? (select number) ")
        s_machine_id = int(machine_id_input) - 1

        # MACHINE EXECUTION BASED ON USER CHOICE
        print("\nConfiguring machine " + machine_id_input + " (" + machines[s_machine_id] + ")\n")
        os.system(app_path + "/86Box.app/Contents/MacOS/86Box -S -P " + "\"" + machine_path + "/" + machines[s_machine_id] + "\"")

    elif main_menu_selection == 5:
        print("Thank you for using parselbox!")
        break
    
    else:
        print("Incorrect value - please try again.")
        print("")
        continue