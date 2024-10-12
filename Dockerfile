# Use the official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy requirements files and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose port 5000
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
