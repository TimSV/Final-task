## Описание проекта:
Данная инструкция позволяет развернуть простое Flask-приложение как локально, так и на удаленном хосте. Проект состоит из самого Flask-приложение написанного на Python и PostgreSQL в качестве СУБД.

В приложении реализованы REST API с эндпоинтами:
1. **POST /submit** - принимает данные следующего формата и сохраняет их в БД PostgreSQL:
	`{"name": "Kirill","score": 88}` 
2. **GET /results** - возвращает все записи из базы данных в формате JSON
3. **GET /ping** - возвращает статус-сообщение {"status": "ok"}

## Запуск проекта локально:
Чтобы запустить проект локально потребуются Ubuntu с установленными пакетами doker, git.

Клонируем репозиторий:
```bash
git clone https://github.com/TimSV/Final-task.git
cd Final-task/
```

Запускаем сборку с помощью docker-compose:
```bash
sudo docker-compose up -d
```

Проверяем:
```bash
curl http://localhost:5000/ping
{"status":"ok"}
```

Для завершения работы приложения:
```bash
sudo docker-compose down
```

## Запуск проекта на удаленном хосте:
Для запуска проекта на удаленном хосте потребуются дополнительные пакеты - Jenkins, python3, pip3, flake8
### Настройка Jenkins:
 1. После установки Jenkins необходимо добавить нужные плагины:
 SSH Agent Plugin, SSH Build Agents plugin, SSH Pipeline Steps, Git plugin, GitHub Branch Source Plugin, GitHub plugin, Docker Pipeline, Multiple SCMs plugin, Scriptler.
 
 2.  Добавить Credentials от GitHub, DockerHub с логином и PAT, а так же данные для подключения  по SSH к удаленному хосту и  закрытый ключ от него.
 3.  Далее необходимо добавить пользователя jenkins в группу docker для управления контейнерами.
 ```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Создание  items:
1. Выбираем "Новый item"
2.  Задаем имя и выбираем тип Pipeline
3. Добавляем описание  pipeline, в разделе Definition указываем Pipeline script from SCM
4. В подразделе SCM задаем данные для подключения к репозиторию (URL и Credantial). В разделе Branches to build указываем main ветку.

После создания Items можно запустить Pipeline в результате которого на удаленном хосте развернется Flask-приложение.

## Проверка работы приложения:
### Проверка с помощью Bash:

Проверка статуса:
```bash
curl http://37.9.53.164:5000/ping
```

Запись данных в БД:
```bash
curl -X POST http://37.9.53.164:5000/submit \
     -H "Content-Type: application/json" \
     -d '{"name":"Kirill","score":88}'
```

Получение записей из БД:
```bash
curl http://37.9.53.164:5000/results
```

### Проверка с помощью cmd.exe:
Проверка статуса:
```bash
curl http://37.9.53.164:5000/ping
```

Запись данных в БД через командную строку cmd.exe:
```bash
curl -X POST http://37.9.53.164:5000/submit -H "Content-Type: application/json" -d "{\"name\":\"Serge\",\"score\":777}"
```

Получение записей из БД:
```bash
curl http://37.9.53.164:5000/results
```

### Проверка с помощью PowerShell:
Проверка статуса:
```PowerShell
curl.exe http://37.9.53.164:5000/ping
```

Запись данных в БД через PowerShell:
```powershell
# 
curl.exe -X POST http://37.9.53.164:5000/submit -H 'Content-Type: application/json' -d '{\"name\":\"Serge\",\"score\":777}'
```

Получение записей из БД:
```PowerShell
curl.exe http://37.9.53.164:5000/results
```

## Как работает CI/CD?
**CI/CD** — это сокращение от **Continuous Integration / Continuous Delivery**

1. Разработчик делает `git push` в репозиторий GitHub
2. Далее Jenkins обнаруживает изменения
3. После чего запускается сборка:
	 a. Делается Checkout из SCM 
	 b. Полученный код проходит проверки Test/Lint
	 c. В случае успешного прохождения тестов собирается Docker Image	 
4.  Полученный образ пушится в Docker Registry (Docker Hub)
5. Затем этот образ загружается из GitHub и разворачивается на тестовый или продуктовый сервер.