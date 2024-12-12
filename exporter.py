from flask import Flask, Response
import psycopg2
from prometheus_client import Gauge, generate_latest
import os

# Initialize Flask app
app = Flask(__name__)

# Metrics
logins_gauge = Gauge('django_logins_total', 'Total number of logins')
registrations_gauge = Gauge('django_registrations_total', 'Total number of new user registrations')

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", 5432)
    )

# Fetch data from the database
def fetch_metrics():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Count logins
        cursor.execute("SELECT COUNT(*) FROM auth_user WHERE last_login IS NOT NULL;")
        logins = cursor.fetchone()[0]
        logins_gauge.set(logins)

        # Count registrations
        cursor.execute("SELECT COUNT(*) FROM auth_user;")
        registrations = cursor.fetchone()[0]
        registrations_gauge.set(registrations)

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error fetching metrics: {e}")

# Expose metrics
@app.route('/metrics')
def metrics():
    fetch_metrics()
    return Response(generate_latest(), content_type='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, threaded=False)
