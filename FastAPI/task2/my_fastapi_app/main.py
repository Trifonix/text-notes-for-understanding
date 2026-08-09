from fastapi import FastAPI     # импорт модуля FastAPI
from pydantic import BaseModel  # импорт модуля BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()                 # создание экземпляра приложения


''' Настройка CORS '''
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],          # разрешение на запросы из любых источников (dev-mode)
  allow_credentials=True,       # разрешение на приватные данные ?
  allow_methods=["*"],          # разрешение на все HTTP-методы (GET, POST и так далее)
  allow_headers=["*"]           # разрешение на все заголовки
)


''' Структура входящих данных '''
tasks_bd = []                   # создание БД в памяти

class Tasks(BaseModel):         # декларация дочернего класса Задачи от БазовойМодели
  title: str                    # поле Заголовок - тип Строка
  completed: bool = False       # поле Завершённость - тип Логический


@app.get("/")                   # декоратор: при GET-запросе на корень вызовет read_root()
def read_root():
  # return {"message": "Привет! Тут сервер работает!"}  # ответ сервера
  return {"status": "ok"}                               # после описания структуры входящих данных


''' Получение списка всех задач '''
@app.get("/tasks")              # декоратор: при GET-запросе на '/tasks/ вызовет get_tasks()
def get_tasks():
  return tasks_bd               # возврат списка задач


''' Добавление новой задачи '''
@app.post("/tasks")             # декоратор: при POST-запросе на '/tasks/' вызовет add_task(task)
def add_task(task: Tasks):      # функция принимает задачу в виде объекта класса Tasks
  tasks_bd.append(task)         # добавляет задачу в список
  return {"message": "Задача добавлена!", "task": task} # возврат словаря из сообщения и задачи