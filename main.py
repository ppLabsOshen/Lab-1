class Owner:
    def __init__(self, name: str, age: int, gender: str):
        self.name = name
        self.age = age
        self.gender = gender


class Pet:
    def __init__(self, name: str, age: int, id: int):
        self.name = name
        self.age = age
        self.id = id


class PetDocument:
    def __init__(self, id: int, issue_date: str):
        self.id = id
        self.issue_date = issue_date


class Organization:
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address


class Dog(Pet):
    def __init__(self, breed: str):
        super().__init__()
        self.breed = breed


class Cat(Pet):
    def __init__(self, breed: str):
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


class PetShop(Organization):
    def __init__(self):
        super().__init__()


class VetClinic(Organization):
    def __init__(self):
        super().__init__()