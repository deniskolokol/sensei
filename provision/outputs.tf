output "ner1_ip_addr" {
    description = "EC2 NER 1 instance public IP address"
    value = aws_instance.sempai_ner_1.public_ip
}

output "ner2_ip_addr" {
    description = "EC2 NER 2 instance public IP address"
    value = aws_instance.sempai_ner_2.public_ip
}

output "db_instance_addr" {
    description = "AWS DB instance address"
    value = aws_db_instance.app_db_instance.address
}