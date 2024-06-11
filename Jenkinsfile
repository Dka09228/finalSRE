pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the GitHub repository
                git branch: 'main', url: 'https://github.com/your-username/your-repo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image using the Dockerfile in the repository
                    docker.build("shuup:latest")
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Run the tests inside the Docker container
                    docker.image("shuup:latest").inside {
                        sh '''
                        cd /app
                        pip3 install -r requirements-tests.txt
                        pytest /Users/kima/Downloads/Telegram\\ Desktop/shuup\\ 2/shuup/shuup_tests
                        '''
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Deploy the application using docker-compose
                    sh '''
                    docker-compose down
                    docker-compose up -d
                    '''
                }
            }
        }
    }

    post {
        always {
            // Clean up the workspace after the build is complete
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
