FROM python:3.10

ENV PYTHONUNBUFFERED=1

RUN pip install "poetry==1.7.1"

RUN mkdir /application
WORKDIR /application

COPY app/pyproject.toml /application

RUN poetry config virtualenvs.create false  \
    && poetry install --no-interaction --no-ansi

COPY app /application

ENV PYTHONPATH "/application"

RUN chmod +x /application/script.sh
CMD [ "sh", "-c", "/application/script.sh" ]
