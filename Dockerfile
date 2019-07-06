FROM python:3.7.3
ENV PYTHONUNBUFFERED 1
WORKDIR /srv
ADD pyproject.toml poetry.lock /srv/
RUN pip3 install poetry && poetry install
