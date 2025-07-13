FROM python:3.11

WORKDIR /app

COPY ./tests /app/tests
COPY ./requirements.txt /app/
COPY ./pytest.ini /app/
COPY ./alembic.ini /app/
COPY ./alembic /app/alembic
EXPOSE 8000
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app

CMD ["python", "-Xfrozen_modules=off", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]