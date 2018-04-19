FROM debian:9-slim
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-setuptools && \
    rm -rf /var/lib/apt/lists
# stretch ostree is too old to work well so we get a backport
RUN echo "deb http://deb.debian.org/debian stretch-backports main" >> /etc/apt/sources.list.d/stretch-backports.list && \
    apt-get update && \
    apt-get install -t stretch-backports -y ostree && \
    rm -rf /var/lib/apt/lists

ADD . /src
RUN cd /src && \
    python3 setup.py install --single-version-externally-managed --record /deploy-ostree.install && \
    rm -rf /src
CMD ["deploy-ostree"]
