# Use a base image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 5000

# Run the DevOps pipeline app
CMD ["python3", "devops_pipeline.py"]
