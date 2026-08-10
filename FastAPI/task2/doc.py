# FastApi: фреймворк, API, бэкенд
# Проверяет типы данных, генерирует документацию

"""
Локальный сервер, обход блокировок браузера (CORS), веб-интерфейс (frontend)
"""

# Сам фреймворк, ASGI-сервер Uvicorn

"""
Создал папку `my_fastapi_app`, зашёл в неё через git bash
"""

# pip install "fastapi[standart]" uvicorn
""" WARNING: fastapi 0.135.3 does not provide the extra 'standart' """

# pip list
""" fastapi                   0.135.3 """

# Создал минимальный main.py

# uvicorn main:app --reload 
# --reload: перезагрузка сервера при изменениях в коде
""" Uvicorn running on http://127.0.0.1:8000 """
""" Получил JSON-ответ """

# перехожу на http://127.0.0.1:8000/docs
""" открылся Swagger UI, можно тестировать запросы """

# добавляю модель данных из Pydantic (библа проверки типов) и работу с памятью
""" from pydantic import BaseModel """

# создаю простой список - базу данных в памяти
""" tasks_bd = [] """

# описываю структуру входящих данных через класс
"""
class Tasks(BaseModel):
  title: str
  completed: bool = False
"""

# исправляю ответ сервера при GET-запросе на корень
""" return {"status": "ok"} """

# пишу Декоратор на получение задач
"""
@app.get("/tasks")
def get_tasks():
  return tasks_bd
"""

# пишу Декоратор на добавление задачи
"""
@app.post("/tasks")              
def add_task(task: Tasks):      
  tasks_bd.append(task)         
  return {"message": "Задача добавлена!", "task": task}
"""

# проверка через документацию
""" POST /tasks Add Task """

# жму Try it out
"""
{
  "title": "А ну-ка учи FastAPI",
  "completed": false
}
"""

# жму Execute
"""
{
  "message": "Задача добавлена!",
  "task": {
    "title": "А ну-ка учи FastAPI",
    "completed": false
  }
}
"""

# открываю GET /tasks, Try it out, Execute
"""
[
  {
    "title": "А ну-ка учи FastAPI",
    "completed": false
  }
]
"""

# CORS - механизм безопасности браузера
# Обычно браузер блокирует запросы с фронтенда (JavaScript)
# Если JS запущен на одном адресе, например `http://localhost:5500`
# А запрос направляется на другой адрес или порт, например `http://127.0.0.1:8000`
# В консоли это будет ошибка:
""" Access to fetch at ... from origin ... has been blocked by CORS policy """

# Чтобы настроить CORS в FastAPI нужно добавить middleware
# Это разрешит фронтенду обращаться к бэкенду

# импортирую класс CORSMiddleware
"""
from fastapi.middleware.cors import CORSMiddleware
"""

# пишу настройку CORS
"""
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)
"""

# связка фронт-бэк
# создаю каркас index.html
"""
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FastAPI + Frontend</title>
</head>
<body>
  ТУТ БУДЕТ РАЗМЕТКА
</body>
</html>
"""

# пишу разметку для вывода задач
"""
<h2>Список моих задач</h2>
<input type="text" id="taskTitle" placeholder="Введи задачу">
<button onclick="addTask()">Добавить задачу</button>
<ul id="taskList"></ul>
"""

# пишу скрипт
"""
<script>
  const API_URL = "http://127.0.0.1:8000";

  // Функция для получения задач от бэкенда
  async function fetchTasks() {
    const response = await fetch(`${API_URL}/tasks`);
    const tasks = await response.json();

    const list = document.getElementById("taskList");
    list.innerHTML = "";
    tasks.forEach(task => {
      const li = document.createElement("li");
      li.textContent = task.title;
      list.appendChild(li);
    });
  }

  // Функция для отправки новой задачи на бэкенд
  async function addTask() {
    const input = document.getElementById("taskTitle");
    if (!input.value) return;

    await fetch(`${API_URL}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: input.value, completed: false })
    });

    input.value = "";
    fetchTasks(); // Обновляем список
  }

  // Загружаем список при старте страницы
  fetchTasks();
</script>
"""

# проверяю работу всей системы
""" Uvicorn запущен """

# через LiveServer открываю index.html
"""
Список моих задач
Введи задачу
 Добавить задачу
Разобрать FastAPI
И получить оффер
"""



# в docker поднимаю 2 контейнера: postgresql, pgAdmin
# создаю пустой docker-compose.yml и описываю там сервисы
# название сервиса становится алиасом в сети Докера
# образ БД на Docker Hub: postgres
# обязательная переменная окружения: POSTGRES_PASSWORD
"""
services:
  db:                                 
    image: postgres
    environment:
      POSTGRES_PASSWORD: goodpswrd
"""

# добавляю второй сервис - интерфейс управления БД: pgAdmin
# образ: dpage/pgadmin4
# порты - пробрасываем порт `5050`, чтобы зайти в pgAdmin через порт `80`
# переменные окружения: логин и пароль
"""
pgadmin:
  image: dpage/pgadmin4
  ports:
    - "5050:80"
  environment:
    PGADMIN_DEFAULT_EMAIL: admin@admin.com
    PGADMIN_DEAFAULT_PASSWORD: root
"""

# запускаем docker-compose, чтобы Докер скачал образы и поднял оба контейнера
# up: поднять
# флаг -d: detached, запуск в фоновом режиме, чтобы работа контейнеров не мешала логами
""" docker-compose up 
$ docker-compose up
[+] up 3/3
 ✔ Network my_fastapi_app_default     Created                                                   0.1s
 ✔ Container my_fastapi_app-pgadmin-1 Created                                                   0.4s
 ✔ Container my_fastapi_app-db-1      Created                                                   0.5s
Attaching to db-1, pgadmin-1
pgadmin-1  | email config is {'CHECK_EMAIL_DELIVERABILITY': False, 'ALLOW_SPECIAL_EMAIL_DOMAINS': []
, 'GLOBALLY_DELIVERABLE': True}
"""

# на этом моменте у меня FastAPI на ноутбуке (хосте), а БД - в изолированном конейнере. Чтобы код достучался до БД, надо пробросить порт базы наружу. Добавляю блок ports в сервис db
"""
ports:
  - "5432:5432"
"""

# перезапускаю контейнеры через CTRL+C и CTRL+D в терминале
""" терминал закрылся """

# заново поднимаю докер с флагом -d чтобы не забивать терминал логами
# docker-compose up -d
"""
$ docker-compose up -d
[+] up 2/2
 ✔ Container my_fastapi_app-db-1      Started                                                   1.4s
 ✔ Container my_fastapi_app-pgadmin-1 Started                                                   0.8s
"""

# подключаю pgAdmin к БД по алиасу
# захожу на http://localhost:5050
# в настройках в поле «Email Address» пишу данные из environment 
""" попадаю в админку pgAdmin """

# нажимаю Add new server
# пишу имя FastAPI_DB
# на вкладке Connection->Host name пишу алиас db
# username - postgres
# password из POSTGRES_PASSWORD, жму Save
"""
вижу появился сервер и Dashboard
это визуальный интерфейс для управления базой
"""

# устанавливаю библиотеки для работы с БД
# FastAPI сам не умеет обращаться к базе, ему нужен ORM и драйвер
# pip install sqlalchemy psycopg2-binary
""" Successfully installed
greenlet-3.5.5
psycopg2-binary-2.9.12
sqlalchemy-2.0.51
typing-extensions-4.1
"""