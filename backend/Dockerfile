FROM python

ADD . /code

WORKDIR /code

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]


# CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
