class GlossaryData:
    def __init__(self):
        self.terms = [
            {
                "id": 1,
                "term": "Переменная",
                "definition": "Именованная область памяти для хранения данных",
                "category": "basic",
                "examples": "x = 5\nname = 'Python'"
            },
            {
                "id": 2,
                "term": "Функция",
                "definition": "Блок кода, выполняющий определенную задачу",
                "category": "basic",
                "examples": "def greet(name):\n    return f'Hello {name}'"
            },
            {
                "id": 3,
                "term": "Класс",
                "definition": "Шаблон для создания объектов в объектно-ориентированном программировании",
                "category": "oop",
                "examples": "class Dog:\n    def __init__(self, name):\n        self.name = name"
            },
            {
                "id": 4,
                "term": "Объект",
                "definition": "Экземпляр класса, содержащий данные и методы",
                "category": "oop",
                "examples": "my_dog = Dog('Rex')"
            },
            {
                "id": 5,
                "term": "Модуль",
                "definition": "Файл с кодом Python, который можно импортировать",
                "category": "modules",
                "examples": "import math\nfrom datetime import datetime"
            },
            {
                "id": 6,
                "term": "Пакет",
                "definition": "Каталог, содержащий модули и файл __init__.py",
                "category": "modules",
                "examples": "from my_package import my_module"
            },
            {
                "id": 7,
                "term": "Список",
                "definition": "Изменяемая упорядоченная коллекция элементов",
                "category": "data_structures",
                "examples": "fruits = ['apple', 'banana', 'orange']"
            },
            {
                "id": 8,
                "term": "Кортеж",
                "definition": "Неизменяемая упорядоченная коллекция элементов",
                "category": "data_structures",
                "examples": "coordinates = (10, 20)"
            },
            {
                "id": 9,
                "term": "Словарь",
                "definition": "Неупорядоченная коллекция пар ключ-значение",
                "category": "data_structures",
                "examples": "person = {'name': 'John', 'age': 30}"
            },
            {
                "id": 10,
                "term": "Множество",
                "definition": "Неупорядоченная коллекция уникальных элементов",
                "category": "data_structures",
                "examples": "unique_numbers = {1, 2, 3, 3, 4}  # {1, 2, 3, 4}"
            }
        ]