# Use the official Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the backend's requirements file into the container
COPY requirements.txt .

RUN apt-get update && apt-get install -y curl
# Install the necessary Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code into the container
COPY . .

# Expose the port your FastAPI app will run on (default 8000)
EXPOSE 8000

# Define the command to run the FastAPI app with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]