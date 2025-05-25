#!/bin/python3
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
launcher_version = str("0.6-beta")

# INTRO OUTPUT
def sl86_header():
    print("         ______  _____")
    print("   _____/ ( __ )/ ___/  snakelauncher86 (sl86) - Version", launcher_version)
    print("  / ___/ / __  / __ \ 	A text-mode 86Box machine manager written in Python")
    print(" (__  ) / /_/ / /_/ / 	Author: Segev A. (DDX) - ddxofficial@outlook.com")
    print("/____/_/\____/\____/  	Source code: https://github.com/DDXofficial/sl86")
    print("")
    print("Esteemed contributors: Zack13358")
    print("")

sl86_header()

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

# RECREATE 'machines' LIST to detect newly created machines
def refresh_machine_list():
    global machine_dir
    machine_dir = os.listdir(machine_path)

    global machines
    machines = []

    global machines_count
    machines_count = len(next(os.walk(machine_path))[1])

    # CREATE A MACHINE IF NONE ARE FOUND
    if machines_count == 0:
        print("ERROR: No machines found in", machine_path + ".")
        machine_create()
    for file in machine_dir:
        machines_list = os.path.join(machine_path, file)
        if os.path.isdir(machines_list):
            machines.append(file)

# INFORMATIONAL BLOCKS OF TEXT
def quit_text():
    print("Thank you for using sl86!")
    print("")
    print("snakelauncher86 (sl86) - Version", launcher_version)
    print("https://github.com/DDXofficial/sl86")

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

# Un-comment this if you still want to show the (outdated) machine creation instructions

# def machine_create_instructions():
#     print("* HOW TO CREATE A MACHINE *")
#     print("")
#     print("Create a folder inside the designated machines folder and relaunch")
#     print("the script.")
#     print("Any machines/folders created while this script is active will not be")
#     print("detected and you will need to relaunch the script for them to appear.")
#     print("This will be worked on in future releases.")
#     print("")

def machine_create():
    new_machine_name = input("Enter new machine name: ")
    new_machine_path = os.path.join(machine_path, new_machine_name)
    if os.path.exists(new_machine_path) is True:
        print("ERROR: Machine", new_machine_name, "already exists.")
        print("Please choose a new name.")
        print("")
        machine_create()
    else:
        os.mkdir(new_machine_path)
        print("Machine", new_machine_name, "successfully created.")
        print("")
        refresh_machine_list()

def sl86_main_menu():
    print("* MAIN MENU *")
    print("")
    print("1 - Select machine")
    print("2 - Create machine")
    print("3 - Display 86Box information (macOS/Linux only)")
    print("0 - Exit")
    print("")

while True:
    # MAIN MENU
    refresh_machine_list()
    sl86_main_menu()
    main_menu_input = input("Select an option: ")
    main_menu_option = int(main_menu_input)

    if main_menu_option == 1:
        # MAIN PROGRAM: MACHINE SELECTION
        while main_menu_option == 1:
            clear_screen()
            sl86_header()
            path_86box_text()
            print("")
            path_machine_text()
            refresh_machine_list()
            # MACHINE LISTING
            machines.sort(key=str.lower)
            print("Machines detected in directory:", machines_count, "\n")
            for i in range(machines_count):
                print(i + 1, "-", machines[i])
            print("")

            # MACHINE CHOICE
            machine_id_input = input("Select a machine (number - enter 0 to return to main menu): ")
            selected_machine_id = int(machine_id_input) - 1

            # EARLY EXIT
            if int(machine_id_input) == 0:
                clear_screen()
                sl86_header()
                path_86box_text()
                print("")
                path_machine_text()
                break

            # LAUNCH, CONFIGURE, RETURN, QUIT?
            print("")
            print("Machine selected: " + machine_id_input + " (" + machines[selected_machine_id] + ")")
            machine_decision_input = input("[L]aunch / [C]onfigure / [D]elete / [M]achine list / [R]eturn to main menu: ")

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
            elif machine_decision_input == 'D' or machine_decision_input == 'd':
                print("\nMachine " + machine_id_input + " (" + machines[selected_machine_id] + ") selected for deletion.\n")
                print("WARNING: ALL FILES IN MACHINE DIRECTORY WILL BE DELETED!\n")
                machine_delete_confirm = input("Are you sure you want to delete this machine? (Y/N) ")
                if machine_delete_confirm == 'Y' or machine_delete_confirm == 'y':
                    shutil.rmtree(os.path.join(machine_path, machines[selected_machine_id]))
                elif machine_delete_confirm == 'N' or machine_delete_confirm == 'n':
                    continue
            elif machine_decision_input == 'M' or machine_decision_input == 'M':
                clear_screen()
                print("")
                path_86box_text()
                print("")
                path_machine_text()
                continue
            elif machine_decision_input == 'r' or machine_decision_input == 'r':
                clear_screen()
                sl86_header()
                path_86box_text()
                print("")
                path_machine_text()
                break
            else:
                print("Invalid input - try again.")
            clear_screen()
            print("")
            path_86box_text()
            path_machine_text()
    
    elif main_menu_option == 2:
        clear_screen()
        sl86_header()
        path_86box_text()
        print("")
        path_machine_text()
        machine_create()

    elif main_menu_option == 3:
        clear_screen()
        sl86_header()
        info_86box()
        continue

    elif main_menu_option == 0:
        clear_screen()
        print("")
        quit_text()
        print("")
        break

    else:
        clear_screen()
        sl86_header()
        print("Invalid input - try again.")
        print("")
