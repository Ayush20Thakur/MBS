resource "aws_db_instance" "postgres" {
  identifier             = "sentinelflow-postgres"
  allocated_storage      = 50
  max_allocated_storage  = 200
  engine                 = "postgres"
  engine_version         = "16.1"
  instance_class         = "db.t4g.medium"
  db_name                = "sentinelflow"
  username               = "sentinel_admin"
  password               = var.db_password
  skip_final_snapshot    = true
  multi_az               = true
  storage_encrypted      = true
  publicly_accessible    = false
}
