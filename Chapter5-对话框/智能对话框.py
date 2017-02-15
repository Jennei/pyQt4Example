#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class NumberFormatDlg(QDialog):
    def __init__(self, format, parent=None):
        super(NumberFormatDlg, self).__init__(parent)
        #在对话关闭之后不是默认隐藏起来而是立即释放内存删除掉
        self.setAttribute(Qt.WA_DeleteOnClose)

        selre = QRegExp(r'[ ,;:.]')

        thousandsLabel = QLabel('&Thousands Separator')
        self.thousandsEdit = QLineEdit(format['thousandsseparator'])
        self.thousandsEdit.setMaxLength(1)
        #设置预防验证
        self.thousandsEdit.setValidator(QRegExpValidator(selre, self))
        thousandsLabel.setBuddy(self.thousandsEdit)

        decimalMakerLabel = QLabel('Decimal &Maker')
        self.decimalEdit = QLineEdit(format['decimalmaker'])
        self.decimalEdit.setMaxLength(1)
        #设置输入掩码，表示接受任意一个字符
        self.decimalEdit.setInputMask('X')
        self.decimalEdit.setValidator(QRegExpValidator(selre, self))
        decimalMakerLabel.setBuddy(self.decimalEdit)

        decimalPlaceLabel = QLabel('&Decimal Places')
        self.decimalPlacesSpin = QSpinBox()
        decimalPlaceLabel.setBuddy(self.decimalPlacesSpin)
        self.decimalPlacesSpin.setRange(0, 6)
        self.decimalPlacesSpin.setValue(format['decimalplaces'])

        self.redCheckbox = QCheckBox('&Red negative numbers')
        self.redCheckbox.setChecked(format['rednegative'])

        btbox = QDialogButtonBox(QDialogButtonBox.Apply|QDialogButtonBox.Cancel)

        self.format = format

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

        self.connect(btbox.button(QDialogButtonBox.Apply), SIGNAL('clicked()'), self.apply)
        self.connect(btbox, SIGNAL('rejected()'), self, SLOT('reject()'))

        self.setWindowTitle(u'非模态对话框')

    def apply(self):
        thousands = unicode(self.thousandsEdit.text())
        decimal = unicode(self.decimalEdit.text())
        place = self.decimalPlacesSpin.value()
        redc = self.redCheckbox.isChecked()

        if thousands == decimal:
            QMessageBox.warning(self, u'千分符错误',u'千分符应该和小树分隔符不同')
            self.thousandsEdit.selectAll()
            self.thousandsEdit.setFocus()
            return
        if len(decimal) == 0:
            QMessageBox.warning(self, u'小数分隔符错误',u'小数分隔符不能为空')
            self.decimalEdit.setFocus()
            self.decimalEdit.selectAll()
            return

        self.format['thousandsseparator'] = thousands
        self.format['decimalmaker'] = decimal
        self.format['decimalplaces'] = place
        self.format['rednegative'] = redc

        #发射信号通知主窗口数据改变
        self.emit(SIGNAL('changed'))
        QDialog.accept(self)

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.format = {}
        self.format['thousandsseparator'] = ','
        self.format['decimalmaker'] = '.'
        self.format['decimalplaces'] = 5
        self.format['rednegative'] = True

        bt = QPushButton(u'非模态对话框')
        la = QHBoxLayout()
        la.addWidget(bt)

        self.setLayout(la)
        self.setWindowTitle(u'智能对话框')

        self.connect(bt, SIGNAL('clicked()'), self.setNumFormat)

    def setNumFormat(self):
        d = NumberFormatDlg(self.format, self)
        self.connect(d, SIGNAL('changed'), self.refreshTable)
        d.show()

    def refreshTable(self):
        for key in self.format:
            print key, self.format[key]

app = QApplication(sys.argv)
f = Form()
f.show()
app.exec_()