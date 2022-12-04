FROM python:3.9.2-alpine

COPY . /code

WORKDIR /code

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]