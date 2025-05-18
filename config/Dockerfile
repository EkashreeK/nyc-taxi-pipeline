FROM python:3.9-slim
WORKDIR /app

# Install Java, procps (for ps command), and curl
RUN apt-get update && apt-get install -y \
    openjdk-17-jre-headless \
    procps \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Install Python dependencies
COPY config/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download MongoDB Spark Connector JAR and its dependency
RUN mkdir -p /app/jars && \
    curl -o /app/jars/mongo-spark-connector_2.12-3.0.2.jar \
    https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.12/3.0.2/mongo-spark-connector_2.12-3.0.2.jar && \
    curl -o /app/jars/mongo-java-driver-3.12.14.jar \
    https://repo1.maven.org/maven2/org/mongodb/mongo-java-driver/3.12.14/mongo-java-driver-3.12.14.jar && \
    ls -lh /app/jars

# Copy application files
COPY src/ src/

EXPOSE 5000
CMD ["python", "src/main.py"]