FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY . /app
ENTRYPOINT ["python"]
CMD  [ "app.py"]