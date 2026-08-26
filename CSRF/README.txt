GMIT CSRF Fly.io deployment

Files in this folder are already corrected.

1. Replace your local:
   - app.py
   - fly.toml
   - Dockerfile

2. From the CSRF project folder run:

   fly deploy

3. Check IPs:

   fly ips list

If you do not have a shared IPv4, run:

   fly ips allocate-v4 --shared

4. Test:

Victim:
https://csrf.fly.dev/

Exploit server:
https://csrf.fly.dev:7001/

The Flask app listens internally on:
7000 = victim
7001 = exploit server
