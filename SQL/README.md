# GMIT SQL Injection Lab

Standalone beginner SQL Injection CTF lab.

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:6001/
```

Test payload:

```text
Username: admin' --
Password: anything
```

## Docker

```bash
docker build -t gmit-sql-lab .
docker run --rm -p 6001:6001 gmit-sql-lab
```

The application is intentionally vulnerable. Keep it isolated from production systems and real data.
