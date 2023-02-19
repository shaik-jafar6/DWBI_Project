import io
import pandas as pd
import requests
from pandas import DataFrame
from pyspark.sql.types import StructType, StructField, StringType,TimestampType, IntegerType
from pyspark.sql import SparkSession
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

spark = SparkSession.builder.getOrCreate()
@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything
    """
    # Specify your data loading logic here

    orders_schema = "order_id integer,order_date string,order_customer_id integer,order_status string"
    orders_data = spark.read.format('csv').schema(orders_schema).load('/Users/jafarshaik/Downloads/orders.csv')
    return orders_data


@test
def test_output(df, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'
