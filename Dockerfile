FROM python:3.9.18
WORKDIR /app/
COPY . .
COPY .env_dev .env
RUN pip install -r requirements.txt
RUN mkdir -p /app/staticfiles
RUN chmod -R 755 /app/staticfiles
EXPOSE 8000
EXPOSE 80