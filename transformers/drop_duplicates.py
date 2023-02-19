from pandas import DataFrame
import math
from pyspark.sql import SparkSession
from mage_ai.data_preparation.variable_manager import get_variable
from pyspark.sql.functions import *

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def transform_helper(df):
    return df.drop_duplicates()

data_list =['load_product_data','load_customer_data','load_categories_data','load_departments','load_orders_data','load_orders_list_data']
spark = SparkSession.builder.getOrCreate()

@transformer
def transform_df(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        df (DataFrame): Data frame from parent block.

    Returns:
        DataFrame: Transformed data frame
    """

    
    # Specify your transformation logic here
    results = []
    for data in data_list:
        if data in ('load_departments','load_categories_data'):
            print(data)
            df = get_variable('retail_pipeline', data, 'output_0', variable_type='dataframe')
            df=spark.createDataFrame(df) 
        else:
            df = get_variable('retail_pipeline', data, 'output_0', variable_type='spark_dataframe', spark=spark)
        results.append(transform_helper(df))
    return results

@test
def test_output(df,*args, **kwargs) -> None:

    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'