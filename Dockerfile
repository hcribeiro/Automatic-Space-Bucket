# Pull base image
FROM resin/rpi-raspbian:wheezy

# Install dependencies
RUN apt-get update && apt-get install -y \
    python \
    python-dev \
    python-pip \
    python-virtualenv 

RUN sudo pip install --upgrade pip 
RUN sudo pip install --upgrade virtualenv  

# Define working directory
WORKDIR /data

# Define default command
CMD ["bash"]