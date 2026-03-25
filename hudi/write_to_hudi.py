import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import functions as F

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# ✅ Input (from SCD Job)
input_path = "s3://your-temp-bucket/scd2/sample_data/"
df = spark.read.json(input_path)

# ✅ Hudi Options
hudi_options = {
    "hoodie.table.name": "customer_hudi_table",
    "hoodie.datasource.write.operation": "upsert",
    "hoodie.datasource.write.recordkey.field": "record_key",
    "hoodie.datasource.write.precombine.field": "precombine_key",
    "hoodie.datasource.write.table.type": "COPY_ON_WRITE",

    # Hive Sync (Optional)
    "hoodie.datasource.hive_sync.enable": "true",
    "hoodie.datasource.hive_sync.database": "default",
    "hoodie.datasource.hive_sync.table": "customer_hudi_table",
    "hoodie.datasource.hive_sync.mode": "hms",
}

# ✅ Hudi output path
hudi_output_path = "s3://your-output-bucket/hudi/customer_hudi_table/"
(
    df.write.format("hudi")
      .options(**hudi_options)
      .mode("append")
      .save(hudi_output_path)
)
print("✅ Hudi table write completed successfully.")
job.commit()
