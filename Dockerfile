FROM python:3.9-slim-bullseye

EXPOSE 50051

# set up virtual env
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# deps
COPY wallycore-0.8.5-cp39-cp39-linux_x86_64.whl .
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Python source code
COPY domain ./domain
COPY handlers ./handlers
COPY services ./services
COPY ocean/v1 ./ocean/v1
COPY gdk-ocean.py ./gdk-ocean.py

# run the main file
CMD ["python3", "gdk-ocean.py"]

