# Use an official lightweight Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN curl -L -o model.pk1 "https://github.com/sehajgupta/tempo/releases/download/v1.0.0/model.pk1" 

# Expose the application port
EXPOSE 5000

# Define the command to run the app
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]