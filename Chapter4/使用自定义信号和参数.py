#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MySpinBox(QSpinBox):
    zeros = 0
    def __init__(self, parent=None):
        super(MySpinBox, self).__init__(parent)

        self.connect(self, SIGNAL('valueChanged(int)'), self.checkZero)

    def checkZero(self, para):
        if self.value() == 0:
            self.zeros += 1
            self.emit(SIGNAL('zeroup'), self.zeros)

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        ms = MySpinBox(self)
        self.connect(ms, SIGNAL('zeroup'), self.countZero)

    def countZero(self, zeros):
        print 'got zero %d times'%zeros

app = QApplication(sys.argv)
f = Form()
f.show() #show方法会像Applicaiton对象的事件队列里添加新的事件
app.exec_() #启动qt的事件循环