# Base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the required dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the desired port
EXPOSE 9000

# Define the environment variables (adjust as needed)
ENV REDIS_HOST redis
ENV REDIS_PORT 6379
ENV REDIS_DB 0
ENV ENVIRONMENT production
ENV PORT 9000

# Start the Redis server and the application
CMD ["sh", "-c", "python hello.py"]
