pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'rakesh80/library-management-system:latest'
        DOCKER_HUB_CREDENTIALS = credentials('dockerhub-credentials')
        CONTAINER_NAME = 'lmsss'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Rakeshhhhhh/Library-Management-System.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build -t %DOCKER_IMAGE% ."
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    bat "docker run --rm %DOCKER_IMAGE% pytest tests/"
                }
            }
        }

        stage('Deploy to Local Server') {
            steps {
                script {
                    echo 'Deploying using local Docker image...'
                    bat """
                        docker stop library-management-container || true
                        docker rm library-management-container || true
                        docker run -d --name library-management-container -p 5000:5000 rakesh80/library-management-system:latest
                    """
                }
            }
        }
    }

    post {
        failure {
            echo "Build failed. Please check the logs."
        }
        success {
            echo "Pipeline successfully completed."
        }
    }
}
