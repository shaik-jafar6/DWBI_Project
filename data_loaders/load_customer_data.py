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
def load_data_from_api(**kwargs) -> DataFrame:
    """
    Template for loading data from API
    """
    customer_schema = "customer_id integer,customer_fname string,customer_lname string,customer_email string,customer_password string,customer_street string,customer_city string,customer_state string,customer_zipcode string"

    customer_data = spark.read.format('csv').schema(customer_schema).load('/Users/jafarshaik/Downloads/customers.csv')
    return customer_data

@test
def test_output(df) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'
