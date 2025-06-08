pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "quartuss/flask-app"
        DOCKER_IMAGE_TAG = "latest"
        DOCKER_REGISTRY_CREDENTIALS_ID = 'docker-hub-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/TimSV/Final-task.git'
            }
        }

        stage('Test/Lint') {
            steps {
                sh 'flake8 .'
            }
        }

        stage('Build & Push with Buildx') {
            steps {
                script {
                    echo "Сборка и отправка образа с использованием Buildx"

                    // Настройка Buildx билдера
                    sh '''
                        docker buildx create --use mybuilder || docker buildx use mybuilder
                    '''

                    // Сборка и отправка
                    withDockerRegistry([credentialsId: DOCKER_REGISTRY_CREDENTIALS_ID, url: "https://registry.hub.docker.com"])  {
                        sh """
                            docker buildx build \\
                                --platform linux/amd64 \\
                                --tag \${DOCKER_IMAGE_NAME}:\${DOCKER_IMAGE_TAG} \\
                                --push \\
                                .
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo '✅ Сборка и отправка прошли успешно!'
        }
        failure {
            echo '❌ Ошибка при сборке или отправке образа'
        }
    }
}