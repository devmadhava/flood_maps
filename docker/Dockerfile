# FROM ghcr.io/osgeo/gdal:ubuntu-full-latest

# # Install Python & required GIS libs only once
# RUN apt-get update && apt-get install -y \
#     python3 python3-pip python3-venv \
#     && apt-get clean

# # Copy your requirements and install them
# COPY backend/requirements.txt /tmp/requirements.txt
# RUN pip3 install -r /tmp/requirements.txt

# WORKDIR /workspace


# Use the OSGeo GDAL image as a base
FROM ghcr.io/osgeo/gdal:ubuntu-full-latest

# Install Python and required dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    && apt-get clean

# Create a virtual environment and set the path
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy your requirements file and install packages into the virtual environment
COPY backend/requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Set the working directory
WORKDIR /workspace
