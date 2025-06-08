pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "quartuss/flask-app"
        DOCKER_IMAGE_TAG = "latest"
        DOCKER_REGISTRY_CREDENTIALS_ID = 'docker-hub-credentials' // ID учетных данных в Jenkins
    }

    stages {
        // Stage 1: Checkout код из Git
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/TimSV/Final-task.git'
            }
        }

        // Stage 2: Lint (проверка кода с помощью flake8)
        stage('Test/Lint') {
            steps {
                script {
                    echo 'Запуск flake8 для проверки кода...'
                    sh 'flake8 . --ignore=E501,E402' // игнорируем длинные строки и импорты сверху
                }
            }
        }

        // Stage 3: Build Docker-образ
        stage('Build') {
            steps {
                script {
                    echo "Сборка Docker-образа: ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                    sh 'docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} .'
                }
            }
        }

        // Stage 4: Push Docker-образа в registry
        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com',  DOCKER_REGISTRY_CREDENTIALS_ID) {
                        def dockerImage = docker.image("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}")
                        echo "Отправка образа в Docker Hub..."
                        dockerImage.push()
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
            echo '❌ Ошибка сборки или отправки образа'
        }
    }
}