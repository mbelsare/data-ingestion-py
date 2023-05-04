from pyspark.sql import SparkSession


def load_spark_session() -> SparkSession:
    return SparkSession.builder \
            .master("local[8]") \
            .appName("Data Ingestion using PySpark") \
            .config('spark.sql.execution.arrow.pyspark.enabled', 'false') \
            .config('spark.driver.bindAddress', '127.0.0.1') \
            .config('spark.driver.host', 'localhost') \
            .getOrCreate()
