from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
from PyQt5.QtCore import QEventLoop, QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QCheckBox, QPushButton, QWidget
from exeUI import Ui_Dialog as MyClamUiDialog

myclam_setor = [0, 0, 0, 0, 0, 0]


class MyClamEmittingStr(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))
        loop = QEventLoop()
        QTimer.singleShot(1000, loop.quit)
        loop.exec_()


class MyClamControlBoard(QDialog, MyClamUiDialog):
    def __init__(self):
        super(MyClamControlBoard, self).__init__()
        self.setupUi(self)
        # 将输出重定向到textBrowser中
        sys.stdout = MyClamEmittingStr(textWritten=self.output_written)
        sys.stderr = MyClamEmittingStr(textWritten=self.output_written)

    def output_written(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def fresh(self):
        print('正在更新病毒库\n')
        d = os.popen("freshclam")
        f = d.read()
        print(f)
        print(".----------- 更新完成 -----------\n")
        print("更新完成!\n")

    def scan(self):
        print('正在病毒扫描\n')
        a = "clamscan --recursive /"
        for i in range(4):
            if myclam_white_choosen[i] == 1:
                a = a + " " + "--exclude-dir=" + myclam_whitelist[i]

        if myclam_setor[3] == 1:
            a = a + " " + "--max-filesize=20M"
            print(a)
        d = os.popen(a)
        f = d.read()
        print(f)
        print(".----------- 扫描结束 -----------\n")
        print("扫描完成!\n")

    def choose(self, openfilename):
        print('正在病毒扫描\n')
        if myclam_setor[3] == 1:
            a = "clamscan --recursive" + " " + "--max-filesize=20M" + " " + openfilename
            print(a)
        else:
            a = "clamscan --recursive" + " " + openfilename
        d = os.popen(a)
        f = d.read()
        print(f)
        print(".----------- 扫描结束 -----------\n")
        print("扫描完成!\n")


def myclam_execute_fresh():
    win = MyClamControlBoard()
    win.setWindowTitle('病毒库更新')
    win.show()
    win.fresh()
    win.exec_()


def myclam_execute_scan():
    win = MyClamControlBoard()
    win.setWindowTitle('病毒扫描')
    win.show()
    win.scan()
    win.exec_()


def myclam_execute_choose(openfilename):
    win = MyClamControlBoard()
    win.setWindowTitle('选择文件扫描')
    win.show()
    win.choose(openfilename)
    win.exec_()
