FROM python:3.8

WORKDIR /code/app

COPY . .

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /code

CMD ["python", "app/app.py"]