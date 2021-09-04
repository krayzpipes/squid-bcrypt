#!/usr/bin/env python3

"""Squid helper for authenticating basic auth against bcrypt hashes.

See Authenticator > Basic Scheme here:
https://wiki.squid-cache.org/Features/AddonHelpers

Designed to work with bcrypt hash files created with htpasswd:
EXAMPLE: htpasswd -cbB -C 10 /path/to/password_file username password

This program loads the password file content into memory based on the
assumption the underlying host is ephemeral and the password file is
populated when the host is bootstrapped.
"""

import sys

import bcrypt


def load_hashes_to_memory(filename: str) -> dict:
    """Return dictionary of usernames and bcrypt hashes.

    Ex: {'myusername': '$2y$10$UwKsKOkgObpauy5wzcN2euKZ/lgQZCP3A8MQsatZfNdPt5hNUXFae'}
    """
    password_kv = {}
    with open(filename, 'r') as f:
        for line in f:
            sections = line.strip().split(':')
            try:
                user = sections[0].strip().lower()
                hash = sections[1].strip()
            except IndexError:
                raise ValueError("password file has invalid content")
            else:
                password_kv[user] = hash
    return password_kv


def write_stdout(response: str) -> None:
    """Write to stdout and flush. Make sure one and
    only one newline exists before writing."""
    response = response.strip()
    sys.stdout.write(f'{response}\n')
    sys.stdout.flush()


def run_loop(password_kv: dict) -> None:
    """Validate username and passwords from the squid proxy
    using bcrypt."""
    while True:
        line = sys.stdin.readline()
        line = line.strip()

        if line == '':
            write_stdout('BH message="empty line from proxy')
            continue

        parts = line.split(' ', 1)  # setting maxsplit to 1 makes sure we handle passwords with spaces in them

        try:
            username = parts[0].strip()
            password = parts[1].strip()
        except IndexError:
            write_stdout('BH message="message from proxy is in unexpected format')
            continue

        password_hash = password_kv.get(username.lower(), None)

        if password_hash is None:
            write_stdout('ERR message="invalid credentials')
            continue

        authenticated = bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

        if not authenticated:
            write_stdout('ERR message="invalid credentials"')
            continue

        write_stdout('OK')
        continue


def main():
    """Load hashes from file into memory and start the
    bcrypt validation service."""

    password_file = sys.argv[1]

    user_hash_kv = load_hashes_to_memory(password_file)

    run_loop(user_hash_kv)


if __name__ == "__main__":
    main()
    exit(0)
