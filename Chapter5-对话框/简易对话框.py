#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class PenPropertiesDlg(QDialog):
    def __init__(self, parent=None):
        super(PenPropertiesDlg, self).__init__(parent)

        widthLabel = QLabel('&Width')

        self.widthSpinBox = QSpinBox()
        widthLabel.setBuddy(self.widthSpinBox)
        self.widthSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.widthSpinBox.setRange(0,24)

        self.beveledCheckBox = QCheckBox('&Beveled Edges')

        styleLabel = QLabel('&Style:')

        self.styleCombox = QComboBox()
        styleLabel.setBuddy(self.styleCombox)
        self.styleCombox.addItems(['Solid', 'Dashed', 'Dotted', 'DashDotted', 'DashDotDotted'])

        okbt = QPushButton('&OK')
        canclebt = QPushButton('Cancel')

        la = QHBoxLayout()
        la.addStretch()
        la.addWidget(okbt)
        la.addWidget(canclebt)

        gl = QGridLayout()
        gl.addWidget(widthLabel, 0, 0)
        gl.addWidget(self.widthSpinBox, 0, 1)
        gl.addWidget(self.beveledCheckBox, 0, 2)
        gl.addWidget(styleLabel, 1, 0)
        gl.addWidget(self.styleCombox, 1, 1, 1, 2)
        gl.addLayout(la, 2, 0, 1, 3)

        self.setLayout(gl)
        self.setWindowTitle(u'简易对话框')

        self.connect(okbt, SIGNAL('clicked()'), self, SLOT('accept()'))
        self.connect(canclebt, SIGNAL('clicked()'), self, SLOT('reject()'))

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        bt = QPushButton(u'模态对话框')
        la = QHBoxLayout()
        la.addWidget(bt)

        self.setLayout(la)
        self.setWindowTitle(u'简易对话框')

        self.connect(bt, SIGNAL('clicked()'), self.setPenPro)

        self.width = 10
        self.beleve = True
        self.style = 'Dashed'

    def setPenPro(self):
        f = PenPropertiesDlg(self)
        f.widthSpinBox.setValue(self.width)
        f.beveledCheckBox.setChecked(self.beleve)
        f.styleCombox.setCurrentIndex(f.styleCombox.findText(self.style))
        if f.exec_():
            print '返回True'
            self.width = f.widthSpinBox.value()
            self.beleve = f.beveledCheckBox.isChecked()
            self.style = unicode(f.styleCombox.currentText())
            self.updateData()
        else:
            print '返回False'

    def updateData(self):
        print 'width', self.width
        print 'beleve', self.beleve
        print 'style', self.style

app = QApplication(sys.argv)
f = Form()
f.show()
app.exec_()