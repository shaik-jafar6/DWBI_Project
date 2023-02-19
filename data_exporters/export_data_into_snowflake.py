from mage_ai.data_preparation.repo_manager import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.snowflake import Snowflake
from pandas import DataFrame
from os import path
from mage_ai.data_preparation.variable_manager import get_variable
from pyspark.sql import SparkSession

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

spark = SparkSession.builder.getOrCreate()
def fix_date_cols(df, tz='UTC'):
    cols = df.select_dtypes(include=['datetime64[ns]']).columns
    for col in cols:
        df[col] = df[col].dt.tz_localize(tz)
    return df

@data_exporter
def export_data_to_snowflake(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a Snowflake warehouse.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading
    """
    data = ['products','customers','categories','departments','orders','order_items']
    for i in range(0,6):
        table_name = data[i]
        df = get_variable('retail_pipeline', 'drop_duplicates', 'output_'+str(i), spark=spark)
        df = df.toPandas()
        if table_name in ('orders'):
            print(table_name)
            df = fix_date_cols(df)
        else:
            df =df

        database = 'RETAIL'
        schema = 'RETAIL_DATA'
        config_path = path.join(get_repo_path(), 'io_config.yaml')
        config_profile = 'default'
        with Snowflake.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
            loader.export(
            df,
            table_name,
            database,
            schema,
            if_exists='replace',  # Specify resolution policy if table already exists
        )