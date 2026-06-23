# Vulnerable Web Application for Security Testing
# WARNING: Contains intentional vulnerabilities - DO NOT use in production!

FROM python:3.11-slim

# VULNERABILITY: Running as root (no non-root user)
# Best practice would be to create a non-root user

WORKDIR /app

# VULNERABILITY: No specific version pinning for some packages
# VULNERABILITY: Installing potentially dangerous packages
RUN apt-get update && apt-get install -y \
    iputils-ping \
    curl \
    wget \
    netcat-openbsd \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create upload directory with permissive permissions (vulnerability)
RUN mkdir -p static/uploads && chmod 777 static/uploads

# VULNERABILITY: Exposing debug port
EXPOSE 5000

# VULNERABILITY: Debug mode enabled, binding to all interfaces
ENV FLASK_DEBUG=1
ENV FLASK_ENV=development

# VULNERABILITY: Running as root with debug enabled
CMD ["python", "app.py"]
