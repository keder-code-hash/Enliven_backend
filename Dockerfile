FROM python:3.9.2
ADD requirements.txt /requirements.txt
COPY ./assessment assessment
COPY ./smartassess smartassess
COPY ./static static
COPY ./staticfiles staticfiles
COPY ./storage storage
COPY ./templates templates
COPY ./users users
ADD db.sqlite3 /db.sqlite3
ADD manage.py /manage.py
ADD Dockerfile /Dockerfile
ADD okteto-stack.yaml /okteto-stack.yaml
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python","manage.py", "runserver", "8080"]