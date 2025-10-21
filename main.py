from enum import Enum # Для использования Enum
from typing import List, Optional # Для подсказок типов (списки и необязательные значения)

class Gender(Enum):
    """Пол питомца или владельца"""
    MALE = "Мужской"
    FEMALE = "Женский"


class DogBreed(Enum):
    """Породы собак"""
    LABRADOR = "Лабрадор"
    HUSKY = "Хаски"
    SHEPHERD = "Овчарка"


class CatBreed(Enum):
    """Породы кошек"""
    MAINE_COON = "Мейн-кун"
    PERSIAN = "Персидская"
    SPHINX = "Сфинкс"


class Color(Enum):
    """Цвет питомца"""
    BLACK = "Черный"
    WHITE = "Белый"
    RED = "Рыжый"
    GRAY = "Серый"
    BROWN = "Коричневый"


class Disease(Enum):
    """Болезни питомца"""
    FLU = "Грипп"
    PARASITES = "Паразиты"
    ALLERGY = "Аллергия"


class Vaccine(Enum):
    """Вакцины для питомца"""
    FLU_SHOT = "Прививка от гриппа"
    PARASITE_SHOT = "Привика от паразитов"
    GENERAL_SHOT = "Общая вакцина"


class Owner:
    """Владелец питомца"""
    def __init__(self, name: str, age: int, gender: Gender):
        self.name = name
        self.age = age
        self.gender = gender
        self.pets: List['Pet'] = []


class PetDocument:
    """Родительский класс для документов питомца"""
    def __init__(self, issue_date: str, pet_name: str, owner: Owner, gender: Gender):
        self.issue_date = issue_date
        self.pet_name = pet_name
        self.owner = owner
        self.gender = gender


class Passport(PetDocument):
    """Паспорт питомца"""
    def __init__(self, issue_date: str, pet_name: str, owner: Owner, gender: Gender,  pet_type: str, breed: str, color: Color):
        super().__init__(issue_date, pet_name, owner, gender)
        self.pet_type = pet_type
        self.breed = breed
        self.color = color


class MedicalCard(PetDocument):
    """Медицинская карта питомца"""
    def __init__(self, issue_date: str, pet_name: str, owner: Owner, gender: Gender):
        super().__init__(issue_date, pet_name, owner, gender)
        self.diseases: List[Disease] = []
        self.vaccines: List[Vaccine] = []


class Pet:
    def __init__(self, name: str, age: int, gender: Gender, color: Color):
        """Родительский класс для питомца"""
        self.name = name
        self.age = age
        self.gender = gender
        self.color = color
        self.passport: Optional[Passport] = None # Паспорт питомца
        self.medical_card: Optional[MedicalCard] = None # Медкарта питомца


class Dog(Pet):
    """Класс собаки"""
    def __init__(self, name: str, age: int, gender: Gender, color: Color, breed: DogBreed):
        super().__init__(name, age, gender, color)
        self.breed = breed


class Cat(Pet):
    """Класс кошки"""
    def __init__(self, name: str, age: int, gender: Gender, color: Color, breed: CatBreed):
        super().__init__(name, age, gender, color)
        self.breed = breed


class Organization:
    """Родительский класс для организаций"""
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address


class PetShop(Organization):
    """"Зоомагазин"""
    def __init__(self, name: str, address: str):
        super().__init__(name, address)
        self.sales: List[dict] = [] # Записи о продажах


class VetClinic(Organization):
    """Ветеринарная клиника"""
    def __init__(self, name: str, address: str):
        super().__init__(name, address)
        self.records: List[dict] = [] # Записи о посещениях