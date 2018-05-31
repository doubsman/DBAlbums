#! /usr/bin/python
# coding: utf-8

__author__ = "doubsman"
__copyright__ = "Copyright 2017, DBAlbums Project"
__credits__ = ["doubsman"]
__license__ = "GPL"
__version__ = "1.54"
__maintainer__ = "doubsman"
__email__ = "doubsman@doubsman.fr"
__status__ = "Production"

from sys import platform, argv, exit
from os import path, getcwd, remove
from csv import writer, QUOTE_ALL
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import (Qt, QDir, QTime, QTimer, pyqtSlot, QDateTime, QSettings, 
						QSize, QRect, qInstallMessageHandler, qDebug) 
from PyQt5.QtWidgets import (QApplication, QMainWindow, QProgressBar, QFileDialog, QMessageBox, 
						QMenu, QCompleter, QStyle, QFrame, QPushButton, QLabel)
from PyQt5.QtMultimedia import QMediaPlayer
# Gui QtDesigner : compiler .ui sans Eric6: pyuic5 file.ui -o Ui_main_file.py
from Ui_DBALBUMS import Ui_MainWindow
# DB DEV
from DBFunction import (buildCommandPowershell, runCommand, openFolder, centerWidget,
						displayCounters, displayStars, ThemeColors, qtmymessagehandler, 
						buildalbumnamehtml)
from DBDatabase import (connectDatabase, getrequest, copyDatabaseInvent, execSqlFile, 
						buildTabFromRequest, buildFileCover, extractCoverb64)
from DBSLoading import DBloadingGui
from DBTProcess import DBProcessGui
from DBAlbsMini import DBAlbumsQT5Mini
from DBModelAbs import ModelTableAlbumsABS, ModelTableTracksABS
from DBArtworks import ArtworksGui, CoverViewGui
from DBFoobarpl import DBFoobar
from DBAuPlayer import DBPlayer
from DBThunbnai import DBThunbnails
from DBDragDrop import QLabeldnd
from DBPThreads import DBPThreadsListStyle
from DBTImports import InventGui


class DBAlbumsMainGui(QMainWindow, Ui_MainWindow):
	"""DBAlbums main constants."""
	qDebug('Start')
	PATH_PROG = path.dirname(path.abspath(__file__))
	PATH_PROG = path.dirname(path.abspath(__file__))
	LOGS_PROG = path.join(PATH_PROG, 'LOG')
	BASE_SQLI = path.join(PATH_PROG, 'LOC', "DBALBUMS_{envt}.db")
	PWSH_SCRU = path.join(PATH_PROG, 'PS1', "UPDATE_ALBUMS.ps1")
	FOOB_UPSC = path.join(PATH_PROG, 'SQL', "DBAlbums_FOOBAR_UPADTESCORE.sql")
	RESS_LABS = path.join(PATH_PROG, 'IMG' , 'LAB')
	RESS_ICOS = path.join(PATH_PROG, 'IMG' , 'ICO')
	RESS_LOGO = path.join(PATH_PROG, 'IMG')
	# Read File DBAlbums.ini
	qDebug('read ini file')
	FILE__INI = 'DBAlbums.ini'
	configini = QSettings(FILE__INI, QSettings.IniFormat)
	configini.beginGroup('dbalbums')
	VERS_PROG = configini.value('prog_build')
	TITL_PROG = "♫ DBAlbums v{v} (2017)".format(v=VERS_PROG)
	WIDT_MAIN = int(configini.value('wgui_width'))
	HEIG_MAIN = int(configini.value('wgui_heigh'))
	WIDT_PICM = int(configini.value('thun_csize'))
	HEIG_LHUN = int(configini.value('thnail_nbl'))
	DISP_CJOKER = configini.value('text_joker')
	WINS_ICO = path.join(PATH_PROG, 'IMG', configini.value('wins_icone'))
	UNIX_ICO = path.join(PATH_PROG, 'IMG', configini.value('unix_icone'))
	PICM_NCO = path.join(PATH_PROG, 'IMG', configini.value('pict_blank'))
	THEM_COL = configini.value('name_theme')
	TEXT_NCO = configini.value('text_nocov')
	ENVT_DEF = configini.value('envt_deflt')
	THUN_DIS = int(configini.value('thnail_dis'))
	THUN_NOD = int(configini.value('thnail_nod'))
	COVE_SIZ = int(configini.value('covers_siz'))
	FONT_MAI = configini.value('font00_ttx')
	configini.endGroup()
	# PROGS LINKS
	configini.beginGroup('programs')
	TAGS_SCAN = configini.value('tagscan')
	FOOB_PLAY = configini.value('foobarP')
	if platform == "darwin" or platform == 'linux':
		EDIT_TEXT = r'' + configini.value('txt_lin')
	else:
		EDIT_TEXT = r'' + configini.value('txt_win')
	configini.endGroup()
	# LIST SCORE
	configini.beginGroup('score')
	SCOR_ALBUMS = {}
	for envt in configini.allKeys():
		SCOR_ALBUMS.update({int(envt): configini.value(envt)})
	SCOR_TRACKS = SCOR_ALBUMS
	configini.endGroup()
	# LIST ENVT
	configini.beginGroup('environments')
	NAME_EVT = []
	for envt in configini.allKeys():
		envtname = configini.value(envt)
		if envtname == ENVT_DEF:
			CURT_EVT = len(NAME_EVT)
		NAME_EVT.append(envtname)
	configini.endGroup()
	C_HEIGHT = 21
	COEF_ZOOM = 100
	
	def __init__(self, parent=None):
		"""Init gui."""
		qDebug('init main gui')
		super(DBAlbumsMainGui, self).__init__(parent)
		self.setupUi(self)
		
		self.parent = parent
		self.envits = None		# environment
		self.dbbase = None		# database connect
		self.modsql = None		# type database
		self.currow = None  	# row tab current album proxy
		self.posrow = None  	# row tab current album
		self.curAlb = None		# current ID album
		self.albumname = None	# current album name
		self.curMd5 = None  	# current MD5 album
		self.pathcover = None	# cover current album
		self.curTrk = None		# ID current track
		self.homMed = None		# playlist player
		self.rootDk = None		# root column music
		self.lstcat = None		# list category for browse folder
		self.infoBox = None		# message box
		self.maintitle = None	# title main tempo
		self.coveral = None		# current cover album
		self.liststy = None     # list ID_CD | TAG_Genres
		# zoom
		self.cuzoom = self.COEF_ZOOM
		self.sizeTN = self.WIDT_PICM
		self.h_main = self.HEIG_MAIN
		self.w_main = self.WIDT_MAIN
		# loading
		self.loadingGui = None

		# font
		font = QFont()
		font.setFamily(self.FONT_MAI)
		font.setFixedPitch(True)
		font.setPointSize(12)
		self.lab_search.setFont(font)
		self.lab_scorealb.setFont(font)
		self.lab_scoretrk.setFont(font)
		self.lab_album.setFont(font)
		self.lab_label.setFont(font)
		self.statusbar.setFont(font)

		# center, size
		centerWidget(self)
		thunnbline = self.HEIG_LHUN
		self.resize(self.w_main, self.h_main)
		
		# menu bar
		self.setWindowTitle(self.TITL_PROG)
		self.setWindowIcon(QIcon(self.WINS_ICO))
		
		# combos Envt
		self.com_envt.addItems(self.NAME_EVT)
		self.com_envt.setCurrentIndex(self.CURT_EVT)
		
		# combos Tip
		self.com_envt.setToolTip('Environment')
		self.com_category.setToolTip('Category')
		self.com_family.setToolTip('Source')
		self.com_label.setToolTip('Label')
		self.com_year.setToolTip('Year')
		self.com_genres.setToolTip('Style')
		
		# buttons
		self.btn_clearsearch.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
		
		# thunbnails list
		self.thunbnails = DBThunbnails(self, self.sizeTN, thunnbline)
		self.layout2thunbnails.addWidget(self.thunbnails)
		
		# minimize ? height main windows
		sizescreen = QApplication.primaryScreen()
		if sizescreen.size().height() < (self.h_main):
			# one line for thunbnails
			thunnbline = 1
			self.resize(self.w_main, self.h_main-self.sizeTN)
			self.setMinimumSize(self.w_main, self.h_main-self.sizeTN)

		# scroring
		self.sli_scorealb.setMaximumSize(16777215, 18)
		self.sli_scorealb.setMinimum(0)
		self.sli_scorealb.setMaximum(len(self.SCOR_ALBUMS)-1)
		self.btn_scorealb.setVisible(False)
		self.sli_scorealb.setValue(0)
		self.sli_scoretrk.setMaximumSize(16777215, 18)
		self.sli_scoretrk.setMinimum(0)
		self.sli_scoretrk.setMaximum(len(self.SCOR_TRACKS)-1)
		self.btn_scoretrk.setVisible(False)
		self.sli_scoretrk.setValue(0)

		# title album
		self.lab_album.setOpenLinks(False)
		
		# Qlabel dnd
		self.labelcover = QLabeldnd(self.framecover, None, self.COVE_SIZ)
		self.framecover.setMaximumSize(self.COVE_SIZ, self.COVE_SIZ)
		self.framecover.setMinimumSize(self.COVE_SIZ, self.COVE_SIZ)
		
		# tab list no header row
		self.tbl_albums.verticalHeader().setVisible(False)
		self.tbl_tracks.verticalHeader().setVisible(False)
		
		# player
		self.playerAudio = DBPlayer()
		self.horizontalplayer.addWidget(self.playerAudio)
		self.horizontalplayer.setSpacing(0)
		
		# progres bar
		self.gaugeBar = QProgressBar(self)
		self.gaugeBar.setVisible(False)
		self.gaugeBar.setMinimum(0)
		self.gaugeBar.setMaximum(100)
		self.statusbar.addPermanentWidget(self.gaugeBar)
		
		# zoom in/out button statu bar
		self.sbframe = QFrame(self.centralwidget)
		self.sbframe.setMinimumSize(QSize(80, 0))
		self.sbframe.setFrameShape(QFrame.StyledPanel)
		self.sbframe.setFrameShadow(QFrame.Raised)
		self.btn_zoomout = QPushButton(self.sbframe)
		self.btn_zoomout.setStyleSheet("border: none;")
		self.btn_zoomout.setGeometry(QRect(2, 3, 16, 16))
		self.btn_zoomout.setIcon(QIcon(path.join(self.RESS_ICOS, 'zoomout.png')))
		self.lab_zoom = QLabel(self.sbframe)
		self.lab_zoom.setMaximumSize(QSize(35, 20))
		self.lab_zoom.setStyleSheet("color: lime;background-color: black;border-radius: 5px;")
		self.lab_zoom.setGeometry(QRect(22, 1, 35, 23))
		self.lab_zoom.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
		self.lab_zoom.setText(str(self.cuzoom) +'%')
		self.btn_zoomin = QPushButton(self.sbframe)
		self.btn_zoomin.setStyleSheet("border: none;")
		self.btn_zoomin.setGeometry(QRect(60, 3, 16, 16))
		self.btn_zoomin.setIcon(QIcon(path.join(self.RESS_ICOS, 'zoomin.png')))
		self.statusbar.addPermanentWidget(self.sbframe)
		self.btn_nogrid = QPushButton(self)
		self.btn_nogrid.setStyleSheet("border: none;")
		self.btn_nogrid.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
		self.statusbar.addPermanentWidget(self.btn_nogrid)
		self.btn_themecolor = QPushButton(self)
		self.btn_themecolor.setStyleSheet("border: none;")
		self.btn_themecolor.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))
		self.statusbar.addPermanentWidget(self.btn_themecolor)
		
		# popup base
		self.menub = QMenu()
		self.menub.addAction(self.style().standardIcon(QStyle.SP_MessageBoxInformation),
							"Show Informations  [F1]", self.showLoadingGui)
		self.menub.addAction(self.style().standardIcon(QStyle.SP_BrowserReload),
							"Reload base Albums [F5]", lambda: self.connectEnvt(True))
		self.action_UBP = self.menub.addAction(QIcon(path.join(self.RESS_ICOS, 'pwr.png')),
							"Update Base (powershell)...", lambda: self.buildInventPython('UPDATE'))
		self.action_UBN = self.menub.addAction(QIcon(path.join(self.RESS_ICOS, 'pwr.png')),
							"Add news albums to Base (powershell)...", lambda: self.buildInventPython('NEW'))
		self.action_CSD = self.menub.addAction(QIcon(path.join(self.RESS_ICOS, 'sql.png')),
							"Create sqlite database...", self.createLocalBase)
		self.action_IFP = self.menub.addAction(QIcon(path.join(self.RESS_ICOS, 'foo.png')),
							"Import Foobar Playlists, Update Score...", self.importFoobar)
		self.menub.addAction(self.style().standardIcon(QStyle.SP_FileDialogDetailedView),
							"Edit {fin}...".format(fin=self.FILE__INI), lambda e=self.EDIT_TEXT, f=self.FILE__INI: runCommand(e, f))
		self.menub.addAction(self.style().standardIcon(QStyle.SP_DialogOpenButton),
							"Open Logs Folder...", lambda flog=self.LOGS_PROG: openFolder(flog))
		# popup albums
		self.menua = QMenu()
		self.action_VIA = self.menua.addAction(QIcon(path.join(self.RESS_ICOS, 'art.png')),
							"View ArtWorks...", self.viewArtworks)
		self.action_OPF = self.menua.addAction(self.style().standardIcon(QStyle.SP_DialogOpenButton),
							"Open Folder...", self.getFolder)
		self.action_EXA = self.menua.addAction(QIcon(path.join(self.RESS_ICOS, 'exp.png')),
							"Export Album...", self.exportAlbums)
		self.action_UAP = self.menua.addAction(QIcon(path.join(self.RESS_ICOS, 'pwr.png')),
							"Update Album...", self.updateAlbums)
		self.action_TAG = self.menua.addAction(QIcon(path.join(self.RESS_ICOS, 'tag.png')),
							"Edit Tags (TagScan)...", self.openTagScan)

		# theme color
		self.curthe = ThemeColors(self.THEM_COL)
		self.applyTheme()
		
		# timer Delay action QLineEdit
		self.m_typingTimer = QTimer(self)
		self.m_typingTimer.setSingleShot(True)
		self.m_typingTimer.timeout.connect(self.onFiltersChanged)
		
		# link Gui
		self.lin_search.textChanged.connect(self.onTextEdited)
		self.btn_clearsearch.clicked.connect(self.clearFilters)
		self.chb_searchtracks.clicked.connect(self.onFiltersChanged)
		self.btn_zoomout.clicked.connect(self.zoomOutThnunnails)
		self.btn_zoomin.clicked.connect(self.zoomInThnunnails)
		self.btn_nogrid.clicked.connect(self.noDisplayTab)
		self.btn_themecolor.clicked.connect(lambda: [self.curthe.nextTheme(), self.applyTheme()])
		self.com_category.currentIndexChanged.connect(self.onFiltersChanged)
		self.com_family.currentIndexChanged.connect(self.onFiltersChanged)
		self.com_label.currentIndexChanged.connect(self.onFiltersChanged)
		self.com_year.currentIndexChanged.connect(self.onFiltersChanged)
		self.com_genres.currentIndexChanged.connect(self.onFiltersChanged)
		self.com_envt.currentIndexChanged.connect(self.connectEnvt)
		self.com_envt.setContextMenuPolicy(Qt.CustomContextMenu)
		self.com_envt.customContextMenuRequested.connect(self.popUpBaseAlbums)
		self.thunbnails.signalthunchgt.connect(self.onSelectThunbnail)
		self.thunbnails.signalthunadds.connect(self.onAddThunbnail)
		self.thunbnails.signalthubuild.connect(self.onBuild)
		self.thunbnails.setContextMenuPolicy(Qt.CustomContextMenu)
		self.thunbnails.customContextMenuRequested.connect(self.popUpTNAlbums)
		self.tbl_albums.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tbl_albums.customContextMenuRequested.connect(self.popUpTreeAlbums)
		self.tbl_albums.clicked.connect(self.onSelectListAlbum)
		self.tbl_albums.currentChanged = self.onSelectListAlbum
		self.tbl_tracks.clicked.connect(self.onSelectTrackChanged)
		self.tbl_tracks.doubleClicked.connect(self.playMediasAlbum)
		self.tbl_tracks.currentChanged = self.onSelectTrackChanged
		self.lab_album.anchorClicked.connect(self.onAnchorClicked)
		self.labelcover.mousePressEvent = self.onPressCover
		self.labelcover.signalcoverchgt.connect(self.updateAlbumsDnd)
		self.sli_scorealb.valueChanged.connect(self.onModifyScoreAlbum)
		self.sli_scoretrk.valueChanged.connect(self.onModifyScoreTrack)
		self.btn_scorealb.clicked.connect(self.onPressButtonEnrScoreAlbum)
		self.btn_scoretrk.clicked.connect(self.onPressButtonEnrScoreTrack)
		self.playerAudio.signaltxt.connect(self.updateStatusBar)
		self.playerAudio.signalnum.connect(self.selectPlayingTack)

		# DISABLED OPTIONS for OS linux: no powershell, foobar, tagscan
		if platform == "darwin" or platform == 'linux':
			self.action_UBP.setEnabled(False)	# Update base powershell
			self.action_UBN.setEnabled(False)	# Add news base powershell
			self.action_IFP.setEnabled(False)   # Import playlists foobar 2000
			self.action_UAP.setEnabled(False)	# Update album powershell)
			self.action_TAG.setEnabled(False)	# TagScan
		
		# init connect
		self.connectEnvt()

	def onTextEdited(self, text):
		"""Limit delay action on text search changed."""
		self.m_typingTimer.start(1000)

	@pyqtSlot()
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()
		elif event.key() == Qt.Key_F1:
			self.showLoadingGui()
		elif event.key() == Qt.Key_F5:
			self.connectEnvt(True)

	@pyqtSlot()
	def wheelEvent(self, event):
		# 120/4.8 = 25 = 1/4
		degre = event.angleDelta()/4.8
		modifiers = QApplication.keyboardModifiers()
		if modifiers == Qt.ControlModifier:
			self.cuzoom += degre.y()
			self.reDisplayThunbnails()
	
	def zoomInThnunnails(self):
		self.cuzoom += 25
		self.reDisplayThunbnails()
	
	def zoomOutThnunnails(self):
		self.cuzoom -= 25
		self.reDisplayThunbnails()
		
	def reDisplayThunbnails(self):
		"""Replace or Rebuild thunbnails."""
		oldsizeTN = self.sizeTN
		nbstep = 3
		self.sizeTN = self.WIDT_PICM * (self.cuzoom/100)
		# default zoom [...|...]
		zmin = self.COEF_ZOOM-(nbstep*25)
		zmax = self.COEF_ZOOM+(nbstep*25)
		if self.cuzoom < zmin or self.cuzoom > zmax:
			self.cuzoom = self.COEF_ZOOM
			self.sizeTN = self.WIDT_PICM
		self.lab_zoom.setText(str(self.cuzoom) +'%')
		# redisplay zoom thunbnails
		if self.sizeTN < oldsizeTN:
			# resize
			qDebug('ZOOM- replace :' + str(self.cuzoom))
			self.thunbnails.stopbuild = True
			self.thunbnails.replaceThunbnails(self.sizeTN)
		elif self.sizeTN > oldsizeTN:
			# rebuild
			qDebug('ZOOM+ rebuild :' + str(self.cuzoom))
			thunlst = self.tableMdlAlb.builListThunbnails()
			#while self.thunbnails.isbuilder:
			self.thunbnails.stopbuild = True
			self.thunbnails.addthunbails(thunlst, self.sizeTN, True, 0, self.thunbnails.getTotalThunbnails(), self.tableMdlAlb.SortFilterProxy.rowCount())

	def noDisplayTab(self):
		"""no disply grid list albums."""
		if self.tbl_albums.isVisible():
			self.tbl_albums.hide()
		else:
			self.tbl_albums.show()

	def applyTheme(self):
		"""Apply color Theme to main Gui."""
		# main
		mainstyle = 'QMainWindow{{background-color: {col1};border: 1px solid black;}}' \
					'QLineEdit{{background-color: {col2};}}' \
					'QComboBox{{background-color: {col2};}}' \
					'QStatusBar{{background-color: {col1};border: 1px solid black;}}' \
					'QMessageBox{{background-color: {col1};border: 1px solid black;}}' \
					'QScrollBar:vertical{{width: 14px;}}' \
					'QScrollBar:horizontal{{height: 14px;}}' \
					'QTableView{{alternate-background-color: {col3};background-color: {col4};}}' \
					'QScrollArea{{background-color: {col2};}}' \
					'QToolTip{{border-radius:3px;background-color: {col2};}}' \
					'QTableView::item:selected{{ background-color:{col5}; color:white;}}'
		mainstyle = mainstyle.format(col1 = self.curthe.listcolors[0], 
									col2 = self.curthe.listcolors[1], 
									col3 = self.curthe.listcolors[2], 
									col4 = self.curthe.listcolors[3],
									col5 = self.curthe.listcolors[4])
		self.setStyleSheet(mainstyle)
		# treeview
		gridstyle = 'QHeaderView::section{{background-color: {col2};border-radius:1px;margin: 1px;padding: 2px;}}'
		gridstyle = gridstyle.format(col2 = self.curthe.listcolors[1])
		self.tbl_albums.setStyleSheet(gridstyle)
		self.tbl_tracks.setStyleSheet(gridstyle)
		# labels title album
		labestyle = 'background-color: {col2};border: 5px solid {col2};border-radius: 10px;'
		labestyle = labestyle.format(col2 = self.curthe.listcolors[1])
		self.lab_label.setStyleSheet(labestyle)
		self.lab_album.setStyleSheet(labestyle)
		# thunnail widget
		self.thunbnails.scrollAreaWidgetthunbnails.setStyleSheet('background-color: {col2};'.format(col2 = self.curthe.listcolors[1]))
	
	def showLoadingGui(self, event=None):
		"""display splashscreen infos."""
		# loading Gui
		if self.loadingGui.isVisible():
			self.loadingGui.hide()
		else:
			self.loadingGui.applyTheme()
			self.loadingGui.show()

	def clearFilters(self):
		"""Clear search, combos."""
		# reset text search + in track
		self.lin_search.setText('')
		self.chb_searchtracks.setCheckState(Qt.Unchecked)
		# reset combos
		self.com_category.setCurrentIndex(0)
		self.com_family.setCurrentIndex(0)
		self.com_label.setCurrentIndex(0)
		self.com_year.setCurrentIndex(0)
		self.com_genres.setCurrentIndex(0)
		self.onFiltersChanged()

	def onFiltersChanged(self):
		"""Send filter to model for update."""
		self.lin_search.setEnabled(False)
		self.btn_clearsearch.setEnabled(False)
		self.chb_searchtracks.setEnabled(False)
		filttext = self.lin_search.text()
		filtcate = self.com_category.currentText()
		filtfami = self.com_family.currentText()
		filtyear = self.com_year.currentText()
		filtlabl = self.com_label.currentText()
		filtgenr = self.com_genres.currentText()
		filtintk = (self.chb_searchtracks.isChecked())
		qDebug('update Filters')
		self.tableMdlAlb.SortFilterProxy.updateFilters(filttext, filtcate, filtfami, filtyear, filtlabl, filtgenr, filtintk)
		self.lin_search.setEnabled(True)
		self.btn_clearsearch.setEnabled(True)
		self.chb_searchtracks.setEnabled(True)

	def displayResultSearch(self):
		"""Build main message status bar."""
		txt_sch = (self.lin_search.text() if len(self.lin_search.text()) > 0 else 'all')
		if self.tableMdlAlb.rowCount()==0:
			message = "Search Result \"{sch}\" : nothing".format(sch=txt_sch)
		else:
			if int(((self.tableMdlAlb.SortFilterProxy.cpt_len/60/60)/24)*10)/10 < 1:
				# seoncd -> Hours
				txt_len = str(int(((self.tableMdlAlb.SortFilterProxy.cpt_len/60/60))*10)/10) + ' Hours'
			else:
				# seoncd -> Days
				txt_len = str(int(((self.tableMdlAlb.SortFilterProxy.cpt_len/60/60)/24)*10)/10) + ' Days'
			if int(self.tableMdlAlb.SortFilterProxy.cpt_siz/1024) == 0:
				txt_siz =  str(self.tableMdlAlb.SortFilterProxy.cpt_siz) + ' Mo'
			else:
				txt_siz = str(int(self.tableMdlAlb.SortFilterProxy.cpt_siz/1024)) + ' Go'
			
			message = "Search Result \"{sch}\" :  {alb} | {trk} | {cds} | {siz} | {dur}"
			message = message.format(alb=displayCounters(self.tableMdlAlb.SortFilterProxy.rowCount(), 'Album'),
									cds=displayCounters(self.tableMdlAlb.SortFilterProxy.cpt_cds, 'CD'),
									trk=displayCounters(self.tableMdlAlb.SortFilterProxy.cpt_trk, 'Track'),
									siz=txt_siz,
									dur=txt_len,
									sch=txt_sch)
		
		self.maintitle = message
		self.updateStatusBar(self.maintitle)

	def updateStatusBar(self, message, t=0):
		"""Update Status Bar Message"""
		self.statusBar().showMessage(message, t)

	def updateGaugeBar(self, purcent, message=None, t=0):
		"""Update Gauge Bar and Status Bar Message"""
		self.gaugeBar.setVisible(True)
		if message is not None:
			self.updateStatusBar(message, t)
		self.gaugeBar.setValue(purcent)
		QApplication.processEvents()
		if purcent == 100:
			self.gaugeBar.setVisible(False)
			self.updateStatusBar(self.maintitle)

	def connectEnvt(self, refresh=False):
		"""Connect Envt."""
		if self.envits != self.com_envt.currentText() or refresh:
			if self.playerAudio.player.state() == QMediaPlayer.PlayingState:
				self.playerAudio.player.stop()
			self.envits = self.com_envt.currentText()
			self.setCursor(Qt.WaitCursor)
			# init search + grids
			self.lin_search.textChanged.disconnect()
			self.lin_search.setText('')
			self.lin_search.textChanged.connect(self.onTextEdited)
			# init combos
			self.com_category.currentIndexChanged.disconnect()
			self.com_family.currentIndexChanged.disconnect()
			self.com_label.currentIndexChanged.disconnect()
			self.com_year.currentIndexChanged.disconnect()
			self.com_genres.currentIndexChanged.disconnect()
			self.com_category.clear()
			self.com_family.clear()
			self.com_label.clear()
			self.com_year.clear()
			self.com_genres.clear()
			self.com_genres.addItems(['Loading...'])
			self.com_genres.setEnabled(False)
			self.liststy = None
			self.com_category.currentIndexChanged.connect(self.onFiltersChanged)
			self.com_family.currentIndexChanged.connect(self.onFiltersChanged)
			self.com_label.currentIndexChanged.connect(self.onFiltersChanged)
			self.com_year.currentIndexChanged.connect(self.onFiltersChanged)
			self.com_genres.currentIndexChanged.connect(self.onFiltersChanged)
			# init scrore
			self.sli_scorealb.setValue(0)
			self.sli_scoretrk.setValue(0)
			# connect
			boolconnect, self.dbbase, self.modsql, self.rootDk, self.lstcat = connectDatabase(self.envits)
			if not boolconnect:
				# no connect
				self.updateStatusBar("Connect Failed, please select other environment...")
			else:
				# mode sqllite, no menu create base
				if self.modsql == 'sqlite':
					self.action_CSD.setEnabled(False)
				else:
					self.action_CSD.setEnabled(True)
				# test path database folder for option update
				if path.exists(self.rootDk):
					self.action_UBP.setEnabled(True)
					self.action_UBN.setEnabled(True)
				else:
					self.action_UBP.setEnabled(False)
					self.action_UBN.setEnabled(False)
				# loading splashscreen
				self.loadingGui = DBloadingGui(self.modsql, self.TITL_PROG, self)
				self.loadingGui.show()
				QApplication.processEvents()
				# last date modifcation base
				curdate = QTime.currentTime().toString('hh:mm:ss')
				self.setWindowTitle('{prog} : Connected base {base} [{mode}] at {hour}'.format(prog=self.TITL_PROG,
																								mode=self.modsql,
																								base=self.envits,
																								hour=curdate))
				# fill model/tree albums list
				qDebug('Fill list albums start')
				req = getrequest('albumslist', self.modsql)
				self.tableMdlAlb = ModelTableAlbumsABS(self, req)
				self.tableMdlAlb.SortFilterProxy.sort(-1)
				self.tableMdlAlb.signalthubuild.connect(self.onBuild)
				self.tbl_albums.setModel(self.tableMdlAlb.SortFilterProxy)
				self.tableMdlAlb.SortFilterProxy.layoutChanged.connect(self.onListAlbumsChanged)
				qDebug('Fill list albums end')
				
				# size grid
				for i in range(len(self.tableMdlAlb.A_C_WIDTH)):
					self.tbl_albums.setColumnWidth(i, self.tableMdlAlb.A_C_WIDTH[i])
				# height rows
				self.tbl_albums.verticalHeader().setDefaultSectionSize(self.tableMdlAlb.C_HEIGHT)

				# fill thunbnails + combos
				self.onListAlbumsChanged()				
				# data ?
				if self.tableMdlAlb.rowCount() > 0:
					if refresh:
						index = self.tableMdlAlb.index(self.posrow, 0)
						index = self.tableMdlAlb.SortFilterProxy.mapToSource(index)
					else:
						self.posrow = 0
						index = self.tableMdlAlb.index(self.posrow, 0)
					self.tbl_albums.selectRow(index.row())
					index = self.tbl_albums.currentIndex()
					self.tbl_albums.scrollTo(index)
					self.displayAlbum()
					# autocompletion list
					autoList = buildTabFromRequest(getrequest('autocompletion', self.modsql))
					self.com_autcom = QCompleter(autoList, self.lin_search)
					self.com_autcom.setCaseSensitivity(Qt.CaseInsensitive)
					self.lin_search.setCompleter(self.com_autcom)
					# build list style
					qDebug('qthread build list style')
					self.obj = DBPThreadsListStyle(self)
					self.obj.finished.connect(self.fillListGenres)
					self.obj.start()

				# end loading
				self.loadingGui.hide()
				# display title
				self.setCursor(Qt.ArrowCursor)
				self.displayResultSearch()
	
	def displayAlbum(self):
		"""Display info current select album."""
		indexsrc = self.tbl_albums.currentIndex()
		indexes = self.tableMdlAlb.SortFilterProxy.mapToSource(indexsrc)
		if indexes.isValid():
			# select thunbnail
			self.thunbnails.selectThunbnail(indexsrc.row())
			if self.tableMdlAlb.getData(indexes.row(), 'Name') != self.albumname:
				self.setCursor(Qt.WaitCursor)
				self.posrow = indexsrc.row()
				self.currow = indexes.row()
				self.curAlb = self.tableMdlAlb.getData(self.currow, 'ID_CD')
				self.curMd5 = self.tableMdlAlb.getData(self.currow, 'MD5')
				self.albumname = self.tableMdlAlb.getData(self.currow, 'Name')
				self.ScoreAlbum = self.tableMdlAlb.getData(self.currow, 'Score')
				self.pathcover = self.tableMdlAlb.getData(self.currow, 'Cover')
				self.AlbumPath = self.tableMdlAlb.getData(self.currow, 'Path')
				
				# fill tracks
				if self.chb_searchtracks.isChecked() and self.lin_search.text() != '':
					searchtxt = self.lin_search.text()
				else:
					searchtxt = ''
				req = (getrequest('trackslist', self.modsql)).format(id=self.curAlb)
				self.tableMdlTrk = ModelTableTracksABS(self, searchtxt, req)
				self.tbl_tracks.setModel(self.tableMdlTrk.SortFilterProxy)
				self.tableMdlTrk.SortFilterProxy.layoutChanged.connect(self.onListTracksChanged)
				
				# size grid
				for i in range(len(self.tableMdlTrk.T_C_WIDTH)):
					self.tbl_tracks.setColumnWidth(i, self.tableMdlTrk.T_C_WIDTH[i])
				self.tbl_tracks.verticalHeader().setDefaultSectionSize(self.tableMdlTrk.C_HEIGHT)
				#self.tbl_tracks.resizeColumnsToContents()
				#self.tbl_tracks.resizeRowsToContents()
				#self.tbl_tracks.horizontalHeader().setStretchLastSection(True)
				
				# build stats album
				cpt_len = self.tableMdlTrk.getSum('TAG_length')
				txt_album, img_lab = buildalbumnamehtml(self.albumname,
											str(self.tableMdlAlb.getData(self.currow, 'Label')),
											str(self.tableMdlAlb.getData(self.currow, 'ISRC')),
											str(self.tableMdlAlb.getData(self.currow, 'Year')),
											int(self.tableMdlAlb.getData(self.currow, 'Qty_CD')),
											self.tableMdlTrk.rowCount(),
											int(((cpt_len/60)*10)/10),
											int(self.tableMdlAlb.getData(self.currow, 'Qty_covers')),
											self.AlbumPath,
											self.RESS_LABS, self.RESS_ICOS)
				# img label
				if img_lab is not None:
					plabel = QPixmap(img_lab)
					self.lab_label.setPixmap(plabel)
					self.lab_label.setVisible(True)
				else:
					self.lab_label.setText('<b>' + self.tableMdlAlb.getData(self.currow, 'Category') + '</b>')
				index = self.com_category.findText(self.tableMdlAlb.getData(self.currow, 'Category'), Qt.MatchFixedString)
				self.lab_label.mousePressEvent = lambda e, ind=index: self.com_category.setCurrentIndex(ind)
				self.lab_label.enterEvent = lambda e, cur=Qt.PointingHandCursor: self.setCursor(cur)
				self.lab_label.leaveEvent = lambda e, cur=Qt.ArrowCursor: self.setCursor(cur)
						
				# title album
				self.lab_album.setHtml(txt_album)

				# fill score album
				self.sli_scorealb.setValue(self.ScoreAlbum)
				self.lab_scorealb.setText(displayStars(self.ScoreAlbum, self.SCOR_ALBUMS))

				# fill cover
				if self.pathcover[0:len(self.TEXT_NCO)] == self.TEXT_NCO:
					self.coveral = QPixmap(self.PICM_NCO)
					self.labelcover.updateLabel(self.AlbumPath)
				else:
					self.labelcover.updateLabel(None)
					self.coveral = extractCoverb64(self.curMd5, self.PICM_NCO)
				self.coveral = self.coveral.scaled(self.COVE_SIZ, self.COVE_SIZ, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
				self.labelcover.setPixmap(self.coveral)

				# fill play medias only is not playing
				self.curtrk = self.tbl_tracks.currentIndex().row()
				if self.playerAudio.player.state() != QMediaPlayer.PlayingState and path.exists(self.AlbumPath):
					self.homMed = self.tableMdlTrk.getMedias()
					self.playerAudio.addMediaslist(self.homMed, self.curtrk, self.albumname)
				# init status bar
				self.updateStatusBar(self.maintitle)
				
				# select track default
				if self.tableMdlTrk.rowCount() > 0:
					self.tbl_tracks.selectRow(0)
					self.curTrk = 0
				self.displaytrack()
				self.setCursor(Qt.ArrowCursor)
			
	def displaytrack(self):
		"""Display info current select track."""
		if self.tableMdlTrk.rowCount() > 0:
			self.ScoreTrack = self.tableMdlTrk.getData(self.curtrk, 'Score')
			self.sli_scoretrk.setEnabled(True)
			self.lab_scoretrk.setEnabled(True)
		else:
			self.curtrk = None
			self.ScoreTrack = 0
			self.sli_scoretrk.setEnabled(False)
			self.lab_scoretrk.setEnabled(False)
		self.sli_scoretrk.setValue(self.ScoreTrack)
		self.lab_scoretrk.setText(displayStars(self.ScoreTrack, self.SCOR_TRACKS))

	def onModifyScoreAlbum(self,  event):
		"""Modify Score Album."""
		listrows = self.getRowsfromListAlbums()
		if listrows is not None:
			self.lab_scorealb.setText(displayStars(self.sli_scorealb.value(), self.SCOR_ALBUMS))
			# display button update
			if self.ScoreAlbum != self.sli_scorealb.value():
				self.btn_scorealb.setVisible(True)
				nbselect = len(listrows)
				self.btn_scorealb.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
				self.btn_scorealb.setText('x' + str(nbselect))
			else:
				self.btn_scorealb.setVisible(False)

	def onModifyScoreTrack(self,  event):
		"""Modify Score Track."""
		listrows = self.getRowsfromListTracks()
		if listrows is not None:
			self.lab_scoretrk.setText(displayStars(self.sli_scoretrk.value(), self.SCOR_TRACKS))
			if self.ScoreTrack != self.sli_scoretrk.value():
				self.btn_scoretrk.setVisible(True)
				nbselect = len(listrows)
				self.btn_scoretrk.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
				self.btn_scoretrk.setText('x' + str(nbselect))
			else:
				self.btn_scoretrk.setVisible(False)
	
	def onSelectThunbnail(self, row):
		"""Reception signal : Select thunbnail."""
		index = self.tableMdlAlb.index(row, 0)
		self.tbl_albums.selectRow(index.row())
		index = self.tbl_albums.currentIndex()
		self.tbl_albums.scrollTo(index)
		self.tbl_albums.setFocus()
		self.displayAlbum()
		
	def onAddThunbnail(self, deb):
		"""Reception signal : Adds thunbnails."""
		thunlst = self.tableMdlAlb.builListThunbnails(False, deb, deb*2)
		self.thunbnails.addthunbails(thunlst, self.sizeTN, False, deb, deb*2, self.tableMdlAlb.SortFilterProxy.rowCount())

	def onBuild(self, ratio, text):
		"""Reception signal : Build Operation."""
		self.updateGaugeBar(ratio, text)

	def onListAlbumsChanged(self):
		"""Reception signal : changed list albums."""
		qDebug('list album changed')
		# clear combos
		self.com_category.currentIndexChanged.disconnect()
		self.com_family.currentIndexChanged.disconnect()
		self.com_label.currentIndexChanged.disconnect()
		self.com_year.currentIndexChanged.disconnect()
		self.com_genres.currentIndexChanged.disconnect()
		self.com_category.clear()
		self.com_family.clear()
		self.com_label.clear()
		self.com_year.clear()
		# fill combos
		if self.liststy is not None:
			self.com_genres.clear()	
			listgenres = []
			for idgenre in self.liststy:
				if idgenre[0] in self.tableMdlAlb.SortFilterProxy.listiddi:
					if idgenre[1] not in listgenres:
						listgenres.append(idgenre[1])
			listgenres.sort(reverse=False)		
			listgenres = [self.DISP_CJOKER] + listgenres
			self.com_genres.addItems(listgenres)
		listcat = self.tableMdlAlb.SortFilterProxy.listcat
		listcat.sort(reverse=True)
		listcat = [self.DISP_CJOKER] + listcat
		self.com_category.addItems(listcat)
		listfam = self.tableMdlAlb.SortFilterProxy.listfam
		listfam = [self.DISP_CJOKER] + listfam
		self.com_family.addItems(listfam)
		listlab = self.tableMdlAlb.SortFilterProxy.listlab
		listlab.sort(reverse=False)
		listlab = [self.DISP_CJOKER] + listlab
		self.com_label.addItems(listlab)
		listyea = self.tableMdlAlb.SortFilterProxy.listyea
		listyea.sort(reverse=True)
		listyea = [self.DISP_CJOKER] + listyea
		self.com_year.addItems(listyea)
		# set combo
		if self.tableMdlAlb.SortFilterProxy.filtcate is not None:
			index = self.com_category.findText(self.tableMdlAlb.SortFilterProxy.filtcate, Qt.MatchFixedString)
			self.com_category.setCurrentIndex(index)
		if self.tableMdlAlb.SortFilterProxy.filtfami is not None:
			index = self.com_family.findText(self.tableMdlAlb.SortFilterProxy.filtfami, Qt.MatchFixedString)
			self.com_family.setCurrentIndex(index)
		if self.tableMdlAlb.SortFilterProxy.filtyear is not None:
			index = self.com_year.findText(self.tableMdlAlb.SortFilterProxy.filtyear, Qt.MatchFixedString)
			self.com_year.setCurrentIndex(index)
		if self.tableMdlAlb.SortFilterProxy.filtlabl is not None:
			index = self.com_label.findText(self.tableMdlAlb.SortFilterProxy.filtlabl, Qt.MatchFixedString)
			self.com_label.setCurrentIndex(index)
		if self.tableMdlAlb.SortFilterProxy.filtgenr is not None:
			index = self.com_genres.findText(self.tableMdlAlb.SortFilterProxy.filtgenr, Qt.MatchFixedString)
			self.com_genres.setCurrentIndex(index)
		self.com_genres.currentIndexChanged.connect(self.onFiltersChanged)
		self.com_category.currentIndexChanged.connect(self.onFiltersChanged)
		self.com_family.currentIndexChanged.connect(self.onFiltersChanged)
		self.com_label.currentIndexChanged.connect(self.onFiltersChanged)
		self.com_year.currentIndexChanged.connect(self.onFiltersChanged)
		self.thunbnails.stopbuild = True
		thunlst = self.tableMdlAlb.builListThunbnails(True, 0, max(self.THUN_DIS, self.thunbnails.getTotalThunbnails()))
		self.thunbnails.addthunbails(thunlst, self.sizeTN, True, 0, max(self.THUN_DIS, self.thunbnails.getTotalThunbnails()), self.tableMdlAlb.SortFilterProxy.rowCount())
		# display title
		self.displayResultSearch()
		# select default row
		if self.tableMdlAlb.SortFilterProxy.rowCount()>0 and self.posrow is not None:
			index = self.tableMdlAlb.index(self.posrow, 0)
			index = self.tableMdlAlb.SortFilterProxy.mapFromSource(index)
			self.tbl_albums.selectRow(index.row())
			index = self.tbl_albums.currentIndex()
			self.tbl_albums.scrollTo(index)
		# focus
		if self.focusWidget() == self.tbl_albums:
			self.tbl_albums.setFocus()
		else:
			self.lin_search.setFocus()
		# display album
		self.displayAlbum()

	def onListTracksChanged(self):
		"""Reception signal : changed list tracks."""
		# fill play medias
		if self.tableMdlTrk.SortFilterProxy.rowCount() > 0:
			playing = False
			if self.playerAudio.player.state() == QMediaPlayer.PlayingState:
				playing = True
				self.playerAudio.player.stop()
			self.curtrk = self.tbl_tracks.currentIndex().row()
			if path.exists(self.AlbumPath):
				self.homMed = self.tableMdlTrk.getMedias()
				self.playerAudio.addMediaslist(self.homMed, self.curtrk, self.albumname)
			if playing:
				self.playerAudio.player.play()

	def fillListGenres(self,  listgenres):
		"""Reception end of Qthread for build list genres."""
		self.liststy = listgenres
		listgenres = []
		for idgenre in self.liststy:
			if idgenre[1] not in listgenres:
				listgenres.append(idgenre[1])
		listgenres.sort(reverse=False)		
		listgenres = [self.DISP_CJOKER] + listgenres
		self.com_genres.currentIndexChanged.disconnect()
		self.com_genres.clear()
		self.com_genres.setEnabled(True)
		self.com_genres.addItems(listgenres)
		self.com_genres.setCurrentIndex(0)
		self.com_genres.currentIndexChanged.connect(self.onFiltersChanged)
		
	def onSelectListAlbum(self, event, indexes=None):
		"""Select Album."""
		indexes = self.tbl_albums.selectedIndexes()
		if len(indexes) > 0:
			self.displayAlbum()

	def onSelectTrackChanged(self, event, indexes=None):
		"""Select Track."""
		indexes = self.tbl_tracks.selectedIndexes()
		if len(indexes) > 0:
			indexes = self.tableMdlTrk.SortFilterProxy.mapToSource(indexes[0])
			if self.curtrk != indexes.row():
				self.curtrk = indexes.row()
				self.displaytrack()
				if self.playerAudio.player.state() != QMediaPlayer.PlayingState:
					self.playerAudio.currentPlaylist.setCurrentIndex(self.curtrk)

	def selectPlayingTack(self, num):
		"""Reception signal num track, player audio."""
		self.tbl_tracks.selectRow(num)
		self.curtrk = self.tbl_tracks.currentIndex().row()
		index = self.tbl_tracks.currentIndex()
		self.tbl_tracks.scrollTo(index)

	def onAnchorClicked(self, url):
		"""Balises html title album clicked"""
		text = str(url.toString())
		if text.startswith('dbfunction://'):
			function = text.replace('dbfunction://','')
			param = function[1:]
			if function.startswith('a'):
				self.viewArtworks()
			elif function.startswith('y'):
				index = self.com_year.findText(param, Qt.MatchFixedString)
				if index >= 0:
					self.com_year.setCurrentIndex(index)
			elif function.startswith('l'):
				index = self.com_label.findText(param.replace('_',' '), Qt.MatchFixedString)
				if index >= 0:
					self.com_label.setCurrentIndex(index)
			elif function.startswith('s'):
				self.lin_search.setText(param.replace('_',' '))
				self.onFiltersChanged()
			elif function.startswith('f'):
				self.getFolder()
			elif function.startswith('t'):
				self.openTagScan()
			elif function.startswith('p'):
				self.updateAlbums()
			#if hasattr(self,function):
			#	getattr(self,function)()
	
	def onPressCover(self,  event):
		"""Display large cover MD5."""
		if self.pathcover is not None:
			if self.pathcover[0:len(self.TEXT_NCO)] != self.TEXT_NCO:
				CoverViewGui(self.coveral, self.albumname, self.h_main, self.h_main)

	def viewArtworks(self):
		"""views artworks covers storage."""
		ArtworksGui(self.AlbumPath, self.albumname, self.pathcover, self.w_main, self.h_main, self.sizeTN)

	def onPressButtonEnrScoreAlbum(self):
		"""Update Score Album."""
		listrows = self.getRowsfromListAlbums()
		if listrows is not None:
			self.ScoreAlbum = self.sli_scorealb.value()
			for rowalb in listrows:
				self.tableMdlAlb.updateScore(rowalb, self.ScoreAlbum)
		# Button
		self.btn_scorealb.setVisible(False)
		self.tableMdlAlb.SortFilterProxy.invalidate()

	def onPressButtonEnrScoreTrack(self):
		"""Update Score Track."""
		listrows = self.getRowsfromListTracks()
		if listrows is not None:
			self.ScoreTrack = self.sli_scoretrk.value()
			for rowtrk in listrows:
				self.tableMdlTrk.updateScore(rowtrk, self.ScoreTrack)
		# Button
		self.btn_scoretrk.setVisible(False)
		self.tableMdlTrk.SortFilterProxy.invalidate()

	def popUpBaseAlbums(self, position):
		"""Menu Database."""
		self.menub.exec_(self.com_envt.mapToGlobal(position))

	def popUpTreeAlbums(self, position):
		"""Menu Thunbnails."""
		listrows = self.getRowsfromListAlbums()
		if listrows is not None:
			if len(listrows) == 1:
				self.displayAlbum()
				self.action_TAG.setEnabled(True)
				self.updateTextPopupAlbum(self.tbl_albums.viewport().mapToGlobal(position))
			else:
				if len(listrows) > 1:
					self.action_VIA.setEnabled(False)
					self.action_OPF.setEnabled(False)
					self.action_EXA.setText("Export " + displayCounters(len(listrows), 'Album')+"cover/csv...")
					self.action_UAP.setText("Update " + displayCounters(len(listrows), 'Album') + "...")
					self.action_TAG.setEnabled(False)
					self.menua.exec_(self.tbl_albums.viewport().mapToGlobal(position))

	def popUpTNAlbums(self,  position):
		"""Mennu Albums."""
		self.updateTextPopupAlbum(self.thunbnails.mapToGlobal(position))

	def updateTextPopupAlbum(self, position):
		"""Update option menu album enabled."""
		if self.tableMdlAlb.getData(self.currow, 'Qty_covers') == 0 or not(path.exists(self.AlbumPath)):
			self.action_VIA.setEnabled(False)
		else:
			self.action_VIA.setEnabled(True)
		# path exist ?
		if not(path.exists(self.AlbumPath)):
			self.action_OPF.setEnabled(False)
		else:
			self.action_OPF.setEnabled(True)
		self.action_EXA.setText("Export cover/csv '" + self.albumname[:15] + "...'")
		self.action_UAP.setText("Update Album (powershell): " + self.albumname[:15] + "...")
		self.menua.exec_(position)
	
	def playMediasAlbum(self, event):
		"""play album tracks."""
		indexes = self.tbl_tracks.selectedIndexes()
		if len(indexes) > 0:
			# playing ? reset
			indexes = self.tableMdlTrk.SortFilterProxy.mapToSource(indexes[0])
			self.curtrk = indexes.row()
			self.homMed = self.tableMdlTrk.getMedias()
			self.playerAudio.addMediaslist(self.homMed, self.curtrk, self.albumname)
			self.playerAudio.player.play()
	
	def getRowsfromListAlbums(self):
		"""Get ID of line in list."""
		indexes = self.tbl_albums.selectedIndexes()
		if len(indexes) > 0:
			listrows = []
			for ind in indexes:
				index = self.tableMdlAlb.SortFilterProxy.mapToSource(ind)
				if index.row() not in listrows:
					listrows.append(index.row())
			return listrows
		else:
			return None

	def getRowsfromListTracks(self):
		"""Get ID of line in list."""
		indexes = self.tbl_tracks.selectedIndexes()
		if len(indexes) > 0:
			listrows = []
			for ind in indexes:
				index = self.tableMdlTrk.SortFilterProxy.mapToSource(ind)
				if index.row() not in listrows:
					listrows.append(index.row())
			return listrows
		else:
			return None
	
	def getFolder(self):
		"""Open album folder."""
		openFolder(self.AlbumPath)

	def openTagScan(self):
		"""Open program TAGs. edit."""
		runCommand(self.TAGS_SCAN, self.AlbumPath)
	
	def buildInventPython(self, typeupdate):
		"""Execute powershell Script update all albums infos."""
		self.prepareInvent = InventGui(self.tableMdlAlb.arraydata,
									self.lstcat,
									typeupdate,
									self.modsql, 
									self.envits, 
									self.curthe)
	
	def importFoobar(self):
		"""Foobar2000 playlists operations."""
		# import fpl playlist to mysql DBFOOBAR
		numtracks = DBFoobar(self, self.FOOB_PLAY)
		if numtracks == 0:
			QMessageBox.critical(self, 'Foobar2000 playlists operations', 'Problem import files fpl playlist from : ' + self.FOOB_PLAY)
		else:
			# synchro score sql
			execSqlFile(self, self.FOOB_UPSC, 9)
		self.updateStatusBar('Foobar2000 playlists finished', 5000)
		QMessageBox.information(self,'Foobar2000 import playlists', 'Operation successfull')

	def updateAlbumsDnd(self):
		"""Execute powershell Script update albums infos."""
		exeprocess, params = buildCommandPowershell(self.PWSH_SCRU, 
													'-Envt', self.envits,
													'-TypeOpe', 'UPDATE',
													'-AlbumInfos', str(self.curAlb))
		pro = DBProcessGui(exeprocess, params, 'Update display album', self.w_main, self.h_main-150)
		pro.signalend.connect(lambda: self.connectEnvt(True))

	def updateAlbums(self):
		"""Execute powershell Script update albums infos."""
		listrows = self.getRowsfromListAlbums()
		listSelect = []
		if listrows is not None:
			for ind in listrows:
				listSelect.append(str(self.tableMdlAlb.getData(ind, 'ID_CD')))
			exeprocess, params = buildCommandPowershell(self.PWSH_SCRU,
														'-Envt', self.envits,
														'-TypeOpe', '|'.join(['UPDATE'] * len(listSelect)), 
														'-AlbumInfos', '|'.join(listSelect))
			pro = DBProcessGui(exeprocess, params, 'Update ' + displayCounters(len(listSelect), "Album "), self.w_main, self.h_main-150)
			pro.signalend.connect(lambda: self.connectEnvt(True))

	def createLocalBase(self):
		"""Create base Sqlite."""
		filename = self.BASE_SQLI.format(envt=self.envits+'_SQLITE')
		# remove if exist
		if path.isfile(filename):
			remove(filename)
		logname = QDateTime.currentDateTime().toString('yyMMddhhmmss') + "_COPY_DATABASE_TO_SQLITE_" + self.envits + ".log"
		copyDatabaseInvent(self, self.dbbase,  filename, path.join(self.LOGS_PROG, logname))
		self.updateStatusBar("Create Database SQLite :"+filename+" Successfull", 7000)
		QMessageBox.information(self,'Create Database SQLite', 'Operation successfull')

	def exportAlbums(self):
		"""Export file cover or list albums select in grid."""
		listrows = self.getRowsfromListAlbums()
		if listrows is not None:
			filename = QFileDialog.getSaveFileName(self,
												"Export from CSV File list or cover jpeg Files",
												getcwd(),
												"Images (*.jpg);;CSV files (*.csv)")
			if filename is None:
				return
			filename = filename[0]
			extension = (path.splitext(filename))[1]
			if extension == '.csv':
				# extract file CSV
				with open(filename, "w") as csv_file:
					wr = writer(csv_file, delimiter=';', doublequote=True, quoting=QUOTE_ALL, lineterminator='\n')
					for ind in listrows:
						textrow = []
						for col in range(self.tableMdlAlb.columnCount()):
							textcol = self.tableMdlAlb.getData(ind, None, col)
							if isinstance(textcol, QDateTime):
								textcol = textcol.toString('dd/mm/yyyy hh:mm:ss')
							textrow.append(textcol)
						wr.writerow(textrow)
				openFolder(path.dirname(filename))
				self.statusBar().showMessage('Export csv list Albums /n Create file csv Sucessfull to :'+filename, 7000)
			elif extension == '.jpg':
				# extract base64\mysql to file JPEG
				for ind in listrows:
					filecover = path.join(path.dirname(filename), self.tableMdlAlb.getData(ind, 'Name'))
					extension = ((self.tableMdlAlb.getData(ind, 'Cover'))[-4:]).replace('.', '')
					filecover = filecover+'.'+extension
					buildFileCover(filecover, self.tableMdlAlb.getData(ind, 'MD5'))
				self.statusBar().showMessage('Export covers Albums /n Create covers Sucessfull to :'+path.dirname(filename), 7000)
				openFolder(path.dirname(filename))
	
	@pyqtSlot()
	def closeEvent(self, event):
		"""Quit."""
		response = QMessageBox.question(self, "Confirmation", "Exit DBAlbums ?", QMessageBox.Yes, QMessageBox.No)
		if response == QMessageBox.Yes:
			if self.dbbase:
				self.dbbase.close()
			if self.playerAudio.player.state() == QMediaPlayer.PlayingState:
				self.playerAudio.player.stop()
			event.accept()
		else:
			event.ignore()


if __name__ == '__main__':
	# working directory
	PATH_PROG = path.dirname(path.abspath(__file__))
	#chdir(PATH_PROG)
	QDir.setCurrent(PATH_PROG)
	# debug
	qInstallMessageHandler(qtmymessagehandler)
	app = QApplication(argv)
	if len(argv)>1 and argv[1] == 'MINI':
		DB = DBAlbumsQT5Mini()
	else:
		DB = DBAlbumsMainGui()
	DB.show()
	rc = app.exec_()
	exit(rc)
