import sys
from PyQt5 import QtWidgets
from mydesign import Ui_Dialog as LoginUi
from EmployeeMenu import Ui_Dialog as EmpMenuUi
from CreateLetter import Ui_Dialog as ChangeLetterUi
from CreateLetter2 import Ui_Dialog as CreateLetterUi
from FindPackage import Ui_Dialog as FindUi
from DeliverPackage import Ui_Dialog as DeliverUi
from OKWindow import Ui_Dialog as OKUi
from CheckPackage import Ui_Dialog as CheckUi
from AdminCreateEmployee import Ui_Dialog as CreateEmployeeUi
from AdminCreateOffice import Ui_Dialog as CreateOfficeUi
from AdminMenu import Ui_Dialog as AdminMenuUi
from Schedule import Ui_Dialog as SheduleUi

import body


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = LoginUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.logincheck)
        self.ui.pushButton_2.clicked.connect(self.close)
        self._new_window = None

    def logincheck(self):
        emp = body.Employee.load_from_db(self.ui.lineEdit.text(), self.ui.lineEdit_2.text())
        admin = body.Admin.load_from_db(self.ui.lineEdit.text(), self.ui.lineEdit_2.text())
        if emp:
            self.create_menu_employee_window(emp)
            self.close()
        elif admin:
            self.create_menu_admin_window(admin)
            self.close()
        else:
            self._new_window = OkWindow(self.close_window, self.close_window, "Wrong login or password")
            self._new_window.show()

    def create_menu_employee_window(self, emp):
        self._new_window = MenuWindow(emp)
        self._new_window.show()

    def create_menu_admin_window(self, admin):
        self._new_window = AdminMenuWindow(admin)
        self._new_window.show()

    def close_window(self):
        self._new_window.close()

class MenuWindow(QtWidgets.QMainWindow):
    def __init__(self, emp):
        super(MenuWindow, self).__init__()
        self.ui = EmpMenuUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.create_package_window)
        self.ui.pushButton_2.clicked.connect(self.create_find_window_2)
        self.ui.pushButton_3.clicked.connect(self.create_find_window_3)
        self.ui.pushButton_4.clicked.connect(self.create_find_window_4)
        self.ui.pushButton_5.clicked.connect(self.create_find_window_5)
        self._new_window = None
        self.logined = emp

    def create_package_window(self):
        self._new_window = CreateLetterWindow(self.logined)
        self._new_window.show()
        self.close()

    def create_find_window_2(self):
        self._new_window = FindWindow(self.logined, 2)
        self._new_window.show()
        self.close()

    def create_find_window_3(self):
        self._new_window = FindWindow(self.logined, 3)
        self._new_window.show()
        self.close()

    def create_find_window_4(self):
        self._new_window = FindWindow(self.logined, 4)
        self._new_window.show()
        self.close()

    def create_find_window_5(self):
        self._new_window = FindWindow(self.logined, 5)
        self._new_window.show()
        self.close()


class CreateLetterWindow(QtWidgets.QMainWindow):
    def __init__(self, emp):
        super(CreateLetterWindow, self).__init__()
        self.ui = CreateLetterUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.create_package)
        self.ui.pushButton_2.clicked.connect(self.go_back)
        self._new_window = None
        self.loggined = emp

    def create_package(self):
        s_name = self.ui.lineEdit.text()
        s_phone = self.ui.lineEdit_2.text()
        s_address = self.ui.lineEdit_3.text()
        s_district = self.ui.lineEdit_4.text()
        s_region = self.ui.lineEdit_5.text()
        s_city = self.ui.lineEdit_6.text()
        g_name = self.ui.lineEdit_7.text()
        g_phone = self.ui.lineEdit_8.text()
        g_address = self.ui.lineEdit_9.text()
        g_district = self.ui.lineEdit_10.text()
        g_region = self.ui.lineEdit_11.text()
        g_city = self.ui.lineEdit_12.text()
        weight = self.ui.lineEdit_14.text()
        volume = self.ui.lineEdit_13.text()
        if self.loggined.check_address(g_district, g_city, g_region) and \
                self.loggined.check_address(s_district, s_city, s_region):
            self.package = self.loggined.create_order(g_name, s_name, g_address, s_address,
                                         g_district, s_district, g_city, s_city, g_region, s_region,
                                         g_phone, s_phone, weight, volume)
            print("here")
            if self.package.validate():
                if self.package.get_getter().check_in_db() == 0:
                    self.package.get_getter().save_to_db()
                if self.package.get_sender().check_in_db() == 0:
                    self.package.get_sender().save_to_db()
                print(self.package.get_getter().check_in_db())
                print(self.package.get_sender().check_in_db())
                if self.package.save_to_db():
                    self._new_window = OkWindow(self.close_window, self.close_window, "Information saved")
                    self._new_window.show()
                else:
                    self._new_window = OkWindow(self.close_window, self.close_window, "Error happened")
                    self._new_window.show()
            else:
                self._new_window = OkWindow(self.close_window, self.close_window, "Validation error")
                self._new_window.show()
        else:
            self._new_window = OkWindow(self.close_window, self.close_window, "Can't be delivered on this address")
            self._new_window.show()

    def go_back(self):
        self.create_menu_employee_window(self.loggined)
        self.close()

    def create_menu_employee_window(self, emp):
        self._new_window = MenuWindow(emp)
        self._new_window.show()

    def close_window(self):
        self._new_window.close()


class ChangeLetterWindow(QtWidgets.QMainWindow):
    def __init__(self, emp, package):
        super(ChangeLetterWindow, self).__init__()
        self.ui = ChangeLetterUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.change)
        self.ui.pushButton_2.clicked.connect(self.go_back)
        self._new_window = None
        self.loggined = emp
        self.package = package
        self.clone = package.clone()
        self.getter = self.package.get_getter()
        self.sender = self.package.get_sender()
        self.ui.lineEdit.setText(self.sender.get_name())
        self.ui.lineEdit_2.setText(self.sender.get_phone())
        self.ui.lineEdit_3.setText(self.sender.get_address())
        self.ui.lineEdit_4.setText(self.sender.get_district())
        self.ui.lineEdit_5.setText(self.sender.get_region())
        self.ui.lineEdit_6.setText(self.sender.get_city())
        self.ui.lineEdit_7.setText(self.getter.get_name())
        self.ui.lineEdit_8.setText(self.getter.get_phone())
        self.ui.lineEdit_9.setText(self.getter.get_address())
        self.ui.lineEdit_10.setText(self.getter.get_district())
        self.ui.lineEdit_11.setText(self.getter.get_region())
        self.ui.lineEdit_12.setText(self.getter.get_city())

    def change(self):
        self.clone = self.package.clone()
        self.sender.set_name(self.ui.lineEdit.text())
        self.sender.set_phone(self.ui.lineEdit_2.text())
        self.sender.set_address(self.ui.lineEdit_3.text())
        self.sender.set_district(self.ui.lineEdit_4.text())
        self.sender.set_region(self.ui.lineEdit_5.text())
        self.sender.set_city(self.ui.lineEdit_6.text())
        self.getter.set_name(self.ui.lineEdit_7.text())
        self.getter.set_phone(self.ui.lineEdit_8.text())
        self.getter.set_address(self.ui.lineEdit_9.text())
        self.getter.set_district(self.ui.lineEdit_10.text())
        self.getter.set_region(self.ui.lineEdit_11.text())
        self.getter.set_city(self.ui.lineEdit_12.text())
        if self.loggined.check_address(self.sender.get_district(), self.sender.get_city(), self.sender.get_region()) and \
                self.loggined.check_address(self.getter.get_district(), self.getter.get_city(), self.getter.get_region()):
            if self.package.validate():
                self._new_window = OkWindow(self.saving, self.close_window, "Are you sure about this changes?")
                self._new_window.show()
            else:
                self._new_window = OkWindow(self.close_window, self.close_window, "Validation error")
                self._new_window.show()
                self.package = self.clone
        else:
            self._new_window = OkWindow(self.close_window, self.close_window, "Can't be delivered on this address")
            self._new_window.show()
            self.package = self.clone

    def go_back(self):
        self.create_menu_employee_window(self.loggined)
        self.close()

    def saving(self):
        a = self.getter.update_in_db()
        b = self.sender.update_in_db()
        c = self.package.update_in_db()
        if a and b and c:
            self._new_window = OkWindow(self.close_window, self.close_window, "Information saved")
            self._new_window.show()
        else:
            self._new_window = OkWindow(self.close_window, self.close_window, "Error happened")
            self._new_window.show()
            self.package = self.clone

    def create_menu_employee_window(self, emp):
        self._new_window = MenuWindow(emp)
        self._new_window.show()

    def create_ok_window(self, text):
        self._new_window = OkWindow(self.close_window, self.close_window, text)
        self._new_window.show()

    def close_window(self):
        self._new_window.close()


class FindWindow(QtWidgets.QMainWindow):
    def __init__(self, emp, choose):
        super(FindWindow, self).__init__()
        self.ui = FindUi()
        self.ui.setupUi(self)
        self._new_window = None
        self.loggined = emp
        self.choose = choose
        self.ui.pushButton.clicked.connect(self.find_package)
        self.ui.pushButton_2.clicked.connect(self.go_back)

    def find_package(self):
        package = body.Package.load_from_db(self.ui.lineEdit.text())
        if package:
            print(self.choose)
            self.package = package
            if self.choose == 2:
                self.create_deliver_window()
                self.close()
            elif self.choose == 3:
                self.create_check_window()
                self.close()
            elif self.choose == 4:
                self.create_information_window()
            elif self.choose == 5:
                self.create_change_window()
                self.close()
        else:
            self.create_ok_window()

    def create_deliver_window(self):
        self._new_window = DeliverWindow(self.loggined, self.package)
        self._new_window.show()

    def create_check_window(self):
        self._new_window = CheckWindow(self.loggined, self.package)
        self._new_window.show()

    def create_change_window(self):
        self._new_window = ChangeLetterWindow(self.loggined, self.package)
        self._new_window.show()

    def create_ok_window(self):
        text = "No such package"
        self._new_window = OkWindow(self.close_window, self.close_window, text)
        self._new_window.show()

    def create_information_window(self):
        text = "Package №" + str(self.package.get_number()) + " is " + str(self.package.get_status())
        self._new_window = OkWindow(self.close_window, self.close_window, text)
        self._new_window.show()

    def close_window(self):
        self._new_window.close()

    def go_back(self):
        self.create_menu_employee_window(self.loggined)
        self.close()

    def create_menu_employee_window(self, emp):
        self._new_window = MenuWindow(emp)
        self._new_window.show()


class DeliverWindow(QtWidgets.QMainWindow):
    def __init__(self, emp, pack):
        super(DeliverWindow, self).__init__()
        self.ui = DeliverUi()
        self.ui.setupUi(self)
        self.loggined = emp
        self._new_window = None
        self.package = pack
        self.ui.label.setText("Package №" + str(self.package.get_number()))
        self.ui.pushButton.clicked.connect(self.delivered)
        self.ui.pushButton_2.clicked.connect(self.create_find_window, 2)

    def delivered(self):
        self.clone = self.package.clone()
        self.package.deliver(self.loggined)
        text = "If you press OK this package will be delivered"
        self._new_window = OkWindow(self.saving, self.close_window, text)
        self._new_window.show()

    def saving(self):
        text = self.package.update_in_db()
        if text is None:
            text = "error happened"
        self._new_window.ui.label.setText(str(text))
        self._new_window.ui.pushButton.clicked.connect(self.close_window)
        self._new_window.ui.pushButton_2.setText("OK")

    def close_window(self):
        self.package = self.clone
        self._new_window.close()

    def create_find_window(self, choose):
        self._new_window = FindWindow(self.loggined, choose)
        self._new_window.show()
        self.close()


class CheckWindow(QtWidgets.QMainWindow):
    def __init__(self, emp, pack):
        super(CheckWindow, self).__init__()
        self.ui = CheckUi()
        self.ui.setupUi(self)
        self.loggined = emp
        self._new_window = None
        self.package = pack
        self.ui.label.setText("Check package №" + str(self.package.get_number()))
        self.ui.pushButton.clicked.connect(self.checked)
        self.ui.pushButton_2.clicked.connect(self.create_find_window)

    def checked(self):
        self.clone = self.package.clone()
        print(self.loggined.get_login())
        print(self.loggined.get_department())
        self.package.check(self.loggined)
        text = "If you press OK this package will be checked"
        self._new_window = OkWindow(self.saving, self.close_window, text)
        self._new_window.show()

    def saving(self):
        text = self.package.update_in_db()
        if text is None:
            text = "Error happened"
        self._new_window.ui.label.setText(str(text))
        self._new_window.ui.pushButton.clicked.connect(self.close_window)
        self._new_window.ui.pushButton_2.setText("OK")

    def close_window(self):
        self.package = self.clone
        self._new_window.close()

    def create_find_window(self, choose):
        self._new_window = FindWindow(self.loggined, choose)
        self._new_window.show()
        self.close()


class OkWindow(QtWidgets.QMainWindow):
    def __init__(self, foo1, foo2, text):
        super(OkWindow, self).__init__()
        self.ui = OKUi()
        self.ui.setupUi(self)
        self._new_window = None
        self.ui.pushButton.clicked.connect(foo1)
        self.ui.pushButton_2.clicked.connect(foo2)
        self.ui.label.setText(text)


class AdminMenuWindow(QtWidgets.QMainWindow):
    def __init__(self, admin):
        super(AdminMenuWindow, self).__init__()
        self.ui = AdminMenuUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.create_employee_window)
        self.ui.pushButton_2.clicked.connect(self.create_department_window)
        self.ui.pushButton_3.clicked.connect(self.close)
        self.ui.pushButton_4.clicked.connect(self.create_schedule_window)
        self._new_window = None
        self.logined = admin

    def create_employee_window(self):
        self._new_window = CreateEmployeeWindow(self.logined)
        self._new_window.show()
        self.close()

    def create_department_window(self):
        self._new_window = CreateDepartmentWindow(self.logined)
        self._new_window.show()
        self.close()

    def create_schedule_window(self):
        self._new_window = CreateScheduleWindow(self.logined)
        self._new_window.show()
        self.close()


class CreateEmployeeWindow(QtWidgets.QMainWindow):
    def __init__(self, admin):
        super(CreateEmployeeWindow, self).__init__()
        self.ui = CreateEmployeeUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.create_new_employee)
        self.ui.pushButton_2.clicked.connect(self.go_back)
        self._new_window = None
        self.loggined = admin

    def create_new_employee(self):
        name = self.ui.lineEdit.text()
        phone = self.ui.lineEdit_2.text()
        login = self.ui.lineEdit_3.text()
        password = self.ui.lineEdit_4.text()
        self.employee = self.loggined.create_employee(name, phone, login, password)
        if self.employee.validate() is None:
            self._new_window = OkWindow(self.close_window, self.close_window, "Value size error")
            self._new_window.show()
        else:
            if self.employee.check_in_db() is None:
                self._new_window = OkWindow(self.saving, self.close_window, "Do you want to  save it?")
                self._new_window.show()
            else:
                self._new_window = OkWindow(self.close_window, self.close_window, "This login already exists")
                self._new_window.show()

    def go_back(self):
        self.create_menu_admin_window(self.loggined)
        self.close()

    def saving(self):
        if self.employee.save_to_db():
            self._new_window = OkWindow(self.close_window, self.close_window, "Information saved")
            self._new_window.show()
        else:
            self._new_window = OkWindow(self.close_window, self.close_window, "Error happened")
            self._new_window.show()

    def create_menu_admin_window(self, admin):
        self._new_window = AdminMenuWindow(admin)
        self._new_window.show()

    def close_window(self):
        self._new_window.close()


class CreateDepartmentWindow(QtWidgets.QMainWindow):
    def __init__(self, admin):
        super(CreateDepartmentWindow, self).__init__()
        self.ui = CreateOfficeUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.create_department)
        self.ui.pushButton_2.clicked.connect(self.go_back)
        self._new_window = None
        self.loggined = admin

    def create_department(self):
        address = self.ui.lineEdit.text()
        district = self.ui.lineEdit_2.text()
        city = self.ui.lineEdit_3.text()
        region = self.ui.lineEdit_4.text()
        phone = self.ui.lineEdit_5.text()
        type = self.ui.lineEdit_6.text()
        volume = self.ui.lineEdit_7.text()
        self.department = self.loggined.create_department(type, phone, address, district, city, region, volume)
        if self.loggined.check_address(district, city, region) is None:
            self._new_window = OkWindow(self.close_window, self.close_window, "Error with this address")
            self._new_window.show()
        else:
            self._new_window = OkWindow(self.saving, self.close_window, "Do you want to save it?")
            self._new_window.show()

    def go_back(self):
        self.create_menu_admin_window(self.loggined)
        self.close()

    def saving(self):
        if self.department.save_to_db():
            self._new_window = OkWindow(self.close_window, self.close_window, "Information saved")
            self._new_window.show()
        else:
            self._new_window = OkWindow(self.close_window, self.close_window, "Error happened")
            self._new_window.show()

    def create_menu_admin_window(self, admin):
        self._new_window = AdminMenuWindow(admin)
        self._new_window.show()

    def close_window(self):
        self._new_window.close()


class CreateScheduleWindow(QtWidgets.QMainWindow):
    def __init__(self, admin):
        super(CreateScheduleWindow, self).__init__()
        self.ui = SheduleUi()
        self.ui.setupUi(self)
        self._new_window = None
        self.ui.pushButton.clicked.connect(self.go_back)
        self.loggined = admin
        self.ui.label.setText(self.loggined.get_schedule())

    def go_back(self):
        self.create_menu_admin_window(self.loggined)
        self.close()

    def create_menu_admin_window(self, admin):
        self._new_window = AdminMenuWindow(admin)
        self._new_window.show()


app = QtWidgets.QApplication([])
application = MyWindow()
application.show()
sys.exit(app.exec())
