from abc import ABC, abstractmethod

class ABS_Employee(ABC):
    name = "name"
    telephone = "000-00-00"
    login = "login"
    password = "string"
    department = "dept_id"

    @abstractmethod
    def calculate_salary(self):
        pass
class Employee(ABS_Employee):
    type = "employee_type"
    worked_days = 10

    def calculate_salary(self):
        return self.worked_days * 100

class Admin(ABS_Employee):

    def calculate_salary(self):
        return 1200

class Courier(ABS_Employee):
    max_weight = 0.1
    max_volume = 1.1
    orders = ["1", "2", "3"]
    orders_for_month = 0

    def calculate_salary(self):
        return self.orders_for_month * 200

class Client():
    id = "id"
    name = "name"
    telephone = "000-00-00"
    type = "sender/getter"
    home_number = "home_number"
    street = "street"
    area = "area"
    city = "city"
    region = "region"

    def __init__(self, id, name, telephone, home_number, street, area, city,region, type):
        self.id = id
        self.name = name
        self.telephone = telephone
        self.home_number = home_number
        self.street = street
        self.area = area
        self.city = city
        self.region = region
        self.type = type

class Letter():
    number = 1
    """номер посылки"""
    sender_id = "id"
    getter_id = "id"
    price = 1.1
    location = 0
    """dept_number"""

    def __init__(self, number, sender_id, getter_id, price, location):
        self.number = number
        self.sender_id = sender_id
        self.getter_id = getter_id
        self.price = price
        self.location = location



class Package(Letter):
    weight = 1.1
    volume = 1.2

    def __init__(self, number, sender_id, getter_id, price, location, weight, volume):
        self.number = number
        self.sender_id = sender_id
        self.getter_id = getter_id
        self.price = price
        self.location = location
        self.volume = volume
        self.weight = weight

class Department():
    home_number = "home_number"
    street = "street"
    area = "area"
    city = "city"
    region = "region"
    number = 0
    """номер отделения"""
    type = "type"
    max_volume = 10.0
    free_volume = 10.0

    def __init__(self, home, street, area, city, region, number, type, max_volume, free_volume):
        self.home_number = home
        self.street = street
        self.area = area
        self.city = city
        self.region = region
        self.number = number
        self.type = type
        self.max_volume = max_volume
        self.free_volume = free_volume

    def set_free_volume(self, space):
        self.free_volume = space




