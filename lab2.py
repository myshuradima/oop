from abc import ABC, abstractmethod

class Worker(ABC):
    def __init__(self, name, phone, login, password, department_num):
        self.__name = name
        self.__phone = phone
        self.__login = login
        self.__password = password
        self.__department_num = department_num

    def set_department(self, department_num):
        self.__department_num = department_num

    def get_name(self):
        return self.__name

    def get_phone(self):
        return self.__phone

    def get_login(self):
        return self.__login

    def get_password(self):
        return self.__password

    def get_department_num(self):
        return self.__department_num

    def set_department(self, new_password):
        self.__password = new_password

    @abstractmethod
    def calculate_salary(self):
        pass


class Employee(Worker):
    def __init__(self, name, phone, login, password, department_num, next_working_day, amount_of_days):
        super().__init__(name, phone, login, password, department_num)
        self.__next_working_day = next_working_day
        self.__amount_of_days = amount_of_days

    def create_order(self,g_name, s_name, g_address, s_address, g_area, s_area, g_city, s_city, g_region, s_region, g_phone, s_phone, weight, volume):
        getter_id= g_phone + "_" + g_city
        sender_id = s_phone + "_" + s_city
        client1 = Client(getter_id, g_name, g_phone, g_address, g_area, g_city, g_region)
        client2 = Client(sender_id, s_name, s_phone, s_address, s_area, s_city, s_region)
        department = self.get_department_num()
        login = self.get_login()
        package = Package(0, client1, client2, department, login, "not delivered", weight, volume)
        #print(client1.get_info())
        #print(client2.get_info())
        return client1, client2, package

    def get_next_working_day(self):
        return self.__next_working_day

    def get_amount_of_days(self):
        return self.__amount_of_days

    def calculate_salary(self):
        pass

class Client():
    def __init__(self, id, name, phone, address, district, city, region):
        self.__id = id
        self.__name = name
        self.__phone = phone
        self.__address = address
        self.__district = district
        self.__city = city
        self.__region = region

    def get_name(self):
        return self.__name

    def get_phone(self):
        return self.__phone

    def get_address(self):
        return self.__address

    def get_district(self):
        return self.__district

    def get_city(self):
        return self.__city

    def get_region(self):
        return self.__region


class Package():
    def __init__(self, number, getter, sender, current_place, checked_by, status, weight, volume):
        self.__number = number
        self.__getter = getter
        self.__sender = sender
        self.__current_place = current_place
        self.__checked_by = checked_by
        self.__status = status
        self.__weight = weight
        self.__volume = volume

    def get_number(self):
        return self.__number

    def get_getter(self):
        return self.__getter

    def get_sender(self):
        return self.__sender

    def get_current_place(self):
        return self.__current_place

    def get_checked_by(self):
        return self.__checked_by

    def get_status(self):
        return self.__status

    def get_weight_volume(self):
            return self.__weight, self.__volume

    def check(self, employee):
        self.__checked_by = employee.get_login()
        self.__current_place = employee.get_department_num()

    def next_move(self, dept_num):
        pass


class Department():
    def __init__(self, number, type, telephone, address, district, city, region, free_volume):
        self.__number = number
        self.__type = type
        self.__telephone = telephone
        self.__address = address
        self.__district = district
        self.__city = city
        self.__region = region
        self.__free_volume = free_volume

    def get_free_volume(self):
        return self.__free_volume

    def get_number(self):
        return self.__number

    def get_type(self):
        return self.__type

    def get_telephone(self):
        return self.__telephone

    def get_address(self):
        return self.__address

    def get_district(self):
        return self.__district

    def get_city(self):
        return self.__city

    def get_region(self):
        return self.__region

    def set_free_volume(self, new_free_volume):
        self.__free_volume = new_free_volume


class Transport():
    def __init__(self, id, max_volume, max_weight, current_place):
        self.__id = id
        self.__max_volume = max_volume
        self.__max_weight = max_weight
        self.__current_place = current_place

    def create_list(self, free_volume, dept_address, dept_district, dept_city, dept_region, dept_type):
        pass
        # create package list
        # program choose from that list packages
        # check cars and dept free volumes and weights


class Courier(Employee, Transport):
    def __init__(self,name, phone, login, password, department_num, next_working_day, amount_of_days, max_volume, max_weight):
        super().__init__(name, phone, login, password, department_num, next_working_day, amount_of_days)
        self.__max_volume = max_volume
        self.__max_weight = max_weight

    def create_list(self):
        pass
        # create package list
        # courier choose from that list packages
        # check cars and dept free volumes and weights


class Admin(Worker):
    def __init__(self, name, phone, login, password, department_num):
        super().__init__(name, phone, login, password, department_num)

    def create_employee(self, name, phone, login, password, department_num):
        next_working_day = '00/00/0000'
        amount_of_days = 0
        emp = Employee(name, phone, login, password, department_num, next_working_day, amount_of_days)
        return emp

    def set_working_days(self):
        pass

    def calculate_salary(self):
        pass