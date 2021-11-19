FROM python:latest
RUN apt-get update && apt-get install -y postgresql postgresql-contrib

COPY main.py .
COPY requirements.txt .
COPY wait-for-postgres.sh .

RUN pip install -r requirements.txt

CMD [ "./wait-for-postgres.sh", "python", "./main.py" ]
