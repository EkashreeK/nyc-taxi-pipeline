import logging
from pyspark.sql import functions as F

logger = logging.getLogger(__name__)

def process_data(spark_df):
    try:
        logger.info("Starting data processing")
        logger.info(f"Spark DataFrame has {spark_df.count()} rows")
        spark_df = spark_df.withColumn(
            "pickup_hour",
            F.hour(F.to_timestamp(F.col("tpep_pickup_datetime"), "yyyy-MM-dd HH:mm:ss"))
        )
        logger.info("Extracted pickup_hour column")
        aggregated_df = spark_df.groupBy("pickup_hour").agg(
            F.count("*").alias("trip_count")
        )
        logger.info(f"Aggregated DataFrame has {aggregated_df.count()} rows")
        logger.info("Data processed successfully")
        return aggregated_df
    except Exception as e:
        logger.error("Error during processing: %s", e, exc_info=True)
        raise
