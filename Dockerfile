FROM python:3.10.2-buster

ENV GECKODRIVER_VERSION v0.30.0
ENV FIREFOX_VERSION 97.0

RUN set -x \
    && apt update \
    && apt upgrade -y \
    && apt install -y \
    firefox-esr

# Add latest FireFox
RUN set -x \
    && apt install -y \
    libx11-xcb1 \
    libdbus-glib-1-2 \
    && curl -sSLO https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VERSION}/linux-x86_64/en-US/firefox-${FIREFOX_VERSION}.tar.bz2 \
    && tar -jxf firefox-* \
    && mv firefox /opt/ \
    && chmod 755 /opt/firefox \
    && chmod 755 /opt/firefox/firefox

# Add geckodriver
RUN set -x \
    && curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz \
    && tar zxf geckodriver-*.tar.gz \
    && mv geckodriver /usr/bin/

WORKDIR /bot

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "bot.py"]
