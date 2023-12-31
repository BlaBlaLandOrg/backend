# syntax=docker/dockerfile:1
FROM python:3.9
RUN apt update ; apt install ffmpeg -y
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install fastapi uvicorn
COPY main.py /code/main.py
COPY ./app /code/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
