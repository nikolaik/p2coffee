web: gunicorn -k gevent coffeesite.wsgi
worker: python manage.py run_huey -w 1 -k greenlet
