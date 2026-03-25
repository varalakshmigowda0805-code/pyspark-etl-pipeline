import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

def extract_from_github(spark, url):
    """
    Read JSON data from GitHub raw URL.
    """
    df = spark.read.option("multiline", "true").json(url)
    return df

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

github_raw_url = "https://github.com/varalakshmigowda0805-code/pyspark-etl-pipeline/blob/main/sample_data.json"

df = extract_from_github(spark, github_raw_url)
df.show(5)

# ✅ Save extracted data to Glue temp S3 path for next job
output_path = "s3://your-temp-bucket/extracted/sample_data/"

df.write.mode("overwrite").json(output_path)

print("✅ Extract job completed.")
job.commit()
