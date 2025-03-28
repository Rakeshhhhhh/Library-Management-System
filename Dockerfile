# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first to leverage Docker's caching
COPY requirements.txt requirements.txt  

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
# ENV FLASK_APP=run.py

# Run the application when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
