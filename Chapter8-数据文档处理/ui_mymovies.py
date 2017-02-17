# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mymovies.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_mymoviesmw(object):
    def setupUi(self, mymoviesmw):
        mymoviesmw.setObjectName(_fromUtf8("mymoviesmw"))
        mymoviesmw.resize(487, 343)
        self.centralwidget = QtGui.QWidget(mymoviesmw)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableWidget = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        mymoviesmw.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(mymoviesmw)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 487, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.fileMenu = QtGui.QMenu(self.menubar)
        self.fileMenu.setObjectName(_fromUtf8("fileMenu"))
        self.editMenu = QtGui.QMenu(self.menubar)
        self.editMenu.setObjectName(_fromUtf8("editMenu"))
        self.helpMenu = QtGui.QMenu(self.menubar)
        self.helpMenu.setObjectName(_fromUtf8("helpMenu"))
        mymoviesmw.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(mymoviesmw)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        mymoviesmw.setStatusBar(self.statusbar)
        self.leftToolBar = QtGui.QToolBar(mymoviesmw)
        self.leftToolBar.setObjectName(_fromUtf8("leftToolBar"))
        mymoviesmw.addToolBar(QtCore.Qt.TopToolBarArea, self.leftToolBar)
        self.rightToolBar = QtGui.QToolBar(mymoviesmw)
        self.rightToolBar.setObjectName(_fromUtf8("rightToolBar"))
        mymoviesmw.addToolBar(QtCore.Qt.TopToolBarArea, self.rightToolBar)
        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.editMenu.menuAction())
        self.menubar.addAction(self.helpMenu.menuAction())

        self.retranslateUi(mymoviesmw)
        QtCore.QMetaObject.connectSlotsByName(mymoviesmw)

    def retranslateUi(self, mymoviesmw):
        mymoviesmw.setWindowTitle(_translate("mymoviesmw", "MyMovies", None))
        self.fileMenu.setTitle(_translate("mymoviesmw", "&File", None))
        self.editMenu.setTitle(_translate("mymoviesmw", "&Edit", None))
        self.helpMenu.setTitle(_translate("mymoviesmw", "&Help", None))
        self.leftToolBar.setWindowTitle(_translate("mymoviesmw", "toolBar", None))
        self.rightToolBar.setWindowTitle(_translate("mymoviesmw", "toolBar", None))

