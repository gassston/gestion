FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy entire project into the image
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the FastAPI app from app.main
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]