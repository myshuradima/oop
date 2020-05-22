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
    @abstractmethod
    def get_info(self):
        pass

class Employee(Worker):
    def __init__(self, name, phone, login, password, department_num, next_working_day, amount_of_days):
        super().__init__(name, phone, login, password, department_num)
        self.__next_working_day = next_working_day
        self.__amount_of_days = amount_of_days

    def create_order(self,g_name, s_name, g_adress, s_adress, g_area, s_area, g_city, s_city, g_region, s_region, g_phone, s_phone, weight, volume):
        getter_id= g_phone + "_" + g_city
        sender_id = s_phone + "_" + s_city
        client1 = Client(getter_id, g_name, g_phone, g_adress, g_area, g_city, g_region)
        client2 = Client(sender_id, s_name, s_phone, s_adress, s_area, s_city, s_region)
        employee = self.get_info()
        package = Package(0, client1, client2, employee['department'], employee['login'], "not delivered", weight, volume)
        #print(client1.get_info())
        #print(client2.get_info())
        return client1, client2, package

    def get_info(self):
        return {'login': self._Worker__login,
                'department': self._Worker__department_num,
                'name': self._Worker__name,
                'phone': self._Worker__phone}


class Client():
    def __init__(self, id, name, phone, adress, area, city, region):
        self.__id = id
        self.__name = name
        self.__phone = phone
        self.__adress = adress
        self.__area = area
        self.__city = city
        self.__region = region
    def get_info(self):
        return {'name': self.__name,
                'phone': self.__phone}
    def get_adress(self):
        return {'adress': self.__adress,
                'area': self.__area,
                'city': self.__city,
                'region': self.__region}
c=Client("client_id","Bob","123-345-67", "12", "area", "Kyiv", "Kyivobl")


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
    def get_info(self):
        return {
            'number': self.__number,
            'getter' : self.__getter,
            'sender' : self.__sender,
            'current_place' : self.__current_place,
            'checked_by' : self.__checked_by,
            'status' : self.__status,
            'weight' : self.__weight,
            'volume' : self.__volume
        }
    def check(self, employee):
        employee_dict = employee.get_info()
        self.__checked_by = employee_dict['login']
        self.__current_place = employee_dict['department']

class Transport():
    def __init__(self, id, max_volume, max_weight):
        self.__id = id
        self.__max_volume = max_volume
        self.__max_weight = max_weight
    def cteate_list(self, package_list, dept_volume):
        free_volume = self.__max_volume
        free_weight = self.__max_weight
        package_list_2 = list()
        for el in package_list:
            temp_dict = el.get_info()
            if(free_volume - temp_dict['volume'] >= 0  and free_weight - temp_dict['weight'] >= 0 and dept_volume - temp_dict['volume'] >= 0):
                free_volume = free_volume - temp_dict['volume']
                free_weight = free_weight - temp_dict['weight']
                dept_volume = dept_volume - temp_dict['volume']
                package_list_2.append({'number': temp_dict['number'], 'city': temp_dict['getter'].get_adress()['city']})
        return package_list_2

class Courier(Employee, Transport):
    def __init__(self,name, phone, login, password, department_num, next_working_day, amount_of_days, max_volume, max_weight):
        super().__init__(name, phone, login, password, department_num, next_working_day, amount_of_days)
        self.__max_volume = max_volume
        self.__max_weight = max_weight
    def get_info(self):
        return {'login': self._Worker__login,
                'department': self._Worker__department_num,
                'name': self._Worker__name,
                'phone': self._Worker__phone}

class Department():
    def __init__(self, number, type, telephone, adress, area, city, region, free_volume):
        self.__number = number
        self.__type = type
        self.__telephone = telephone
        self.__adress = adress
        self.__area = area
        self.__city = city
        self.__region = region
        self.__free_volume = free_volume
    def get_volume(self):
        return self.__free_volume

class Admin(Worker):
    def __init__(self, name, phone, login, password, department_num):
        super().__init__(name, phone, login, password, department_num)
    def create_employee(self, name, phone, login, password, department_num):
        next_working_day = '00/00/0000'
        amount_of_days = 0
        emp = Employee(name, phone, login, password, department_num, next_working_day, amount_of_days)


newEmployee1 = Employee("Adam", "123-45-67", "adams_login", "123456", 2, "13.09.2019", 6)
newEmployee2 = Employee("Bob", "123-45-67", "bobs_login", "123456", 12, "13.09.2019", 6)
courier = Courier("Bob", "123-45-67", "bobs_login", "123456", 12, "13.09.2019", 6, 20, 30)
print(courier.get_info())
newEmployee1.set_department(3)
print(newEmployee1.get_info())
client1, client2, package =newEmployee1.create_order("Getter Name", "Sender Name", "Getter Adress", "Sender Adress",
                                                    "Getter Area", "Sender Area","Getter City", "Sender City", "Getter Region",
                                                    "Sender Region", "Getter Phone", "Sender Phone", 13, 15)
print(client1.get_info())
print(client2.get_info())
print(package.get_info())
package.check(newEmployee2)
print(package.get_info())
