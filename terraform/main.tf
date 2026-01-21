# terraform/main.tf

terraform {
    required_providers {
        google = {
            source = "hashicorp/google"
            version = "4.51.0"
        }
    }
}

provider "google" {
    credentials = file("../google_credentials.json")
    project = "wallstreet-data-ops"
    region = "asia-southeast1"
}

# 1. Create GCS Bucket (Data Lake)
resource "google_storage_bucket" "data_lake" {
    name = "wallstreet-data-lake-ananyot"
    location = "ASIA-SOUTHEAST1"
    force_destroy = true
}

# 2. Create BigQuery Dataset (Data Warehouse)
resource "google_bigquery_dataset" "dataset" {
    dataset_id = "wallstreet_warehouse"
    location   = "ASIA-SOUTHEAST1"
}