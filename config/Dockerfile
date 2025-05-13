FROM python:3.9-slim
WORKDIR /app

# Install Java and procps (for ps command)
RUN apt-get update && apt-get install -y \
    openjdk-17-jre-headless \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Install Python dependencies
COPY config/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download MongoDB Spark Connector JAR
RUN mkdir -p /app/jars && \
    curl -o /app/jars/mongo-spark-connector_2.12-10.3.0.jar \
    https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.12/10.3.0/mongo-spark-connector_2.12-10.3.0.jar

# Copy application files
COPY src/ src/
COPY nyc_taxi_data.csv .

EXPOSE 5000
CMD ["python", "src/pipeline.py"]