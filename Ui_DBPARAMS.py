# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'R:\Projets\DBAlbums.Github\DBPARAMS.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ParamsJson(object):
    def setupUi(self, ParamsJson):
        ParamsJson.setObjectName("ParamsJson")
        ParamsJson.resize(1072, 958)
        self.gridLayout = QtWidgets.QGridLayout(ParamsJson)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayoutenvt = QtWidgets.QVBoxLayout()
        self.verticalLayoutenvt.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayoutenvt.setObjectName("verticalLayoutenvt")
        self.label = QtWidgets.QLabel(ParamsJson)
        self.label.setObjectName("label")
        self.verticalLayoutenvt.addWidget(self.label)
        self.line_2 = QtWidgets.QFrame(ParamsJson)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayoutenvt.addWidget(self.line_2)
        self.tableWidget_general = QtWidgets.QTableWidget(ParamsJson)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_general.sizePolicy().hasHeightForWidth())
        self.tableWidget_general.setSizePolicy(sizePolicy)
        self.tableWidget_general.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_general.setObjectName("tableWidget_general")
        self.tableWidget_general.setColumnCount(0)
        self.tableWidget_general.setRowCount(0)
        self.verticalLayoutenvt.addWidget(self.tableWidget_general)
        self.horizontalLayout.addLayout(self.verticalLayoutenvt)
        self.line = QtWidgets.QFrame(ParamsJson)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayoutcombo = QtWidgets.QHBoxLayout()
        self.horizontalLayoutcombo.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayoutcombo.setObjectName("horizontalLayoutcombo")
        self.lab_envt = QtWidgets.QLabel(ParamsJson)
        self.lab_envt.setObjectName("lab_envt")
        self.horizontalLayoutcombo.addWidget(self.lab_envt)
        self.comboBox_Envt = QtWidgets.QComboBox(ParamsJson)
        self.comboBox_Envt.setObjectName("comboBox_Envt")
        self.horizontalLayoutcombo.addWidget(self.comboBox_Envt)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutcombo.addItem(spacerItem)
        self.verticalLayout_7.addLayout(self.horizontalLayoutcombo)
        self.horizontalLayoutrelease = QtWidgets.QHBoxLayout()
        self.horizontalLayoutrelease.setObjectName("horizontalLayoutrelease")
        self.tableWidget_envt = QtWidgets.QTableWidget(ParamsJson)
        self.tableWidget_envt.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_envt.sizePolicy().hasHeightForWidth())
        self.tableWidget_envt.setSizePolicy(sizePolicy)
        self.tableWidget_envt.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_envt.setAlternatingRowColors(False)
        self.tableWidget_envt.setObjectName("tableWidget_envt")
        self.tableWidget_envt.setColumnCount(0)
        self.tableWidget_envt.setRowCount(0)
        self.horizontalLayoutrelease.addWidget(self.tableWidget_envt)
        self.tableWidget_category = QtWidgets.QTableWidget(ParamsJson)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_category.sizePolicy().hasHeightForWidth())
        self.tableWidget_category.setSizePolicy(sizePolicy)
        self.tableWidget_category.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_category.setObjectName("tableWidget_category")
        self.tableWidget_category.setColumnCount(0)
        self.tableWidget_category.setRowCount(0)
        self.horizontalLayoutrelease.addWidget(self.tableWidget_category)
        self.tableWidget_listcategory = QtWidgets.QTableWidget(ParamsJson)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_listcategory.sizePolicy().hasHeightForWidth())
        self.tableWidget_listcategory.setSizePolicy(sizePolicy)
        self.tableWidget_listcategory.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_listcategory.setObjectName("tableWidget_listcategory")
        self.tableWidget_listcategory.setColumnCount(0)
        self.tableWidget_listcategory.setRowCount(0)
        self.horizontalLayoutrelease.addWidget(self.tableWidget_listcategory)
        self.tableWidget_infos = QtWidgets.QTableWidget(ParamsJson)
        self.tableWidget_infos.setObjectName("tableWidget_infos")
        self.tableWidget_infos.setColumnCount(0)
        self.tableWidget_infos.setRowCount(0)
        self.horizontalLayoutrelease.addWidget(self.tableWidget_infos)
        self.verticalLayout_7.addLayout(self.horizontalLayoutrelease)
        self.horizontalLayout.addLayout(self.verticalLayout_7)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayoutcommands = QtWidgets.QHBoxLayout()
        self.horizontalLayoutcommands.setObjectName("horizontalLayoutcommands")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutcommands.addItem(spacerItem1)
        self.btn_save = QtWidgets.QPushButton(ParamsJson)
        self.btn_save.setEnabled(False)
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayoutcommands.addWidget(self.btn_save)
        self.btn_quit = QtWidgets.QPushButton(ParamsJson)
        self.btn_quit.setObjectName("btn_quit")
        self.horizontalLayoutcommands.addWidget(self.btn_quit)
        self.verticalLayout.addLayout(self.horizontalLayoutcommands)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(ParamsJson)
        QtCore.QMetaObject.connectSlotsByName(ParamsJson)

    def retranslateUi(self, ParamsJson):
        _translate = QtCore.QCoreApplication.translate
        ParamsJson.setWindowTitle(_translate("ParamsJson", "Form"))
        self.label.setText(_translate("ParamsJson", "General"))
        self.lab_envt.setText(_translate("ParamsJson", "Environment"))
        self.btn_save.setText(_translate("ParamsJson", "Save Json"))
        self.btn_quit.setText(_translate("ParamsJson", "Quit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ParamsJson = QtWidgets.QWidget()
    ui = Ui_ParamsJson()
    ui.setupUi(ParamsJson)
    ParamsJson.show()
    sys.exit(app.exec_())

