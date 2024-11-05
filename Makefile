runserver:
	python manage.py runserver

build:
	poetry build

lint:
	poetry run flake8 task_manager
