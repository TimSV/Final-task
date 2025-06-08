#### Проверка с помощью Bash:

Проверка статуса:
```bash
curl http://37.9.53.14:5000/ping
```

```bash
# Получение записей из БД
curl http://37.9.53.14:5000/results
```

```bash
# Запись данных в БД
curl -X POST http://37.9.53.14:5000/submit \
     -H "Content-Type: application/json" \
     -d '{"name":"Kirill","score":88}'
```

#### Проверка с помощью cmd.exe:

Получение записей из БД:
```bash
curl http://37.9.53.14:5000/results
```

Запись данных в БД через командную строку cmd.exe:
```bash
curl -X POST http://localhost:5000/submit -H "Content-Type: application/json" -d "{\"name\":\"Serge\",\"score\":777}"
```

Запись данных в БД через командную строку cmd.exe:
```bash
curl -X POST http://37.9.53.14:5000/submit -H "Content-Type: application/json" -d "{\"name\":\"Serge\",\"score\":777}"
```

#### Проверка с помощью PowerShell:

```PowerShell
curl.exe http://37.9.53.14:5000/results
```

```powershell
# Запись данных в БД через PowerShell
curl.exe -X POST http://37.9.53.14:5000/submit -H 'Content-Type: application/json' -d '{\"name\":\"Serge\",\"score\":777}'
```
test