import os
import platform
import shutil
import subprocess
import configparser as cp

# PLATFORM-AGNOSTIC SCREEN CLEARING METHOD
def clear_screen():
    if platform.system() == 'Windows':
        os.system("cls")
    elif platform.system() == 'Darwin' or platform.system() == 'Linux':
        os.system("clear")

# CLEAN STATE
clear_screen()

# VERSION
launcher_version = str("0.4")

# INTRO OUTPUT
print("         ______  _____")
print("   _____/ ( __ )/ ___/  snakelauncher86 (sl86) - Version", launcher_version)
print("  / ___/ / __  / __ \ 	A text-mode 86Box machine manager written in Python")
print(" (__  ) / /_/ / /_/ / 	Author: Segev A. (DDX) - ddxofficial@outlook.com")
print("/____/_/\____/\____/  	Source code: https://github.com/ddxofficial/sl86")
print("")

# ERROR HANDLING (EXIT)
def error_quit_text():
    print("Exiting.")
    print("")
    quit()

# CONFIGPARSER (init)
config = cp.ConfigParser()

# LAUNCHER FILES CHECK
default_launcher_path = "launcher.cfg"
default_launcher_template_path = os.path.join("templates", "launcher.cfg")

launcher_check = os.path.exists(default_launcher_path)
launcher_template_check = os.path.exists(default_launcher_template_path)

print("Checking for launcher config file...")
if launcher_template_check is True:
    if launcher_check is False:
        print("WARNING: Launcher config file does not exist.")
        print("Copying from template folder...")
        shutil.copyfile(default_launcher_template_path, default_launcher_path)
        print("")
        print("Default launcher config file copied successfully.")
        print("Please specify the app and machine paths and then launch again.")
        print("")
        quit()
    elif launcher_check is True:
        print("Launcher config file found.")
        print("")
    else:
        # /!\ ERROR 0: NO LAUNCHER TEMPLATE FOUND
        print("ERROR: Launcher template file not found.")
        print("Ensure you have downloaded all files and try again.")
        error_quit_text()

# CONFIGPARSER (read from launcher.cfg)
config.read(r'launcher.cfg')
app_path = config.get('launcher', 'app')
machine_path = config.get('launcher', 'machines')

# /!\ ERROR 1: NO PATHS SET (CHANGEME)
if app_path and machine_path == "CHANGEME":
    print("ERROR: Paths not set in launcher.cfg.")
    print("Please specify correct paths for the 86Box executable and machines.")
    print("Instructions can be found in the launcher config file.")
    error_quit_text()

# /!\ ERROR 1.1A: INVALID PATH (86BOX)
if os.path.exists(app_path) is False:
    print("ERROR: Executable", app_path, "not found.")
    print("Please check your config file for errors.")
    error_quit_text()

# /!\ ERROR 1.1B: INVALID PATH (MACHINES)
if os.path.isdir(machine_path) is False:
    print("ERROR: Directory", machine_path, "not found.")
    print("Please check your config file for errors.")
    error_quit_text()

# MACHINE LIST
machine_dir = os.listdir(machine_path)

# EMPTY MACHINES LIST VARIABLE
machines = []

# MACHINE QUANTITY
machines_count = len(next(os.walk(machine_path))[1])

# /!\ ERROR 2: NO MACHINES FOUND
if machines_count == 0:
    print("ERROR: No machines found in", machine_path + ".")
    print("Please specify a path to a directory that contains machine files.")
    error_quit_text()

# IMPORTING MACHINE NAMES TO 'machines' LIST
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

def path_86box_text():
    print("86Box path:")
    print("-->", app_path)

def path_machine_text():
    print("86Box machine path:")
    print("-->", machine_path, "\n")

def info_86box():
    print("86Box executable information (logfile extraction):")
    print("")
    subprocess.run([app_path, "-Y"])
    print("")

# VIEW APP AND MACHINE PATHS
path_86box_text()
print("")
path_machine_text()
info_86box()

# INSTRUCTIONS (i STILL suck at python rn leave me alone)
print("To create a machine, create a folder inside the designated 'machines' folder")
print("and relaunch the script.\n")
print("NOTE: Any machines/folders created while this script is active will not be")
print("detected and you will need to relaunch the script for them to appear.")
print("This will be worked on in future releases.")
print("")

while True:
    # MACHINE LISTING
    machines.sort(key=str.lower)
    print("Machines detected in directory:", machines_count, "\n")
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
        subprocess.run([app_path, "-P", f"{machine_path}/{machines[selected_machine_id]}"])
    elif machine_decision_input == 'C' or machine_decision_input == 'c':
        # MACHINE CONFIGURATION BASED ON USER CHOICE
        print("\nMachine " + machine_id_input + " (" + machines[selected_machine_id] + ") selected for configuration.\n")
        print("Starting 86Box...")
        subprocess.run([app_path, "-S", f"{machine_path}/{machines[selected_machine_id]}/86box.cfg"])
    elif machine_decision_input == 'R' or machine_decision_input == 'r':
        clear_screen()
        print("")
        path_86box_text()
        path_machine_text()
        continue
    elif machine_decision_input == 'Q' or machine_decision_input == 'q':
        clear_screen()
        print("")
        quit_text()
        print("")
        break
    else:
        print("Invalid input - try again.")

    clear_screen()
    print("")
    path_86box_text()
    path_machine_text()
