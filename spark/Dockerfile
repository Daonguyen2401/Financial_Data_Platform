# Use bitnami/spark as the base image
FROM bitnami/spark:3.5.4

# Switch to root user to install packages
USER root

# Update apt and install python3-pip, curl, iputils-ping (for ping), and telnet
RUN apt-get update && \
    apt-get install -y \
      python3-pip \
      curl \
      iputils-ping \
      telnet \
      unzip \
      ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws

# Copy requirements.txt into the container
COPY requirements.txt /opt/bitnami/spark/requirements.txt

# Install Python dependencies
RUN pip3 install --no-cache-dir -r /opt/bitnami/spark/requirements.txt

# Switch back to the non-root user
USER 1001