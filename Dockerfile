FROM python:3.10.2-alpine3.15
ENV PYTHONUNBUFFERED 1
ENV PYTHONUNBUFFERED 1

# generating directories structure
RUN mkdir -p /app/code

ADD ./requirements.txt /app/requirements.txt

# update pip
RUN python -m pip install --upgrade pip

# install requirements
RUN pip install --no-cache-dir -r /app/requirements.txt

# set working directory
WORKDIR /app/code

ADD . /app/code
