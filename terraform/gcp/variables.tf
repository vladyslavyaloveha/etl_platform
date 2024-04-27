variable "credentials_path" {
  type = string
}

variable "project_name" {
  type = string
}

variable "region" {
  type    = string
  default = "europe-north1"
}

variable "storage_bucket_name" {
  type    = string
  default = "etl_platform"
}

variable "storage_bucket_location" {
  type    = string
  default = "EUROPE-CENTRAL2"
}

variable "bigquery_dataset_id" {
  type    = string
  default = "etl_platform"
}

variable "bigquery_dataset_location" {
  type    = string
  default = "EU"
}

variable "bigquery_dataset_default_table_expiration_ms" {
  type    = number
  default = 3600000
}
