FROM python:3
MAINTAINER pravarag "pravarag@gmail.com"
RUN ls
#RUN apt-get update -y
#RUN apt-get install -y python-pip python-dev build-essential
COPY . /app1
WORKDIR /app1/jaeger_trace
run ls
#run apt-get install git-core -y
run pip install -r requirements.txt
run ls
ENTRYPOINT ["python"]
CMD ["main_app.py"]
