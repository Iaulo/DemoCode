.PHONY: install dev test coverage badge e2e perf

install:
    pip install -r requirements.txt -r requirements-dev.txt
    python -m playwright install --with-deps

dev:
    uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000

test:
    pytest -q

coverage:
    pytest --cov=backend/app --cov-report=term-missing --cov-report=xml

badge:
    coverage run -m pytest
    coverage-badge -o coverage.svg

e2e:
    pytest -q e2e/test_ui.py

perf:
    locust -f locustfile.py --host http://127.0.0.1:8000
