install:
	uv sync
collectstatic:
	uv run python3 manage.py collectstatic --no-input
migrate:
	uv run python3 manage.py migrate
start:
	uv run manage.py runserver 0.0.0.0:8000
build:
	./build.sh
render-start:
	gunicorn task_manager.wsgi
lint:
	uv run ruff check .
