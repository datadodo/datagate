# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/app/ ./app/
COPY backend/globaldashboard-4598e-firebase-adminsdk-fbsvc-8820178d65.json ./

# Set environment variables
ENV PORT=8080
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8080

# Run the application with increased timeout and limits for large file uploads
WORKDIR /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--timeout-keep-alive", "600", "--limit-max-requests", "1000"]
