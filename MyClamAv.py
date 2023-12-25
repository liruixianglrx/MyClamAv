from PyQt5 import QtWidgets, QtGui
import sys
import os
from PyQt5.QtCore import QEventLoop, QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QCheckBox, QPushButton, QWidget, QMessageBox, QTableWidgetItem, QHeaderView
import webbrowser
from execute import *
from VirusTotal import VirusTotalScanner as MyClamVirusTotalScanner
from MainUI import Ui_MainWindow as MyClamUiMainWindow

class MyClamMainWindow(QMainWindow, MyClamUiMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.file_scan.clicked.connect(self.myclam_begin_file_scan)
        self.full_scan.clicked.connect(self.myclam_begin_full_scan)
        self.settings.clicked.connect(self.myclam_begin_settings)
        self.update_db.clicked.connect(self.myclam_begin_fresh)
        self.scanner = MyClamVirusTotalScanner()
        self.blackmail.clicked.connect(self.myclam_begin_blackmail)
        self.url_scan.clicked.connect(self.myclam_begin_url_scan)

    def myclam_begin_blackmail(self):
        open_file_name = QFileDialog.getOpenFileName(self, '选择文件')
        positives, total = self.scanner.scan_file(open_file_name[0])
        self.myclam_show_result_dialog("文件检测结果", f"被不同检测手段判为恶意软件次数：{positives}/{total}")

    def myclam_begin_url_scan(self):
        url, ok = QInputDialog.getText(self, '恶意URL检测', '请输入待检测的URL:')
        positives, total = self.scanner.scan_url(url)
        self.myclam_show_result_dialog("URL检测结果", f"被不同检测手段判为恶意软件次数：{positives}/{total}")

    def myclam_begin_file_scan(self):
        items = ('选择文件扫描', '选择文件夹扫描')
        item, ok = QInputDialog.getItem(self, "选择扫描", 'choose', items, 0, False)
        if ok and item:
            if item == '选择文件扫描':
                open_file_name = QFileDialog.getOpenFileName(self, '选择文件')
                myclam_execute_choose(open_file_name[0])
            else:
                open_file_name = QFileDialog.getExistingDirectory(self, '选择文件夹')
                myclam_execute_choose(open_file_name)

    def myclam_begin_full_scan(self):
        myclam_execute_scan()

    def myclam_begin_settings(self):
        self.settings_window = MyClamSettingsWindow()
        self.settings_window.show()

    def myclam_begin_fresh(self):
        myclam_execute_fresh()

    def myclam_show_result_dialog(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

class MyClamSettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.myclam_init_ui()

    def myclam_init_ui(self):
        self.cb3 = QCheckBox("扫描以(.*)的文件", self)
        self.cb4 = QCheckBox("扫描大于20M的文件", self)
        self.cb5 = QCheckBox("扫描文件下所有子文件", self)

        bt = QPushButton('Back', self)

        self.resize(357, 507)
        self.setWindowTitle('设置')

        self.cb3.move(35, 110)
        self.cb4.move(35, 150)
        self.cb5.move(35, 190)

        bt.move(130, 370)

        if myclam_setor[2] == 1:
            self.cb3.setChecked(True)
        if myclam_setor[3] == 1:
            self.cb4.setChecked(True)
        if myclam_setor[4] == 1:
            self.cb5.setChecked(True)

        self.cb3.stateChanged.connect(self.myclam_change_cb3)
        self.cb4.stateChanged.connect(self.myclam_change_cb4)
        self.cb5.stateChanged.connect(self.myclam_change_cb5)

        bt.clicked.connect(self.myclam_close_window)

        self.show()

    def myclam_close_window(self):
        self.close()

    def myclam_change_cb3(self):
        myclam_setor[2] = 1 if self.cb3.isChecked() else 0

    def myclam_change_cb4(self):
        myclam_setor[3] = 1 if self.cb4.isChecked() else 0

    def myclam_change_cb5(self):
        myclam_setor[4] = 1 if self.cb5.isChecked() else 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyClamMainWindow()
    window.show()
    sys.exit(app.exec_())
