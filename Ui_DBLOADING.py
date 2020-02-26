# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'R:\Python\DBAlbums\DBLOADING.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoadingWindow(object):
    def setupUi(self, LoadingWindow):
        LoadingWindow.setObjectName("LoadingWindow")
        LoadingWindow.resize(450, 350)
        LoadingWindow.setStyleSheet("border-radius: 10px;")
        self.verticalLayout = QtWidgets.QVBoxLayout(LoadingWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_logo = QtWidgets.QHBoxLayout()
        self.horizontalLayout_logo.setObjectName("horizontalLayout_logo")
        self.lab_logo = QtWidgets.QLabel(LoadingWindow)
        self.lab_logo.setText("")
        self.lab_logo.setObjectName("lab_logo")
        self.horizontalLayout_logo.addWidget(self.lab_logo)
        self.lab_text = QtWidgets.QLabel(LoadingWindow)
        self.lab_text.setText("")
        self.lab_text.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_text.setObjectName("lab_text")
        self.horizontalLayout_logo.addWidget(self.lab_text)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_logo.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_logo)
        self.horizontalLayout_tab = QtWidgets.QHBoxLayout()
        self.horizontalLayout_tab.setObjectName("horizontalLayout_tab")
        self.tabWidget = QtWidgets.QTabWidget(LoadingWindow)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setAccessibleName("")
        self.tab_1.setStyleSheet("")
        self.tab_1.setObjectName("tab_1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.tableWid1 = QtWidgets.QTableView(self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWid1.sizePolicy().hasHeightForWidth())
        self.tableWid1.setSizePolicy(sizePolicy)
        self.tableWid1.setMinimumSize(QtCore.QSize(0, 0))
        self.tableWid1.setStyleSheet("alternate-background-color: #D9D9D9;                                background-color: #E5E5E5;")
        self.tableWid1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWid1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableWid1.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWid1.setAlternatingRowColors(True)
        self.tableWid1.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWid1.setObjectName("tableWid1")
        self.gridLayout.addWidget(self.tableWid1, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableWid2 = QtWidgets.QTableView(self.tab_2)
        self.tableWid2.setStyleSheet("alternate-background-color: #D9D9D9;                                background-color: #E5E5E5;")
        self.tableWid2.setAlternatingRowColors(True)
        self.tableWid2.setObjectName("tableWid2")
        self.gridLayout_3.addWidget(self.tableWid2, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.tableWid3 = QtWidgets.QTableView(self.tab_3)
        self.tableWid3.setStyleSheet("alternate-background-color: #D9D9D9;                                background-color: #E5E5E5;")
        self.tableWid3.setAlternatingRowColors(True)
        self.tableWid3.setObjectName("tableWid3")
        self.gridLayout_5.addWidget(self.tableWid3, 0, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.horizontalLayout_tab.addWidget(self.tabWidget)
        self.verticalLayout.addLayout(self.horizontalLayout_tab)

        self.retranslateUi(LoadingWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(LoadingWindow)

    def retranslateUi(self, LoadingWindow):
        _translate = QtCore.QCoreApplication.translate
        LoadingWindow.setWindowTitle(_translate("LoadingWindow", "Form"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("LoadingWindow", "Style"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("LoadingWindow", "Volume"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("LoadingWindow", "Year"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LoadingWindow = QtWidgets.QWidget()
    ui = Ui_LoadingWindow()
    ui.setupUi(LoadingWindow)
    LoadingWindow.show()
    sys.exit(app.exec_())
