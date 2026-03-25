✅ README.md — Hudi ETL Pipeline (AWS Glue)
Hudi ETL Pipeline using AWS Glue
This repository contains a complete end‑to‑end ETL pipeline built using AWS Glue (PySpark).
The pipeline reads raw data from GitHub, performs transformations, applies SCD Type‑2 logic, and finally writes the curated data into an Apache Hudi table on Amazon S3.

✅ Architecture Workflow
Extract (GitHub JSON)
       ↓
Transform (Add timestamps, business logic)
       ↓
SCD Type‑2 Job (Add record_key, start_time, end_time, current_flag)
       ↓
Hudi Write Job (Upsert into Hudi COW table on S3)


✅ Folder Structure
hudi-etl-pipeline/
│── glue/
│    ├── extract_job.py          # Read JSON from GitHub raw URL
│    ├── transform_job.py        # Apply transformations
│    ├── scd_job.py              # SCD Type‑2 logic
│    ├── hudi_job.py             # Write/Upsert to Hudi table
│
│── data/
│    └── sample_data.json        # Sample dataset for testing
│
└── README.md


✅ 1. Extract Job
File: glue/extract_job.py
This job reads JSON data from a GitHub raw URL using PySpark and writes it to a temporary S3 location.

Input: sample_data.json from GitHub
Output: s3://your-temp-bucket/extracted/sample_data/


✅ 2. Transform Job
File: glue/transform_job.py
This job reads extracted JSON and applies transformations:

Adds processed_timestamp
Adds partition columns year and month

Output is stored in:
s3://your-temp-bucket/transformed/sample_data/

✅ 3. SCD Type‑2 Job (Separate)
File: glue/scd_job.py
This job enriches transformed data with SCD Type‑2 metadata:

record_key
precombine_key
is_current
start_time
end_time (9999‑12‑31)

Output path:
s3://your-temp-bucket/scd2/sample_data/

✅ 4. Hudi Write Job (Separate)
File: glue/hudi_job.py
This job writes the SCD‑ready data to Apache Hudi using UPSERT operation.
Hudi configuration:

Table type: Copy-On-Write
Operation: Upsert
Record key: record_key
Precombine key: precombine_key

Output path:
s3://your-output-bucket/hudi/customer_hudi_table/

✅ Sample Data File
A sample dataset (sample_data.json) is placed inside data/ folder for testing locally or via GitHub Raw URL.
Example record:
JSON{  "id": 1,  "name": "John",  "city": "Bangalore",  "amount": 5000,  "updated_at": "2026-03-01"}Show more lines

✅ Technologies Used

Component	Purpose
AWS Glue	Serverless ETL execution
PySpark	Data processing & transformations
Apache Hudi	Incremental storage & SCD management
Amazon S3	Data lake storage
GitHub	Raw data hosting & code repository

✅ How to Run This Pipeline
Step 1: Upload All Scripts to Glue Jobs
Create these Glue Jobs:

extract_job
transform_job
scd_job
hudi_job

Step 2: Set Job Parameters
Choose:

Glue Version: 4.0 / 3.0
Worker Type: G.1X or above
Python Version: 3

Step 3: Run in Order
Extract → Transform → SCD → Hudi

Step 4: Validate Hudi Table
Use Athena or EMR/Spark to verify Hudi output.

✅ Future Enhancements
✅ Add Glue Workflow to automate job chaining
✅ Add CI/CD deployment using GitHub Actions
✅ Add Terraform/CloudFormation for infra creation
✅ Add Delta file support for incremental loads

✅ Author
Varalakshmi G
Senior Data Engineer
Specialized in AWS, GCP, Databricks, PySpark, Apache Hudi
