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

# теперь нужно заменить временный список tasks_bd на реальные запросы к БД
# в FastAPI есть механизм зависимостей Depends
""" from fastapi import FastAPI, Depends """

# беру SQLAlchemy - библиотеку для работы с БД через python-код
"""
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session
"""

# составляю URL для подключения
# dialect://username:password@host:port/database
"""
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:goodpswrd@127.0.0.1:5432/postgres"
"""

# создаю движок для подключения
""" engine = create_engine(SQLALCHEMY_DATABASE_URL) """

# создание фабрики сессий
""" SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) """

# инициализирую базовый класс для создания таблиц
""" Base = declarative_base() """

# нужно объяснить базе как выглядит таблица для задач
# создаю класс `TaskDB`, описываю колонки: id, title, completed
# при запуске программы FastAPI автоматически создаст эту таблицу в PostgreSQL
# описываю таблицу
"""
class TaskDB(Base):
  __tablename__ = "tasks"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True)
  completed = Column(Boolean, default=False)
"""

# пишу команду на создание таблицы в БД при запуске 
""" Base.metadata.create_all(bind=engine) """

# начинаю переписывать структуру входящих данных
# удаляю временный список tasks_bd
# нужно будет обновить Pydantic - составить схему данных
# разделю класс `Tasks` на два класса: TaskCreate и TaskResponse
# класс Tasks становится классом TaskCreate
# схема для получения данных от пользователя (POST-запрос)
"""
class TaskCreate(BaseModel):    
  title: str                    
  completed: bool = False
"""

# схема для отправки данных пользователю (GET-запрос, ID из БД)
"""
class TaskResponse(BaseModel):
  id: int
  title: str
  completed: bool

  model_config = {"from_attributes": True}
"""

# функция `get_db()` будет выдавать сессию БД на время запроса и закрывать
"""
def get_db():
  db = SessionLocal()
  try:
    yield db              
  finally:
    db.close()
"""

# создаю роутеры - CRUD операции с БД
# в декоратор вторым аргументом передаю список объектов TaskResponse
""" @app.get("/tasks", response_model=list[TaskResponse]) """

# внедряю зависимость от БД в get_tasks()
""" def get_tasks(db: Session = Depends(get_db)): """

# прописываю эквивалент команды `SELECT * FROM tasks;`
""" tasks = db.query(TaskDB).all() """

# функция возвращает tasks
""" return tasks """

# в добавление новой задачи также добавляю модель ответа
""" @app.post("/tasks", response_model=TaskResponse) """

# функция добавления задачи принимает вторым аргументом записимость от БД
""" def add_task(task: TaskCreate, db: Session = Depends(get_db)): """

# создаю объект для БД
""" db_task = TaskDB(title=task.title, completed=task.completed) """

# меняю `tasks_bd.append()` на `db.add()` - задача добавляется в сессию
""" db.add(db_task) """

# после добавления задачи изменение коммитится в базу
""" db.commit() """

# чтобы получить сгенерированный ID у задачи, её объект нужно обновить
""" db.refresh(db_task) """

# возврат созданной задачи
""" return db_task """

# проверяю работу программы
# запускаю Docker Desktop
# поднимаю контейнеры командой `docker-compose up -d`
""" [+] up 2/2 """

# проверяю статус запущенных контейнеров командой `docker-compose ps`
"""
my_fastapi_app-db-1        postgres         "docker-entrypoint.s…"   db        17 hours ago   Up 5 seconds   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp
my_fastapi_app-pgadmin-1   dpage/pgadmin4   "/entrypoint.sh"         pgadmin   18 hours ago   Up 5 seconds   0.0.0.0:5050->80/tcp, [::]:5050->80/tcp
"""

# устанавливаю Uvicorn `pip install 'uvicorn[standard]'`
""" Successfully installed click-8.4.2 colorama-0.4.6 h11-0.16.0 httptools-0.8.0 python-dotenv-1.2.2 pyyaml-6.0.3 uvicorn-0.52.1 watchfiles-1.2.0 websockets-17.0.1 """

# запускаю сервер Uvicorn командой `uvicorn main:app --reload`
""" INFO:     Application startup complete. """

# захожу на http://127.0.0.1:8000/docs
""" открылся Swagger """

# через POST /tasks пробую добавить две задачи
""" 200	Successful Response """

# захожу в pgAdmin: http://localhost:5050
# открываю сервер FastAPI_DB
# выбираю Databases->postgres->Schemas->public->Tables->tasks
# нажимаю ПКМ по tasks --- > View/Edit Data -> All Rows
""" открылась таблица с id, title, completed и видно две мои задачи """