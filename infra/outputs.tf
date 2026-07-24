# displays connection details after deployment

output "instance_public_ip" {
  description = "public ip address of the ec2 instance"
  value       = aws_instance.gradpath.public_ip
}

output "dashboard_url" {
  description = "url for the gradpath streamlit dashboard"
  value       = "http://${aws_instance.gradpath.public_ip}:8501"
}

output "ssh_command" {
  description = "ssh command template for the ec2 instance"
  value       = "ssh -i path/to/${var.key_name}.pem ec2-user@${aws_instance.gradpath.public_ip}"
}