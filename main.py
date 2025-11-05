import json
import os
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import List, Optional
import xml.etree.ElementTree as ET
from xml.dom import minidom


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
    RED = "Рыжий"
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
    PARASITE_SHOT = "Прививка от паразитов"
    GENERAL_SHOT = "Общая вакцина"


@dataclass
class Passport:
    pet_name: str
    age: int
    color: str
    gender: str
    breed: str
    birth_date: str = field(
        default_factory=lambda: datetime.now().strftime("%d.%m.%y"))

    def __str__(self) -> str:
        return (f"Паспорт питомца: {self.pet_name}\n"
                f"  Пол: {self.gender}\n"
                f"  Цвет: {self.color}\n"
                f"  Порода: {self.breed}\n"
                f"  Дата завода: {self.birth_date}\n"
                f"  Возраст: {self.age}")


@dataclass
class MedicalCard:
    pet_name: str
    vaccinations: List[str] = field(default_factory=list)
    diseases: List[str] = field(default_factory=list)

    def add_vaccination(self, vaccine: Vaccine):
        if vaccine.value not in self.vaccinations:
            self.vaccinations.append(vaccine.value)

    def add_disease(self, disease: Disease):
        if disease.value not in self.diseases:
            self.diseases.append(disease.value)

    def __str__(self):
        vac = ", ".join(
            self.vaccinations) if self.vaccinations else "Нет прививок"
        dis = ", ".join(self.diseases) if self.diseases else "Нет болезней"
        return f"Медкарта питомца: {self.pet_name}\n  Прививки: {vac}\n  Болезни: {dis}"


@dataclass
class Pet:
    name: str
    age: int
    gender: str
    color: str
    breed: Optional[str] = None
    passport: Optional[Passport] = None
    medical_card: MedicalCard = field(init=False)

    def __post_init__(self):
        self.medical_card = MedicalCard(self.name)


@dataclass
class Dog(Pet):
    def __post_init__(self):
        super().__post_init__()
        self.passport = Passport(
            self.name, self.age, self.color, self.gender, self.breed)

    def __str__(self):
        return f"Собака {self.name}, пол {self.gender}, цвет {self.color}, возраст {self.age}"


@dataclass
class Cat(Pet):
    def __post_init__(self):
        super().__post_init__()
        self.passport = Passport(
            self.name, self.age, self.color, self.gender, self.breed)

    def __str__(self):
        return f"Кошка {self.name}, пол {self.gender}, цвет {self.color}, возраст {self.age}"

@dataclass
class Owner:
    """Владелец питомца"""
    name: str
    age: int
    gender: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def remove_pet(self, idx: int):
        if 0 <= idx < len(self.pets):
            return self.pets.pop(idx)
        return None

    def show_pets(self):
        if not self.pets:
            print("У вас пока нет питомцев.\n")
            return
        print("Ваши питомцы:\n")
        for i, pet in enumerate(self.pets, 1):
            print(f"{i}. {pet}")

    def __str__(self):
        return f"{self.name}, возраст: {self.age}, пол {self.gender}"


@dataclass
class Organization:
    name: str
    address: str


@dataclass
class PetShop(Organization):
    available_pets: List[Pet] = field(default_factory=list)
    sales: List[dict] = field(default_factory=list)

    def create_pet(self):
        print("\nСоздание питомца для магазина.")
        name = input_name("\nИмя питомца: ")
        age = input_int("\nВозраст питомца: ", 0)
        gender = choose_enum(Gender, "пол питомца").value
        color = choose_enum(Color, "цвет питомца").value
        print("\n1. Собака\n2. Кошка")
        while True:
            t = input("Выбор: ").strip()
            if t == "1":
                breed = choose_enum(DogBreed, "породу собаки").value
                pet = Dog(name, age, gender, color, breed)
                break
            elif t == "2":
                breed = choose_enum(CatBreed, "породу кошки").value
                pet = Cat(name, age, gender, color, breed)
                break
            else:
                print("Выбор: ")
        self.available_pets.append(pet)
        print(f"Питомец {pet.name} добавлен в магазин.")

    def list_available(self):
        if not self.available_pets:
            print("\nВ магазине нет питомцев.")
            return
        print(f"\nПитомцы в магазине {self.name}:")
        for i, p in enumerate(self.available_pets, 1):
            print(f"{i}. {p}")

    def sell_pet(self, owner: Owner, idx: int):
        if 1 <= idx <= len(self.available_pets):
            pet = self.available_pets.pop(idx - 1)
            owner.add_pet(pet)
            rec = {
                "owner_name": owner.name,
                "pet_name": pet.name,
                "date": datetime.now().strftime("%d.%m.%y %H:%M:%S")
            }
            self.sales.append(rec)
            return rec
        else:
            raise IndexError("Неверный индекс питомца для продажи.")


@dataclass
class VetClinic(Organization):
    records: List[dict] = field(default_factory=list)

    def treat_interactive(self, pet: Pet):
        if pet.medical_card is None:
            pet.medical_card = MedicalCard(pet.name)
        while True:
            print("\nВетклиника:")
            print("1. Добавить болезнь")
            print("2. Добавить прививку")
            print("3. Посмотреть медкарту")
            print("0. Назад")
            choice = input("Выбор: ").strip()
            if choice == "0":
                break
            if choice == "1":
                disease = choose_enum(Disease, "болезнь")
                pet.medical_card.add_disease(disease)
                rec = {
                    "pet_name": pet.name,
                    "type": "Болезнь",
                    "detail": disease.value,
                    "date": datetime.now().strftime("%d.%m.%y %H:%M:%S")
                }
                self.records.append(rec)
                print("Запись болезни добавлена.")
            elif choice == "2":
                vaccine = choose_enum(Vaccine, "вакцину")
                pet.medical_card.add_vaccination(vaccine)
                rec = {
                    "pet_name": pet.name,
                    "type": "Вакцина",
                    "detail": vaccine.value,
                    "date": datetime.now().strftime("%d.%m.%y %H:%M:%S")
                }
                self.records.append(rec)
                print("Вакцинация добавлена.")
            elif choice == "3":
                print("\n" + str(pet.medical_card))
            else:
                print("Неверный выбор.")


class DataManager:
    JSON_FILE = "data.json"
    XML_FILE = "data.xml"

    def __init__(self):
        self.owners: List[Owner] = []
        self.petshop = PetShop(name="Зоомагазин", address="ул. Главная, 1")
        self.vetclinic = VetClinic("Ветклиника", "ул. Здоровая, 2")

    def save_all(self):
        payload = {
            "owners": [asdict(o) for o in self.owners],
            "petshop": {
                "available_pets": [asdict(p) for p in self.petshop.available_pets],
                "sales": self.petshop.sales
            },
            "vetclinic": {"records": self.vetclinic.records}
        }

        # JSON
        with open(self.JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=4)

        # XML
        root = ET.Element("data")
        owners_el = ET.SubElement(root, "owners")
        for o in self.owners:
            o_el = ET.SubElement(owners_el, "owner")
            ET.SubElement(o_el, "name").text = o.name
            ET.SubElement(o_el, "age").text = str(o.age)
            ET.SubElement(o_el, "gender").text = o.gender
            pets_el = ET.SubElement(o_el, "pets")
            for p in o.pets:
                p_el = ET.SubElement(pets_el, "pet", type=p.__class__.__name__)
                ET.SubElement(p_el, "name").text = p.name
                ET.SubElement(p_el, "age").text = str(p.age)
                ET.SubElement(p_el, "gender").text = p.gender
                ET.SubElement(p_el, "color").text = p.color
                ET.SubElement(p_el, "breed").text = p.breed if p.breed else ""
                if p.passport:
                    pass_el = ET.SubElement(p_el, "passport")
                    for k, v in asdict(p.passport).items():
                        ET.SubElement(pass_el, k).text = str(v)
                if p.medical_card:
                    med_el = ET.SubElement(p_el, "medical_card")
                    vacc_el = ET.SubElement(med_el, "vaccinations")
                    for v in p.medical_card.vaccinations:
                        ET.SubElement(vacc_el, "vaccine").text = v
                    dis_el = ET.SubElement(med_el, "diseases")
                    for d in p.medical_card.diseases:
                        ET.SubElement(dis_el, "disease").text = d

        # PetShop
        petshop_el = ET.SubElement(root, "petshop")
        avail_el = ET.SubElement(petshop_el, "available_pets")
        for p in self.petshop.available_pets:
            p_el = ET.SubElement(avail_el, "pet", type=p.__class__.__name__)
            for k, v in asdict(p).items():
                if v is None:
                    continue
                if isinstance(v, dict):
                    sub = ET.SubElement(p_el, k)
                    for kk, vv in v.items():
                        ET.SubElement(sub, kk).text = str(vv)
                else:
                    ET.SubElement(p_el, k).text = str(v)
        sales_el = ET.SubElement(petshop_el, "sales")
        for s in self.petshop.sales:
            r = ET.SubElement(sales_el, "record")
            for k, v in s.items():
                ET.SubElement(r, k).text = str(v)

        # VetClinic
        clinic_el = ET.SubElement(root, "vetclinic")
        records_el = ET.SubElement(clinic_el, "records")
        for r in self.vetclinic.records:
            rec_el = ET.SubElement(records_el, "record")
            for k, v in r.items():
                ET.SubElement(rec_el, k).text = str(v)

        xml_str = minidom.parseString(
            ET.tostring(root)).toprettyxml(indent="  ")
        with open(self.XML_FILE, "w", encoding="utf-8") as f:
            f.write(xml_str)

    def load_all(self):
        if not os.path.exists(self.JSON_FILE):
            return
        try:
            with open(self.JSON_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return

        self.owners = []
        for od in data.get("owners", []):
            pets = []
            for pd in od.get("pets", []):
                cls = Dog if pd.get("breed") in [
                    b.value for b in DogBreed] else Cat
                pet = cls(pd["name"], pd["age"], pd["gender"],
                          pd["color"], pd.get("breed"))
                pets.append(pet)
            owner = Owner(od["name"], od["age"], od["gender"], pets)
            self.owners.append(owner)

        # PetShop
        ps_data = data.get("petshop", {})
        self.petshop.available_pets = []
        for pd in ps_data.get("available_pets", []):
            cls = Dog if pd.get("breed") in [
                b.value for b in DogBreed] else Cat
            pet = cls(pd["name"], pd["age"], pd["gender"],
                      pd["color"], pd.get("breed"))
            self.petshop.available_pets.append(pet)
        self.petshop.sales = ps_data.get("sales", [])

        # VetClinic
        self.vetclinic.records = data.get("vetclinic", {}).get("records", [])


def choose_enum(enum_class: Enum, title: str):
    values = list(enum_class)
    print(f"\nВыберите {title}:")
    for i, item in enumerate(values, 1):
        print(f"{i}. {item.value}")
    while True:
        choice = input("Выбор: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(values):
                return values[idx - 1]
        print("Введите корректный номер из списка.")


def input_name(prompt: str) -> str:
    while True:
        name = input(prompt).strip()
        if not name:
            print("Имя не может быть пустым.")
            continue
        if not re.match(r'^[A-ЯA-Z][а-яa-zA-Z\- ]*$', name):
            print(
                "Имя должно начинаться с заглавной буквы и содержать только буквы или пробелы")
            continue
        return name


def input_int(prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    while True:
        s = input(prompt).strip()
        if not s.isdigit():
            print("Введите целое число.")
            continue
        v = int(s)
        if min_val is not None and v < min_val:
            print(f"Значение должно быть не меньше {min_val}.")
            continue
        if max_val is not None and v > max_val:
            print(f"Значение должно быть не больше {max_val}.")
            continue
        return v


def choose_owner(manager: DataManager) -> Optional[Owner]:
    if not manager.owners:
        print("Нет владельцев.")
        return None
    print("\nВыберите владельца:")
    for i, o in enumerate(manager.owners, 1):
        print(f"{i}. {o.name} ({len(o.pets)} питомцев)")
    idx = input_int("Выбор (0 для отмены): ", 0, len(manager.owners))
    if idx == 0:
        return None
    return manager.owners[idx - 1]


def choose_pet_from_owner(owner: Owner) -> Optional[Pet]:
    if not owner.pets:
        print("У владельца нет питомцев.")
        return None
    owner.show_pets()
    idx = input_int("Выбор (0 для отмены): ", 0, len(owner.pets))
    if idx == 0:
        return None
    return owner.pets[idx - 1]


def menu_owner(manager: DataManager):
    while True:
        print("\nМеню владельцев:")
        print("1. Создать владельца")
        print("2. Просмотреть владельцев")
        print("3. Удалить владельца")
        print("4. Управлять питомцами владельца")
        print("0. Назад")
        choice = input("Выбор: ").strip()
        if choice == "0":
            break
        if choice == "1":
            name = input_name("\nИмя владельца: ")
            age = input_int("\nВозраст владельца: ", 0)
            gender = choose_enum(Gender, "пол владельца").value
            manager.owners.append(Owner(name, age, gender))
            manager.save_all()
            print("\nВладелец создан.")
        elif choice == "2":
            if not manager.owners:
                print("\nНет владельцев.")
            else:
                for o in manager.owners:
                    print("\n" + str(o))
                    o.show_pets()
        elif choice == "3":
            if not manager.owners:
                print("\nНет владельцев.")
                continue
            for i, o in enumerate(manager.owners, 1):
                print(f"{i}. {o.name}")
            idx = input_int("Выбор (0 отмена): ", 0, len(manager.owners))
            if idx == 0:
                continue
            removed = manager.owners.pop(idx - 1)
            manager.save_all()
            print(f"Владелец {removed.name} удалён.")
        elif choice == "4":
            owner = choose_owner(manager)
            if owner:
                menu_owner_pets(manager, owner)
        else:
            print("Неверный выбор.")


def menu_owner_pets(manager: DataManager, owner: Owner):
    while True:
        print(f"\nУправление питомцами владельца {owner.name}:")
        print("1. Просмотреть питомцев")
        print("2. Добавить питомца владельцу (из магазина)")
        print("3. Удалить питомца")
        print("4. Просмотреть паспорт питомца")
        print("5. Просмотреть медкарту питомца")
        print("6. Отвезти питомца в клинику")
        print("0. Назад")
        choice = input("Выбор: ").strip()
        if choice == "0":
            break
        if choice == "1":
            owner.show_pets()
        elif choice == "2":
            manager.petshop.list_available()
            if not manager.petshop.available_pets:
                continue
            idx = input_int("Выбор (0 отмена): ", 0, len(
                manager.petshop.available_pets))
            if idx == 0:
                continue
            try:
                manager.petshop.sell_pet(owner, idx)
                manager.save_all()
                print("Питомец куплен.")
            except IndexError as e:
                print(str(e))
        elif choice == "3":
            owner.show_pets()
            if not owner.pets:
                continue
            idx = input_int("Выбор (0 отмена): ", 0, len(owner.pets))
            if idx == 0:
                continue
            removed = owner.remove_pet(idx - 1)
            manager.save_all()
            print(f"Питомец {removed.name} удалён.")
        elif choice == "4":
            pet = choose_pet_from_owner(owner)
            if pet and pet.passport:
                print("\n" + str(pet.passport))
            else:
                print("У питомца нет паспорта.")
        elif choice == "5":
            pet = choose_pet_from_owner(owner)
            if pet and pet.medical_card:
                print("\n" + str(pet.medical_card))
            else:
                print("У питомца нет медкарты.")
        elif choice == "6":
            pet = choose_pet_from_owner(owner)
            if pet:
                manager.vetclinic.treat_interactive(pet)
                manager.save_all()
        else:
            print("Неверный выбор.")


def menu_petshop(manager: DataManager):
    while True:
        print("\nМеню зоомагазина:")
        print("1. Добавить питомца в магазин")
        print("2. Показать доступных питомцев")
        print("3. Показать журнал продаж")
        print("0. Назад")
        choice = input("Выбор: ").strip()
        if choice == "0":
            break
        elif choice == "1":
            manager.petshop.create_pet()
            manager.save_all()
        elif choice == "2":
            manager.petshop.list_available()
        elif choice == "3":
            if not manager.petshop.sales:
                print("Журнал продаж пуст.")
            else:
                for i, s in enumerate(manager.petshop.sales, 1):
                    print(
                        f"{i}. {s['date']} - {s['owner_name']} купил {s['pet_name']}")
        else:
            print("Неверный выбор.")


def menu_vetclinic(manager: DataManager):
    while True:
        print("\nМеню ветклиники:")
        print("1. Просмотреть записи клиники")
        print("2. Просмотреть медкарты всех питомцев")
        print("0. Назад")
        choice = input("Выбор: ").strip()
        if choice == "0":
            break
        elif choice == "1":
            if not manager.vetclinic.records:
                print("Записей нет.")
            else:
                for i, r in enumerate(manager.vetclinic.records, 1):
                    print(
                        f"{i}. {r['pet_name']}: {r['type']} — {r['detail']} ({r['date']})")
        elif choice == "2":
            for owner in manager.owners:
                for pet in owner.pets:
                    print(f"\n{pet.name}:")
                    print(pet.medical_card)
        else:
            print("Неверный выбор.")


def main():
    manager = DataManager()
    manager.load_all()
    print("Добро пожаловать.")

    while True:
        print("\nГлавное меню:")
        print("1. Владельцы")
        print("2. Зоомагазин")
        print("3. Ветклиника")
        print("4. Сохранить и выйти")
        choice = input("Выбор: ").strip()
        if choice == "1":
            menu_owner(manager)
        elif choice == "2":
            menu_petshop(manager)
        elif choice == "3":
            menu_vetclinic(manager)
        elif choice == "4":
            manager.save_all()
            print("Данные сохранены. Выход.")
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()
