# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app/requirements.txt
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Expose the port that the app runs on (Flask default is 5000, but we set it to 8003 in main.py)
EXPOSE 8003

# Define the command to run the application
CMD ["python", "main.py"]
