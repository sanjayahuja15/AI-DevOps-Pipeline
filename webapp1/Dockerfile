# Use Ubuntu 22.04 as a more compatible base image
FROM ubuntu:22.04

#Set the working directory inside the container
WORKDIR /app

#Install required dependencies securely
RUN apt update && apt upgrade -y && \
    apt install -y python3 python3-pip gcc python3-dev && rm -rf /var/lib/apt/lists/*

#Copy all files from the current directory to the container
COPY . .

#Ensure requirements.txt is copied before running pip install
COPY requirements.txt /app/

# Install required dependencies
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask app
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
