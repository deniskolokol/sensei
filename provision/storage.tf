# S3
resource "aws_s3_bucket" "models_nlp" {
    bucket = var.bucket_name_mod
    force_destroy = true
}

resource "aws_s3_bucket_versioning" "mod_bucket_ver" {
    bucket = aws_s3_bucket.models_nlp.id
    versioning_configuration {
        status = "Enabled"
    }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "mod_bucket_enc" {
  bucket = aws_s3_bucket.models_nlp.id
  rule {
    apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
    }
  }
}
