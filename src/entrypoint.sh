#!/bin/bash

set -e

MSG="[SQUID PROXY]"

echo "$MSG setting up password file"
htpasswd -cbB -C 10 /etc/squid/passwords "${PROXYUSER}" "${PROXYPASS}"

SQUIDBIN=$(which squid)
echo "$MSG starting squid proxy at ${SQUIDBIN}"
$SQUIDBIN -f /etc/squid/squid.conf -NYCd 1
echo "$MSG squid proxy stopped..."
