terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~>5.25.0"
    }
  }
  required_version = ">=1.8.0"
}

provider "google" {
  credentials = file(var.credentials_path)
  project     = var.project_name
  region      = var.region
}

resource "google_storage_bucket" "etl_platform_bucket" {
  name          = var.storage_bucket_name
  location      = var.storage_bucket_location
  force_destroy = true
}

resource "google_bigquery_dataset" "etl_platform_dataset" {
  dataset_id                  = var.bigquery_dataset_id
  location                    = var.bigquery_dataset_location
  default_table_expiration_ms = var.bigquery_dataset_default_table_expiration_ms
  delete_contents_on_destroy  = true
}
