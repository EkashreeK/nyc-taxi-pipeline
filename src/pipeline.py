import pandas as pd
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pymongo import MongoClient
from flask import Flask, jsonify
import schedule
import time
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Spark session
spark = SparkSession.builder \
    .appName("NYC Taxi Data Processing") \
    .config("spark.mongodb.output.uri", "mongodb://mongo:27017/taxi_db.processed_data") \
    .getOrCreate()

# Initialize Flask app
app = Flask(__name__)

# Simulated NYC Taxi dataset path (replace with actual CSV path)
DATA_PATH = "./nyc_taxi_data.csv"

# MongoDB connection
mongo_client = MongoClient("mongodb://mongo:27017/")
db = mongo_client["taxi_db"]
collection = db["processed_data"]

def ingest_data():
    """Simulate data ingestion from CSV files."""
    try:
        logger.info("Ingesting data from %s", DATA_PATH)
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"Data file {DATA_PATH} not found")
        
        # Read CSV using Pandas for simplicity
        df = pd.read_csv(DATA_PATH)
        logger.info("Data ingested successfully")
        return df
    except Exception as e:
        logger.error("Error during ingestion: %s", e)
        raise

def process_data(df):
    try:
        logger.info("Starting data processing")
        spark_df = spark.createDataFrame(df)
        spark_df = spark_df.withColumn(
            "pickup_hour",
            F.hour(F.to_timestamp("lpep_pickup_datetime", "yyyy-MM-dd HH:mm:ss"))
        )
        aggregated_df = spark_df.groupBy(
            "pickup_hour"
        ).agg(
            F.count("*").alias("trip_count")
        )
        logger.info("Data processed successfully")
        return aggregated_df
    except Exception as e:
        logger.error("Error during processing: %s", e)
        raise

def store_data(spark_df):
    """Store processed data in MongoDB."""
    try:
        logger.info("Storing data in MongoDB")
        # Write to MongoDB
        spark_df.write \
            .format("mongo") \
            .mode("append") \
            .save()
        logger.info("Data stored successfully")
    except Exception as e:
        logger.error("Error during storage: %s", e)
        raise

def schedule_pipeline():
    """Simulate quarterly processing."""
    logger.info("Starting scheduled pipeline")
    df = ingest_data()
    processed_df = process_data(df)
    store_data(processed_df)
    logger.info("Pipeline execution completed")

# Flask API endpoints
@app.route("/api/taxi_data", methods=["GET"])
def get_taxi_data():
    """Retrieve aggregated taxi data."""
    try:
        data = list(collection.find({}, {"_id": 0}))
        return jsonify(data)
    except Exception as e:
        logger.error("Error retrieving data: %s", e)
        return jsonify({"error": str(e)}), 500

def run_scheduler():
    """Run the pipeline on a schedule (simulated quarterly)."""
    schedule.every(10).seconds.do(schedule_pipeline)  # For demo, run every 10s
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    import threading
    
    # Run Flask API in a separate thread
    flask_thread = threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000))
    flask_thread.daemon = True
    flask_thread.start()
    
    # Run scheduler
    run_scheduler()
