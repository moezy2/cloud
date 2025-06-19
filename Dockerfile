# Use official lightweight Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y build-essential

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Expose the port Flask runs on
EXPOSE 8080

# Run the app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
