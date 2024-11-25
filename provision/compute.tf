# EC2 INSTANCES
resource "aws_instance" "sempai_ner_1" {
    ami             = var.ami
    instance_type   = var.ec2_instance_type
    security_groups = [aws_security_group.instances.name]
    tags = {
        Name     = var.instance_name_ner
    }
    user_data = <<-EOF
                #!/bin/bash
                echo "<h1>NER response 1</h1>" > index.html
                python3 -m http.server 8080 &
                EOF
}

resource "aws_instance" "sempai_ner_2" {
    ami             = var.ami
    instance_type   = var.ec2_instance_type
    security_groups = [aws_security_group.instances.name]
    tags = {
        Name     = var.instance_name_ner
        ExtraTag = local.extra_tag
    }
    user_data = <<-EOF
                #!/bin/bash
                echo "<h1>NER response 2</h1>" > index.html
                python3 -m http.server 8080 &
                EOF
}
