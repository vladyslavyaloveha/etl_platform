variable "region" {
  type    = string
  default = "us-east-1"
}

variable "access_key_id" {
  type      = string
  sensitive = true
}

variable "secret_access_key" {
  type      = string
  sensitive = true
}

variable "s3_bucket" {
  type    = string
  default = "etl-platform"
}

variable "redshift_cluster_identifier" {
  type    = string
  default = "etl-platform"
}

variable "redshift_node_type" {
  type    = string
  default = "dc2.large"
}
variable "redshift_cluster_type" {
  type    = string
  default = "multi-node"
}

variable "redshift_number_of_nodes" {
  type    = number
  default = 2
  validation {
    condition     = var.redshift_number_of_nodes >= 1 && var.redshift_number_of_nodes <= 5
    error_message = "The number of nodes must be in range [1, 5]"
  }
}
variable "redshift_automated_snapshot_retention_period" {
  type    = number
  default = 15
}

variable "redshift_database_name" {
  type    = string
  default = "etl_platform"
}

variable "redshift_master_username" {
  type    = string
  default = "master"
}

variable "redshift_master_password" {
  type      = string
  sensitive = true
}

variable "redshift_port" {
  type    = string
  default = "5439"
}
