from pyspark.sql import functions as F

def transform_data(df):
    """
    Apply business rules and column transformations.
    """

    transformed_df = (
        df.withColumn("processed_timestamp", F.current_timestamp())
          .withColumn("year", F.year("processed_timestamp"))
          .withColumn("month", F.month("processed_timestamp"))
    )

    return transformed_df
