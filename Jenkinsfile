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
        stage('Preprocess Data') {
            steps {
                sh 'python scripts/preprocess.py'
            }
        }
        stage('Train Model') {
            steps {
                sh 'python scripts/train_model.py'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("$DOCKER_IMAGE")
                }
            }
        }
        stage('Trigger Airflow Deployment') {
            steps {
                script {
                    // HTTP request to Airflow's API to trigger a DAG
                    httpRequest(
                        url: 'https://0862-24-240-132-86.ngrok-free.app/api/v1/dags/deploy_docker_image/dagRuns',
                        method: 'POST',
                        contentType: 'application/json',
                        requestBody: '{"conf": {"image_tag": "' + DOCKER_IMAGE + '"}}'
                    )
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
