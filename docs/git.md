# Git Guide

This guide explains how Git works, how to manage changes, and best practices for contributing safely to the project.
It’s written for beginners and assumes you are working inside your local repository on the feature-test branch.



# Understanding Git Basics
Git is a distributed version control system that allows multiple people to work on the same project at the same time. Each contributor has a local copy of the repository on their computer, while a remote repository (hosted on GitHub) stores the official version of the project. When you run git pull, you download the latest changes from the remote repository to your local branch. After making changes locally, you stage and commit them, then use git push to upload your commits to the remote repository. This allows other contributors to pull your changes and keep their local copies up to date.

Sometimes, multiple people may edit the same part of a file simultaneously, which can lead to a merge conflict. When this happens, Git will notify you and mark the conflicting sections in the file. To fix a merge conflict, you must manually edit the file to resolve the differences, then stage and commit the resolved version. Once pushed, everyone else can pull the updated file and continue working safely.



# Checking Your Status
Before making changes, check which branch you are on and if you have uncommitted changes:

git status

Shows the current branch (should be feature-test).
Lists files that have been modified, staged, or untracked.



# Updating Your Branch
Always make sure your branch is up to date with the remote before starting work:

git pull origin feature-test

Downloads any new commits from GitHub.
Prevents conflicts when you push your changes later.



# Staging and Committing Changes

## Staging your changes
Before committing, you need to stage files you want to include:

git add <filename>

or for multiple files:

git add <filename> <filename> <filename> <filename>

or to stage all changes:

git add .

## Commit your changes
After staging, create a commit with a descriptive message:

git commit -m "Add feature X or fix bug Y"

The message should briefly explain what changed and why.



# Pushing Changes
When your commit is ready to share:

git push origin feature-test

Sends your changes to the remote feature-test branch on GitHub.
Only push after pulling first to avoid conflicts.



# Do’s and Don’ts
Do:

Always work on feature-test, not main.
Pull updates from the remote branch before starting work.
Write clear, descriptive commit messages.
Stage only the files you want to include in a commit.

Don’t:

Don’t commit sensitive files (like .vscode/settings.json if listed in .gitignore).
Don’t push directly to main.
Don’t commit unfinished experimental work to the shared branch — use your local commits first.
Don’t ignore merge conflicts — resolve them carefully if they occur.

# Checking Your Work
To see commit history:

git log --oneline

To see what changed in a file:

git diff <filename>

To see which files are staged:

git status


By following these steps, you can safely edit files, stage, commit, and push changes without breaking the repository. Always make sure you’re on the feature-test branch and pull the latest updates before starting work.

For a visual overview and advanced Git tools, you can also explore GitLens in VS Code.

Command	Description
git status	-  Shows the current branch, staged changes, and untracked files.
git branch	-  Lists local branches. Add -a to see remote branches too.
git checkout <branch>	-  Switches to the specified branch.
git checkout -b <new-branch>	-  Creates a new branch and switches to it.
git add <file>	-  Stages a specific file for commit.
git add .	-  Stages all changes in the current directory.
git commit -m "message"	  -  Creates a commit with a descriptive message.
git log	    -   Shows commit history. Use --oneline for a compact view.
git diff	-  Shows changes in files that are not staged.
git diff --staged	  -  Shows changes that are staged for commit.
git pull origin <branch>	-  Pulls updates from the remote branch to your local branch.
git push origin <branch>	-  Pushes your local commits to the remote branch.
git clone <repo-url>	-  Copies a remote repository to your local machine.
git remote -v	-  Lists the remote repositories linked to your repo.
git fetch	-  Downloads updates from the remote without merging.
git merge <branch>	-  Merges another branch into your current branch.
git reset <file>	-  Unstages a file that was added with git add.
git restore <file>	-  Reverts changes in a file to the last committed version.
git stash	-  Temporarily saves uncommitted changes. Useful if you need to switch branches without committing.
git stash pop	-   Restores the most recently stashed changes.
git rm <file>	-   Removes a file from the repo and stages the deletion.
git mv <old> <new>	-   Renames or moves a file and stages the change.