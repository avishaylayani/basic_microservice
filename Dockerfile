# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install dependencies using Poetry
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

RUN pip install gunicorn


# Expose the port that Gunicorn will listen on
EXPOSE 8000

# Run the app with Gunicorn
CMD ["gunicorn", "--config", "gunicorn_conf.py", "main:app"]