#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        dial = QDial()
        dial.setNotchesVisible(True)

        sp = QSpinBox()

        la = QHBoxLayout()
        la.addWidget(dial)
        la.addWidget(sp)

        self.setLayout(la)

        #self.connect(dial, SIGNAL('valueChanged(int)'), sp.setValue)
        self.connect(dial, SIGNAL('valueChanged(int)'), sp, SLOT('setValue(int)'))

        self.connect(sp, SIGNAL('valueChanged(int)'), dial.setValue)

        self.setWindowTitle(u'信号和槽')

app = QApplication(sys.argv)
f = Form()
f.show()
app.exec_()