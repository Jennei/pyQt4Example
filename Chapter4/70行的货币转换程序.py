#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import urllib2
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        date = self.getData()
        rates = sorted(self.rates.keys())

        datelabel = QLabel(date)
        self.fc = QComboBox()
        self.fc.addItems(rates)

        self.sb = QSpinBox()
        self.sb.setRange(0.01, 10000000.00)
        self.sb.setValue(1.00)

        self.tc = QComboBox()
        self.tc.addItems(rates)

        self.lb = QLabel("1.00")

        grid = QGridLayout()
        grid.addWidget(datelabel, 0, 0)
        grid.addWidget(self.fc, 1, 0)
        grid.addWidget(self.tc, 2, 0)
        grid.addWidget(self.sb, 1, 1)
        grid.addWidget(self.lb, 2, 1)
        self.setLayout(grid)

        self.connect(self.fc, SIGNAL('currentIndexChanged(int)'), self.updateUI)
        self.connect(self.tc, SIGNAL('currentIndexChanged(int)'), self.updateUI)
        self.connect(self.sb, SIGNAL('valueChanged(double)'), self.updateUI)

        self.setWindowTitle('Currency')

    def updateUI(self):
        t = unicode(self.fc.currentText())
        f = unicode(self.tc.currentText())
        amount = (self.rates[f]/self.rates[t])*self.sb.value()
        self.lb.setText("%0.2f"%amount)

    def getData(self):
        self.rates = {}
        try:
            date = 'Unknown'
            fh = urllib2.urlopen('http://www.bankofcanada.ca/en/markets/csv/exchange_eng.csv')
            for line in fh:
                if not line or line.startswith('#'):
                    continue
                fields = line.split(',')
                if line.startswith('Date '):
                    date = fields[-1]
                else:
                    try:
                        value = float(fields[-1])
                        self.rates[unicode(fields[0])] = value
                    except ValueError:
                        pass
            return 'Exchange Rates Date: '+ date
        except Exception, e:
            return 'Failed to download:\n%s'%e.message

app = QApplication(sys.argv)
f = Form()
f.show()
app.exec_()