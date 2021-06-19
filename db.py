#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import sqlite3
from PyQt5 import QtSql, QtWidgets
from PyQt5.QtSql import QSqlRelation
from PyQt5.QtCore import Qt


class PatientsDB():
    def __init__(self):
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.model = QtSql.QSqlTableModel()
        # self.analyseModel = QtSql.QSqlRelationalTableModel()
        self.resultsModel = QtSql.QSqlTableModel()
        self.createConnection()
        self.createModel()

    def createConnection(self):
        self.db.setDatabaseName("patients.sqlite")
        if not self.db.open():
            QtWidgets.QMessageBox.critical(None, "Cannot open database",
                                           "Unable to establish a database connection.\n"
                                           "This example needs SQLite support. Please read "
                                           "the Qt SQL driver documentation for information how "
                                           "to build it.\n\n"
                                           "Click Cancel to exit.", QtWidgets.QMessageBox.Cancel)
            return False

        return True

    def closeEvent(self, e):
        if (self.db.open()):
            self.db.close()

    def addPatient(self, data):
        # print(data)
        row = self.model.rowCount()
        self.model.insertRows(row, 1)
        self.model.setData(self.model.index(row, 1), data['fio'])
        self.model.setData(self.model.index(row, 2), data['addr'])
        self.model.setData(self.model.index(row, 3), data['iin'])
        self.model.setData(self.model.index(row, 4), data['date_birth'])
        self.model.setData(self.model.index(row, 5), data['is_male'])
        self.model.setData(self.model.index(row, 6), data['dateReg'])
        self.model.setData(self.model.index(row, 7), data['datePrint'])
        self.model.setData(self.model.index(row, 8), data['result'])
        self.model.submitAll()

    def updatePatient(self, data, mi):
        row = mi.row()
        self.model.setData(self.model.index(row, 1), data['fio'])
        self.model.setData(self.model.index(row, 2), data['addr'])
        self.model.setData(self.model.index(row, 3), data['iin'])
        self.model.setData(self.model.index(row, 4), data['date_birth'])
        self.model.setData(self.model.index(row, 5), data['is_male'])
        self.model.setData(self.model.index(row, 6), data['dateReg'])
        self.model.setData(self.model.index(row, 7), data['datePrint'])
        self.model.setData(self.model.index(row, 8), data['result'])
        self.model.submitAll()

    def createModel(self):
        self.model.setTable("data")
        self.model.setSort(2, Qt.AscendingOrder)
        self.model.setHeaderData(1, Qt.Horizontal, "ФИО")
        self.model.setHeaderData(2, Qt.Horizontal, "Адрес")
        self.model.setHeaderData(3, Qt.Horizontal, "ИИН")
        self.model.setHeaderData(4, Qt.Horizontal, "Дата рождения")
        self.model.setHeaderData(5, Qt.Horizontal, "Пол")
        self.model.select()

    def getPatient(self, row):
        data = {
            'id': self.model.record(row).value('id'),
            'fio': self.model.record(row).value('fio'),
            'addr': self.model.record(row).value('addr'),
            'iin': self.model.record(row).value('iin'),
            'date_birth': self.model.record(row).value('date_birth'),
            'is_male': self.model.record(row).value('is_male'),
            'dateReg': self.model.record(row).value('dateReg'),
            'result': self.model.record(row).value('result'),
            'datePrint': self.model.record(row).value('datePrint'),
        }
        # print(data)

        return data

    def getAllPatients(self):
        return self.model