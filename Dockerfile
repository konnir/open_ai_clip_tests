# Use a base Docker image (e.g., Python)
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /usr/src/app

# Create a directory index.html
RUN mkdir -p /app/templates

# Copy the current directory contents into the container at /usr/src/app
COPY *.py /usr/src/app/
COPY requirements.txt /usr/src/app/
COPY templates/index.html /usr/src/app/templates

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Cleaning up - not to inflate the docker image
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# Make port 8081 available to the world outside this container
EXPOSE 8081

# Specify the command to run your application
CMD ["python", "./clip_server.py"]