# Pull base image
FROM python:3.7
# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code/
# Install dependencies
RUN pip install pyhumps fastapi uvicorn sqlalchemy psycopg2
COPY . /code/
EXPOSE 8000
CMD ["python", "main.py"]