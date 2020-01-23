FROM python:3.7-alpine
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY challenge challenge
COPY setup_script.sh challenge/setup_script.sh
WORKDIR challenge
RUN chmod +x setup_script.sh
RUN /setup_script.sh