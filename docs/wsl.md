# WSL / Linux Basics Guide

This guide explains the basics of using WSL (Windows Subsystem for Linux) and Linux commands.
It assumes you have already installed WSL and are working in the Ubuntu environment inside VS Code.

# Understanding WSL

WSL gives you a full Linux environment on your Windows computer.
You can run Linux commands, install packages, and manage files independently from Windows.
Think of it as a virtual Linux computer where your coding projects live, separate from your Windows system.

# Navigating the File System
## Current Location
pwd

Prints the current working directory (path you are in).

# List files and folders
ls

Shows files and directories in the current folder.

Common options:
ls -l → detailed list with permissions and sizes
ls -a → shows hidden files (starting with .)

# Change directory
cd <folder>

Moves you into another directory.

cd ~ → goes to your home directory
cd .. → goes up one directory level

# Make a new directory
mkdir <folder-name>

Creates a new folder.
Example: mkdir ~/projects to hold your repositories.

# Managing Files
Command	Description
touch <file>	            Creates a new empty file.
rm <file>	                Deletes a file.
rm -r <folder>	            Deletes a folder and all its contents.
mv <old> <new>	            Moves or renames a file/folder.
cp <source> <destination>	Copies a file or folder.
cat <file>	                Displays the contents of a file.
nano <file>	                Opens a simple text editor in the terminal.

# Viewing and Editing Files

View a file: 
cat filename
Edit a file in terminal: 
nano filename
Save in Nano: Ctrl+O, then Enter
Exit Nano: Ctrl+X
For bigger edits, you can always open the file in VS Code with:
code <file>

# Permissions (basic overview)
Linux files have read, write, and execute permissions.
Check permissions:

ls -l

example output: -rw-r--r--
r = read, w = write, x = execute

Change permissions:

chmod +x script.sh  # makes a script executable


# Installing Packages
Update package lists:

sudo apt update

Upgrade installed packages:

sudo apt upgrade -y

Install new software:

sudo apt install <package-name>
examples:
sudo apt install git 
sudo apt install python3-pip 

# Useful Shortcuts

Shortcut	                  Description
Tab	                          Autocomplete file/folder names
Ctrl+C	                      Stop a running command
Ctrl+L	                      Clear terminal screen
!!	                          Repeat last command

WSL allows you to run Linux commands, manage files, and work in a separate environment from Windows.
All your coding projects, Git operations, and package installations happen inside this virtual Linux system.

Use pwd, ls, and cd to navigate.
Use mkdir, touch, and nano to create and edit files.
Use sudo apt install to install new software.