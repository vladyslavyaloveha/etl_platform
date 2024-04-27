output "s3_bucket_domain_name" {
  value = module.s3_bucket.s3_bucket_bucket_domain_name
}

output "s3_bucket_arm" {
  value = module.s3_bucket.s3_bucket_arn
}

output "redshift_cluster_endpoint" {
  value = aws_redshift_cluster.redshift_cluster.endpoint
}

output "redshift_database" {
  value = aws_redshift_cluster.redshift_cluster.database_name
}

output "redshift_cluster" {
  value = aws_redshift_cluster.redshift_cluster.cluster_identifier
}
