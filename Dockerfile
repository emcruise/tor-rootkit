FROM python:3.9

RUN apt-get update && apt-get upgrade -y
RUN apt install tor -y
RUN mkdir /executables
COPY listener/ ./listener
COPY client/ ./client
RUN pip install -r listener/requirements.txt
CMD [ "python", "./listener/listener.py", "8843", "8843" ]