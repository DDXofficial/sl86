import os
import platform
import configparser as cp
import sys

# sl86 current release, now adapted for Linux
# (thanks SilverMoon for handling macOS for me!!)
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
launcher_version = str("0.1a")

# INTRO OUTPUT
print("         ______  _____")
print("   _____/ ( __ )/ ___/  snakelauncher86 (sl86) - Version", launcher_version)
print("  / ___/ / __  / __ \ 	A text-mode 86Box machine manager written in Python")
print(" (__  ) / /_/ / /_/ / 	Author: Segev A. (DDX) - ddxofficial@outlook.com")
print("/____/_/\____/\____/  	Source code: https://github.com/ddxofficial/sl86")
print("                  	Contributor: Alex. (CypherNebula84) - CypherNebula84@outlook.com")
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
    machine_id_input = input("Select a machine (number), create a new one with 'c', or enter 0 to quit: ")

    if machine_id_input.lower() == 'c':
        # Logic for creating a new machine
        new_machine_name = input("Enter a name for the new machine: ")
        new_machine_path = os.path.join(machine_path, new_machine_name)

        # Check if the folder already exists
        if os.path.exists(new_machine_path):
            print(f"Machine '{new_machine_name}' already exists. Please choose a different name.")
        else:
            # Create a new folder for the machine
            os.makedirs(new_machine_path)
            print(f"New machine '{new_machine_name}' created in '{machine_path}'!")

            # Ask if the user wants to configure the new machine
            configure_new_machine = input("Do you want to configure this new machine? (y/n): ").lower()

            if configure_new_machine == 'y':
                # Configure the new machine
                print("Starting 86Box for configuration...")
                os.system(app_path + f" -S \"{machine_path}/{new_machine_name}/86box.cfg\"")

            # Reload the script to detect the new machine
            print("Reloading the script...")
            script_path = os.path.abspath(__file__)
            os.execv(sys.executable, [sys.executable, script_path])

        continue

    selected_machine_id = int(machine_id_input) - 1

    # EARLY EXIT
    if selected_machine_id == -1:
        clear_screen()
        print("")
        quit_text()
        print("")
        break

    # LAUNCH, CONFIGURE, RETURN, QUIT?
    print("")
    print("Machine selected:", machine_id_input, "(", machines[selected_machine_id], ")")
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
        os.system(app_path + " -S " + "\"" + machine_path + "/" + machines[selected_machine_id] + "/86box.cfg" + "\"")
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