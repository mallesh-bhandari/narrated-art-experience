# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Ensure the static/outputs directory exists inside the container
RUN mkdir -p static/outputs

# Expose the port Flask runs on
EXPOSE 5000

# Command to run your Flask application
CMD ["python", "app.py"]