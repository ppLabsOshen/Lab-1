from enum import Enum


class Gender(Enum):
    MALE = "Мужской"
    FEMALE = "Женский"


class DogBreed(Enum):
    LABRADOR = "Лабрадор"
    HUSKY = "Хаски"
    SHEPHERD = "Овчарка"


class CatBreed(Enum):
    MAINE_COON = "Мейн-кун"
    PERSIAN = "Персидская"
    SPHINX = "Сфинкс"


class Owner:
    def __init__(self, name: str, age: int, gender: Gender):
        self.name = name
        self.age = age
        self.gender = gender


class Pet:
    def __init__(self, name: str, age: int, gender: Gender):
        self.name = name
        self.age = age
        self.gender = gender


class PetDocument:
    def __init__(self, issue_date: str):
        self.issue_date = issue_date


class Organization:
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address


class Dog(Pet):
    def __init__(self, breed: DogBreed):
        super().__init__()
        self.breed = breed


class Cat(Pet):
    def __init__(self, breed: CatBreed):
        super().__init__()
        self.breed = breed


class Passport(PetDocument):
    def __init__(self, name: str):
        super().__init__()
        self.name = name


class MedicalCard(PetDocument):
    def __init__(self, name: str, disease: str):
        super().__init__()
        self.name = name
        self.disease = disease


class PetShop(Organization):
    def __init__(self):
        super().__init__()


class VetClinic(Organization):
    def __init__(self):
        super().__init__()