from pyspark.sql import SparkSession

def extract_from_s3(spark, input_path):
    """
    Extract raw data from S3.
    """
    df = spark.read.json(input_path)
    return df

if __name__ == "__main__":
    spark = SparkSession.builder.appName("ExtractData").getOrCreate()

    input_path = "s3://your-bucket/raw/data/"
    df = extract_from_s3(spark, input_path)

    df.show(5)
