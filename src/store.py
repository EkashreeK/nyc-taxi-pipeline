import logging

logger = logging.getLogger(__name__)

def store_data(spark_df):
    try:
        logger.info("Storing data in MongoDB")
        row_count = spark_df.count()
        logger.info(f"Attempting to store {row_count} rows")
        spark_df.write \
            .format("com.mongodb.spark.sql.DefaultSource") \
            .option("uri", "mongodb://mongo:27017/taxi_db.processed_data") \
            .mode("append") \
            .save()
        logger.info("Data stored successfully")
    except Exception as e:
        logger.error("Error during storage: %s", e, exc_info=True)
        raise
