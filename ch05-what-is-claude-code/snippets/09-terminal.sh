poetry install           # creates the environment, installs the project and groups
poetry run pytest -q
eval $(poetry env activate)
