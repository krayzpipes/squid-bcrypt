FROM ubuntu:18.04

RUN apt update -y
RUN DEBIAN_FRONTEND=noninteractive apt install -y squid apache2-utils python3 python3-pip build-essential libffi-dev python-dev

COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

RUN apt-get purge -y --auto-remove libffi-dev python-dev build-essential && apt-get clean

COPY squid.conf /etc/squid/
COPY basic_bcrypt_auth.py /usr/lib/squid/
COPY entrypoint.sh /app/

RUN chmod 544 /app/entrypoint.sh \
    && chmod 555 /usr/lib/squid/basic_bcrypt_auth.py

EXPOSE 3128/tcp

ENTRYPOINT ["/app/entrypoint.sh"]
