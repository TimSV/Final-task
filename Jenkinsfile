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
                    echo 'Запуск flake8 внутри Docker-контейнера'
                    sh '''
                        docker build -t flask-app-linter .
                        docker run --rm flask-app-linter python -m flake8 . --ignore=E501,E402
                    '''
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
            echo 'Сборка успешна!'
            slackSend channel: '#jenkins', color: 'good', message: '✅ Сборка прошла успешно!'
        }
        failure {
            echo 'Ошибка сборки!'
            slackSend channel: '#jenkins', color: 'danger', message: '❌ Ошибка сборки!'
        }
    }
}