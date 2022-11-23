FROM python:3.8

RUN mkdir /app
WORKDIR /app

EXPOSE 5001

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv
RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt

COPY . ./

CMD ["python", "main.py"]