FROM python:3.11-slim

WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run your app (change if needed)
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]