
# Django Metrics Exporter

**Django Metrics Exporter** is a lightweight containerized solution for exposing Django application metrics (e.g., user logins, registrations, and database table stats) to Prometheus, designed for seamless integration with Grafana for real-time monitoring.

---

## Features

- Exposes custom Django metrics via a `/metrics` endpoint.
- Tracks user logins and registrations by default.
- Reports database statistics, including:
  - Total size (bytes) of the 10 largest tables.
  - Index size (bytes) of the 10 largest tables.
  - Accurate row count of the 10 largest tables.
- Easily configurable using environment variables.
- Integrates with existing Prometheus and Grafana setups.

---

## Usage

### Docker Compose

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/django-metrics-exporter.git
   cd django-metrics-exporter
   ```

2. Prepare an `.env` file with your database credentials:
   ```env
   POSTGRES_DB=your_db
   POSTGRES_USER=your_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_HOST=your_host
   POSTGRES_PORT=5432
   ```

3. Run the exporter with Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Access the metrics at:
   ```
   http://localhost:8001/metrics
   ```

---

## Metrics Exposed

| Metric                        | Description                                          |
|-------------------------------|------------------------------------------------------|
| `django_logins_total`         | Total number of user logins.                        |
| `django_registrations_total`  | Total number of new user registrations.             |
| `db_table_size_bytes`         | Size of a table in bytes (10 largest tables).       |
| `db_index_size_bytes`         | Size of table indexes in bytes (10 largest tables). |
| `db_table_row_count`          | Accurate row count for the 10 largest tables.       |

---

## Environment Variables

| Variable          | Description                       | Default        |
|--------------------|-----------------------------------|----------------|
| `POSTGRES_DB`      | Name of the PostgreSQL database   | None (required)|
| `POSTGRES_USER`    | PostgreSQL username              | None (required)|
| `POSTGRES_PASSWORD`| PostgreSQL password              | None (required)|
| `POSTGRES_HOST`    | PostgreSQL host                  | `localhost`    |
| `POSTGRES_PORT`    | PostgreSQL port                  | `5432`         |

---

## Prometheus Configuration

Add the following job to your Prometheus configuration:

```yaml
- job_name: django_exporter
  scrape_interval: 15s
  static_configs:
    - targets:
        - localhost:8001
      labels:
        instance: django_exporter
```

---

## Grafana Integration

- Import the metrics (`django_logins_total`, `django_registrations_total`, `db_table_size_bytes`, `db_index_size_bytes`, `db_table_row_count`) into your Grafana dashboard.
- Visualize real-time trends for user activity and database usage.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to suggest improvements.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
