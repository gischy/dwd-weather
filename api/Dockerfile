FROM python:latest

COPY api.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD [ "python", "-u", "api.py" ]

