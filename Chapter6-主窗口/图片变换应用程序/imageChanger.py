#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#加载资源模块
import resources

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.image = QImage()

        self.imageLabel = QLabel()
        self.imageLabel.setMinimumSize(200, 200)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        #设置部件的上下文菜单策略
        self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
        #设置主窗口的中心部件
        self.setCentralWidget(self.imageLabel)
        #设置主窗口的停靠部件
        logDock = QDockWidget('log', self)
        logDock.setObjectName('LogDock')
        #设置主窗口允许的停靠区域
        logDock.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        #设置停靠窗口内嵌的列表部件
        self.list = QListWidget()
        logDock.setWidget(self.list)
        #在主窗口设置停靠部件
        self.addDockWidget(Qt.LeftDockWidgetArea, logDock)

        self.printer = None
        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        #设置主窗口的状态栏
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage('Ready', 5000)

        #创建用户动作
        fileNewAction = self.createAction('&New...', self.fileNew, QKeySequence.New, 'filenew', 'create a image file')
        fileQuitAction = self.createAction('&Quit', self.close, 'Ctrl+Q', 'filequit', 'Close the application')
        fileOpenAction = self.createAction('&Open', self.fileOpen, QKeySequence.Open, 'fileopen', 'open files')
        fileSaveAction = self.createAction('&Save', self.fileSave, QKeySequence.Save, 'filesave', 'save file')
        fileSaveAsAction = self.createAction('&SaveAs', self.fileSaveAs, 'Crtl+Shift+S', 'filesaveas', 'file save as')

        editZoomAction = self.createAction('&Zoom...', self.editZoom, 'Alt+Z', 'editzoom', 'Zoom the image')
        editInvertAction = self.createAction('&Invert', self.editInvert, 'Ctrl+I', 'editinvert', 'invert the image colors', True, 'toggled(bool)')
        editSwapAction = self.createAction('&Swap', self.editSwap, 'Ctrl+R', 'editswap', u'交换', True, 'toggled(bool)')

        mirrorGroup = QActionGroup(self)

        editUnMirrorAction = self.createAction('&Unmirror', self.editUnMirror, 'Ctrl+U', 'editunmirror', 'Umirror the image', True, 'toggled(bool)')
        editMirrorVAction = self.createAction('&MirrorVertical', self.editMirrorV, 'Ctrl+M+V', 'editmirrorvert', u'垂直镜像' , True, 'toggled(bool)')
        editMirrorHAction = self.createAction('&MirrorHorizontal', self.editMirrorH, 'Ctrl+M+H', 'editmirrorhoriz', u"水平镜像", True, 'toggled(bool)')
        editUnMirrorAction.setChecked(True)
        mirrorGroup.addAction(editUnMirrorAction)
        mirrorGroup.addAction(editMirrorVAction)
        mirrorGroup.addAction(editMirrorHAction)

        self.fileMenu = self.menuBar().addMenu('&File')

        self.fileMenuActions = (fileNewAction, fileOpenAction, fileSaveAction, fileSaveAsAction, None, fileQuitAction)

        self.addActions(self.fileMenu, self.fileMenuActions)

        self.connect(self.fileMenu, SIGNAL('aboutToShow()'), self.updateFileMenu)

        editMenu = self.menuBar().addMenu('&Edit')
        self.addActions(editMenu, (editInvertAction, editSwapAction, editZoomAction, None))

        mirrorMenu = editMenu.addMenu(QIcon(':/editmirror.png'), '&Mirror')

        self.addActions(mirrorMenu, (editUnMirrorAction, None, editMirrorHAction, editMirrorVAction))

        fileToolBar = self.addToolBar('File')
        fileToolBar.setObjectName('FileToolBar')
        self.addActions(fileToolBar, (fileNewAction, fileOpenAction, fileSaveAsAction))

        editToolBar = self.addToolBar('Edit')
        editToolBar.setObjectName('EditToolBar')
        self.addActions(editToolBar, (editInvertAction, editSwapAction, None, editUnMirrorAction, editMirrorHAction, editMirrorVAction))

        #创建工具栏内嵌的旋转按钮
        self.zoomSpinBox = QSpinBox()
        self.zoomSpinBox.setRange(1, 400)
        self.zoomSpinBox.setSuffix(' %')
        self.zoomSpinBox.setValue(100)
        self.zoomSpinBox.setToolTip('zoom the image')
        self.zoomSpinBox.setStatusTip(self.zoomSpinBox.toolTip())
        self.zoomSpinBox.setFocusPolicy(Qt.NoFocus)

        editToolBar.addWidget(self.zoomSpinBox)
        #根据部件上的菜单策略在部件上添加上下文菜单
        separator = QAction(self)
        #部件没有addSeparator方法，所以要创建一个
        separator.setSeparator(True)
        self.addActions(self.imageLabel, (editInvertAction, editSwapAction, separator, editUnMirrorAction, editMirrorHAction, editMirrorVAction))
        #是否有脏数据，即未保存的数据
        self.dirty = False
        #记录当前打开的文件
        self.fileName = None
        #记录最近操作过的文件列表
        self.recentFiles = None

        #每次重新打开主窗口时，恢复上次打开时的状态，动态更新文件菜单
        settings = QSettings()
        self.recentFiles = settings.value('RecentFiles').toStringList()
        size = settings.value('MainWindow/Size', QVariant(QSize(800, 600))).toSize()
        self.resize(size)
        position = settings.value('MainWindow/Position').toPoint()
        self.move(position)
        self.restoreState(settings.value('MainWindow/State').toByteArray())
        self.setWindowTitle('Image Changer')
        #利用最近打开的文件名列表，动态更新文件菜单
        self.updateFileMenu()
        #将长时间准备的加载文件处理即恢复上一次打开的文件，异步添加到事件循环队列里,参数0表示添加到事件队列后立即返回
        QTimer.singleShot(0, self.loadInitialFile)

    def closeEvent(self, event):
        """
        覆写MainWindow的close方法，在关闭前做处理
        :param event:
        :return:
        """
        if self.okToContinue():
            settings = QSettings()
            filename = QVariant(QString(self.fileName)) if self.fileName is not None else QVariant()
            settings.setValue('LastFile', filename)
            recentFiles = QVariant(self.recentFiles) if self.recentFiles else QVariant()
            settings.setValue('RecentFiles', recentFiles)
            settings.setValue('MainWindow/Size', QVariant(self.size()))
            settings.setValue('MainWindow/Position', QVariant(self.pos()))
            settings.setValue('MainWindow/State', QVariant(self.saveState()))

    def loadInitialFile(self):
        """

        :return:
        """
        pass

    def updateFileMenu(self):
        """
        当文件菜单显示前，回调的槽，用来动态更新文件菜单
        :return:
        """
        #没每次更新菜单时候，先删除当前菜单的所有动作
        self.fileMenu.clear()
        #把最后一个以外的动作添加到文件菜单
        self.addActions(self.fileMenu, self.fileMenuActions[:-1])
        #获取当前文件名
        current = QString(self.fileName) if self.fileName is not None else None
        recentFiles = []
        for fname in self.recentFiles:
            #在最近打开的文件里，除过自己，且确实存在该文件
            if fname != current and QFile.exists(fname):
                recentFiles.append(fname)
        if recentFiles:
            self.fileMenu.addSeparator()
            #以最近打开的文件创建用户动作
            for i, fname in enumerate(recentFiles):
                action = QAction(QIcon(':/icon.png'), '&%d. %s'%(i+1, QFileInfo(fname).fileName()), self)
                action.setData(QVariant(fname))
                self.connect(action, SIGNAL('triggered()'), self.loadFile)
                self.fileMenu.addAction(action)
        self.fileMenu.addSeparator()
        #把最后一个用户动作加上
        self.fileMenu.addAction(self.fileMenuActions[-1])

    def loadFile(self, fname):
        """

        :return:
        """
        pass

    def okToContinue(self):
        """
        在关闭前询问用户的意见，做处理
        :return:
        """
        #如果为保存标志为True
        if self.dirty:
            reply = QMessageBox.question(self, u'提示', u'保存未保存项？', QMessageBox.Yes, QMessageBox.No, QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                self.fileSave()
            else:
                return False
        return True

    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal='triggered()'):
        """
        创建动作的辅助函数
        :param text: 动作的文本
        :param slot: 动作触发的槽
        :param shortcut: 动作的快捷键
        :param icon: 动作显示的图标名字
        :param tip: 动作的提示文本
        :param checkable: 动作是否是复选
        :param signal: 动作发出的信号，默认为triggered（）
        :return: 设置好的动作对象
        """
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(':/%s.png'%icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)

        return action

    def addActions(self, target, actions):
        """
        动作添加的辅助方法
        :param target:要被添加动作的目标
        :param action:动作列表
        :return:无
        """
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def fileNew(self):
        """
        文件新建的槽
        :return:
        """
        if not self.okToContinue():
            return
        pass

        ###########测试动态菜单时候，请去掉updatefilemenu里的QFile.exists
        self.addRecentFiles('test10')
        self.dirty = True

    def addRecentFiles(self, fname):
        """
        设置self.recentFiles列表
        :param fname:
        :return:
        """
        if fname is None:return
        #recentfiles QStringList
        if not self.recentFiles.contains(fname):
            self.recentFiles.prepend(QString(fname))
            while self.recentFiles.count() > 9:
                self.recentFiles.takeLast()

    def fileOpen(self):
        """
        文件打开
        :return:
        """
        if not self.okToContinue():
            return
        import os
        dir = os.path.dirname(self.fileName) if self.fileName is not None else '.'
        formats = ['*.%s'%unicode(fmt).lower() for fmt in QImageReader.supportedImageFormats() ]
        fname  =unicode(QFileDialog.getOpenFileName(self, 'choose image', dir, 'image files(%s)'%'\n'.join(formats)))
        print 'got filename', fname
        if fname:
            self.loadFile(fname)
    def fileSave(self):
        """
        文件保存
        :return:
        """
        pass

    def fileSaveAs(self):
        """
        文件另存
        :return:
        """
        pass

    def editZoom(self):
        """

        :return:
        """
        pass

    def editInvert(self):
        """

        :return:
        """
        pass

    def editSwap(self):
        """

        :return:
        """
        pass

    def editUnMirror(self):
        """

        :return:
        """
        pass

    def editMirrorH(self):
        """

        :return:
        """
        pass

    def editMirrorV(self):
        """

        :return:
        """
        pass

app = QApplication(sys.argv)
#在这里设置组织名字，组织域名还有应用名字后，就可以直接引用QSettings了
app.setOrganizationName('Qtrac Ltd.')
app.setOrganizationDomain('qtrac.eu')
app.setApplicationName('image changer')
#设置应用程序图标
app.setWindowIcon(QIcon(':/icon.png'))
f = MainWindow()
f.show()
app.exec_()
