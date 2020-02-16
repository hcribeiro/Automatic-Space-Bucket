# Pull base image
FROM raspbian/jessie

# Install dependencies
RUN apt-get update && apt-get install -y python3 wget python-rpi.gpio
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

RUN mkdir /data
RUN pip install virtualenv 
RUN virtualenv -p python3 /data

# Define working directory
WORKDIR /data
COPY * /data/

# Donwload libraries
RUN pip3 install -r requirements.txt

# Define default command
CMD ["python3 bucket"]
