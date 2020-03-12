# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'R:\Python\DBAlbums\DBVIEWTBL.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ViewTablesDatas(object):
    def setupUi(self, ViewTablesDatas):
        ViewTablesDatas.setObjectName("ViewTablesDatas")
        ViewTablesDatas.resize(1120, 934)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(ViewTablesDatas)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboboxlist = QtWidgets.QComboBox(ViewTablesDatas)
        self.comboboxlist.setObjectName("comboboxlist")
        self.horizontalLayout.addWidget(self.comboboxlist)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.viewtable = QtWidgets.QTableView(ViewTablesDatas)
        self.viewtable.setObjectName("viewtable")
        self.verticalLayout.addWidget(self.viewtable)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnsav = QtWidgets.QPushButton(ViewTablesDatas)
        self.btnsav.setObjectName("btnsav")
        self.horizontalLayout_3.addWidget(self.btnsav)
        self.btncan = QtWidgets.QPushButton(ViewTablesDatas)
        self.btncan.setObjectName("btncan")
        self.horizontalLayout_3.addWidget(self.btncan)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.btnclo = QtWidgets.QPushButton(ViewTablesDatas)
        self.btnclo.setObjectName("btnclo")
        self.horizontalLayout_3.addWidget(self.btnclo)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(ViewTablesDatas)
        QtCore.QMetaObject.connectSlotsByName(ViewTablesDatas)

    def retranslateUi(self, ViewTablesDatas):
        _translate = QtCore.QCoreApplication.translate
        ViewTablesDatas.setWindowTitle(_translate("ViewTablesDatas", "Form"))
        self.btnsav.setText(_translate("ViewTablesDatas", "Save Modifications"))
        self.btncan.setText(_translate("ViewTablesDatas", "Cancel Modifications"))
        self.btnclo.setText(_translate("ViewTablesDatas", "Quit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ViewTablesDatas = QtWidgets.QWidget()
    ui = Ui_ViewTablesDatas()
    ui.setupUi(ViewTablesDatas)
    ViewTablesDatas.show()
    sys.exit(app.exec_())
