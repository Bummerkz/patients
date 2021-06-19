# -*- coding: utf-8 -*-
import jinja2

import sys, os
from PyQt5 import QtCore, QtWidgets, QtPrintSupport


class Report():
    def __init__(self, data):
        self.data = data
        self.data = data
        self.loadTemplate()
        self.editor = QtWidgets.QTextEdit()

    def loadTemplate(self):
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "template.html"
        self.template = templateEnv.get_template(TEMPLATE_FILE)

    def createReport(self):
        outputText = self.template.render(
            fio=self.data['fio'],
            dateReg=self.data['dateReg'],
            datePrint=self.data['datePrint'],
            iin=self.data['iin'],
            doctor='Еникеева М.Х.',
            dateBirth=self.data['date_birth'],
            sex=self.data['is_male'],
            addr=self.data['addr'],
            result=self.data['result']
        )

        html_file = open('report.html', 'w', encoding='utf-8')
        html_file.write(outputText)
        html_file.close()

        file = QtCore.QFile('report.html')
        if file.open(QtCore.QIODevice.ReadOnly):
            stream = QtCore.QTextStream(file)
            stream.setCodec('utf8')
            text = stream.readAll()
            self.editor.setHtml(text)

        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.editor.print_)
        dialog.exec_()
