# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'R:\Python\DBAlbums\DBPARAMS.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ParamsJson(object):
    def setupUi(self, ParamsJson):
        ParamsJson.setObjectName("ParamsJson")
        ParamsJson.resize(1192, 876)
        self.verticalLayout = QtWidgets.QVBoxLayout(ParamsJson)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_main = QtWidgets.QHBoxLayout()
        self.horizontalLayout_main.setObjectName("horizontalLayout_main")
        self.verticalLayout_general = QtWidgets.QVBoxLayout()
        self.verticalLayout_general.setObjectName("verticalLayout_general")
        self.label_libgeneral = QtWidgets.QLabel(ParamsJson)
        self.label_libgeneral.setAlignment(QtCore.Qt.AlignCenter)
        self.label_libgeneral.setObjectName("label_libgeneral")
        self.verticalLayout_general.addWidget(self.label_libgeneral)
        self.tableWidget_general = QtWidgets.QTableWidget(ParamsJson)
        self.tableWidget_general.setAlternatingRowColors(True)
        self.tableWidget_general.setObjectName("tableWidget_general")
        self.tableWidget_general.setColumnCount(0)
        self.tableWidget_general.setRowCount(0)
        self.verticalLayout_general.addWidget(self.tableWidget_general)
        self.horizontalLayout_main.addLayout(self.verticalLayout_general)
        self.line = QtWidgets.QFrame(ParamsJson)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_main.addWidget(self.line)
        self.verticalLayout_environments = QtWidgets.QVBoxLayout()
        self.verticalLayout_environments.setObjectName("verticalLayout_environments")
        self.label_libenvt = QtWidgets.QLabel(ParamsJson)
        self.label_libenvt.setAlignment(QtCore.Qt.AlignCenter)
        self.label_libenvt.setObjectName("label_libenvt")
        self.verticalLayout_environments.addWidget(self.label_libenvt)
        self.horizontalLayout_combo = QtWidgets.QHBoxLayout()
        self.horizontalLayout_combo.setObjectName("horizontalLayout_combo")
        self.comboBox_Envt = QtWidgets.QComboBox(ParamsJson)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_Envt.sizePolicy().hasHeightForWidth())
        self.comboBox_Envt.setSizePolicy(sizePolicy)
        self.comboBox_Envt.setObjectName("comboBox_Envt")
        self.horizontalLayout_combo.addWidget(self.comboBox_Envt)
        self.btn_delenvt = QtWidgets.QPushButton(ParamsJson)
        self.btn_delenvt.setObjectName("btn_delenvt")
        self.horizontalLayout_combo.addWidget(self.btn_delenvt)
        self.btn_addenvt = QtWidgets.QPushButton(ParamsJson)
        self.btn_addenvt.setObjectName("btn_addenvt")
        self.horizontalLayout_combo.addWidget(self.btn_addenvt)
        self.verticalLayout_environments.addLayout(self.horizontalLayout_combo)
        self.tableWidget_envt = QtWidgets.QTableWidget(ParamsJson)
        self.tableWidget_envt.setAlternatingRowColors(True)
        self.tableWidget_envt.setObjectName("tableWidget_envt")
        self.tableWidget_envt.setColumnCount(0)
        self.tableWidget_envt.setRowCount(0)
        self.verticalLayout_environments.addWidget(self.tableWidget_envt)
        self.horizontalLayout_main.addLayout(self.verticalLayout_environments)
        self.verticalLayout_category = QtWidgets.QVBoxLayout()
        self.verticalLayout_category.setObjectName("verticalLayout_category")
        self.label_libcate = QtWidgets.QLabel(ParamsJson)
        self.label_libcate.setAlignment(QtCore.Qt.AlignCenter)
        self.label_libcate.setObjectName("label_libcate")
        self.verticalLayout_category.addWidget(self.label_libcate)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox_cate = QtWidgets.QComboBox(ParamsJson)
        self.comboBox_cate.setObjectName("comboBox_cate")
        self.horizontalLayout.addWidget(self.comboBox_cate)
        self.btn_delcate = QtWidgets.QPushButton(ParamsJson)
        self.btn_delcate.setObjectName("btn_delcate")
        self.horizontalLayout.addWidget(self.btn_delcate)
        self.btn_addcate = QtWidgets.QPushButton(ParamsJson)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_addcate.sizePolicy().hasHeightForWidth())
        self.btn_addcate.setSizePolicy(sizePolicy)
        self.btn_addcate.setMinimumSize(QtCore.QSize(0, 0))
        self.btn_addcate.setBaseSize(QtCore.QSize(0, 0))
        self.btn_addcate.setObjectName("btn_addcate")
        self.horizontalLayout.addWidget(self.btn_addcate)
        self.verticalLayout_category.addLayout(self.horizontalLayout)
        self.tableWidget_category = QtWidgets.QTableWidget(ParamsJson)
        self.tableWidget_category.setAlternatingRowColors(True)
        self.tableWidget_category.setObjectName("tableWidget_category")
        self.tableWidget_category.setColumnCount(0)
        self.tableWidget_category.setRowCount(0)
        self.verticalLayout_category.addWidget(self.tableWidget_category)
        self.textEdit = QtWidgets.QTextEdit(ParamsJson)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_category.addWidget(self.textEdit)
        self.horizontalLayout_main.addLayout(self.verticalLayout_category)
        self.verticalLayout.addLayout(self.horizontalLayout_main)
        self.horizontalLayout_menu = QtWidgets.QHBoxLayout()
        self.horizontalLayout_menu.setObjectName("horizontalLayout_menu")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_menu.addItem(spacerItem)
        self.btn_save = QtWidgets.QPushButton(ParamsJson)
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout_menu.addWidget(self.btn_save)
        self.btn_open = QtWidgets.QPushButton(ParamsJson)
        self.btn_open.setObjectName("btn_open")
        self.horizontalLayout_menu.addWidget(self.btn_open)
        self.btn_quit = QtWidgets.QPushButton(ParamsJson)
        self.btn_quit.setObjectName("btn_quit")
        self.horizontalLayout_menu.addWidget(self.btn_quit)
        self.verticalLayout.addLayout(self.horizontalLayout_menu)

        self.retranslateUi(ParamsJson)
        QtCore.QMetaObject.connectSlotsByName(ParamsJson)

    def retranslateUi(self, ParamsJson):
        _translate = QtCore.QCoreApplication.translate
        ParamsJson.setWindowTitle(_translate("ParamsJson", "Form"))
        self.label_libgeneral.setText(_translate("ParamsJson", "General : Parameters"))
        self.label_libenvt.setText(_translate("ParamsJson", "Environment : Database"))
        self.btn_delenvt.setText(_translate("ParamsJson", "Del"))
        self.btn_addenvt.setText(_translate("ParamsJson", "Add"))
        self.label_libcate.setText(_translate("ParamsJson", "Category : Storage"))
        self.btn_delcate.setText(_translate("ParamsJson", "Del"))
        self.btn_addcate.setText(_translate("ParamsJson", "Add"))
        self.btn_save.setText(_translate("ParamsJson", "Save Json"))
        self.btn_open.setText(_translate("ParamsJson", "View Json"))
        self.btn_quit.setText(_translate("ParamsJson", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ParamsJson = QtWidgets.QWidget()
    ui = Ui_ParamsJson()
    ui.setupUi(ParamsJson)
    ParamsJson.show()
    sys.exit(app.exec_())
