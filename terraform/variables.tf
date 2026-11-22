variable "aws_region" {
  description = "AWS deployment region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment name"
  type        = string
  default     = "production"
}

variable "db_password" {
  description = "Master password for PostgreSQL RDS cluster"
  type        = string
  sensitive   = true
}
