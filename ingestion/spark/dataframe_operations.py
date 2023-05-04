from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, split, size


def load_data(
        spark: SparkSession,
        input_path: str
) -> DataFrame:
    return spark \
        .read \
        .option("header", "true") \
        .option("inferschema", "true") \
        .csv(input_path)


def filter_null_records(
        dataframe: DataFrame,
        filter_col: str
) -> DataFrame:
    return dataframe.filter(col(filter_col).isNotNull())


def filter_invalid_ip_records(
        dataframe: DataFrame
) -> DataFrame:
    return dataframe.filter(size(split(col('ip_address'), '[\.]')) == 4)


def filter_invalid_email_records(
        dataframe: DataFrame
) -> DataFrame:
    return dataframe.where(col('email').contains('@'))
