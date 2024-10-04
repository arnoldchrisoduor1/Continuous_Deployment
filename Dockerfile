# We'll use the official python image as a base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copying the requirements file into the container.
COPY requirements.txt .

# Installing dependancies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container.
COPY . .

# Expose the port that your app runs on
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=app.py

# Command to run the Flak app
CMD ["python", "app.py"]