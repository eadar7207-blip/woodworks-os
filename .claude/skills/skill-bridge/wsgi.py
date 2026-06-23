"""
WSGI Entry Point for Dashboard

Use with Gunicorn or other WSGI servers:
    gunicorn wsgi:app --bind 0.0.0.0:8080

Or with other servers:
    waitress-serve wsgi:app --listen=127.0.0.1:8080
    uwsgi --http :8080 --wsgi-file wsgi.py --callable app
"""

from dashboard import app

if __name__ == '__main__':
    app.run()
