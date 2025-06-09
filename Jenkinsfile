pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "quartuss/flask-app"
        DOCKER_IMAGE_TAG = "latest"
        DOCKER_REGISTRY_CREDENTIALS_ID = 'docker-hub-credentials'
        SSH_CREDENTIALS_ID = "server-ssh-credentials"
        REMOTE_HOST = "ubuntu@37.9.53.164"
    }

    // Stage 1: Checkout код из Git
    stages {
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
                    sh 'flake8 . --ignore=E501,E402'
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

        // Stage 5: Деплой на целевой машине
        stage('Deploy via SSH') {
            steps {
                script {
                    echo "Разворачивание на удалённом сервере"

                    sshCommand(
                        hostname: REMOTE_HOST,
                        credentialsId: SSH_CREDENTIALS_ID,
                        command: '''
                            echo "Переход в папку проекта"
                            cd /home/ubuntu/flask-app || { echo "Не найдена директория"; exit 1; }

                            echo "Остановка текущего контейнера"
                            sudo docker-compose down

                            echo "Обновление образа"
                            sudo docker-compose pull

                            echo "Перезапуск сервиса"
                            sudo docker-compose up -d
                        '''
                    )
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