#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import datetime

from report import Report
from db import PatientsDB

import sqlite3
import sys

main_ui, _ = loadUiType('main.ui')
add_ui, _ = loadUiType('add.ui')
edit_ui, _ = loadUiType('edit.ui')


class MainWindow(QMainWindow, main_ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.setupUi(self)
        self.setWindowTitle('PCR')
        self.db = PatientsDB()
        self.proxyModelPatient = QSortFilterProxyModel(self)
        self.proxyModelPatient.setSourceModel(self.db.model)

        self.init_table()

        self.handle_buttons()
        self.handle_search()
        self.handle_table()

    def init_table(self):
        self.tblPatients.setModel(self.proxyModelPatient)
        mode = QAbstractItemView.SelectRows
        self.tblPatients.setSelectionBehavior(mode)
        self.tblPatients.setColumnHidden(0, True)
        self.tblPatients.setColumnHidden(6, True)
        self.tblPatients.setColumnHidden(7, True)
        self.tblPatients.setColumnHidden(8, True)
        self.tblPatients.setColumnWidth(1, 200)
        self.tblPatients.setColumnWidth(2, 250)
        self.tblPatients.setColumnWidth(3, 180)

    def handle_buttons(self):
        self.btnAddPatient.clicked.connect(self.add_new_patient)

    def handle_table(self):
        self.tblPatients.doubleClicked.connect(self.row_clicked)

    def handle_search(self):
        self.txtSearch.textEdited.connect(self.search_patient)

    def add_new_patient(self):
        addWindow = AddPatientWindow()
        addWindow.setWindowTitle('Новый пациент')
        if addWindow.exec_():
            data = {
                'fio': addWindow.txtFIO.text(),
                'addr': addWindow.txtAddr.text(),
                'iin': addWindow.txtIIN.text(),
                'date_birth': addWindow.dateBirth.date().toString('dd.MM.yyyy'),
                'is_male': addWindow.cmbSex.currentText(),
                'dateReg': QtCore.QDateTime.currentDateTime().toString('dd.MM.yyyy hh:mm'),
                'datePrint': QtCore.QDateTime.currentDateTime().toString('dd.MM.yyyy hh:mm'),
                'result': 'Отрицательный'
            }
            self.db.addPatient(data)

    def row_clicked(self, mi):
        # print('Table double clicked')
        row = self.proxyModelPatient.mapToSource(mi)
        data = self.db.getPatient(row.row())
        self.proxyModelPatient.setFilterRegExp('')
        self.txtSearch.setText('')

        editWindow = EditPatientWindow(data)
        editWindow.setWindowTitle('Изменить')
        if editWindow.exec_():
            data = {
                'fio': editWindow.txtFIO.text(),
                'addr': editWindow.txtAddr.text(),
                'iin': editWindow.txtIIN.text(),
                'date_birth': editWindow.dateBirth.date().toString('dd.MM.yyyy'),
                'is_male': editWindow.cmbSex.currentText(),
                'dateReg': editWindow.dateReg.dateTime().toString('dd.MM.yyyy hh:mm'),
                'datePrint': editWindow.datePrint.dateTime().toString('dd.MM.yyyy hh:mm'),
                'result': editWindow.cmbResult.currentText()
            }
            self.db.updatePatient(data, row)

    def search_patient(self, text):
        self.proxyModelPatient.setFilterKeyColumn(4)
        self.proxyModelPatient.setFilterRegExp(str(text))

class EditPatientWindow(QDialog, edit_ui):
    def __init__(self, data):
        QWidget.__init__(self)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.setupUi(self)
        self.data = data
        sex_type = ["Мужской", "Женский"] 
        self.cmbSex.addItems(sex_type)
        sex = data['is_male']
  
        self.cmbSex.setCurrentText(sex)
        self.txtFIO.setText(data['fio'])
        self.txtAddr.setText(data['addr'])
        self.txtIIN.setText(data['iin'])
        qtDate = QtCore.QDate.fromString(data['date_birth'], 'dd.MM.yyyy')
        self.dateBirth.setDate(qtDate)

        result_type = ["Положительный", "Отрицательный"] 
        self.cmbResult.addItems(result_type)
  
        self.cmbResult.setCurrentText(data['result'])

        self.dateReg.setDateTime(QtCore.QDateTime.fromString(data['dateReg'], 'dd.MM.yyyy hh:mm'))
        self.datePrint.setDateTime(QtCore.QDateTime.fromString(data['datePrint'], 'dd.MM.yyyy hh:mm'))

        reg_ex = QRegExp("[0-9]{,12}")
        IIN_input_validator = QRegExpValidator(reg_ex, self.txtIIN)
        self.txtIIN.setValidator(IIN_input_validator)

        self.btnPrint.clicked.connect(self.printReport)

    def printReport(self):

        data = {
            'fio': self.txtFIO.text(),
            'addr': self.txtAddr.text(),
            'iin': self.txtIIN.text(),
            'date_birth': self.dateBirth.date().toString('dd.MM.yyyy'),
            'is_male': self.cmbSex.currentText(),
            'dateReg': self.dateReg.dateTime().toString('dd.MM.yyyy hh:mm'),
            'datePrint': self.datePrint.dateTime().toString('dd.MM.yyyy hh:mm'),
            'result': self.cmbResult.currentText()
        }

        report = Report(data)

        report.createReport()

class AddPatientWindow(QDialog, add_ui):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

        sex_type = ["Мужской", "Женский"] 
  
        self.cmbSex.addItems(sex_type) 
  
        item = sex_type[0]
  
        self.cmbSex.setCurrentText(item) 

        reg_ex = QRegExp("[0-9]{,12}")
        IIN_input_validator = QRegExpValidator(reg_ex, self.txtIIN)
        self.txtIIN.setValidator(IIN_input_validator)

def main():

    MainEventThread = QApplication([])
    MainEventThread.setStyle('Fusion')

    application = MainWindow()
    application.show()

    MainEventThread.exec()

if __name__ == '__main__':
    main()
