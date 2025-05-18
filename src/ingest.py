import logging

logger = logging.getLogger(__name__)

def ingest_data(spark, data_path):
    try:
        logger.info("Ingesting data from %s", data_path)
        spark_df = spark.read.csv(data_path, header=True, inferSchema=True)
        if spark_df.count() == 0:
            raise ValueError("Dataset is empty")
        spark_df.persist()
        logger.info("Data ingested successfully")
        return spark_df
    except Exception as e:
        logger.error("Error during ingestion: %s", e, exc_info=True)
        raise
