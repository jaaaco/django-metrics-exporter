
# Use a slim Python base image
FROM python:3.9-slim

# Install required dependencies
RUN pip install flask prometheus_client psycopg2-binary

# Set the working directory
WORKDIR /app

# Copy the application code
COPY exporter.py /app/exporter.py

# Expose the port for the metrics endpoint
EXPOSE 8001

# Run the application
CMD ["python", "exporter.py"]
