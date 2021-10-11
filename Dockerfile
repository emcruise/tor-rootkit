FROM python:3.9

# Create the mountpoint
RUN mkdir /executables

# Copy dependencies to container.
COPY listener/requirements.txt .

# Copy Python necessary python source.
COPY listener/ ./listener
COPY client/ ./client

# Update the container.
RUN apt-get update && apt-get upgrade -y

# Install dependencies in order for listener to run.
RUN pip install -r requirements.txt

# Install tor package to use hidden services.
RUN apt install tor -y

# Start Listener container with listen and forward port 8843.
CMD [ "python", "./listener/listener.py", "8843", "8843" ]