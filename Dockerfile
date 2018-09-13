FROM python:3.5-alpine
RUN apk add --no-cache \
    e2fsprogs-extra \
    make \
    ostree

ARG PACKAGE
COPY dist/${PACKAGE} /
RUN pip install /${PACKAGE}[test] && \
    rm /${PACKAGE}
CMD ["deploy-ostree"]
