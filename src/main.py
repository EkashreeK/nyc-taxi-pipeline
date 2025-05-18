import logging
import schedule
import time
from pyspark.sql import SparkSession
from ingest import ingest_data
from process import process_data
from store import store_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

DATA_PATH = "./nyc_taxi_data_small.csv"

spark = SparkSession.builder \
    .appName("NYC Taxi Data Processing") \
    .config("spark.mongodb.output.uri", "mongodb://mongo:27017/taxi_db.processed_data") \
    .config("spark.jars", "/app/jars/mongo-spark-connector_2.12-3.0.2.jar,/app/jars/mongo-java-driver-3.12.14.jar") \
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "4g") \
    .config("spark.memory.offHeap.enabled", "true") \
    .config("spark.memory.offHeap.size", "2g") \
    .config("spark.sql.shuffle.partitions", "400") \
    .config("spark.default.parallelism", "400") \
    .config("spark.mongodb.input.uri", "mongodb://mongo:27017/taxi_db.processed_data") \
    .getOrCreate()

def schedule_pipeline():
    logger.info("Starting scheduled pipeline")
    df = ingest_data(spark, DATA_PATH)
    processed_df = process_data(df)
    store_data(processed_df)

def run_scheduler():
    schedule.every(10).seconds.do(schedule_pipeline)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()
