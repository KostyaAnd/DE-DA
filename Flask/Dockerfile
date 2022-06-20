FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY flask_lab04_tutorial_app.py .

CMD ["python3", "flask_lab04_tutorial_app.py"]
