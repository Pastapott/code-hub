# Setup Guide
This guide will help you set up your development environment for this project and any future ones.
This will cover **WSL installation**, **VS Code setup**, and **Git configuration**.

---

## 1. Install Windows Subsystem for Linux (WSL)

1. Open **Windows PowerShell** as Administrator.  
2. Run the following command to install WSL and the default Ubuntu distribution:

wsl --install

You may see an error if virtualization is not enabled in your BIOS/UEFI settings.
Check your BIOS and make sure Intel VT-x or AMD-V is enabled.
Installation may also fail if your Windows is not fully updated.

3. Restart your computer if prompted.
4. Open Ubuntu from the Start menu and follow the initial setup (username, password).
5. Update packages with this command:

sudo apt update

## 2. Install VS Code

1. Download VS Code from https://code.visualstudio.com
2. Install it with default options.

## 3. Install VS Code Extensions
Open VS Code and install the following extensions:
GitLens — Shows commit history, authors, and file blame.
Python — Official Python support.
Pylance — Smart IntelliSense and type checking for Python.
Live Share — Optional: collaborate in real time.
Settings Sync — Sync extensions and settings across devices.
Remote - WSL — Integrates VS Code with your WSL Linux environment.
Prettier - Code Formatter — Auto-formats your code.
Material Icon Theme — Makes file icons clearer.
Bookmarks — Quickly jump between important lines in code.

To install, go to Extensions (Ctrl+Shift+X), search for the extension, and click Install.

## 4. Open and Use WSL in VS Code

Install the Remote - WSL extension in VS Code (if not done already).
Open VS Code. Press Ctrl+Shift+P (or Cmd+Shift+P on Mac) to open the Command Palette.
Type and select:

WSL: Connect to WSL in New Window

This will open a new VS Code window connected to your WSL Ubuntu environment.
Any commands you run in the integrated terminal will now execute inside WSL, not Windows.
It behaves like a separate Linux computer running on your Windows machine.
The files and programs inside WSL are separate from your Windows filesystem, although you can access Windows files from WSL if needed.
This means you can experiment, install Linux packages, and run scripts without affecting your main Windows system.

## 5. Check your current location
In the VScode WSL terminal (integrated in VS Code), type:

pwd

pwd stands for “print working directory”.
It shows the path to the folder you are currently in.
By default, you will start in your Linux home directory, e.g., /home/ollie.

## 6. Create a directory for your repositories
Before cloning or working with repos, it’s good practice to create a dedicated folder. For example:

mkdir ~/project

This directory can be called anything. e.g ~/MyProject, ~/Game, ~/LocalRepo
mkdir means “make directory”.
~ is a shortcut for your Linux home directory (/home/ollie).
This will create a folder called projects where you can store all your cloned repositories.
Check that the folder was created with:

ls 

ls lists all files and folders in the current directory.
You should see projects in the list.

## 7. Clone the Repository

Now that you have your projects folder, you can clone the repository from GitHub to work on it locally inside WSL.

### Navigate to your projects folder
In the VScode WSL terminal, type:

cd ~/projects (or whatever you decided to call your directory)

cd means “change directory”.
This moves you into the folder you created for your repositories.
You can check your current location with:

pwd

You should see something like /home/your_name/projects

### Clone the repository
Next, run:

git clone https://github.com/Pastapott/code-hub.git

git clone <URL> downloads a copy of the repository from GitHub.
This will create a folder called code-hub inside your projects directory.

### Verify the setup
Optional but recommended, run:

git status

Confirms that Git is working and shows the current branch.
You should see something like:

On branch main
Your branch is up to date with 'origin/main'.

### 8. Work on a Feature Branch
Inside the repository folder run:

git branch -a

Shows all local and remote branches.
You should see something like:

* main
  feature-test
  remotes/origin/main
  remotes/origin/feature-test

* main indicates your current branch.

### Switch to the feature branch
To move to feature-test:

git checkout feature-test

checkout switches your local workspace to the branch.
Now any changes you make will be recorded on feature-test, not main.
Verify with:

git status

You should see On branch feature-test.

### Pull the latest changes
Before making any changes, make sure your branch is up to date:

git pull origin feature-test

This downloads any updates from the remote repository.
Prevents conflicts if someone else has made changes.

With your environment set up and feature-test branch ready, you can now start coding in your local repository. For detailed instructions on staging, committing, and pushing changes — as well as best practices for using Git and version control safely — please see git.md