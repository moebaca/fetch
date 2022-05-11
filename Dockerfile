# Grab Python 3.10 which fetch was developed on
FROM python:3.10

# Update container OS packages
RUN apt-get update

# Add files to /fetch
ADD . /fetch

# Alias fetch
RUN echo "alias fetch=/fetch/fetch.py" >> /root/.bashrc

# Set working directory to /fetch
WORKDIR /fetch

# Run pip install for dependencies
RUN pip install -r requirements.txt
