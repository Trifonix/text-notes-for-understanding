    # @classmethod  # Это декоратор из которого состоит метод класса (но декоратор не считается составным элементом класса отдельным)
    def do_sound():  # метод класса  он считается не реализованным если в нем отсутствует бизнес логика.
        pass


    def do_drive():  # метод класса
        pass


    def do_fuel():  # Абстрация - это тоже прием в ООП, когда родительский класс является интерфейсом для всех дочерних ему присущих
        pass


    def move(person: Person):
        person.do_moving()

    # Интерфейсом является класс родитель, у которого ни в одном методе нет реализованной бизнес логики.
    # Что такое интерфейс и Абстрактный класс. В чем разница? *
    # Абстрактым классом является родитель, у которого есть как методы без реализации так и какие-то методы с реализацией.

MyTransport.DATABASE_URL = "dfijefeifjefijef"

class Engine:
    """ Это двигатель для машины. """
    def __init__(self, power, price):
        self.power = power
        self.price = price

    
class Car(MyTransport):  # Здесь происходит обычное наследования (посмотреть что такое C3 алгоритм при параллельном наследовании и __mro__*)
    def __init__(self, price, color, engine):
        super().__init__()  # Посмотреть какие аргументы могут быть у функции super() и как ей пользоваться при параллельном наследовании.
        self.price = price
        self.color = color
        self.engine = Engine(power=100, price=9999)  # Пример использования композиции. (это один из приемов ооп на равне с Наследованием полимофризмом и тд..)


    # @classmethod
    # Переопределение метода родительского класса в дочернем с сохранением контракта называется Мнимым Полиморфизмом (ad-hoc). (посмотреть как это выглядит в других примерах и посмотреть что такое истинный полиморфизм.)
    def do_sound():  # это будет переопределением метода вне зависимости от того есть ли бизнес логика в MyTransport или нет.
        return "би-би"

    def do_drive():
        return "ездит"


class Horse(MyTransport):
    def __init__(self, price, color):
        super().__init__()
        self.price = price
        self.color = color


    # @classmethod
    def do_sound():  # это будет переопределением метода вне зависимости от того есть ли бизнес логика в MyTransport или нет.
        return "игого"

    def do_drive():
        return "скакать"


# SOLID это чисто собесная история.
    



a = 10
# print(MyTransport.a)
print(a)

ferrari = Car(1000, "черный", "V12")
ferrari.material_type_korpus = ""
ferrari._material_type_salon = "вшаоуауша"  # private method
ferrari.__material_type_engine = "fefef"
white_horse = Horse(1000, "white")

# GoF-паттерны их знание (Пораждающие (singleton, builder...), пару структурных дополнительно, концептуально третья группа.)