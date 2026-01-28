# Wallstreet Data Ops: End-to-End Stock Analytics Pipeline 📈

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.7-red)
![GCP](https://img.shields.io/badge/Google_Cloud-Platform-yellow)
![Terraform](https://img.shields.io/badge/Terraform-IaC-purple)
![dbt](https://img.shields.io/badge/dbt-Transformation-orange)

## 📖 Project Overview
This project demonstrates a comprehensive **Data Engineering pipeline** that extracts US Stock Market data (NVDA, MSFT, GOOGL, TSLA), creates a Data Lake on Google Cloud Storage, warehouses the data in BigQuery, and performs analytical transformations using dbt.

The goal is to provide automated daily insights on stock movements and moving averages, simulating a real-world financial data platform.

---

## 🏗 Architecture
![Project Workflow](./images/wallstreet-data-ops-workflow.drawio.svg)

1.  **Infrastructure as Code:** Terraform provisions GCS Buckets and BigQuery Datasets.
2.  **Orchestration:** Airflow (running in Docker) manages the DAGs.
3.  **Extraction:** Python script fetches daily stock data from Yahoo Finance.
4.  **Load:** Data is uploaded to GCS (Data Lake) and loaded into BigQuery (Raw Layer).
5.  **Transformation:** dbt models clean the data and calculate metrics (e.g., 7-day Moving Average, Daily Returns).

---

## 🛠 Tech Stack
* **Cloud Provider:** Google Cloud Platform (GCP)
* **Infrastructure as Code:** Terraform
* **Containerization:** Docker & Docker Compose
* **Orchestration:** Apache Airflow
* **Data Warehouse:** Google BigQuery
* **Transformation:** dbt (data build tool)
* **Language:** Python, SQL

---

## 🚀 How to Run This Project

### Prerequisites
* Docker Desktop installed (4GB+ RAM recommended)
* Google Cloud Platform Account
* Terraform installed
* dbt CLI installed

### Step 1: Clone the Repository
```bash
git clone [https://github.com/ananyot-damnoenkiat/wallstreet-data-ops.git](https://github.com/ananyot-damnoenkiat/wallstreet-data-ops.git)
cd wallstreet-data-ops
```

### Step 2: Google Cloud Setup
1. Create a Service Account in GCP with Storage Admin and BigQuery Admin roles.
2. Download the JSON key and save it as google_credentials.json in the project root.
3. Note: This file is git-ignored for security.

### Step 3: Infrastructure Provisioning (Terraform)
Initialize and apply Terraform configuration to create GCS Buckets and BigQuery Datasets automatically.
```bash
cd terraform
terraform init
terraform apply
# Type 'yes' to confirm
```

### Step 4: Start Airflow (Docker)
Start the Airflow services (Webserver, Scheduler, Postgres).
```bash
cd ..
docker-compose up -d
```
Access the Airflow UI at http://localhost:8080 (Default User/Pass: airflow/airflow).

### Step 5: Trigger the Pipeline
1. In Airflow UI, find wallstreet_pipeline.
2. Toggle the switch to Unpause.
3. Click the Play button to trigger the DAG manually.
4. Wait for all tasks (extract, upload_gcs, load_bq) to turn dark green (Success).

### Step 6: Run Transformations (dbt)
Once raw data is in BigQuery, run dbt to create analytics tables.
```bash
cd dbt_project
dbt run
```
Check BigQuery: You should see a new view/table stock_analytics with calculated metrics.

---

## 💡 Design Decisions (Why I did this?)
* Why Terraform?

    * To follow Infrastructure as Code (IaC) principles. It allows the infrastructure to be version-controlled and reproducible, avoiding "ClickOps" errors in the GCP Console.

* Why dbt?

    * I decoupled the "Transformation" logic from Airflow. Airflow handles orchestration (scheduling), while dbt handles the SQL logic. This is the modern standard for maintainable ELT pipelines.

* Why Docker?

    * Ensures the environment is consistent across different machines (eliminating "it works on my machine" issues).

---

## 📈 Future Improvements
* CI/CD: Implement GitHub Actions to automatically test dbt models on Pull Requests.

* Data Quality: Add Great Expectations or dbt tests to validate data schema and null values.

* Dashboard: Connect Google Looker Studio to the BigQuery analytics table.

---

## 👤 Author
Ananyot Damnoenkiat

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ananyot-damnoenkiat)