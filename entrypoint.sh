#!/bin/sh
poetry run alembic upgrade head
poetry run uvicorn --host 0.0.0.0 --port 8000 it_myprompt.app:app