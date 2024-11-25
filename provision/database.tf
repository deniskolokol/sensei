# DATABASES
resource "aws_db_instance" "app_db_instance" {
    allocated_storage   = 20
    storage_type        = "gp2"
    engine              = "postgres"
    engine_version      = "17.1"
    instance_class      = "db.t2.micro"
    db_name             = var.db_name
    username            = var.db_user
    password            = var.db_pwd
    skip_final_snapshot = true
}
