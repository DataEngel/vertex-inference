FROM python:3.10.13


COPY . /app
WORKDIR /app



EXPOSE 8080

RUN set -ex; apt-get update; apt-get install -y --no-install-recommends autoconf automake bzip2 dpkg-dev file g++ gcc imagemagick libbz2-dev libc6-dev libcurl4-openssl-dev libdb-dev libevent-dev libffi-dev libgdbm-dev libglib2.0-dev libgmp-dev libjpeg-dev libkrb5-dev liblzma-dev libmagickcore-dev libmagickwand-dev libmaxminddb-dev libncurses5-dev libncursesw5-dev libpng-dev libpq-dev libreadline-dev libsqlite3-dev libssl-dev libtool libwebp-dev libxml2-dev libxslt-dev libyaml-dev make patch unzip xz-utils zlib1g-dev $( if apt-cache show 'default-libmysqlclient-dev' 2>/dev/null | grep -q '^Version:'; then echo 'default-libmysqlclient-dev'; else echo 'libmysqlclient-dev'; fi ) ; rm -rf /var/lib/apt/lists/*
RUN set -eux; apt-get install -y --no-install-recommends ca-certificates curl gnupg netbase sq wget ; rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip install -r Requirements.txt

CMD uwsgi --http 0.0.0.0:8080  --wsgi-file app.py --callable app --master --die-on-term --need-app --harakiri 60 

RUN /bin/sh -c set -eux;  apt-get install -y --no-install-recommends libbluetooth-dev tk-dev uuid-dev ; rm -rf /var/lib/apt/lists/* # buildkit
RUN  apt-get install -y --no-install-recommends git mercurial openssh-client subversion procps && rm -rf /var/lib/apt/lists/*
RUN /bin/sh -c set -eux; wget -O get-pip.py "$PYTHON_GET_PIP_URL"; echo "$PYTHON_GET_PIP_SHA256 *get-pip.py" | sha256sum -c -; export PYTHONDONTWRITEBYTECODE=1; python get-pip.py --disable-pip-version-check --no-cache-dir --no-compile "pip==$PYTHON_PIP_VERSION" "setuptools==$PYTHON_SETUPTOOLS_VERSION" ; rm -f get-pip.py; pip --version # buildkit
