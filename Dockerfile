FROM python:3.9-slim

# Install Python dependencies
RUN pip install --no-cache-dir flask numpy pandas

# Copy application files
COPY app.py /app/app.py

# Set up working directory
WORKDIR /app

# Create symbolic link to ensure 'python' command works
RUN ln -s /usr/local/bin/python /usr/bin/python

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]