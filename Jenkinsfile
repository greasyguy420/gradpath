pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Pulling latest repository code from GitHub...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building GradPath Docker image from Dockerfile...'
                // Builds using the Dockerfile located in the root directory
                sh 'docker build -t gradpath-app:latest .'
            }
        }

        stage('Ensure Terraform') {
            steps {
                echo 'Checking for Terraform installation...'
                sh '''
                    if ! command -v terraform &> /dev/null; then
                        apt-get update && apt-get install -y wget unzip
                        wget https://releases.hashicorp.com/terraform/1.7.0/terraform_1.7.0_linux_amd64.zip
                        unzip terraform_1.7.0_linux_amd64.zip -d /usr/local/bin/
                        rm terraform_1.7.0_linux_amd64.zip
                    fi
                '''
            }
        }

        stage('Terraform Deploy') {
            steps {
                echo 'Initializing and applying Terraform configuration in infra/ directory...'
                // Changes directory into infra/ where your team stored the .tf files
                dir('infra') {
                    sh '''
                        terraform init
                        terraform apply -auto-approve
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'GradPath deployed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check stage logs above.'
        }
    }
}
