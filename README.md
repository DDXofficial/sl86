# SnakeLauncher86 (sl86) — a text-mode 86Box machine manager
This Python script allows you to manage your 86Box machines from the command line.
<br/>Originally written primarily with macOS in mind, this script has now been rewritten and extended to officially support Windows and Linux as well.

## Setup
1. Locate your 86Box installation
2. Download the latest release and copy it to your 86Box folder
3. Edit your `launcher.cfg` file to contain the path to your 86Box executable (i.e. `C:\Users\foo\86Box\86Box.exe`) and machines folder (i.e. `C:\Users\foo\86Box\machines`)
4. Run `python launcher.py` or `python3 launcher.py` in your terminal of choice

## Linux Flatpak Steps
You MUST install a couple of dependencies. On Ubuntu/Debian: `sudo apt-get install libslirp0 librtmidi6 libfluidsynth3`

Other distros, you're on your own!

## Support

I am available in the 86Box Discord server (https://discord.86box.net) if you have any questions.

_Last updated April 21, 2024_
