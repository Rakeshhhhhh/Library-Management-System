pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'rakesh80/library-management-system:latest'
        DOCKER_HUB_CREDENTIALS = credentials('dockerhub-credentials')
    }

    stages {
        stage('Checkout') {
            steps {
                // Pull the latest code from GitHub
                git branch: 'main', url: 'https://github.com/Rakeshhhhhh/Library-Management-System.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    bat 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    // Run the unit tests inside the container
                    bat 'docker run --rm $DOCKER_IMAGE pytest tests/'
                }
            }
        }

        stage('Push to DockerHub') {
            when {
                branch 'main'
            }
            steps {
                script {
                    // Push the Docker image to DockerHub if tests are successful
                    bat "docker login -u ${DOCKER_HUB_CREDENTIALS_USR} -p ${DOCKER_HUB_CREDENTIALS_PSW}"
                    bat 'docker push $DOCKER_IMAGE'
                }
            }
        }

        stage('Deploy to Local Server') {
            when {
                branch 'main'
            }
            steps {
                script {
                    // Deploy the container on the local server
                    bat 'docker pull $DOCKER_IMAGE'
                    bat 'docker run -d -p 5000:5000 $DOCKER_IMAGE'
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
