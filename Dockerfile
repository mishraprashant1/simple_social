FROM python:3.11-slim as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root

COPY ./simple_social /app/

CMD bash "poetry run python manage.py migrate"

FROM base as development

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM base as production

EXPOSE 8000

CMD ["poetry", "run", "gunicorn", "simple_social.wsgi:application", "--bind", "0.0.0.0:8000"]
