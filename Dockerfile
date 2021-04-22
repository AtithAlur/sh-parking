FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

RUN apt update && apt install -y postgresql postgresql-contrib

ENTRYPOINT ["/code/entrypoint.sh"]
