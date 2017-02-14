#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
#        self.setWindowFlags(Qt.SplashScreen)

        b1 = QPushButton('one')
        b2 = QPushButton('two')
        b3 = QPushButton('three')
        b4 = QPushButton('four')
        b5 = QPushButton('five')

        self.lb = QLabel('@_@')

        la = QHBoxLayout()
        la.addWidget(b1)
        la.addWidget(b2)
        la.addWidget(b3)
        la.addWidget(b4)
        la.addWidget(b5)
        la.addWidget(self.lb)

        self.setLayout(la)

        self.connect(b1, SIGNAL('clicked()'), self.onclick)
        self.connect(b2, SIGNAL('clicked()'), self.onclick)
        self.connect(b3, SIGNAL('clicked()'), self.onclick)
        self.connect(b4, SIGNAL('clicked()'), self.onclick)
        self.connect(b5, SIGNAL('clicked()'), self.onclick)

    def onclick(self):
        bt = self.sender()
        if bt is None or not isinstance(bt, QPushButton):
            return
        self.lb.setText('you clicked %s'%bt.text())

app = QApplication(sys.argv)
f = Form()
f.show()
app.exec_()