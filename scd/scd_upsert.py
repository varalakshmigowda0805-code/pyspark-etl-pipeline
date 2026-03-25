from pyspark.sql import functions as F

def scd2_transform(df):
    """
    Add SCD Type 2 columns.
    """

    scd_df = (
        df.withColumn("record_key", F.col("id"))
          .withColumn("precombine_key", F.col("processed_timestamp"))
          .withColumn("is_current", F.lit(True))
          .withColumn("start_time", F.current_timestamp())
          .withColumn("end_time", F.lit("9999-12-31"))
    )

    return scd_df
