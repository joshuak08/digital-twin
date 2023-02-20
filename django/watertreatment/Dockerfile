# Running container in python 3.10 environment
FROM python:3.10-slim-buster

# Create diretory for the applications
WORKDIR /app

# Update pip to latest
RUN pip install pip --upgrade

# Copy over the requirements file to be installed in the environment
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8000/tcp

# Copy over all the files and run the server with the created image
COPY . .
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# Commands to build, run, and push onto docker hub
# docker build -t joshuak08/python-django:latest .
# docker run -p 8000:8000 joshuak08/python-django:latest
# docker push joshuak08/python-django:latest