output "storage_bucket_name" {
  value = google_storage_bucket.etl_platform_bucket.name
}

output "bigquery_dataset_self_link" {
  value = google_bigquery_dataset.etl_platform_dataset.self_link
}
