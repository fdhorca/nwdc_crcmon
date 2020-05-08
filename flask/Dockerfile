#FROM base image to use (from official docker images)
FROM python:3.8.2-buster

#Set container working directory to /app
WORKDIR /app

# Copy the current directory contents into the /app directory of the container
COPY . /app

# Install dependencies
RUN pip3 install --proxy http://muc1-prxy.sdi.trendnet.org:8080/ -r requirements.txt

#Command to start uWSGI
CMD ["uwsgi", "app.ini"]

