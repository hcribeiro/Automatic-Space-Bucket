# Pull base image
FROM desktopcontainers/raspberrypi

# Install dependencies
RUN sudo apt-get update && sudo apt-get install -y python3 wget python-pip python3-dev
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

RUN mkdir /data
RUN pip install virtualenv 
RUN virtualenv -p python3 /data

# Define working directory
WORKDIR /data
COPY * /data/

# Donwload libraries
RUN pip3 install RPi.GPIO
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

# Define default command
CMD ["python3 bucket"]
