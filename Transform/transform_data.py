import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import functions as F

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# ✅ Input from previous job output
input_path = "s3://your-temp-bucket/extracted/sample_data/"

df = spark.read.json(input_path)

# ✅ Transformations
transformed_df = (
    df.withColumn("processed_timestamp", F.current_timestamp())
      .withColumn("year", F.year("processed_timestamp"))
      .withColumn("month", F.month("processed_timestamp"))
)

transformed_df.show(5)

# ✅ Save for next job
output_path = "s3://your-temp-bucket/transformed/sample_data/"
transformed_df.write.mode("overwrite").json(output_path)

print("✅ Transform job completed.")
job.commit()
