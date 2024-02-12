FROM python:latest

RUN pip install pgzero
RUN pip install pylint
RUN pip install pytest

ADD betrayal.py .
ADD docker_shell.sh .


COPY ./assets ./assets
#COPY ./lib ./lib
#COPY ./src ./src



ENTRYPOINT ["/docker_shell.sh"]
#CMD ["ls"]
#CMD ["python","betrayal.py"]