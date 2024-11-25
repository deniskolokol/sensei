variable "region" {
    description = "Defaut region for provider"
    type        = string
    default     = "eu-central-1"
}

# EC Variables
variable "instance_name_ner" {
    description = "Name of ec2 instance (NER)"
    type        = string
}

variable "ami" {
    description = "AWS image to use for ec2 instance"
    type        = string
    default     = "ami-0084a47cc718c111a" # Ubuntu Server 24.04 LTS eu-central-1
}

variable "ec2_instance_type" {
    description = "ec2 instance type"
    type        = string
    default     = "t2.micro"
}

# S3 Variables
variable "bucket_name_mod" {
    description = "Bucket name for NLP models"
    type        = string
}

# DB Variables
variable "db_name" {
    description = "DB name"
    type        = string
}

variable "db_user" {
    description = "DB username"
    type        = string
    default     = " v"
}

variable "db_pwd" {
    description = "DB password"
    type        = string
    sensitive   = true
}

# Route53
variable "domain" {
    description = "Domain for website"
    type        = string
}