import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import functions as F

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# ✅ Input (from transform job)
input_path = "s3://your-temp-bucket/transformed/sample_data/"

df = spark.read.json(input_path)

# ✅ Add SCD2 columns
scd_df = (
    df.withColumn("record_key", F.col("id"))
      .withColumn("precombine_key", F.col("processed_timestamp"))
      .withColumn("is_current", F.lit(True))
      .withColumn("start_time", F.current_timestamp())
      .withColumn("end_time", F.lit("9999-12-31"))
)

scd_df.show(5)

# ✅ Output SCD dataframe for next job
output_path = "s3://your-temp-bucket/scd2/sample_data/"
scd_df.write.mode("overwrite").json(output_path)

print("✅ SCD Type‑2 job completed successfully.")

job.commit()
