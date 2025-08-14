# Use Python 3.9.23 slim image
FROM python:3.9.23-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files to container
COPY . .

# Expose port 5000 for FastAPI
EXPOSE 5000

# Command to run FastAPI app with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]

