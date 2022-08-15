FROM python:3.9-slim-bullseye

EXPOSE 50051

# set up virtual env
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# deps
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Python source code
COPY domain ./domain
COPY handlers ./handlers
COPY services ./services
COPY ocean/v1alpha ./ocean/v1alpha
COPY gdk-ocean.py ./gdk-ocean.py

# run the main file
CMD ["python3", "gdk-ocean.py"]

