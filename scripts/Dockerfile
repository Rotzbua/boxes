# Docker container for running a basic webserver of Boxes.py.
# This is a multi-stage build.

# Note that it downloads Boxes.py from GitHub and does not use your local copy
# of the repository. Adjust the git command below to get it from somewhere else.

# Build with:
#  docker build --pull -t boxes.py .
# Run with:
#  docker run -ti -p 4000:8000 boxes.py
# to get the web interface at http://localhost:4000
# First access may take a while as the Python files need to be complied.

# Stage 1. Fetch the code.
FROM alpine as boxescode

RUN apk --no-cache add git
RUN git clone --depth 1 -b master https://github.com/florianfesti/boxes.git \
      && rm -rf /boxes/.git


# Stage 2. Generate final image.
FROM python:3.11-slim

# Install system dependencies.
RUN apt-get update \
 && apt-get install --no-install-recommends -y \
      python3-cairo \
 && rm -rf /var/lib/apt/lists/*

# Install python dependencies.
RUN pip3 install markdown cairocffi

# Copy boxes code.
COPY --from=boxescode /boxes /boxes

# Expose port of boxesserver.
EXPOSE 8000

# Start the boxes web server on container start up.
CMD ["boxes/scripts/boxesserver"]
