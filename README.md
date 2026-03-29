# ✅ README.md — Hudi ETL Pipeline (AWS Glue)

## Hudi ETL Pipeline using AWS Glue

This repository contains a complete **end‑to‑end ETL pipeline** built using **AWS Glue (PySpark)**.  
The pipeline reads raw data from **GitHub**, performs transformations, applies **SCD Type‑2 logic**, and finally writes curated data into an **Apache Hudi table on Amazon S3**.

---

## ✅ Architecture Workflow

```
Extract (GitHub JSON)
       ↓
Transform (Add timestamps, business logic)
       ↓
SCD Type‑2 Job (record_key, start_time, end_time, current_flag)
       ↓
Hudi Write Job (Upsert into Hudi COW table on S3)
```

---

## ✅ Folder Structure

```
hudi-etl-pipeline/
│── glue/
│    ├── extract_job.py          # Read JSON from GitHub raw URL
│    ├── transform_job.py        # Apply transformations
│    ├── scd_job.py              # SCD Type‑2 logic
│    ├── hudi_job.py             # Write/Upsert to Hudi table
│
│── step-functions/
│    └── glue_hudi_pipeline.json # AWS Step Functions orchestration
│
│── data/
│    └── sample_data.json        # Sample dataset for testing
│
└── README.md
```

---

## ✅ 1. Extract Job

**File:** `glue/extract_job.py`

This job reads JSON data from a **GitHub raw URL** using PySpark and writes it to a temporary S3 location.

- **Input:** `sample_data.json` from GitHub  
- **Output:**  
  ```
  s3://your-temp-bucket/extracted/sample_data/
  ```

---

## ✅ 2. Transform Job

**File:** `glue/transform_job.py`

This job reads the extracted JSON and applies transformations:

- Adds `processed_timestamp`
- Adds partition columns `year` and `month`

**Output path:**
```
s3://your-temp-bucket/transformed/sample_data/
```

---

## ✅ 3. SCD Type‑2 Job (Separate)

**File:** `glue/scd_job.py`

This job enriches transformed data with **SCD Type‑2 metadata**:

- `record_key`
- `precombine_key`
- `is_current`
- `start_time`
- `end_time` (`9999‑12‑31` for active records)

**Output path:**
```
s3://your-temp-bucket/scd2/sample_data/
```

---

## ✅ 4. Hudi Write Job (Separate)

**File:** `glue/hudi_job.py`

This job writes the SCD‑ready data into **Apache Hudi** using the **UPSERT** operation.

### Hudi Configuration
- **Table Type:** Copy‑On‑Write (COW)
- **Operation:** Upsert
- **Record Key:** `record_key`
- **Precombine Key:** `precombine_key`

**Output path:**
```
s3://your-output-bucket/hudi/customer_hudi_table/
```

---

## ✅ AWS Step Functions Orchestration

**File:** `step-functions/glue_hudi_pipeline.json`

This pipeline is orchestrated using **AWS Step Functions**, ensuring **sequential execution** and failure handling for all Glue jobs.

### 🔹 Orchestration Flow

```
Extract Glue Job
      ↓
Transform Glue Job
      ↓
SCD Type‑2 Glue Job
      ↓
Hudi Write Glue Job
```

### 🔹 Key Features

- Uses `glue:startJobRun.sync` for synchronous execution
- Ensures strict job ordering
- Built‑in failure handling and observability
- Production‑ready orchestration

### 🔹 Managed Glue Jobs

- `extract_job`
- `transform_job`
- `scd_job`
- `hudi_job`

---

## ✅ Sample Data File

A sample dataset (`sample_data.json`) is included under the `data/` directory.

**Example record:**
```json
{
  "id": 1,
  "name": "John",
  "city": "Bangalore",
  "amount": 5000,
  "updated_at": "2026-03-01"
}
```

---

## ✅ Technologies Used

| Component | Purpose |
|---------|---------|
| AWS Glue | Serverless ETL execution |
| PySpark | Data processing & transformations |
| Apache Hudi | Incremental storage & SCD management |
| Amazon S3 | Data lake storage |
| AWS Step Functions | Workflow orchestration |
| GitHub | Code & raw data hosting |

---

## ✅ How to Run This Pipeline

### Step 1: Create Glue Jobs

- `extract_job`
- `transform_job`
- `scd_job`
- `hudi_job`

### Step 2: Set Job Parameters

- **Glue Version:** 4.0 / 3.0
- **Worker Type:** G.1X or above
- **Python Version:** 3

### Step 3: Trigger Pipeline

- Manually execute Glue jobs **or**
- Trigger via **AWS Step Functions**

### Step 4: Validate Output

- Query using **Amazon Athena**
- Or **EMR / Spark SQL**

---

## ✅ Future Enhancements

✅ Add EventBridge scheduling  
✅ Add retries and alerting in Step Functions  
✅ Terraform / CloudFormation IaC  
✅ CI/CD with GitHub Actions  
✅ Incremental Delta ingestion support  

---

## ✅ Author

**Varalakshmi G**  
Senior Data Engineer  
Specialized in **AWS, GCP, Databricks, PySpark, Apache Hudi**
