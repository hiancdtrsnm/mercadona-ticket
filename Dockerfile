FROM python:3.12

# Set the working directory

WORKDIR /app

# Copy the current directory contents into the container at /app

COPY . /app

# Install any needed packages using poetry

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

# Run the fastapi app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]