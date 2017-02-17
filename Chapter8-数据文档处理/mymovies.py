#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_mymovies
import qrc_resources

class MyMoviesMW(QMainWindow, ui_mymovies.Ui_mymoviesmw):
    def __init__(self, parent=None):
        super(MyMoviesMW, self).__init__(parent)

        self.setupUi(self)
        self.setupMyUI()

    def setupMyUI(self):
        fileNewAction = QAction(QIcon(':/filenew'), u'新建', self)
        fileOpenAction = QAction(QIcon(':/fileopen'), u'打开', self)
        fileSaveAction = QAction(QIcon(':/filesave'), u'保存', self)
        fileSaveAsAction = QAction(QIcon(':/filesaveas'), u'另存为', self)
        fileQuitAction = QAction(QIcon(':/filequit'), u'退出', self)

        editAddAction = QAction(QIcon(':/editadd'), u'增加', self)
        editEditAction = QAction(QIcon(':/editedit'), u'编辑', self)
        editDelAction = QAction(QIcon(':/editdelete'), u'删除', self)

        self.tableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.tableWidget.addAction(fileQuitAction)

        self.fileMenu.addAction(fileNewAction)
        self.fileMenu.addAction(fileOpenAction)
        self.fileMenu.addAction(fileSaveAction)
        self.fileMenu.addAction(fileSaveAsAction)
        self.fileMenu.addAction(fileQuitAction)

        self.editMenu.addAction(editAddAction)
        self.editMenu.addAction(editEditAction)
        self.editMenu.addAction(editDelAction)

        self.connect(fileQuitAction, SIGNAL('triggered()'), self, SLOT('close()'))

        self.leftToolBar.addAction(fileNewAction)
        self.leftToolBar.addAction(fileOpenAction)
        self.leftToolBar.addAction(fileSaveAction)
        self.rightToolBar.addAction(editAddAction)
        self.rightToolBar.addAction(editEditAction)
        self.rightToolBar.addAction(editDelAction)

        self.updateTable()

    def updateTable(self, current=None):
        """

        :param current:
        :return:
        """
        self.tableWidget.clear()
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['Title', 'Year', 'Mins', 'Acquired', 'Notes'])
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget.setSelectionMode(QTableWidget.SingleSelection)

import sys
app = QApplication(sys.argv)
f = MyMoviesMW()
f.show()
app.exec_()