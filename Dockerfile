FROM python:latest

ADD requirements.txt .
RUN pip install -r requirements.txt


ADD betrayal.py .
ADD docker_shell.sh .


COPY ./images ./images
COPY ./sounds ./sounds
COPY ./fonts ./fonts
#COPY ./lib ./lib
#COPY ./src ./src

#ENV DISPLAY=:0
ENV PULSE_SERVER=/tmp/PulseServer


ENTRYPOINT ["/docker_shell.sh"]
#CMD ["ls"]
#CMD ["python","betrayal.py"]