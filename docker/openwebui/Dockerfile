# source: https://github.com/open-webui/open-webui/blob/main/Dockerfile
FROM ghcr.io/open-webui/pipelines:main
WORKDIR /app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


CMD ["bash", "start.sh"]
