# Pull base image
FROM python:3.6.6

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install node / npm
RUN apt-get update
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash
RUN apt-get install -y nodejs
RUN apt-get install -y npm

# Set work directory
WORKDIR /code

# Copy python and node requirements
COPY ./requirements.txt .
COPY ./package.json .

# Install python and node dependencies
RUN pip install -r requirements.txt
RUN npm install

# Copy project
COPY . .