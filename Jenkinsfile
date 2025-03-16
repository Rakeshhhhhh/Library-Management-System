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
                // Pull the latest code from GitHub
                git branch: 'main', url: 'https://github.com/Rakeshhhhhh/Library-Management-System.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    bat "docker build -t %DOCKER_IMAGE% ."
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    // Run the unit tests inside the container
                    bat "docker run --rm %DOCKER_IMAGE% pytest tests/"
                }
            }
        }

        // stage('Push to DockerHub') {
        //     // when {
        //     //     branch 'main'
        //     // }
        //     steps {
        //         withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
        //             bat "docker login -u %DOCKER_USERNAME% -p %DOCKER_PASSWORD%"
        //             bat "docker push %DOCKER_IMAGE%"
        //         }
        //     }
        // }

    //     stage('Deploy to Local Server') {
    //         // when {
    //         //     branch 'main'
    //         // }
    //         steps {
    //             script {
    //                 echo "Pulling latest Docker image..."
    //                 bat "docker pull %DOCKER_IMAGE%"

    //                 echo "Stopping any old container..."
    //                 bat "docker stop %CONTAINER_NAME% || echo Container not running"

    //                 echo "Removing old container..."
    //                 bat "docker rm %CONTAINER_NAME% || echo No container to remove"

    //                 echo "Running new container with Gunicorn..."
    //                 bat "docker run -d -p 5000:5000 --name %CONTAINER_NAME% %DOCKER_IMAGE%:latest gunicorn --bind 0.0.0.0:5000 run:app"
    //             }
    //         }
    //     }
    // }
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


    post {
        failure {
            echo "Build failed. Please check the logs."
        }
        success {
            echo "Pipeline successfully completed."
        }
    }
}
}
