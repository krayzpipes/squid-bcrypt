# squid-bcrypt
Squid proxy helper for validating bcrypt hashed passwords.

## Where is it?

The helper is `src/basic_bcrypt_auth.py`.

## What is it?

A squid helper that allows squid to validate usernames and passwords
it receives from basic authentication against bcrypt hashes.

## Getting Started

### Test it out
1. Run `docker compose up`
2. Set your http and https proxy to `http://myproxyuser:myproxypassword@127.0.0.1:3128` and
   browse to something like http://neverssl.com.
    - You should get through to the site you're attempting to browse to.
3. Now set your http and https proxy to `http://127.0.0.1:3128` and try again
    - You should get an HTTP 407 error

### Using it yourself

- Checkout `src/squid.conf`
- especially this line:
    ```bash
    auth_param basic program /usr/lib/squid/basic_bcrypt_auth.py /etc/squid/passwords
    ```

## How does it work?

The squid helper is opinionated.

1. It assumes that you are creating your bcrypt hash
via the `htpasswd` tool, which is often times found throughout Squid proxy documentation
for generating basic authentication credential files.
   
    - For example: `htpasswd -cbB -C 10 /etc/squid/passwords <username> <password>`

    - This creates a new password file, using bcrypt as the hashing algorithm, with a cost factor of 10.


2. It loads your password file contents (usernames and hashes) into memory at the start of the program.
   - It assumes your underlying host is ephemeral.
   - Due to the ephemeral nature of the host, it assumes your credential file is generated as part
    of the host's bootstrap process.
 
## References and inspiration

- [AddonHelpers Documentation](https://wiki.squid-cache.org/Features/AddonHelpers)
- [auth_param documenation](http://www.squid-cache.org/Doc/config/auth_param/)
- [htpasswd documentation](https://httpd.apache.org/docs/2.4/programs/htpasswd.html)
- [funway's redis squid-helper](https://github.com/funway/squid-helper/blob/master/digest_redis_auth.py)

