# Pull base image
FROM raspbian/jessie

# Install dependencies
RUN apt-get update && apt-get install -y python3 wget
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

RUN mkdir /data
RUN pip install virtualenv 
RUN virtualenv -p python3 /data

# Define working directory
WORKDIR /data
COPY * /data/

# Define default command
CMD ["sh"]