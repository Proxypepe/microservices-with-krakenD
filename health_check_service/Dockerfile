FROM python:3.9.2-alpine

COPY . /code

WORKDIR /code

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python3", "main.py"]
