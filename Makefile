install:
	uv sync
collectstatic:
	python3 manage.py collectstatic --noinput
migrate:
	python3 manage.py migrate
runserver:
	python3 manage.py runserver
build:
	./build.sh
render-start:
	gunicorn task_manager.wsgi
lint:
	uv run ruff check .
