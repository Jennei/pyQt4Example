#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class NumberFormatDlg(QDialog):
    def __init__(self, format, parent=None):
        super(NumberFormatDlg, self).__init__(parent)

        thousandsLabel = QLabel('&Thousands Separator')
        self.thousandsEdit = QLineEdit(format['thousandsseparator'])
        thousandsLabel.setBuddy(self.thousandsEdit)

        decimalMakerLabel = QLabel('Decimal &Maker')
        self.decimalEdit = QLineEdit(format['decimalmaker'])
        decimalMakerLabel.setBuddy(self.decimalEdit)

        decimalPlaceLabel = QLabel('&Decimal Places')
        self.decimalPlacesSpin = QSpinBox()
        decimalPlaceLabel.setBuddy(self.decimalPlacesSpin)
        self.decimalPlacesSpin.setRange(0, 6)
        self.decimalPlacesSpin.setValue(format['decimalplaces'])

        self.redCheckbox = QCheckBox('&Red negative numbers')
        self.redCheckbox.setChecked(format['rednegative'])

        btbox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)

        self.format = format.copy()

        grid = QGridLayout()
        grid.addWidget(thousandsLabel, 0, 0)
        grid.addWidget(self.thousandsEdit, 0, 1)
        grid.addWidget(decimalMakerLabel, 1, 0)
        grid.addWidget(self.decimalEdit, 1, 1)
        grid.addWidget(decimalPlaceLabel, 2, 0)
        grid.addWidget(self.decimalPlacesSpin, 2, 1)
        grid.addWidget(self.redCheckbox, 3,0, 1, 2)
        grid.addWidget(btbox, 4, 0, 1, 2)

        self.setLayout(grid)

        self.connect(btbox, SIGNAL('accepted()'), self, SLOT('accept()'))
        self.connect(btbox, SIGNAL('rejected()'), self, SLOT('reject()'))

        self.setWindowTitle(u'模态对话框')

    def accept(self):
        """
        提交后验证
        :return:
        """
        class ThousandsError(Exception):pass
        class DecimalError(Exception):pass

        thousands = unicode(self.thousandsEdit.text())
        decimal = unicode(self.decimalEdit.text())
        place = self.decimalPlacesSpin.value()
        redc = self.redCheckbox.isChecked()

        sel = frozenset(' ,;:.')
        try:
            if len(decimal) == 0:
                raise DecimalError, u'小数点标识不能为空'
            if len(thousands) > 1:
                raise ThousandsError, u'千分位分隔符不能是一个以上的字符'
            if len(decimal) > 1:
                raise DecimalError, u'小数点分隔符不能是一个以上的字符'
            if thousands == decimal:
                raise ThousandsError, u'小数点分隔符和千分位分割符不能相同'
            if thousands and thousands not in sel:
                raise ThousandsError, u'千分符必须是空格 , ; : .其中的一个'
            if decimal not in sel:
                raise DecimalError, u"小数点分隔符必须是空格 , ; : .其中的一个"
        except ThousandsError as e:
            QMessageBox.warning(self, u'千分符错误', unicode(e))
            self.thousandsEdit.selectAll()
            self.thousandsEdit.setFocus()
            return
        except DecimalError as e:
            QMessageBox.warning(self, u'小数点错误', unicode(e))
            self.decimalEdit.selectAll()
            self.decimalEdit.setFocus()
            return

        self.format['thousandsseparator'] = thousands
        self.format['decimalmaker'] = decimal
        self.format['decimalplaces'] = place
        self.format['rednegative'] = redc

        QDialog.accept(self)


    def numFormat(self):
        return self.format

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.format = {}
        self.format['thousandsseparator'] = ','
        self.format['decimalmaker'] = '.'
        self.format['decimalplaces'] = 2
        self.format['rednegative'] = True

        bt = QPushButton(u'模态对话框')
        la = QHBoxLayout()
        la.addWidget(bt)

        self.setLayout(la)
        self.setWindowTitle(u'标准对话框')

        self.connect(bt, SIGNAL('clicked()'), self.setNumFormat)

    def setNumFormat(self):
        d = NumberFormatDlg(self.format, self)
        if d.exec_():
            self.format = d.numFormat()
            self.refreshTable()

    def refreshTable(self):
        for key in self.format:
            print key, self.format[key]

app = QApplication(sys.argv)
f = Form()
f.show()
app.exec_()