# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'R:\Projets\DBAlbums.Github\DBPARAMS.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_UpdateWindows(object):
    def setupUi(self, UpdateWindows):
        UpdateWindows.setObjectName("UpdateWindows")
        UpdateWindows.resize(1072, 958)
        self.gridLayout = QtWidgets.QGridLayout(UpdateWindows)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayoutprepare = QtWidgets.QHBoxLayout()
        self.horizontalLayoutprepare.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayoutprepare.setObjectName("horizontalLayoutprepare")
        self.comboBox_Envt = QtWidgets.QComboBox(UpdateWindows)
        self.comboBox_Envt.setObjectName("comboBox_Envt")
        self.horizontalLayoutprepare.addWidget(self.comboBox_Envt)
        self.lab_envt = QtWidgets.QLabel(UpdateWindows)
        self.lab_envt.setObjectName("lab_envt")
        self.horizontalLayoutprepare.addWidget(self.lab_envt)
        self.verticalLayout.addLayout(self.horizontalLayoutprepare)
        self.horizontalLayoutrelease = QtWidgets.QHBoxLayout()
        self.horizontalLayoutrelease.setObjectName("horizontalLayoutrelease")
        self.tableView_envt = QtWidgets.QTableView(UpdateWindows)
        self.tableView_envt.setObjectName("tableView_envt")
        self.horizontalLayoutrelease.addWidget(self.tableView_envt)
        self.tableView_category = QtWidgets.QTableView(UpdateWindows)
        self.tableView_category.setObjectName("tableView_category")
        self.horizontalLayoutrelease.addWidget(self.tableView_category)
        self.tableView_listcategory = QtWidgets.QTableView(UpdateWindows)
        self.tableView_listcategory.setObjectName("tableView_listcategory")
        self.horizontalLayoutrelease.addWidget(self.tableView_listcategory)
        self.verticalLayout.addLayout(self.horizontalLayoutrelease)
        self.horizontalLayoutcommands = QtWidgets.QHBoxLayout()
        self.horizontalLayoutcommands.setObjectName("horizontalLayoutcommands")
        self.btn_save = QtWidgets.QPushButton(UpdateWindows)
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayoutcommands.addWidget(self.btn_save)
        self.btn_quit = QtWidgets.QPushButton(UpdateWindows)
        self.btn_quit.setObjectName("btn_quit")
        self.horizontalLayoutcommands.addWidget(self.btn_quit)
        self.verticalLayout.addLayout(self.horizontalLayoutcommands)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(UpdateWindows)
        QtCore.QMetaObject.connectSlotsByName(UpdateWindows)

    def retranslateUi(self, UpdateWindows):
        _translate = QtCore.QCoreApplication.translate
        UpdateWindows.setWindowTitle(_translate("UpdateWindows", "Form"))
        self.lab_envt.setText(_translate("UpdateWindows", "Environment"))
        self.btn_save.setText(_translate("UpdateWindows", "Save"))
        self.btn_quit.setText(_translate("UpdateWindows", "Abort"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    UpdateWindows = QtWidgets.QWidget()
    ui = Ui_UpdateWindows()
    ui.setupUi(UpdateWindows)
    UpdateWindows.show()
    sys.exit(app.exec_())

