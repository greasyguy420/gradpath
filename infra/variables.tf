# defines configurable infrastructure values

variable "aws_region" {
  description = "aws region for the ec2 instance"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "name used to tag project resources"
  type        = string
  default     = "gradpath"
}

variable "instance_type" {
  description = "ec2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  description = "name of an existing ec2 key pair"
  type        = string
}

variable "allowed_ssh_cidr" {
  description = "cidr block allowed to access ssh"
  type        = string
  default     = "0.0.0.0/0"
}

variable "allowed_app_cidr" {
  description = "cidr block allowed to access streamlit"
  type        = string
  default     = "0.0.0.0/0"
}

variable "repo_url" {
  description = "git repository cloned onto the ec2 instance"
  type        = string
  default     = "https://github.com/greasyguy420/gradpath.git"
}

variable "repo_branch" {
  description = "git branch deployed onto the ec2 instance"
  type        = string
  default     = "main"
}
