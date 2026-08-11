from fastapi import FastAPI, Depends                # импорт модулей
from pydantic import BaseModel                      # импорт модуля BaseModel
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session

''' Настройка базы данных '''
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:goodpswrd@127.0.0.1:5432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

''' Описание таблицы в БД, модель SQLAlchemy '''
class TaskDB(Base):
  __tablename__ = "tasks"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True)
  completed = Column(Boolean, default=False)

''' Создание таблицы в БД при запуске '''
Base.metadata.create_all(bind=engine)


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
class TaskCreate(BaseModel):    # декларация дочернего класса Задачи от БазовойМодели
  title: str                    # поле Заголовок - тип Строка
  completed: bool = False       # поле Завершённость - тип Логический

''' Структура исходящих данных '''
class TaskResponse(BaseModel):
  id: int
  title: str
  completed: bool

  model_config = {"from_attributes": True}  # настройка для Pydantic->SQLAlchemy

''' Получение сессии БД '''
def get_db():
  db = SessionLocal()
  try:
    yield db              # передача сессии роутеру
  finally:
    db.close()            # закрытие после выполнения


@app.get("/")                   # декоратор: при GET-запросе на корень вызовет read_root()
def read_root():
  # return {"message": "Привет! Тут сервер работает!"}  # ответ сервера
  return {"status": "ok"}                               # после описания структуры входящих данных


''' Получение списка всех задач '''
@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
  tasks = db.query(TaskDB).all()                # Аналог SELECT * FROM tasks;
  return tasks                                  # возврат списка задач


''' Добавление новой задачи '''
@app.post("/tasks", response_model=TaskResponse)
def add_task(task: TaskCreate, db: Session = Depends(get_db)):
  db_task = TaskDB(title=task.title, completed=task.completed)
  db.add(db_task)
  db.commit()
  db.refresh(db_task)
  return db_task