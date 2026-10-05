pipeline {
    agent any

    environment {
        PATH = "C:\\Users\\Kaustubhi\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;${env.PATH}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out Employee Management project...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                bat 'docker compose build'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying Employee Management System...'

                bat '''
                    docker compose down
                    docker compose up -d
                '''
            }
        }
    }

    post {
        success {
            echo 'Employee Management System deployed successfully!'
        }

        failure {
            echo 'Deployment failed. Check the Jenkins console output.'
        }
    }
}