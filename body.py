from abc import ABC, abstractmethod
import cx_Oracle
import csv
import copy


class Worker(ABC):
    def __init__(self, name, phone, login, password, department):
        self.__name = name
        self.__phone = phone
        self.__login = login
        self.__password = password
        self.__department = department

    def set_login(self, login):
        self.__login = login

    def set_department(self, department):
        self.__department = department

    def get_name(self):
        return self.__name

    def get_phone(self):
        return self.__phone

    def get_login(self):
        return self.__login

    def get_password(self):
        return self.__password

    def get_department(self):
        return self.__department

    def set_password(self, new_password):
        self.__password = new_password

    def set_name(self, name):
        self.__name = name

    def set_phone(self, phone):
        self.__phone = phone

    def set_department(self, department):
        self.__department = department

    @abstractmethod
    def calculate_salary(self):
        pass


class IDBWorker(ABC):
    @abstractmethod
    def load_from_db(self, *identification):
        pass

    @abstractmethod
    def save_to_db(self):
        pass

    @abstractmethod
    def update_in_db(self):
        pass


class Prototype(ABC):
    @abstractmethod
    def clone(self):
        pass


class Validation(ABC):
    @abstractmethod
    def validate(self):
        pass


# ------------------Employee-----------------------------
class Employee(Worker, IDBWorker, Prototype, Validation):
    def __init__(self, name, phone, login, password, department, next_working_day, amount_of_days):
        super().__init__(name, phone, login, password, department)
        self.__next_working_day = next_working_day
        self.__amount_of_days = amount_of_days

    def create_order(self, g_name, s_name, g_address, s_address, g_area, s_area, g_city, s_city, g_region, s_region,
                     g_phone, s_phone, weight, volume):
        getter = Client(0, g_name, g_phone, g_address, g_area, g_city, g_region)
        sender = Client(0, s_name, s_phone, s_address, s_area, s_city, s_region)
        package = Package(0, getter, sender, self.get_department(), self.get_login(), 'not delivered', weight, volume)
        return package

    def get_next_working_day(self):
        return self.__next_working_day

    def get_amount_of_days(self):
        return self.__amount_of_days

    def set_amount_of_days(self, amount_of_days):
        self.__amount_of_days = amount_of_days

    def calculate_salary(self):
        return self.__amount_of_days * 200

    def check_address(self, district, city, region):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")

            cursor = connection.cursor()
            query = """select * from district join city on district.city_city_id = city.city_id
                    join region on city.region_region_id = region.region_id
                    where district_name = :district and city_name = :city and region_name = :region"""
            cursor.execute(query, district=district, city=city, region=region)
            list1 = cursor.fetchone()
            connection.close()
            if list1:
                return list1[0]
            else:
                return None

        except cx_Oracle.DataError as e:
            print(e)
            return None
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading employee")
            return None

    def check_in_db(self):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")

            cursor = connection.cursor()
            query = """select login
                      from employees
                      where
                      login = :login"""
            cursor.execute(query, login=self.get_login())
            list1 = cursor.fetchone()
            query = """select login
                                  from admin
                                  where
                                  login = :login"""
            cursor.execute(query, login=self.get_login())
            list2 = cursor.fetchone()
            connection.close()
            if list1 or list2:
                return "existing"
            else:
                return None
        except cx_Oracle.DataError as e:
            print(e)
            return 1
        except cx_Oracle.DatabaseError as e:
            print(e)
            return 1
        except Exception as e:
            print("smth go wrong with loading employee")
            return 1

    @classmethod
    def load_from_db(cls, *identification):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")

            cursor = connection.cursor()
            query = """select login
                      , employee_name
                      , emp_password
                      , phone
                      , amount_of_days
                      , department_id
                      , work_date
                      from employees join schedule on employees.login = schedule.employee_id 
                      where schedule.work_date > sysdate and ROWNUM < 2
                      and login = :login and emp_password = :password"""
            cursor.execute(query, login=identification[0], password=identification[1])
            list1 = cursor.fetchone()
            connection.close()
            if list1:
                return cls(list1[1], list1[3], list1[0], list1[2], list1[5], str(list1[6]).split()[0], list1[4])
            else:
                print("Login denied")
                return None

        except cx_Oracle.DataError as e:
            print(e)
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading employee")
            return None

    def save_to_db(self):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")

            cursor = connection.cursor()
            query = """insert into employees(login, employee_name, emp_password, phone, amount_of_days, department_id)
                    values(:login, :name, :password, :phone, :days, :dept)"""
            cursor.execute(query, login=self.get_login(), name=self.get_name(), password=self.get_password(),
                           phone=self.get_phone(), days=str(self.__amount_of_days), dept=self.get_department())
            connection.commit()
            connection.close()
            return "Saved"
        except cx_Oracle.DataError as e:
            print(e)
            return None
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading employee")
            return None

    def update_in_db(self):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")

            cursor = connection.cursor()
            query = """update employees 
                    set 
                    employee_name = :name, 
                    emp_password = :password, 
                    phone = :phone,
                    amount_of_days = :days, 
                    department_id = :dept
                    where login = :login
                """
            cursor.execute(query, login=self.get_login(), name=self.get_name(), password=self.get_password(),
                           phone=self.get_phone(), days=self.__amount_of_days, dept=self.get_department())
            connection.commit()
            connection.close()

        except cx_Oracle.DataError as e:
            print(e)
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading employee")
            return None

    def clone(self):
        return copy.copy(self)

    def validate(self):
        if 1 < len(self.get_name()) < 50 and 1 < len(self.get_phone()) < 50 and \
                1 < len(self.get_login()) < 50 and 1 < len(self.get_password()) < 50:
            return "Yest"
        else:
            return None


# -------------Client----------------------------
class Client(IDBWorker, Validation):
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

    def set_name(self, name):
        self.__name = name

    def set_phone(self, phone):
        self.__phone = phone

    def set_address(self, address):
        self.__address = address

    def set_district(self, district):
        self.__district = district

    def set_city(self, city):
        self.__city = city

    def set_region(self, region):
        self.__region = region

    @classmethod
    def load_from_db(cls, *identification):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")
            cursor = connection.cursor()
            query = """select clients.client_id
                    ,clients.client_name
                    ,clients.phone
                    ,clients.address
                    ,district.district_name
                    ,city.city_name
                    ,region.region_name
                   from clients join district on clients.district_district_id = district.district_id
                        join city on district.city_city_id = city.city_id
                        join region on city.region_region_id = region.region_id
                    where client_id = :numb"""
            cursor.execute(query, numb=identification[0])
            list1 = cursor.fetchone()
            return cls(list1[0], list1[1], list1[2], list1[3], list1[4], list1[5], list1[6])
        except cx_Oracle.DataError as e:
            print(e)
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading getter or sender")
            return None

    def check_in_db(self):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")
            cursor = connection.cursor()
            query = """select district_id from district where district_name = :district_name"""
            cursor.execute(query, district_name=self.__district)
            district_id = cursor.fetchone()[0]
            query = """select clients.client_id
                   from clients 
                   where client_name = :name and phone = :phone 
                   and address = :address and district_district_id = :district_id"""
            cursor.execute(query, name=self.__name, phone=self.__phone, address=self.__address, district_id=district_id)
            list1 = cursor.fetchone()
            connection.close()
            if list1:
                return list1[0]
            else:
                return 0
        except cx_Oracle.DataError as e:
            print(e)
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading getter or sender")
            return None

    def save_to_db(self):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")
            cursor = connection.cursor()
            query = """select district_id from district where district_name = :district_name"""
            cursor.execute(query, district_name=self.__district)
            district_id = cursor.fetchone()[0]
            query = """insert into clients(client_id, client_name, phone, address, district_district_id)
                        values(0, :name, :phone, :address, :district_id)"""
            cursor.execute(query, name=self.__name, phone=self.__phone, address=self.__address, district_id=district_id)
            connection.commit()
            connection.close()
        except cx_Oracle.DataError as e:
            print(e)
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading getter or sender")
            return None

    def update_in_db(self):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")
            cursor = connection.cursor()
            query = """select district_id from district where district_name = :district_name"""
            cursor.execute(query, district_name=self.__district)
            district_id = cursor.fetchone()[0]
            query = """update clients
                    set  
                    client_name = :name, 
                    phone = :phone, 
                    address = :address, 
                    district_district_id = :district_id
                    where client_id = :id"""
            cursor.execute(query, id=self.__id, name=self.__name, phone=self.__phone, address=self.__address,
                           district_id=district_id)
            connection.commit()
            connection.close()
            return "Saved"
        except cx_Oracle.DataError as e:
            print(e)
            return None
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading getter or sender")
            return None

    def clone(self):
        return copy.copy(self)

    def validate(self):
        if 5 < len(self.__name) < 50 and 5 < len(self.__phone) < 50 and 5 < len(self.__address) < 50:
            return 1
        else:
            return None


# ---------------------Package-----------------------
class Package(IDBWorker, Prototype, Validation):
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
        self.__current_place = Department.load_from_db(employee.get_department())

    def deliver(self, employee):
        self.__checked_by = employee.get_login()
        self.__status = "delivered"

    def extraction(self):
        with open("extraction.csv", "a", newline="") as file:
            writer = csv.writer(file)
            getter = "[" + self.__getter.get_name() + "," + self.__getter.get_phone() + "," \
                     + self.__getter.get_address() + "," + self.__getter.get_district() + "," \
                     + self.__getter.get_city() + "," + self.__getter.get_region() + "]"
            sender = "[" + self.__sender.get_name() + "," + self.__sender.get_phone() + "," \
                     + self.__sender.get_address() + "," + self.__sender.get_district() + "," \
                     + self.__sender.get_city() + "," + self.__sender.get_region() + "]"
            writer.writerow([self.__number, self.__status, self.__weight, self.__volume, getter, sender,
                             self.__current_place, self.__checked_by])

    def next_move(self):
        if self.__current_place.get_region() == self.__getter.get_region():
            if self.__current_place.get_city() == self.__getter.get_city():
                if self.__current_place.get_district() == self.__getter.get_district():
                    print("here")
                else:
                    print("deliver to the other district")
            else:
                print("deliver to another city")
        else:
            print("deliver to other region")

    @classmethod
    def load_from_db(cls, *identification):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")

            cursor = connection.cursor()
            query = """select package_id
                        , getter_id
                        , sender_id
                        , department_department_id
                        , checked_by
                        , status
                        , package_weigth
                        , package_volume
                   from package_table
                   where package_id = :numb"""
            cursor.execute(query, numb=identification[0])

            list1 = cursor.fetchone()
            connection.close()
            if list1:
                getter = Client.load_from_db(list1[1])
                sender = Client.load_from_db(list1[2])
                department = Department.load_from_db(list1[3])
                return cls(list1[0], getter, sender, department, list1[4], list1[5], list1[6], list1[7])

            else:
                print("No such package")
                return None

        except cx_Oracle.DataError as e:
            print(e)
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading package")
            return None

    def save_to_db(self):
        getter_id = self.__getter.check_in_db()
        sender_id = self.__sender.check_in_db()
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")

            cursor = connection.cursor()
            query = """insert into package_table(package_id, getter_id, sender_id, department_department_id, 
                    package_weigth, package_volume, checked_by, status ) 
                    values(0, :getter_id, :sender_id, :current_place, :weight, :volume, :checked_by, :status)"""
            cursor.execute(query, getter_id=getter_id, sender_id=sender_id, current_place=self.__current_place,
                           weight=self.__weight, volume=self.__volume, checked_by=self.__checked_by,
                           status=self.__status)
            connection.commit()
            connection.close()
            return "saved"
        except cx_Oracle.DataError as e:
            self.extraction()
            print(e)
            return None
        except cx_Oracle.DatabaseError as e:
            self.extraction()
            print(e)
            return None

    #        except Exception as e:
    #            self.extraction()
    #            print("smth go wrong with loading package to db")
    #            return None

    def update_in_db(self):
        getter_id = self.__getter.check_in_db()
        sender_id = self.__sender.check_in_db()
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")
            print(self.__current_place.get_number())
            cursor = connection.cursor()
            query = """update package_table
                        set 
                        getter_id = :getter_id, 
                        sender_id = :sender_id, 
                        department_department_id = :current_place, 
                        package_weigth = :weight, 
                        package_volume = :volume, 
                        checked_by = :checked_by, 
                        status = :status 
                        where package_id = :package_id"""
            cursor.execute(query, package_id=self.__number, getter_id=getter_id, sender_id=sender_id,
                           current_place=self.__current_place.get_number(),
                           weight=self.__weight, volume=self.__volume, checked_by=self.__checked_by,
                           status=self.__status)
            connection.commit()
            connection.close()
            return "Information saved"
        except cx_Oracle.DataError as e:
            self.extraction()
            print(e)
            return None
        except cx_Oracle.DatabaseError as e:
            self.extraction()
            print(e)
            return None
        except Exception as e:
            self.extraction()
            e = "smth go wrong with updating package in db"
            return None

    def clone(self):
        return copy.copy(self)

    def validate(self):
        try:
            a = float(self.__volume)
            b = float(self.__weight)
            c = self.__getter.validate()
            d = self.__sender.validate()
            if c and d and a>0 and b>0 :
                return True
            else:
                return None
        except:
            return None


# -------------Department
class Department(IDBWorker):
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

    @classmethod
    def load_from_db(cls, *num):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")
            cursor = connection.cursor()
            query = """select department.department_id
                    , department.department_type
                    , department.telephone
                    , department.address
                    , district.district_name
                    , city.city_name
                    , region.region_name
                    , department.free_volume
                    from department join district on department.district_district_id = district.district_id
                        join city on district.city_city_id = city.city_id
                        join region on city.region_region_id = region.region_id
                    where department_id = :numb"""
            cursor.execute(query, numb=num[0])
            list1 = cursor.fetchone()
            return cls(list1[0], list1[1], list1[2], list1[3], list1[4], list1[5], list1[6], list1[7])
        except cx_Oracle.DataError as e:
            print(e)
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading department")
            return None

    def save_to_db(self):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")
            cursor = connection.cursor()
            query = """select district_id from district where district_name = :district_name"""
            cursor.execute(query, district_name=self.__district)
            district_id = cursor.fetchone()[0]
            query = """insert into department(department_id, department_type, telephone, address, district_district_id, 
            free_volume)
            values(0, :type, :phone, :address, :district, :volume)"""
            cursor.execute(query, type=self.__type, phone=self.__telephone, address=self.__address,
                           district=district_id,
                           volume=self.__free_volume)
            connection.commit()
            connection.close()
            return "saved"
        except cx_Oracle.DataError as e:
            print(e)
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading getter or sender")
            return None

    def update_in_db(self):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")
            cursor = connection.cursor()
            query = """select district_id from district where district_name = :district_name"""
            cursor.execute(query, district_name=self.__district)
            district_id = cursor.fetchone()[0]
            query = """update department
                    set  
                    department_type = :type, 
                    telephone = :phone, 
                    address = :address, 
                    district_district_id = :district, 
                    free_volume = :volume
                    where department_id = :dept_id"""
            cursor.execute(query, dept_id=self.__number, type=self.__type, phone=self.__telephone,
                           address=self.__address, district=district_id,
                           volume=self.__free_volume)
            connection.commit()
            connection.close()
        except cx_Oracle.DataError as e:
            print(e)
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading getter or sender")
            return None


# --------Transport--------
class Transport():
    def __init__(self, id, max_volume, max_weight, current_place):
        self.__id = id
        self.__max_volume = max_volume
        self.__max_weight = max_weight
        self.__current_place = current_place

    def create_list(self):
        pass


# ---------Courier-------
class Courier(Employee, Transport):
    def __init__(self, name, phone, login, password, department_num, next_working_day, amount_of_days, max_volume,
                 max_weight):
        super().__init__(name, phone, login, password, department_num, next_working_day, amount_of_days)
        self.__max_volume = max_volume
        self.__max_weight = max_weight

    def create_list(self):
        pass

    @classmethod
    def load_from_db(cls, *identification):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")

            cursor = connection.cursor()
            query = """select login
                         , name
                         , password
                         , phone
                         , amount_of_days
                         , max_volume
                         , max_weight
                         , department_id
                         , work_date
                         from courier join schedule on courier.login = schedule.employee_id 
                         where schedule.work_date > sysdate and ROWNUM < 2
                         and login = :login and emp_password = :password"""
            cursor.execute(query, login=identification[0], password=identification[1])
            list1 = cursor.fetchone()
            connection.close()
            if list1:
                return cls(list1[1], list1[3], list1[0], list1[2], list1[7], str(list1[8]).split()[0], list1[7],
                           list1[5], list1[6])
            else:
                print("Login denied")
                return None

        except cx_Oracle.DataError as e:
            print(e)
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading employee")
            return None

    def save_to_db(self):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")

            cursor = connection.cursor()
            query = """insert into courier(login, password, );"""
            cursor.execute(query, login=self.get_login(), name=self.get_name(), password=self.get_password(),
                           phone=self.get_phone(), days=self.__amount_of_days, dept=self.get_department())
            connection.commit()
            connection.close()

        except cx_Oracle.DataError as e:
            print(e)
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading employee")
            return None

    def update_in_db(self):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")

            cursor = connection.cursor()
            query = """insert into courier(login, password, );"""
            cursor.execute(query, login=self.get_login(), name=self.get_name(), password=self.get_password(),
                           phone=self.get_phone(), days=self.__amount_of_days, dept=self.get_department())
            connection.commit()
            connection.close()

        except cx_Oracle.DataError as e:
            print(e)
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading employee")
            return None


# ---------Admin---------
class Admin(Worker, IDBWorker):
    def __init__(self, name, phone, login, password, department_num):
        super().__init__(name, phone, login, password, department_num)

    def create_employee(self, name, phone, login, password):
        next_working_day = '00/00/0000'
        amount_of_days = 0
        emp = Employee(name, phone, login, password, self.get_department(), next_working_day, amount_of_days)
        return emp

    def create_department(self, type, telephone, address, district, city, region, volume):
        dept = Department(0, type, telephone, address, district, city, region, volume)
        if dept:
            return dept
        else:
            return None

    def get_schedule(self):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")

            cursor = connection.cursor()
            query = """select employee_id, schedule.work_date
                    from schedule join employees on schedule.employee_id = employees.login
                    where employees.department_id = 1 and 
                    to_date(schedule.work_date,'dd.mm.yyyy') = to_date(sysdate, 'dd.mm.yyyy')"""
            cursor.execute(query)
            list1 = cursor.fetchall()
            connection.close()
            if list1:
                string = "Today are working: \n"
                for el in list1:
                    print(el)
                    string = string + el[0] + "\n"
                return string
            else:
                return None

        except cx_Oracle.DataError as e:
            print(e)
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading employee")
            return None

    def check_address(self, district, city, region):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")

            cursor = connection.cursor()
            query = """select * from district join city on district.city_city_id = city.city_id
                    join region on city.region_region_id = region.region_id
                    where district_name = :district and city_name = :city and region_name = :region"""
            cursor.execute(query, district=district, city=city, region=region)
            list1 = cursor.fetchone()
            connection.close()
            if list1:
                return list1[0]
            else:
                return None

        except cx_Oracle.DataError as e:
            print(e)
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading employee")
            return None

    @classmethod
    def load_from_db(cls, *identification):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")

            cursor = connection.cursor()
            query = """select login
                         , name
                         , password
                         , phone
                         , department_department_id
                         from admin
                         where login = :login and password = :password"""
            cursor.execute(query, login=identification[0], password=identification[1])
            list1 = cursor.fetchone()
            connection.close()
            if list1:
                return cls(list1[1], list1[3], list1[0], list1[2], list1[4])
            else:
                return None

        except cx_Oracle.DataError as e:
            print(e)
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading employee")
            return None

    def save_to_db(self):
        try:
            connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")

            cursor = connection.cursor()
            query = """insert into admin(login, password, name,phone, department_id)
                       values(:login, :password, :name, :phone, :days, :dept);"""
            cursor.execute(query, login=self.get_login(), name=self.get_name(), password=self.get_password(),
                           phone=self.get_phone(), dept=self.get_department())
            connection.commit()
            connection.close()

        except cx_Oracle.DataError as e:
            print(e)
        except cx_Oracle.DatabaseError as e:
            print(e)
            return None
        except Exception as e:
            print("smth go wrong with loading employee")
            return None

    def update_in_db(self):
        pass

    def calculate_salary(self):
        pass
