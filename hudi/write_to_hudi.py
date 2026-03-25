from pyspark.sql import SparkSession
from extract.extract_data import extract_from_s3
from transform.transform_data import transform_data
from scd.scd_upsert import scd2_transform

def write_to_hudi(df, hudi_path):
    """
    Write or upsert data into Apache Hudi table on S3.
    """

    hudi_options = {
        "hoodie.table.name": "customer_hudi_table",
        "hoodie.datasource.write.recordkey.field": "record_key",
        "hoodie.datasource.write.precombine.field": "precombine_key",
        "hoodie.datasource.write.table.type": "COPY_ON_WRITE",
        "hoodie.datasource.write.operation": "upsert",
        "hoodie.datasource.hive_sync.enable": "true",
        "hoodie.datasource.hive_sync.database": "default",
        "hoodie.datasource.hive_sync.table": "customer_hudi_table",
        "hoodie.datasource.hive_sync.mode": "jdbc",
        "hoodie.datasource.hive_sync.support_timestamp": "true",
    }

    (
        df.write.format("hudi")
          .options(**hudi_options)
          .mode("append")
          .save(hudi_path)
    )

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("HudiETLPipeline") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .config("spark.sql.hive.convertMetastoreParquet", "false") \
        .getOrCreate()

    
    input_path = "s3://your-bucket/raw/data/"
    raw_df = extract_from_s3(spark, input_path)

    
    transformed_df = transform_data(raw_df)

    
    scd_df = scd2_transform(transformed_df)


    hudi_path = "s3://your-bucket/hudi/customer_hudi_table/"
    write_to_hudi(scd_df, hudi_path)

    spark.stop()