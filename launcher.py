import os
import platform
import configparser as cp
import subprocess

# PLATFORM-AGNOSTIC SCREEN CLEARING METHOD
def clear_screen():
    if platform.system() == 'Windows':
        os.system("cls")
    elif platform.system() == 'Darwin' or platform.system() == 'Linux':
        os.system("clear")

# FUNCTION TO CHECK FOR 86BOX INSTALLATION
def find_86box():
    app_path = config.get('launcher', 'app', fallback="")
    if app_path and os.path.exists(app_path):
        return app_path

    if platform.system() == 'Linux':
        flatpak_path = config.get('launcher', 'flatpak_path', fallback=None)
        if flatpak_path and os.path.exists(flatpak_path):
            return flatpak_path

        # Check if flatpak is installed and get the installation path
        flatpak_installed = subprocess.run(['which', 'flatpak'], capture_output=True, text=True).stdout.strip()
        if flatpak_installed:
            # Try to locate the Flatpak application directory
            flatpak_apps_dir = "/var/lib/flatpak/app"
            if os.path.exists(flatpak_apps_dir):
                flatpak_app_dirs = os.listdir(flatpak_apps_dir)
                for app_dir in flatpak_app_dirs:
                    if "net._86box._86Box" in app_dir:
                        # Construct the path to the executable
                        flatpak_path = os.path.join(flatpak_apps_dir, app_dir, "x86_64", "stable", "835e5760d4478bbf16fb677bb6248090f57066e158de2fcbec7048d2f56aba58", "files", "bin", "86Box")
                        if os.path.exists(flatpak_path):
                            return flatpak_path

    # If neither direct path nor flatpak path found, return None
    return None


# CONFIGPARSER: READS DATA FROM launcher.cfg
config = cp.ConfigParser()
config.read(r'launcher.cfg')

# CHECK FOR 86BOX INSTALLATION
app_path = config.get('launcher', 'app', fallback="")
if app_path == "":
    app_path = find_86box()

if app_path is None:
    print("86Box installation not found.")
    exit()

# CONFIGURE 86BOX PATH
config.set('launcher', 'app', app_path)
with open('launcher.cfg', 'w') as configfile:
    config.write(configfile)

# INTRO OUTPUT
print("86Box detected at:", app_path)

# CLEAN STATE
clear_screen()

# VERSION
launcher_version = str("0.2-beta")

# INTRO OUTPUT
print("         ______  _____")
print("   _____/ ( __ )/ ___/  snakelauncher86 (sl86) - Version", launcher_version)
print("  / ___/ / __  / __ \    A text-mode 86Box machine manager written in Python")
print(" (__  ) / /_/ / /_/ /    Author: Segev A. (DDX) - ddxofficial@outlook.com")
print("/____/_/\____/\____/     Source code: https://github.com/ddxofficial/sl86")
print("")

# CONFIGPARSER: READS DATA FROM launcher.cfg
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
    print("86Box path:")
    print("-->", app_path)
    print("")
    print("86Box machine path:")
    print("-->", machine_path, "\n")

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
        # Obtain 86Box path
        app_path = find_86box()
        if app_path is None:
            print("86Box installation not found.")
            exit()

        # Construct command to launch 86Box
        launch_command = "\"" + app_path + "\" -P \"" + os.path.join(machine_path, machines[selected_machine_id]) + "\""
        print("\nMachine " + machine_id_input + " (" + machines[selected_machine_id] + ") selected for launch.\n")
        print("Starting 86Box...")
        os.system(launch_command)
    elif machine_decision_input == 'C' or machine_decision_input == 'c':
        # Obtain 86Box path
        app_path = find_86box()
        if app_path is None:
            print("86Box installation not found.")
            exit()

        # Construct command to configure 86Box
        config_command = "\"" + app_path + "\" -S \"" + os.path.join(machine_path, machines[selected_machine_id], "86box.cfg") + "\""
        print("\nMachine " + machine_id_input + " (" + machines[selected_machine_id] + ") selected for configuration.\n")
        print("Starting 86Box...")
        os.system(config_command)

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
