FROM ubuntu:latest

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    sudo \
    tar \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /airbyte-install

# Download Airbyte CLI
RUN curl -LsfS -o abctl-v0.24.0-linux-amd64.tar.gz https://github.com/airbytehq/abctl/releases/download/v0.24.0/abctl-v0.24.0-linux-amd64.tar.gz

# Extract and install Airbyte CLI
RUN tar -xvzf abctl-v0.24.0-linux-amd64.tar.gz && \
    chmod +x abctl-v0.24.0-linux-amd64/abctl && \
    sudo mv abctl-v0.24.0-linux-amd64/abctl /usr/local/bin/

# Cleanup
RUN rm -rf /airbyte-install

# Set entrypoint
CMD ["/bin/bash"]
