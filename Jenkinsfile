pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'vigneshsundaram1006/bigmartsales:latest'
    }
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/216vignesh/Big-Mart-Sales-Prediction.git', branch: 'main'
            }
        }
        stage('Setup Python Environment') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Preprocess Data') {
            steps {
                bat 'python scripts\\preprocess.py'
            }
        }
        stage('Train Model') {
            steps {
                bat 'python scripts\\train_model.py'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build -t $DOCKER_IMAGE ."
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    bat "docker push $DOCKER_IMAGE"
                }
            }
        }
        stage('Trigger Airflow Deployment') {
            steps {
                script {
                    // Make sure to update your API URL and add authentication if needed
                    bat "curl -X POST -H 'Content-Type: application/json' -d '{\"conf\": {\"image_tag\": \"${DOCKER_IMAGE}\"}}' https://0862-24-240-132-86.ngrok-free.app/api/v1/dags/deploy_docker_image/dagRuns"
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
