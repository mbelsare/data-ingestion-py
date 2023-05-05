import argparse

from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, split, size


# Get SparkSession
def load_spark_session() -> SparkSession:
    return SparkSession.builder \
        .master("local[8]") \
        .appName("Data Ingestion using PySpark") \
        .config('spark.sql.execution.arrow.pyspark.enabled', 'false') \
        .config('spark.driver.bindAddress', '127.0.0.1') \
        .config('spark.driver.host', 'localhost') \
        .config('spark.jars', '/usr/share/java/mysql-connector-j-8.0.33.jar') \
        .getOrCreate()


# Load input data into Spark Dataframe
def load_data(
        spark: SparkSession,
        input_path: str
) -> DataFrame:
    return spark \
        .read \
        .option("header", "true") \
        .option("inferschema", "true") \
        .csv(input_path)


# Apply filter operation to filter out null records
def filter_null_records(
        dataframe: DataFrame,
        filter_col: str
) -> DataFrame:
    return dataframe.filter(col(filter_col).isNotNull())


def filter_invalid_ip_records(
        dataframe: DataFrame
) -> DataFrame:
    return dataframe.where(size(split(col('ip_address'), '[\.]')) == 4)


def filter_invalid_email_records(
        dataframe: DataFrame
) -> DataFrame:
    return dataframe.where(col('email').contains('@'))


def ingest_data(
        input_path: str,
        mysql_host: str,
        mysql_port: str,
        mysql_db: str,
        mysql_table: str,
        db_user: str,
        db_password: str
):
    # load spark session
    spark = load_spark_session()

    # load the input dataset
    df = load_data(spark=spark, input_path=input_path)

    # filter empty records for email & IP address
    df = filter_null_records(dataframe=df, filter_col='email')
    df = filter_null_records(dataframe=df, filter_col='ip_address')

    # filter invalid email records
    df = filter_invalid_email_records(dataframe=df)

    # filter invalid IP address records
    df = filter_invalid_ip_records(dataframe=df)

    df.write.format('jdbc').options(
        url=f'jdbc:mysql://{mysql_host}:{mysql_port}/{mysql_db}',
        driver='com.mysql.cj.jdbc.Driver',
        dbtable=f'{mysql_table}',
        user=f'{db_user}',
        password=f'{db_password}') \
        .mode('overwrite') \
        .save()


def main():
    args_parser = argparse.ArgumentParser(description='Data Ingestion')
    args_parser.add_argument('--input_path',
                             required=True,
                             type=str,
                             help=f'Input path of the dataset to load'
                             )
    args_parser.add_argument('--mysql_host',
                             required=False,
                             default='localhost',
                             type=str,
                             help=f'MySQL DB hostname/IP'
                             )
    args_parser.add_argument('--mysql_port',
                             required=False,
                             default='3306',
                             type=str,
                             help=f'MySQL DB port. Default = 3306'
                             )
    args_parser.add_argument('--mysql_db',
                             required=False,
                             default='test',
                             type=str,
                             help=f'MySQL database to use for data ingestion'
                             )
    args_parser.add_argument('--mysql_table',
                             required=False,
                             default='PERSON',
                             type=str,
                             help=f'MySQL table to store the ingested data'
                             )
    args_parser.add_argument('--db_user',
                             required=False,
                             default='root',
                             type=str,
                             help=f'Username to authenticate with DB'
                             )
    args_parser.add_argument('--db_password',
                             required=False,
                             default='root',
                             type=str,
                             help=f'Password for database authentication'
                             )
    args = vars(args_parser.parse_args())
    ingest_data(**args)


if __name__ == '__main__':
    main()
