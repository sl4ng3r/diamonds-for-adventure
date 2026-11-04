FROM --platform=linux/amd64 debian:bookworm-slim
ARG BEDROCK_VERSION=1.26.61.1
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl unzip procps libcurl4 && rm -rf /var/lib/apt/lists/*
WORKDIR /server
RUN curl -fsSL -A 'Mozilla/5.0' "https://www.minecraft.net/bedrockdedicatedserver/bin-linux/bedrock-server-${BEDROCK_VERSION}.zip" -o /tmp/bedrock.zip && unzip -q /tmp/bedrock.zip && rm /tmp/bedrock.zip
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENV LD_LIBRARY_PATH=/server
ENTRYPOINT ["/entrypoint.sh"]
