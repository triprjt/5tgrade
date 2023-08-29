# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Install gunicorn
RUN pip install gunicorn

# If you have static files or database migrations, you can add them here.
# Example:
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Set environment variables
ENV DJANGO_SETTINGS_MODULE approval_system.settings
