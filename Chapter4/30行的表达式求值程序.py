#!/usr/bin/env python
# -*_ coding:utf-8 -*-

from __future__ import division
import sys
from math import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.browser = QTextBrowser()
        self.lineedit = QLineEdit('please input a expression')
        self.lineedit.selectAll()

        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.lineedit)

        self.setLayout(layout)

        self.lineedit.setFocus()

        self.connect(self.lineedit, SIGNAL("returnPressed()"), self.updateUi)

        self.setWindowTitle("Calculate")

    def updateUi(self):
        try:
            text = unicode(self.lineedit.text())
            self.browser.append("<font color=red size=10>%s=<b>%s</b></font>"%(text, eval(text)))
        except:
            self.browser.append('<font color=red size=10><b>expression is invalid!</b></font>')

app = QApplication(sys.argv)
form = Form()
form.show()
sys.exit(app.exec_())