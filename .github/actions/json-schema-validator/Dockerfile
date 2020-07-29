FROM python:3.7-slim-stretch

ARG buildDeps="freetds-dev \
  libkrb5-dev \
  libsasl2-dev \
  libssl-dev \
  libffi-dev \
  libpq-dev \
  git \
"

RUN set -ex \
    && apt-get update -yqq \
    && mkdir -p /usr/share/man/man1 \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        ca-certificates \
        gnupg \
        freetds-bin \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
        file \
        openjdk-8-jre-headless \
        openjdk-8-jdk-headless \
        maven \
        autoconf \
        automake \
        libtool \
        jq \
        python-dev

RUN pip install jsonschema requests

COPY entrypoint.sh /entrypoint.sh
COPY validate.py /validate.py

RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
