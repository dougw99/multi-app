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

# Expose the port that the app runs on (Streamlit default is 8501)
EXPOSE 8501

# Define the command to run the application
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0"]
