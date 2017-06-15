# Pull base image
FROM resin/rpi-raspbian:jessie

# Install dependencies
RUN apt-get update && apt-get install -y python3 wget
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

RUN mkdir /data
RUN virtualenv -p python3 /data

RUN pip install virtualenv  

# Define working directory
WORKDIR /data

# Define default command
CMD ["bash"]