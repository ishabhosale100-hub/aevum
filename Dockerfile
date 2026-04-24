FROM python:3.9

# Set the working directory
WORKDIR /code

# Install system dependencies for OpenCV (if needed)
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Copy and install requirements
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy all project files
COPY . .

# Set permissions so the app can write images (crucial for Shielding)
RUN chmod -R 777 /code

# Run the app on Hugging Face's required port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]