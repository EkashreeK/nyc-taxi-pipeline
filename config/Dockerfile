FROM python:3.9-slim
WORKDIR /app
COPY config/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ src/
COPY nyc_taxi_data.csv .
EXPOSE 5000
CMD ["python", "src/pipeline.py"]