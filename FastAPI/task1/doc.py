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