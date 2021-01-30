# How to activate virtual env
- Install virtual env: ``pip install virtualenv``
- $ mkdir myproject
- $ cd myproject
## Initializing
- Linux command: ``$ python3 -m venv venv ``
- windows command: ``$ py -3 -m venv venv``
## Later on
- Then on Linux: ``$ . venv/bin/activate ```
- Or windows: ``. venv\Scripts\activate``

## For the backend:
- Activate the virtual environment first
- To install the packages: ``pip install -r requirements.txt``
- Should you install a pip package just do: ``pip freeze > requirements.txt``
- Push the file to this repo
