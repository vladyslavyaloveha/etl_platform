terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>5.45.0"
    }
  }
  required_version = ">=1.8.0"
}

provider "aws" {
  region     = var.region
  access_key = var.access_key_id
  secret_key = var.secret_access_key
}

module "s3_bucket" {
  version                  = "~>4.1.2"
  source                   = "terraform-aws-modules/s3-bucket/aws"
  bucket                   = var.s3_bucket
  acl                      = "private"
  force_destroy            = true
  control_object_ownership = true
  object_ownership         = "ObjectWriter"

  tags = {
    Terraform = "true"
  }
}

resource "aws_redshift_cluster" "redshift_cluster" {
  cluster_identifier                  = var.redshift_cluster_identifier
  database_name                       = var.redshift_database_name
  master_username                     = var.redshift_master_username
  master_password                     = var.redshift_master_password
  port                                = var.redshift_port
  node_type                           = var.redshift_node_type
  cluster_type                        = var.redshift_cluster_type
  number_of_nodes                     = var.redshift_number_of_nodes
  automated_snapshot_retention_period = var.redshift_automated_snapshot_retention_period

  apply_immediately     = true
  encrypted             = true
  publicly_accessible   = true
  skip_final_snapshot   = true
  allow_version_upgrade = true
  enhanced_vpc_routing  = true

  tags = {
    Terraform = "true"
  }
}
