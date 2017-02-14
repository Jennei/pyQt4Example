#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt4.QtCore import *

class TextRate(QObject):
    def __init__(self):
        super(TextRate, self).__init__()

        self.__rate = 17.5

    def rate(self):
        return self.__rate

    def setRate(self, rate):
        if rate != self.__rate:
            self.__rate = rate
            self.emit(SIGNAL('rateChanged'), self.__rate)

def gotChange(value):
    print 'rate changed to %.2f'%value

r = TextRate()
r.connect(r, SIGNAL('rateChanged'), gotChange)

#r.setRate(1213.1231213)