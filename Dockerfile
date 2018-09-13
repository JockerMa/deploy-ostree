FROM debian:9-slim
RUN apt-get update && \
    apt-get install -y \
        ca-certificates \
        make \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists
# stretch ostree is too old to work well so we get a backport
RUN echo "deb http://deb.debian.org/debian stretch-backports main" >> /etc/apt/sources.list.d/stretch-backports.list && \
    apt-get update && \
    apt-get install -t stretch-backports -y ostree && \
    rm -rf /var/lib/apt/lists

ARG PACKAGE
COPY dist/${PACKAGE} /
RUN pip3 install /${PACKAGE}[dev] && \
    rm /${PACKAGE}
CMD ["deploy-ostree"]
