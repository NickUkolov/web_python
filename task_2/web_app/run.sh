python manage.py collectstatic --no-input
python manage.py migrate
gunicorn stocks_products.wsgi:application --bind 0.0.0.0:8000