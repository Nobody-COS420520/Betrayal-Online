FROM python:latest

RUN pip install pgzero
RUN pip install pylint
RUN pip install pytest

ADD betrayal.py .
ADD docker_shell.sh .


COPY ./images ./images
#COPY ./lib ./lib
#COPY ./src ./src

#ENV DISPLAY=:0
#0 is default location for DISPLAY
ENV PULSE_SERVER=/tmp/PulseServer


ENTRYPOINT ["/docker_shell.sh"]
#CMD ["ls"]
#CMD ["python","betrayal.py"]