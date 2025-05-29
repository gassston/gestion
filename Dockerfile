FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Update
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project into the image
COPY . .

EXPOSE 8000

# Run the FastAPI app from app.main
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]