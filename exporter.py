from flask import Flask, Response
import psycopg2
from prometheus_client import Gauge, generate_latest
import os

# Initialize Flask app
app = Flask(__name__)

# Metrics
logins_gauge = Gauge('django_logins_total', 'Total number of logins')
registrations_gauge = Gauge('django_registrations_total', 'Total number of new user registrations')

# Gauges for database tables
table_size_gauge = Gauge('db_table_size_bytes', 'Size of the table in bytes', ['table_name'])
index_size_gauge = Gauge('db_index_size_bytes', 'Size of the table indexes in bytes', ['table_name'])
row_count_gauge = Gauge('db_table_row_count', 'Number of rows in the table', ['table_name'])

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

        # Get table metrics
        cursor.execute("""
            SELECT
                relname AS table_name,
                pg_total_relation_size(relid) AS total_size,
                pg_indexes_size(relid) AS index_size,
                n_live_tup AS row_count
            FROM pg_stat_user_tables
            ORDER BY total_size DESC
            LIMIT 10;
        """)
        tables = cursor.fetchall()

        # Update Prometheus gauges for table metrics
        for table_name, total_size, index_size, row_count in tables:
            table_size_gauge.labels(table_name=table_name).set(total_size)
            index_size_gauge.labels(table_name=table_name).set(index_size)
            row_count_gauge.labels(table_name=table_name).set(row_count)

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
