# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'R:\Python\DBAlbums\DBALBUMS.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1147, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_COM = QtWidgets.QHBoxLayout()
        self.horizontalLayout_COM.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_COM.setObjectName("horizontalLayout_COM")
        self.lab_search = QtWidgets.QLabel(self.centralwidget)
        self.lab_search.setObjectName("lab_search")
        self.horizontalLayout_COM.addWidget(self.lab_search)
        self.lin_search = QtWidgets.QLineEdit(self.centralwidget)
        self.lin_search.setObjectName("lin_search")
        self.horizontalLayout_COM.addWidget(self.lin_search)
        self.btn_clearsearch = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clearsearch.setStyleSheet("border: none;")
        self.btn_clearsearch.setText("")
        self.btn_clearsearch.setObjectName("btn_clearsearch")
        self.horizontalLayout_COM.addWidget(self.btn_clearsearch)
        self.chb_searchtracks = QtWidgets.QCheckBox(self.centralwidget)
        self.chb_searchtracks.setObjectName("chb_searchtracks")
        self.horizontalLayout_COM.addWidget(self.chb_searchtracks)
        self.com_category = QtWidgets.QComboBox(self.centralwidget)
        self.com_category.setObjectName("com_category")
        self.horizontalLayout_COM.addWidget(self.com_category)
        self.com_family = QtWidgets.QComboBox(self.centralwidget)
        self.com_family.setObjectName("com_family")
        self.horizontalLayout_COM.addWidget(self.com_family)
        self.com_genres = QtWidgets.QComboBox(self.centralwidget)
        self.com_genres.setObjectName("com_genres")
        self.horizontalLayout_COM.addWidget(self.com_genres)
        self.com_label = QtWidgets.QComboBox(self.centralwidget)
        self.com_label.setObjectName("com_label")
        self.horizontalLayout_COM.addWidget(self.com_label)
        self.com_year = QtWidgets.QComboBox(self.centralwidget)
        self.com_year.setObjectName("com_year")
        self.horizontalLayout_COM.addWidget(self.com_year)
        self.com_country = QtWidgets.QComboBox(self.centralwidget)
        self.com_country.setObjectName("com_country")
        self.horizontalLayout_COM.addWidget(self.com_country)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_COM.addItem(spacerItem)
        self.lab_comenvt = QtWidgets.QLabel(self.centralwidget)
        self.lab_comenvt.setText("")
        self.lab_comenvt.setObjectName("lab_comenvt")
        self.horizontalLayout_COM.addWidget(self.lab_comenvt)
        self.com_envt = QtWidgets.QComboBox(self.centralwidget)
        self.com_envt.setObjectName("com_envt")
        self.horizontalLayout_COM.addWidget(self.com_envt)
        self.verticalLayout.addLayout(self.horizontalLayout_COM)
        self.horizontalLayout_THU = QtWidgets.QHBoxLayout()
        self.horizontalLayout_THU.setObjectName("horizontalLayout_THU")
        self.verticalLayout.addLayout(self.horizontalLayout_THU)
        self.horizontalLayout_ALB = QtWidgets.QHBoxLayout()
        self.horizontalLayout_ALB.setObjectName("horizontalLayout_ALB")
        self.tbl_albums = QtWidgets.QTableView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbl_albums.sizePolicy().hasHeightForWidth())
        self.tbl_albums.setSizePolicy(sizePolicy)
        self.tbl_albums.setAlternatingRowColors(True)
        self.tbl_albums.setObjectName("tbl_albums")
        self.horizontalLayout_ALB.addWidget(self.tbl_albums)
        self.verticalLayout.addLayout(self.horizontalLayout_ALB)
        self.horizontalLayoutTRK = QtWidgets.QHBoxLayout()
        self.horizontalLayoutTRK.setObjectName("horizontalLayoutTRK")
        self.framecover = QtWidgets.QFrame(self.centralwidget)
        self.framecover.setMinimumSize(QtCore.QSize(400, 400))
        self.framecover.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.framecover.setFrameShadow(QtWidgets.QFrame.Raised)
        self.framecover.setObjectName("framecover")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.framecover)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayoutTRK.addWidget(self.framecover, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayoutLAB = QtWidgets.QHBoxLayout()
        self.horizontalLayoutLAB.setObjectName("horizontalLayoutLAB")
        self.lab_album = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lab_album.sizePolicy().hasHeightForWidth())
        self.lab_album.setSizePolicy(sizePolicy)
        self.lab_album.setMinimumSize(QtCore.QSize(0, 0))
        self.lab_album.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.lab_album.setObjectName("lab_album")
        self.horizontalLayoutLAB.addWidget(self.lab_album)
        self.lab_label = QtWidgets.QLabel(self.centralwidget)
        self.lab_label.setText("")
        self.lab_label.setObjectName("lab_label")
        self.horizontalLayoutLAB.addWidget(self.lab_label)
        self.verticalLayout_2.addLayout(self.horizontalLayoutLAB)
        self.tbl_tracks = QtWidgets.QTableView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbl_tracks.sizePolicy().hasHeightForWidth())
        self.tbl_tracks.setSizePolicy(sizePolicy)
        self.tbl_tracks.setAlternatingRowColors(True)
        self.tbl_tracks.setObjectName("tbl_tracks")
        self.verticalLayout_2.addWidget(self.tbl_tracks)
        self.horizontalLayoutTRK.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayoutTRK)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lab_search.setText(_translate("MainWindow", "Search"))
        self.chb_searchtracks.setText(_translate("MainWindow", "Search in tracks"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
