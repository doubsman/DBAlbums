# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'R:\Python\DBAlbums\DBCONTROL.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ViewControlDatas(object):
    def setupUi(self, ViewControlDatas):
        ViewControlDatas.setObjectName("ViewControlDatas")
        ViewControlDatas.resize(1120, 934)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(ViewControlDatas)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboboxlist = QtWidgets.QComboBox(ViewControlDatas)
        self.comboboxlist.setObjectName("comboboxlist")
        self.horizontalLayout.addWidget(self.comboboxlist)
        self.btngo = QtWidgets.QPushButton(ViewControlDatas)
        self.btngo.setObjectName("btngo")
        self.horizontalLayout.addWidget(self.btngo)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textEdit = QtWidgets.QTextEdit(ViewControlDatas)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.btnclo = QtWidgets.QPushButton(ViewControlDatas)
        self.btnclo.setObjectName("btnclo")
        self.horizontalLayout_3.addWidget(self.btnclo)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(ViewControlDatas)
        QtCore.QMetaObject.connectSlotsByName(ViewControlDatas)

    def retranslateUi(self, ViewControlDatas):
        _translate = QtCore.QCoreApplication.translate
        ViewControlDatas.setWindowTitle(_translate("ViewControlDatas", "Form"))
        self.btngo.setText(_translate("ViewControlDatas", "Go"))
        self.btnclo.setText(_translate("ViewControlDatas", "Quit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ViewControlDatas = QtWidgets.QWidget()
    ui = Ui_ViewControlDatas()
    ui.setupUi(ViewControlDatas)
    ViewControlDatas.show()
    sys.exit(app.exec_())
