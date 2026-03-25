from pyspark.sql import SparkSession

def extract_from_s3(spark, input_path):
    """
    Extract raw data from S3/as of now we are using sample data file which in git .
    """
    df = spark.read.json(input_path)
    return df

if __name__ == "__main__":
    spark = SparkSession.builder.appName("ExtractData").getOrCreate()

    input_path = "https://github.com/varalakshmigowda0805-code/pyspark-etl-pipeline/blob/main/sample_data.json"
    df = extract_from_s3(spark, input_path)

    df.show(5)
