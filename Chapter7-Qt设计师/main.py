#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import findandreplacedlg

class FindAndReplaceDlg(QDialog, findandreplacedlg.Ui_FindAndReplaceDlg):
    def __init__(self, text, parent=None):
        super(FindAndReplaceDlg, self).__init__(parent)
        self.__text = unicode(text)
        self.__index = 0
        #设置ui里编辑好的控件
        self.setupUi(self)

        self.findButton.setFocusPolicy(Qt.NoFocus)
        self.replaceButton.setFocusPolicy(Qt.NoFocus)
        self.replaceAllButton.setFocusPolicy(Qt.NoFocus)

        self.updateUI()

    def updateUI(self):
        """
        更新用户界面状态
        :return:
        """
        enable = not self.findLineEdit.text().isEmpty()
        self.findButton.setEnabled(enable)
        self.replaceButton.setEnabled(enable)
        self.replaceAllButton.setEnabled(enable)

    @pyqtSignature('QString')
    def on_findLineEdit_textEdited(self, text):
        """
        使用setui后，自动连接的槽，上面的装饰器用来说明信号附带的参数类型
        :param text:
        :return:
        """
        print 'got change ', text
        self.__index = 0
        self.updateUI()

    @pyqtSignature("")
    def on_findButton_clicked(self):
        """
        findButton的clicked()信号自动回掉的槽
        :return:
        """
        regex = self.makeRegex()
        match = regex.search(self.__text, self.__index)
        if match is not None:
            self.__index = match.end()
            self.emit(SIGNAL('found'), match.start())
        else:
            self.emit(SIGNAL('notfound'))

    @pyqtSignature('')
    def on_replaceButton_clicked(self):
        """

        :return:
        """
        regex = self.makeRegex()
        self.__text = regex.sub(unicode(self.replaceLineEdit.text()), self.__text, 1)

    @pyqtSignature('')
    def on_replaceAllButton(self):
        """

        :return:
        """
        regex = self.makeRegex()
        self.__text = regex.sub(unicode(self.replaceLineEdit.text()), self.__text)


    def text(self):
        return self.__text

    def makeRegex(self):
        findText = unicode(self.findLineEdit.text())
        if unicode(self.syntaxComboBox.currentText()) == 'Literal':
            #将findText字符串变成转义的字符串，防止里面含有正则表达式特殊符号造成影响
            findText = re.escape(findText)
        flags = re.MULTILINE|re.DOTALL|re.UNICODE
        if not self.caseCheckBox.isChecked():
            flags |= re.IGNORECASE
        if self.wholeCheckBox.isChecked():
            findText = r'\b%s\b'%findText
        return re.compile(findText, flags)

    def found(self, where):
        """
        found信号回调的槽
        :return:
        """
        print 'found at %d'%where

    def notfound(self):
        """
        notfound信号回调的槽
        :return:
        """
        print 'no more found'


import sys
text = """US experience shows that, unlike traditional patents,
software patents do not encourage innovation and R&D, quite the
contrary. In particular they hurt small and medium-sized enterprises
and generally newcomers in the market. They will just weaken the market
and increase spending on patents and litigation, at the expense of
technological innovation and research. Especially dangerous are
attempts to abuse the patent system by preventing interoperability as a
means of avoiding competition with technological ability.
--- Extract quoted from Linus Torvalds and Alan Cox's letter
to the President of the European Parliament
http://www.effi.org/patentit/patents_torvalds_cox.html"""

app = QApplication(sys.argv)
f = FindAndReplaceDlg(text)
f.connect(f, SIGNAL('found'), f.found)
f.connect(f, SIGNAL('notfound'), f.notfound)
f.show()
app.exec_()

print f.text()