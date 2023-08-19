import os
import platform
import configparser as cp

# sl86 current release, now adapted for Linux
# (thanks Bruninho and SilverMoon for handling macOS for me!!)
# https://github.com/brunocastello/Swift86
# https://github.com/Moonif/MacBox

# PLATFORM-AGNOSTIC SCREEN CLEARING METHOD
def clear_screen():
    if platform.system() == 'Windows':
        os.system("cls")
    elif platform.system() == 'Darwin' or platform.system() == 'Linux':
        os.system("clear")

# CLEAN STATE
clear_screen()

# VERSION
launcher_version = str("0.1")

# INTRO OUTPUT
print("         ______  _____")
print("   _____/ ( __ )/ ___/   snakelauncher86 (sl86) - Version", launcher_version)
print("  / ___/ / __  / __ \ 	A text-mode 86Box machine manager written in Python")
print(" (__  ) / /_/ / /_/ / 	Author: Segev A. (DDX) - contact@ddxofficial.com")
print("/____/_/\____/\____/  	Source code: https://github.com/ddxofficial/sl86")
print("")

# CONFIGPARSER: READS DATA FROM launcher.cfg
config = cp.ConfigParser()
config.read(r'launcher.cfg')
app_path = config.get('launcher', 'app')
machine_path = config.get('launcher', 'machines')

# MACHINE LIST
machine_dir = os.listdir(machine_path)

# EMPTY MACHINES LIST VARIABLE
machines = []

# MACHINE QUANTITY
machines_count = len(next(os.walk(machine_path))[1])

# IMPORTING MACHINE NAMES TO 'machines' LIST
def machine_list_load():
    for file in machine_dir:
        machines_list = os.path.join(machine_path, file)
        if os.path.isdir(machines_list):
            machines.append(file)

# JUST SO I DON'T COPY HUGE CHUNKS OF CODE EVERY TIME:
def quit_text():
    print("Thank you for using sl86!")
    print("")
    print("snakelauncher86 (sl86) - Version", launcher_version)
    print("https://github.com/ddxofficial/sl86")

def path_text():
    print("86Box path:", app_path)
    print("86Box machine path:", machine_path, "\n")

# VIEW APP AND MACHINE PATHS
print("To set app and machine paths, edit the 'launcher.cfg' file.")
print("Ensure that the 'app' path points to the actual executable instead of its path.")
print("")
path_text()

# INSTRUCTIONS (i suck at python rn leave me alone)
print("To create a machine, create a folder inside the designated 'machines' folder")
print("and relaunch the script.\n")
print("NOTE: Any machines/folders created while this script is active will not be")
print("detected and you will need to relaunch the script for them to appear.")
print("This will be worked on in future releases.")
print("")

while True:
    # MACHINE LISTING
    machine_list_load()
    print("Machines detected in directory:", machines_count)
    for i in range(machines_count):
        print(i + 1, "-", machines[i])
    print("")

    # MACHINE CHOICE
    machine_id_input = input("Select a machine (number - enter 0 to quit): ")
    selected_machine_id = int(machine_id_input) - 1

    # EARLY EXIT
    if int(machine_id_input) == 0:
        clear_screen()
        print("")
        quit_text()
        print("")
        break

    # LAUNCH, CONFIGURE, RETURN, QUIT?
    print("")
    print("Machine selected: " + machine_id_input + " (" + machines[selected_machine_id] + ")")
    machine_decision_input = input("[L]aunch / [C]onfigure / [R]eturn to machine list / [Q]uit launcher? ")

    if machine_decision_input == 'L' or machine_decision_input == 'l':
        # MACHINE EXECUTION BASED ON USER CHOICE
        print("\nMachine " + machine_id_input + " (" + machines[selected_machine_id] + ") selected for launch.\n")
        print("Starting 86Box...")
        os.system(app_path + " -P " + "\"" + machine_path + "/" + machines[selected_machine_id] + "\"")
    elif machine_decision_input == 'C' or machine_decision_input == 'c':
        # MACHINE CONFIGURATION BASED ON USER CHOICE
        print("\nMachine " + machine_id_input + " (" + machines[selected_machine_id] + ") selected for configuration.\n")
        print("Starting 86Box...")
        print(os.system(app_path + " -S " + "\"" + machine_path + "/" + machines[selected_machine_id] + "/86box.cfg" + "\""))
    elif machine_decision_input == 'R' or machine_decision_input == 'r':
        clear_screen()
        print("")
        path_text()
        continue
    elif machine_decision_input == 'Q' or machine_decision_input == 'q':
        clear_screen()
        print("")
        quit_text()
        print("")
        break
    else:
        print("Invalid input - try again")

    clear_screen()
    print("")
    path_text()