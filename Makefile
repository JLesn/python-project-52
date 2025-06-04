install:
	uv sync
runserver:
	python3 manage.py runserver
build:
	./build.sh
render-start:
	gunicorn task_manager.wsgi
