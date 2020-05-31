# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\myshu\PycharmProjects\PYQT\LoginWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(355, 200)
        self.username_label = QtWidgets.QLabel(Dialog)
        self.username_label.setGeometry(QtCore.QRect(20, 50, 61, 21))
        self.username_label.setObjectName("username_label")
        self.password_label = QtWidgets.QLabel(Dialog)
        self.password_label.setGeometry(QtCore.QRect(20, 90, 61, 16))
        self.password_label.setObjectName("password_label")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(90, 50, 211, 20))
        self.lineEdit.setText("")
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 90, 211, 20))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(230, 130, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(90, 130, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 170, 101, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        '''================================================'''

        self.pushButton_2.clicked.connect(self.close_window)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.username_label.setText(_translate("Dialog", "USERNAME"))
        self.password_label.setText(_translate("Dialog", "PASSWORD"))
        self.pushButton_2.setText(_translate("Dialog", "Exit"))
        self.pushButton.setText(_translate("Dialog", "Login"))
        self.pushButton_3.setText(_translate("Dialog", "Forget password"))

    def close_window(self):
        quit()