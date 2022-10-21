import os

# parselBox pre-release 2022-10-21

# IMPORTANT: SET THIS BEFORE USING
app_path = "/Users/ddx/86Box-2-py"
machine_path = "/Users/ddx/86Box-2-py/machines"

# CLEAN STATE
os.system("clear")

# BASIC DIRECTORY LISTING (APP & MACHINE)
app_dir = os.listdir(app_path)
machine_dir = os.listdir(machine_path)

# EMPTY MACHINE ARRAY
machines = []

# MACHINE QUANTITY
machines_count = len(next(os.walk(machine_path))[1])

# IMPORTING MACHINE NAMES TO 'machines' LIST
for file in machine_dir:
    machines_list = os.path.join(machine_path, file)
    if os.path.isdir(machines_list):
        machines.append(file)

# OUTPUT STARTS HERE.
print("P A R S E L B O X - VERSION [who cares]")
print("A text-mode 86Box machine manager written in Python")
print("Author: Segev A. (DDX) - contact@ddxofficial.com\n")

# PLANNED MAIN MENU:
# 1. Launch machine
# 2. Create machine
# 3. Configure machine
# 4. Set app path
# 5. Set machine path
# 6. Exit

# VIEW APP AND MACHINE 
print("86Box path:", app_path)
print("86Box machine path:", machine_path, "\n")

# MACHINE LISTING
print("Machines detected in directory:", machines_count)
for i in range(machines_count):
    print(i + 1, "-", machines[i])

# MACHINE CHOICE
print("")
machine_id_input = input("Which machine would you like to start? (select number) ")
s_machine_id = int(machine_id_input) - 1

# MACHINE EXECUTION BASED ON USER CHOICE
print("\nStarting machine " + machine_id_input + " (" + machines[s_machine_id] + ")\n")
os.system(app_path + "/86Box.app/Contents/MacOS/86Box -P " + machine_path + "/" + machines[s_machine_id])

