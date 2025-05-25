import logging
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

logger = logging.getLogger(__name__)

# Define the schema for the NYC taxi data
schema = StructType([
    StructField("VendorID", IntegerType(), True),
    StructField("tpep_pickup_datetime", TimestampType(), True),
    StructField("tpep_dropoff_datetime", TimestampType(), True),
    StructField("passenger_count", IntegerType(), True),
    StructField("trip_distance", DoubleType(), True),
    StructField("pickup_longitude", DoubleType(), True),
    StructField("pickup_latitude", DoubleType(), True),
    StructField("RateCodeID", IntegerType(), True),
    StructField("store_and_fwd_flag", StringType(), True),
    StructField("dropoff_longitude", DoubleType(), True),
    StructField("dropoff_latitude", DoubleType(), True),
    StructField("payment_type", IntegerType(), True),
    StructField("fare_amount", DoubleType(), True),
    StructField("extra", DoubleType(), True),
    StructField("mta_tax", DoubleType(), True),
    StructField("tip_amount", DoubleType(), True),
    StructField("tolls_amount", DoubleType(), True),
    StructField("improvement_surcharge", DoubleType(), True),
    StructField("total_amount", DoubleType(), True)
])

def ingest_data(spark, data_path):
    try:
        logger.info("Ingesting data from %s", data_path)
        spark_df = spark.read.csv(data_path, header=True, schema=schema)
        row_count = spark_df.count()
        if row_count == 0:
            raise ValueError("Dataset is empty")
        logger.info("Data ingested successfully. Row count: %d", row_count)
        spark_df.persist()
        return spark_df
    except Exception as e:
        logger.error("Error during ingestion: %s", e, exc_info=True)
        raise
