
# Django Metrics Exporter

**Django Metrics Exporter** is a lightweight containerized solution for exposing Django application metrics (e.g., user logins, registrations) to Prometheus, designed for seamless integration with Grafana for real-time monitoring.

---

## Features

- Exposes custom Django metrics via a `/metrics` endpoint.
- Tracks user logins and registrations by default.
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

- Import the metrics (`django_logins_total`, `django_registrations_total`) into your Grafana dashboard.
- Visualize real-time trends for user activity in your Django application.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to suggest improvements.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
