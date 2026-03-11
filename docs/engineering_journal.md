# Engineering Journal

Day 1 – I successfully configured SSH and connected my local machine to GitHub.

This marks the beginning of my professional identity as a Data Engineer.

Day 2 - Practicing my workflow again to build confidence and independence. And editing my project using VS Code instead of nano.

Learning to use professional tools.
 
Day 2 - Practicing my workflow again to build confidence and independence. And editing my project using VS Code instead of nano.
Learning to use professional tools.

Complete workflow learned. The standard Git workflow is as follows:

  cd project 
  git pull
  git checkout -b new-branch

  edit files

  git status
  git add file
  git commit -m "message"
  git push

  create Pull Request
  merge to main


cd project: Changes the current directory to the specified location.

git status: Shows the status of files in the working directory and staging area (e.g., untracked, modified, staged).

git pull: Fetches changes from the remote repository and merges them into your current local branch.

git checkout -b new-branch: Creates a new branch and immediately switches to it. 

code .: Opens the project in VS Code for edited the file

git add file: Adds a specific file to the staging area, preparing it for a commit.
  git add .: Stages all changes in the current directory.

git commit -m "[message]": Records the staged changes as a commit with a descriptive message

git push: Uploads local commits to the remote repository.

Pull Request (PR) - GitHub: Is a proposal to merge code changes from one branch into another, serving as a central hub for discussion, review, and automated quality checks before the changes are integrated into the main codebase.

git branch -r: View remote branches

git branch -a: View all branches

There are three types of branches:
local branch
remote branch
tracking branch

git fetch --prune: Clean remote references

git branch -d new-branch: Delete the local new-branch

git branch -D new-branch: Force delete the local new-branch