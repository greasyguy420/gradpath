# GradPath Terraform Infrastructure

This Terraform setup creates one Amazon Linux 2023 EC2 instance in the default VPC. It creates a security group for SSH and Streamlit, then uses EC2 user data to install Git and Docker, clone the GradPath repository, build the existing Dockerfile, and run the dashboard on port 8501.

## Required tools

Install these tools before starting:

- Terraform 1.5 or newer
- AWS CLI
- Git
- an AWS account with permission to create EC2 instances and security groups

## Configure AWS CLI

Configure credentials for the AWS account:

```bash
aws configure
```

Enter the AWS access key, secret access key, default region, and output format when prompted. The default region in this project is `us-east-1`.

## Create an EC2 key pair

Create an EC2 key pair in the same AWS region before running Terraform. Download the private `.pem` file and keep it in a secure location. Set `key_name` to the AWS key pair name, not the local file path.

## Configure variables

Copy the example variables file:

```bash
cd infra
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` to set the key pair, repository URL, branch, allowed CIDR blocks, or other values. The repository URL can be changed there if the GradPath repository is hosted at a different URL.

Variables can also be supplied on the command line:

```bash
terraform apply \
  -var="key_name=your-key-name" \
  -var="repo_url=https://github.com/typicaleoxx/gradpath.git" \
  -var="repo_branch=main"
```

## Deploy

Run these commands from the repository root:

```bash
cd infra
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

Review the plan before confirming `terraform apply`. After deployment, Terraform displays the instance public IP, dashboard URL, and an example SSH command. Replace `<your-key-file.pem>` in the SSH command with the path to the downloaded private key.

## Destroy

Remove the EC2 instance and security group when they are no longer needed:

```bash
terraform destroy
```

Review the destroy plan before confirming it.

## Security note

The default CIDR value `0.0.0.0/0` allows access from any IP address. This is acceptable for short class testing, but real deployments should restrict `allowed_ssh_cidr` and `allowed_app_cidr` to trusted IP addresses.
