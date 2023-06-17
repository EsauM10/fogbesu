FROM ubuntu:focal


RUN apt-get update \
    # Install Containernet Dependencies
    && apt-get install -y \
    net-tools \
    iputils-ping \
    iproute2 \
    curl \
    # Install OpenJDK 
    && apt-get install -y openjdk-17-jdk libjemalloc-dev=5.* \
    && apt-get clean \
    # Install Besu
    && curl -LO https://hyperledger.jfrog.io/artifactory/besu-binaries/besu/23.4.1/besu-23.4.1.tar.gz \
    && tar -xvzf besu-23.4.1.tar.gz \
    && cp -a besu-23.4.1 /opt/besu \
    && rm -rf besu-23.4.1 \
    && rm -rf besu-23.4.1.tar.gz \ 
    && apt-get autoremove -y

WORKDIR /opt/besu


# Expose services ports
# 8545 HTTP JSON-RPC
# 8546 WS JSON-RPC
# 8547 HTTP GraphQL
# 8550 HTTP ENGINE JSON-RPC
# 8551 WS ENGINE JSON-RPC
# 30303 P2P
EXPOSE 8545 8546 8547 8550 8551 30303

# defaults for host interfaces
ENV BESU_RPC_HTTP_HOST 0.0.0.0
ENV BESU_RPC_WS_HOST 0.0.0.0
ENV BESU_GRAPHQL_HTTP_HOST 0.0.0.0
ENV BESU_PID_PATH "/tmp/pid"

ENV OLDPATH="${PATH}"
ENV PATH="/opt/besu/bin:${OLDPATH}"

ENTRYPOINT [ "besu" ]

CMD [ "/bin/bash" ]
