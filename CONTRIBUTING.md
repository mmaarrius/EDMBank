# Contributing to this project

## 1. Clone the repository

```bash
git clone <repo>
```
and create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```
installing dependencies:
```bash
pip install -r requirements.txt
```

## 2. Create a branch

Use a descriptive branch name related to the work you are doing.

```bash
git checkout -b <branch name>
```

## 3. Make your changes and commit with meaningful messages
```bash
git add .
git commit -m "Add login form and validation"
```
Please add all your newly installed dependencies with the command:
```bash
pip freeze > requirements.txt
```

## 4. Push your branch

```bash
git push origin <branch-name>
```

## 5. Open a Pull Request

1. Go to the repository on GitHub.
2. Click "Compare & pull request" for your branch.
3. Add a clear title and description explaining the change and any context needed to review it.
4. Request reviewers and assign the PR if appropriate.

## 6. Merge

After the PR has been reviewed and approved, it can be merged into `main`.
