# Base Image
FROM python:3.8

# create and set working directory
RUN mkdir /app
WORKDIR /app

# Add current directory code to working directory
ADD . /app/

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive 

# set project environment variables
# grab these via Python's os.environ
# these are 100% optional here
ENV PORT=8888


# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* 


RUN  apt-get update && apt-get install -yyq netcat

# install environment dependencies
RUN pip3 install --upgrade pip 
RUN pip3 install pipenv

# Install project dependencies
RUN pipenv install --skip-lock --system --dev

COPY entrypoint.sh .

RUN chmod 755 entrypoint.sh

ENTRYPOINT ["bash","entrypoint.sh"]


EXPOSE 8888
CMD gunicorn stockup_project.wsgi:application --bind 0.0.0.0:$PORT


# docker build -t sparrows-invest -f Dockerfile .
# docker run -it -p 8888:8888 sparrows-invest

# docker run -it -d -p 8888:8888 sparrows-invest (background)
# docker ps > docker stop image
# docker image rm (filename) --force
# gunicorn stockup_project.wsgi:application --bind 0.0.0.0:8000
# docker rmi $(docker images -f “dangling=true” -q) - remove

# docker-compose down -v
# docker-compose -f docker-compose.yml up -d --build -p sparrows-invest-dev


# COPY entrypoint.sh /usr/bin/
# RUN chmod +x /usr/bin/entrypoint.sh
# ENTRYPOINT ["entrypoint.sh"]
