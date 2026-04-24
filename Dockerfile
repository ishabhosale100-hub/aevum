FROM python:3.9

# Set working directory inside the container
WORKDIR /code

# Install system dependencies for image processing
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies and install
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy all project files from your VS Code folder
COPY . .

# CRITICAL: Grant full permissions so the app can save shielded images
RUN chmod -R 777 /code

# Run the app on the specific port Hugging Face requires (7860)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]