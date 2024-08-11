pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'vigneshsundaram1006/bigmartsales:latest'
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials'
    }
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/216vignesh/Big-Mart-Sales-Prediction.git', branch: 'main'
            }
        }
        stage('Setup Python Environment') {
            steps {
                bat 'python -m venv venv'
                bat '.\\venv\\Scripts\\activate'
                bat 'pip install --user -r requirements.txt'
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
        stage('Login to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKER_CREDENTIALS_ID) {
                        bat "docker push $DOCKER_IMAGE"
                    }
                }
            }
        }
        
        stage('Trigger Airflow Deployment') {
            steps {
                script {
                    // Make sure to update your API URL and add authentication if needed
                    bat "curl -X POST -H 'Content-Type: application/json' -d '{\"conf\": {\"image_tag\": \"${DOCKER_IMAGE}\"}}' http://localhost:8080/api/v1/dags/deploy_docker_image/dagRuns"
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
