# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY .env /app/
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --default-timeout=100 -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Make the script file executable
RUN chmod +x sage.py

ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV DISCORD_BOT_TOKEN=$DISCORD_BOT_TOKEN
# Define the command to run the script file when the container starts
CMD ["python", "./sage.py"]