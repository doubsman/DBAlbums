#! /usr/bin/python
# coding: utf-8

__author__ = "doubsman"
__copyright__ = "Copyright 2017, DBAlbums Project"
__credits__ = ["doubsman"]
__license__ = "GPL"
__version__ = "1.6"
__maintainer__ = "doubsman"
__email__ = "doubsman@doubsman.fr"
__status__ = "Production"

from sys import platform, argv, executable, exit
from csv import writer, QUOTE_ALL
from os import system, path, getcwd, remove
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import (Qt, QDir, QTime, pyqtSlot, QDateTime, QSettings, QtInfoMsg,
						QtWarningMsg, QtCriticalMsg, QtFatalMsg, qInstallMessageHandler, qDebug) 
from PyQt5.QtWidgets import (QApplication, QMainWindow, QProgressBar, QFileDialog, QMessageBox, 
						QMenu, QCompleter, QStyle)
from PyQt5.QtMultimedia import QMediaPlayer
# Gui QtDesigner : compiler .ui sans Eric6: pyuic5 file.ui -o Ui_main_file.py
from Ui_DBALBUMS import Ui_MainWindow

# DB DEV
from DBFunction import buildCommandPowershell, runCommand, openFolder, centerWidget, convertUNC
from DBLoadProc import DBloadingGui, ProcessGui
from DBDatabase import (connectDatabase, getrequest, copyDatabaseInvent, execSqlFile, 
						buildTabFromRequest, updateBaseScore, buildFileCover, extractCoverb64)
from DBModeldat import ModelTbl
from DBArtworks import ArtworksGui, CoverViewGui
from DBAuPlayer import DBPlayer
from DBFoobarpl import foobarMajDBFOOBAR


# ##################################################################
# CONSTANTS
# path
qDebug('Start')
if getattr(system, 'frozen', False):
	# frozen
	PATH_PROG = path.dirname(executable)
else:
	# unfrozen
	PATH_PROG = path.realpath(path.dirname(argv[0]))
	# PATH_PROG = path.dirname(__file__)
# working directory
# chdir(PATH_PROG)
QDir.setCurrent(PATH_PROG)
LOGS_PROG = path.join(PATH_PROG, 'LOG')
BASE_SQLI = path.join(PATH_PROG, 'LOC', "DBALBUMS_{envt}.db")
PWSH_SCRI = path.join(PATH_PROG, 'PS1', "BUILD_INVENT_{mod}.ps1")
PWSH_SCRU = path.join(PATH_PROG, 'PS1', "UPDATE_ALBUMS.ps1")
PWSH_SCRA = path.join(PATH_PROG, 'PS1', "ADD_ALBUMS.ps1")
FOOB_UPSC = path.join(PATH_PROG, 'SQL', "DBAlbums_FOOBAR_UPADTESCORE.sql")
RESS_LABS = 'LAB'
MASKCOVER = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.bmp', '.tiff')


# ##################################################################
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
HEIG_LTAB = int(configini.value('tagrid_nbl'))
DISP_CJOKER = configini.value('text_joker')
WINS_ICO = path.join(PATH_PROG, 'IMG', configini.value('wins_icone'))
UNIX_ICO = path.join(PATH_PROG, 'IMG', configini.value('unix_icone'))
CDRO_ICO = path.join(PATH_PROG, 'IMG', configini.value('cdro_icone'))
LOGO_PRG = path.join(PATH_PROG, 'IMG', configini.value('progr_logo'))
PICT_NCO = path.join(PATH_PROG, 'IMG', configini.value('pict_blank'))
PICM_NCO = path.join(PATH_PROG, 'IMG', configini.value('picm_blank'))
THUN_DBA = path.join(PATH_PROG, 'IMG', configini.value('picm_endof'))
TEXT_NCO = configini.value('text_nocov')
ENVT_DEF = configini.value('envt_deflt')
TREE_CO0 = configini.value('color0_lin')
TREE_CO1 = configini.value('color1_lin')
TREE_CO2 = configini.value('color2_lin')
TREE_CO3 = configini.value('color3_lin')
THUN_CO0 = configini.value('color0_thu')
THUN_CO1 = configini.value('color1_thu')
THUN_SE1 = configini.value('color0_sel')
THUN_SE2 = configini.value('color1_sel')
THUN_DIS = int(configini.value('thnail_dis'))
THUN_NOD = int(configini.value('thnail_nod'))
COVE_SIZ = int(configini.value('covers_siz'))
FONT_MAI = configini.value('font00_ttx')
FONT_CON = configini.value('font01_ttx')
configini.endGroup()
# PROGS LINKS
configini.beginGroup('programs')
TAGS_SCAN = r'' + configini.value('tagscan')
FOOB_PLAY = r'' + configini.value('foobarP')
if platform == "darwin" or platform == 'linux':
	EDIT_TEXT = r'' + configini.value('txt_lin')
	LOGS_PROG = convertUNC(LOGS_PROG)
	BASE_SQLI = convertUNC(BASE_SQLI)
	WINS_ICO = convertUNC(WINS_ICO)
	UNIX_ICO = convertUNC(UNIX_ICO)
	CDRO_ICO = convertUNC(CDRO_ICO)	
	LOGO_PRG = convertUNC(LOGO_PRG)
	PICT_NCO = convertUNC(PICT_NCO)
	PICM_NCO = convertUNC(PICM_NCO)
	THUN_DBA = convertUNC(THUN_DBA)
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


# ##################################################################
# Logging
def qtmymessagehandler(mode, context, message):
	if mode == QtInfoMsg:
		mode = 'INFO'
	elif mode == QtWarningMsg:
		mode = 'WARNING'
	elif mode == QtCriticalMsg:
		mode = 'CRITICAL'
	elif mode == QtFatalMsg:
		mode = 'FATAL'
	else:
		mode = 'DEBUG'
	print('qt_message_handler: line: {li}, func: {fu}(), file: {fi}'.format(li=context.line,
																		 fu=context.function,
																		 fi=context.file))
	print('  {m}: {e}\n'.format(m=mode, e=message))


qInstallMessageHandler(qtmymessagehandler)

# ##################################################################
# ## definition list albums
# columns position 0-19 wrapper
A_POSITIO = (	'Category', 'Family', 'Name', 'Label', 'ISRC',
				'Qty_Tracks', 'Qty_CD', 'Year', 'Length', 'Size',
				'Score', 'Qty_covers', 'Date_Insert', 'Date_Modifs', 'Position',
				'Typ_Tag', 'Path', 'Cover', 'MD5', 'ID_CD')
# columns grid name
A_COLNAME = (	'Category', 'Family', 'Name', 'Label', 'ISRC',
				'Trk', 'CD', 'Year', 'Time', 'Size',
				'Score', 'Pic', 'Add', 'Modified', 'Position',
				'Tag', 'Path', 'Cover', 'MD5', 'ID_CD')
# ## definition list tracks
# columns position 0-8 wrapper
T_POSITIO = (	'ODR_Track', 'TAG_Artists', 'TAG_Title', 'TAG_length',
				'Score', 'TAG_Genres', 'FIL_Track', 'REP_Track', 'ID_TRACK')
# columns grid name
T_COLNAME = (	'N°', 'Artist', 'Title', 'Time',
				'Score', 'Style', 'File', 'Folder', 'ID_TRACK')


def displayCounters(num=0, text=''):
	"""format 0 000 + plural."""
	strtxt = " %s%s" % (text, "s"[num == 1:])
	if num > 9999:
		strnum = '{0:,}'.format(num).replace(",", " ")
	else:
		strnum = str(num)
	return (strnum + strtxt)


def displayStars(star, scorelist):
	"""scoring."""
	maxstar = len(scorelist)-1
	txt_score = scorelist[star]
	return (txt_score+'  '+star*'★'+(maxstar-star)*'☆')


def albumnameextract(name, label, isrc, year, nbcd, nbtracks, nbmin, nbcovers ):
	"""buil label name & album name."""
	# name + label
	infoslabel = ""
	infosaisrc = ""
	infonameal = ""
	infosayear = ""
	imglabel = None
	if '[' in name:
		textsalbum = name[name.find('[')+1:name.find(']')]
		infonameal = name.replace('['+textsalbum+']', '')
		infoslabel += textsalbum.replace('-', ' • ')
	else:
		infonameal = name
	snbcd = str(nbcd)
	sctxt = infonameal.split(' - ')[0].rstrip()
	if sctxt=='':
		sctxt = infonameal.split('—')[0].rstrip()
	infonameal = infonameal.replace('('+snbcd+'CD)', '').replace(snbcd+'CD', '')
	infonameal = infonameal.replace(snbcd+'CD', '').replace(snbcd+'CD', '')
	infonameal = '<a style="text-decoration:none;color: black;" href="dbfunction://s' + sctxt + '"><b><big>' + infonameal + '</big></b></a>'
	# label
	if label != "":
		imglabel = RESS_LABS +'/'+ label.replace(' ','_') +'.jpg'
		if not path.isfile(imglabel):
			imglabel = None
		infoslabel = '<a style="color: black;" href="dbfunction://l'+label+'">' + label + '</a>'
	elif infoslabel != "":
		if infoslabel.find('-') > 0:
			label = infoslabel.split('-')[0].replace('[', '').rstrip()
			infoslabel = '<big>' + label + '</big>'
			isrc = infoslabel.split('-')[1].replace(']', '').lstrip()
	# isrc
	if isrc != "":
		infosaisrc = isrc
	# year
	if year != "":
		infosayear = '<b><big> - <a style="color: black;" href="dbfunction://y'+year+'">' + year + '</a></big></b> '
	# nb cd
	if nbcd<6:
		infosnbcd = '<img style="vertical-align:Bottom;" src="' + CDRO_ICO + '" height="15">'
		infosnbcd = nbcd*infosnbcd
	else:
		infosnbcd = displayCounters(nbcd, 'CD')
	# others
	infotrack = displayCounters(nbtracks, 'Track')
	infoduree = displayCounters(nbmin, 'min')
	infoartco = displayCounters(nbcovers, 'art')
	if nbcovers>0:
		infoartco = '<a style="color: black;" href="dbfunction://a">' + infoartco + '</a>'
	infoshtml = '<span>' + infonameal + infosayear + '</span>' + infosnbcd + '<br/>'
	if infoslabel != "":
		if infosaisrc != "":
			infoshtml += infoslabel + ' • ' + infosaisrc + ' • '
		else:
			infoshtml += infoslabel + ' • '
	infoshtml += infotrack + ' • ' + infoduree + ' • ' + infoartco
	return infoshtml, imglabel


# ##################################################################
qDebug('init main gui')
class DBAlbumsMainGui(QMainWindow, Ui_MainWindow):
	"""DBAlbums main gui."""
	# default value
	WIDT_PICM = WIDT_PICM
	HEIG_MAIN = HEIG_MAIN
	WIDT_MAIN = WIDT_MAIN
	COVE_SIZ = COVE_SIZ
	COEF_ZOOM = 100

	def __init__(self, parent=None):
		"""Init gui."""
		super(DBAlbumsMainGui, self).__init__(parent)
		self.setupUi(self)

		self.envits = None				# environment
		self.dbbase = None				# database connect
		self.modsql = None				# type database
		self.currow = None  			# row tab current album
		self.curAlb = None				# ID current album
		self.curMd5 = None  			# MD5 current album
		self.pathcov = None				# cover current album
		self.curTrk = None				# ID current track
		self.homMed = None				# playlist player
		self.rootDk = None				# root colume music
		self.infoBox = None				# message box
		self.maintitle = 'Loading...'	# status bar main message
		self.coveral = QPixmap(PICT_NCO)	# current cover album
		# zoom
		self.cuzoom = self.COEF_ZOOM
		self.sizeTN = self.WIDT_PICM
		self.h_main = self.HEIG_MAIN
		self.w_main = self.WIDT_MAIN
		# loading
		self.loadingGui = None

		# font
		font = QFont()
		font.setFamily(FONT_MAI)
		font.setFixedPitch(True)
		font.setPointSize(12)
		self.lab_search.setFont(font)
		self.lab_scorealb.setFont(font)
		self.lab_scoretrk.setFont(font)
		self.lab_album.setFont(font)

		# center
		centerWidget(self)

		self.setWindowTitle(TITL_PROG)
		self.resize(self.w_main, self.h_main)
		self.setWindowIcon(QIcon(WINS_ICO))
		self.setStyleSheet('QMainWindow{background-color: #D9D9D9;border: 1px solid black;} '
						   'QStatusBar{background-color: #D9D9D9;border: 1px solid black;}')

		# init combos Envt
		self.com_envt.addItems(NAME_EVT)
		self.com_envt.setCurrentIndex(CURT_EVT)
		
		# buttons
		self.btn_clearsearch.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
		self.btn_search.setIcon(self.style().standardIcon(QStyle.SP_FileDialogContentsView))
		self.btn_notreeview.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
		
		# init scrore
		self.sli_scorealb.setMinimum(0)
		self.sli_scorealb.setMaximum(len(SCOR_ALBUMS)-1)
		self.btn_scorealb.setVisible(False)
		self.sli_scorealb.setValue(0)
		self.sli_scoretrk.setMinimum(0)
		self.sli_scoretrk.setMaximum(len(SCOR_TRACKS)-1)
		self.btn_scoretrk.setVisible(False)
		self.sli_scoretrk.setValue(0)

		# init title album
		self.lab_album.setOpenLinks(False)
		
		# tab list no header row
		self.tbl_albums.verticalHeader().setVisible(False)
		self.tbl_tracks.verticalHeader().setVisible(False)
		
		# init player
		self.playerAudio = DBPlayer()
		self.horizontalplayer.addWidget(self.playerAudio)

		# init progres bar
		self.gaugeBar = QProgressBar(self)
		self.gaugeBar.setVisible(False)
		self.gaugeBar.setMinimum(0)
		self.gaugeBar.setMaximum(1)
		self.statusbar.addPermanentWidget(self.gaugeBar)

		# popup category
		self.menuc = QMenu()
		self.action_UCP = self.menuc.addAction("Update Category (powershell)...", lambda c=self.com_category.currentText(): self.buildInvent(c))
		# popup base
		self.menub = QMenu()
		self.menub.addAction("Show Informations  [F1]", self.showLoadingGui)
		self.menub.addAction("Reload base Albums [F5]", lambda: self.connectEnvt(True))
		self.action_UBP = self.menub.addAction("Update Base (powershell)...", self.buildInvent)
		self.action_CSD = self.menub.addAction("Create sqlite database", self.createLocalBase)
		self.action_IFP = self.menub.addAction("Import Foobar Playlists, Update Score...", self.importFoobar)
		self.menub.addAction("Edit %s..." % FILE__INI, lambda e=EDIT_TEXT, f=FILE__INI: runCommand(e, f))
		self.menub.addAction("Open Logs Folder...", lambda flog=LOGS_PROG: openFolder(flog))
		# popup albums
		self.menua = QMenu()
		self.action_VIA = self.menua.addAction("View ArtWorks...", self.viewArtworks)
		self.action_OPF = self.menua.addAction("Open Folder...", self.getFolder)
		self.action_EXA = self.menua.addAction("Export Album...", self.exportAlbums)
		self.action_UAP = self.menua.addAction("Update Album...", self.updateAlbums)
		self.action_TAG = self.menua.addAction("Edit Tags (TagScan)...", self.openTagScan)
		
		# link Gui
		self.lin_search.returnPressed.connect(self.onFiltersChanged)
		self.btn_clearsearch.clicked.connect(self.clearFilters)
		self.btn_search.clicked.connect(self.onFiltersChanged)
		self.chb_searchtracks.clicked.connect(self.onFiltersChanged)
		self.com_category.setContextMenuPolicy(Qt.CustomContextMenu)
		self.com_category.customContextMenuRequested.connect(self.popUpCategoryAlbums)
		self.com_category.currentIndexChanged.connect(self.onFiltersChanged)
		self.com_family.currentIndexChanged.connect(self.onFiltersChanged)
		self.com_label.currentIndexChanged.connect(self.onFiltersChanged)
		self.com_year.currentIndexChanged.connect(self.onFiltersChanged)
		self.btn_notreeview.clicked.connect(self.noDisplayTab)
		self.com_envt.currentIndexChanged.connect(self.connectEnvt)
		self.com_envt.setContextMenuPolicy(Qt.CustomContextMenu)
		self.com_envt.customContextMenuRequested.connect(self.popUpBaseAlbums)
		self.scrollArea.setContextMenuPolicy(Qt.CustomContextMenu)
		self.scrollArea.customContextMenuRequested.connect(self.popUpTNAlbums)
		self.tbl_albums.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tbl_albums.customContextMenuRequested.connect(self.popUpTreeAlbums)
		self.tbl_albums.clicked.connect(self.onSelectListChanged)
		self.tbl_albums.currentChanged = self.onSelectListChanged
		self.tbl_tracks.clicked.connect(self.onSelectTrackChanged)
		self.tbl_tracks.doubleClicked.connect(self.playMediasAlbum)
		self.tbl_tracks.currentChanged = self.onSelectTrackChanged
		self.lab_album.anchorClicked.connect(self.onAnchorClicked)
		self.labelcover.mousePressEvent = self.onPressCover
		self.sli_scorealb.valueChanged.connect(self.onModifyScoreAlbum)
		self.sli_scoretrk.valueChanged.connect(self.onModifyScoreTrack)
		self.btn_scorealb.clicked.connect(self.onPressButtonEnrScoreAlbum)
		self.btn_scoretrk.clicked.connect(self.onPressButtonEnrScoreTrack)
		self.playerAudio.signaltxt.connect(self.updateStatusBar)

		# DISABLED OPTIONS for OS linux: no powershell, foobar, tagscan
		if platform == "darwin" or platform == 'linux':
			self.action_UBP.setEnabled(False)	# Update base powershell
			self.action_IFP.setEnabled(False)   # Import playlists foobar 2000
			self.action_UCP.setEnabled(False)	# Update category powershell
			self.action_UAP.setEnabled(False)	# Update album powershell)
			self.action_TAG.setEnabled(False)	# TagScan

		# init connect
		self.connectEnvt()

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
		degre = event.angleDelta()/4.8 # 120/4.8=25
		nbstep = 3
		modifiers = QApplication.keyboardModifiers()
		oldsizeTN = self.sizeTN
		if modifiers == Qt.ControlModifier:
			self.cuzoom += degre.y()
			self.sizeTN = DBAlbumsMainGui.WIDT_PICM * (self.cuzoom/100)
		# default zoom [...|...]
		zmin = DBAlbumsMainGui.COEF_ZOOM-(nbstep*abs(degre.y()))
		zmax = DBAlbumsMainGui.COEF_ZOOM+(nbstep*abs(degre.y()))
		if self.cuzoom < zmin or self.cuzoom > zmax:
			self.cuzoom = DBAlbumsMainGui.COEF_ZOOM
			self.sizeTN = DBAlbumsMainGui.WIDT_PICM
		# redisplay zoom thunbnails
		if self.sizeTN < oldsizeTN:
			# resize
			self.tableMdlAlb.replaceThunbnails(self.sizeTN, oldsizeTN)
		elif self.sizeTN > oldsizeTN:
			# rebuild
			self.tableMdlAlb.displayThunbnails()

	@pyqtSlot()
	def resizeEvent(self, event):
		if self.gridthunbnails.count() > 0:
			self.tableMdlAlb.replaceThunbnails(self.sizeTN, self.sizeTN)

	@pyqtSlot()
	def closeEvent(self, event):
		"""Quit."""
		response = QMessageBox.question(self, "Confirmation", "Exit DBAlbums ?", QMessageBox.Yes, QMessageBox.No)
		if response == QMessageBox.Yes:
			if self.dbbase:
				self.dbbase.close()
			event.accept()
		else:
			event.ignore()

	def noDisplayTab(self):
		if self.tbl_albums.isVisible():
			self.tbl_albums.hide()
		else:
			self.tbl_albums.show()

	def showLoadingGui(self, event=None):
		# loading Gui
		if self.loadingGui.isVisible():
			self.loadingGui.hide()
		else:
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
		self.onFiltersChanged()

	def onFiltersChanged(self): # ####################
		category = self.com_category.currentText()
		if category != DISP_CJOKER and category is not None:
			print('category Filter')
			self.tableMdlAlb.setFilter('Category', self.com_category.currentText())
			print("Category   : "+str(self.com_category.currentText())+"'")
			print("txt search : "+self.lin_search.text())
			#print("search In  : "+(self.chb_searchtracks.isChecked()))

	def updateStatusBar(self, message, t=0):
		"""Update Status Bar Message"""
		self.statusBar().showMessage(message, t)

	def updateGaugeBar(self, purcent, message=None, t=0):
		"""Update Gauge Bar and Status Bar Message"""
		if message is not None:
			self.updateStatusBar(message, t)
		self.gaugeBar.setValue(purcent)
		self.update()
		if purcent == 1:
			self.gaugeBar.setVisible(False)
			self.updateStatusBar(self.maintitle, t)
		else:
			self.gaugeBar.setVisible(True)

	def connectEnvt(self, refresh=False):
		"""Connect Envt."""
		if self.envits != self.com_envt.currentText() or refresh:
			self.envits = self.com_envt.currentText()
			# clear combos
			self.com_category.clear()
			self.com_family.clear()
			self.com_label.clear()
			self.com_year.clear()
			# connect
			boolconnect, self.dbbase, self.modsql, self.rootDk = connectDatabase(self.envits)
			if not boolconnect:
				# no connect
				self.updateStatusBar("Connect Failed, please select other environment...")
				# init combos
				self.com_category.addItems([DISP_CJOKER])
				self.com_family.addItems([DISP_CJOKER])
				self.com_label.addItems([DISP_CJOKER])
				self.com_year.addItems([DISP_CJOKER])
				# cover blank
				self.coveral = QPixmap(PICT_NCO)
				self.labelcover.setPixmap(self.coveral)
				# init scrore
				self.sli_scorealb.setValue(0)
				self.sli_scoretrk.setValue(0)
			else:
				# mode sqllite, no menu create base
				if self.modsql == 'sqlite':
					self.action_CSD.setEnabled(False)
				else:
					self.action_CSD.setEnabled(True)
				# loading splashscreen
				self.loadingGui = DBloadingGui(self.modsql)
				# last date modifcation base
				curdate = QTime.currentTime().toString('hh:mm:ss')
				self.setWindowTitle('{prog} : Connected base {base} [{mode}] at {hour}'.format(prog=TITL_PROG,
																								mode=self.modsql,
																								base=self.envits,
																								hour=curdate))
				# fill model/tree albums list/thunbnails
				req = getrequest('albumslist', self.modsql)
				self.tableMdlAlb = ModelTbl(self, req, self.gridthunbnails, A_COLNAME, A_POSITIO)
				self.tbl_albums.setModel(self.tableMdlAlb)
				self.tbl_albums.resizeColumnsToContents()
				self.tbl_albums.resizeRowsToContents()
				# data ?
				if self.tableMdlAlb.rowCount() > 0:
					# fill combos
					self.com_category.addItems(self.tableMdlAlb.datacombos('Category'))
					self.com_family.addItems(self.tableMdlAlb.datacombos('Family'))
					self.com_label.addItems(self.tableMdlAlb.datacombos('Label'))
					self.com_year.addItems(self.tableMdlAlb.datacombos('Year'))
					# fill thunbnails
					self.tableMdlAlb.displayThunbnails()
					self.tableMdlAlb.builListThunbnails2()
					# autocompletion list
					autoList = buildTabFromRequest(getrequest('autocompletion', self.modsql))
					self.com_autcom = QCompleter(autoList, self.lin_search)
					self.com_autcom.setCaseSensitivity(Qt.CaseInsensitive)
					self.lin_search.setCompleter(self.com_autcom)
					# select default row
					if not refresh:
						self.currow = 0
					self.tbl_albums.selectRow(self.currow)
					if self.focusWidget() == self.tbl_albums:
						self.tbl_albums.setFocus()
					else:
						self.lin_search.setFocus()
					# display album
					self.currow = self.tbl_albums.currentIndex().row()
					self.displayAlbum()
					# build message
					txt_siz = str(int(self.tableMdlAlb.getSum('Size')/1024)) + ' Go'
					cpt_len = self.tableMdlAlb.getSum('Length')
					cpt_cds = self.tableMdlAlb.getSum('Qty_CD')
					cpt_trk = self.tableMdlAlb.getSum('Qty_Tracks')
					if int(((cpt_len/60/60)/24)*10)/10 < 1:
						# seoncd -> Hours
						txt_len = str(int(((cpt_len/60/60))*10)/10) + ' Hours'
					else:
						# seoncd -> Days
						txt_len = str(int(((cpt_len/60/60)/24)*10)/10) + ' Days'
					message = "Search Result \"{sch}\" :  {alb} | {trk} | {cds} | {siz} | {dur}".format(alb=displayCounters(self.tableMdlAlb.rowCount(), 'Album'),
																										cds=displayCounters(cpt_cds, 'CD'),
																										trk=displayCounters(cpt_trk, 'Track'),
																										siz=txt_siz,
																										dur=txt_len,
																										sch='{sch}')
					# end loading
					self.loadingGui.hide()
				else:
					message = "Search Result \"{sch}\" : nothing"
					# init combos
					self.com_category.addItems([DISP_CJOKER])
					self.com_family.addItems([DISP_CJOKER])
					self.com_label.addItems([DISP_CJOKER])
					self.com_year.addItems([DISP_CJOKER])
					# cover blank
					self.coveral = QPixmap(PICT_NCO)
					self.labelcover.setPixmap(self.coveral)
					# init scrore
					self.sli_scorealb.setValue(0)
					self.sli_scoretrk.setValue(0)
				# display message
				txt_sch = (self.lin_search.text() if len(self.lin_search.text()) > 0 else 'all')
				self.maintitle = message.format(sch=txt_sch)
				self.updateStatusBar(self.maintitle)

	def displayAlbum(self):
		"""Display info current select album."""
		self.curAlb = self.tableMdlAlb.getData(self.currow, 'ID_CD').value()
		self.curMd5 = self.tableMdlAlb.getData(self.currow, 'MD5').value()
		self.albumname = self.tableMdlAlb.getData(self.currow, 'Name').value()
		self.ScoreAlbum = int(self.tableMdlAlb.getData(self.currow, 'Score').value()) # len
		self.pathcover = self.tableMdlAlb.getData(self.currow, 'Cover').value()
		self.AlbumPath = self.tableMdlAlb.getData(self.currow, 'Path').value()

		# select thunbnail
		for i in range(self.gridthunbnails.count()):
			if int(self.gridthunbnails.itemAt(i).widget().Name) == int(self.currow):
				self.gridthunbnails.itemAt(i).widget().setStyleSheet("border: 2px solid red;")
				curthu = self.gridthunbnails.itemAt(i).widget()
				# move scroll to widget
				self.scrollArea.ensureWidgetVisible(curthu)
				break

		# fill tracks
		req = (getrequest('trackslist', self.modsql)).format(id=self.curAlb)
		self.tableMdlTrk = ModelTbl(self, req, None, T_COLNAME, T_POSITIO)
		self.tbl_tracks.setModel(self.tableMdlTrk)
		self.tbl_tracks.resizeColumnsToContents()
		self.tbl_tracks.resizeRowsToContents()

		# build stats album
		cpt_len = self.tableMdlTrk.getSum('TAG_length')
		txt_album, img_lab = albumnameextract(self.albumname,
									str(self.tableMdlAlb.getData(self.currow, 'Label').value()),
									str(self.tableMdlAlb.getData(self.currow, 'ISRC').value()),
									str(self.tableMdlAlb.getData(self.currow, 'Year').value()),
									int(self.tableMdlAlb.getData(self.currow, 'Qty_CD').value()),
									self.tableMdlTrk.rowCount(),
									int(((cpt_len/60)*10)/10),
									int(self.tableMdlAlb.getData(self.currow, 'Qty_covers').value()))
		# img label
		if img_lab is not None:
			plabel = QPixmap(img_lab)
			self.lab_label.setPixmap(plabel)
			self.lab_label.setVisible(True)
		else:
			self.lab_label.setVisible(False)
		
		# title album
		self.lab_album.setHtml(txt_album)

		# fill score album
		self.sli_scorealb.setValue(self.ScoreAlbum)
		self.lab_scorealb.setText(displayStars(self.ScoreAlbum, SCOR_ALBUMS))

		# fill cover
		self.coveral = extractCoverb64(self.curMd5, PICM_NCO)
		self.coveral = self.coveral.scaled(self.COVE_SIZ, self.COVE_SIZ, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
		self.labelcover.setPixmap(self.coveral)

		# fill play medias only is not playing
		if self.playerAudio.player.state() != QMediaPlayer.PlayingState:
			self.curtrk = self.tbl_tracks.currentIndex().row()
			self.homMed = self.tableMdlTrk.getMedias()
			self.playerAudio.addMediaslist(self.homMed, self.curtrk)
			
		# init status bar
		self.updateStatusBar(self.maintitle)
		
		# select track default
		if self.tableMdlTrk.rowCount() > 0:
			self.tbl_tracks.selectRow(0)
			self.curTrk = 0
		self.displaytrack()

	def displaytrack(self):
		"""Display info current select track."""
		if self.tableMdlTrk.rowCount() > 0:
			self.curtrk = self.tbl_tracks.currentIndex().row()
			self.ScoreTrack = int(self.tableMdlTrk.getData(self.curtrk, 'Score').value()) # len
			self.sli_scoretrk.setEnabled(True)
			self.lab_scoretrk.setEnabled(True)
		else:
			self.curtrk = None
			self.ScoreTrack = 0
			self.sli_scoretrk.setEnabled(False)
			self.lab_scoretrk.setEnabled(False)
		self.sli_scoretrk.setValue(self.ScoreTrack)
		self.lab_scoretrk.setText(displayStars(self.ScoreTrack, SCOR_TRACKS))

	def onModifyScoreAlbum(self,  event):
		"""Modify Score Album."""
		indexes = self.tbl_albums.selectedIndexes()
		if len(indexes) > 0:
			self.lab_scorealb.setText(displayStars(self.sli_scorealb.value(), SCOR_ALBUMS))
			if self.ScoreAlbum != self.sli_scorealb.value():
				self.btn_scorealb.setVisible(True)
				listRows = []
				for ind in indexes:
					listRows.append(ind.row())
				nbselect = len(list(set(listRows)))
				if nbselect == 1:
					self.btn_scorealb.setText('Update')
				else:
					self.btn_scorealb.setText('Upd*' + str(nbselect))
			else:
				self.btn_scorealb.setVisible(False)

	def onModifyScoreTrack(self,  event):
		"""Modify Score Track."""
		indexes = self.tbl_tracks.selectedIndexes()
		if len(indexes) > 0:
			self.lab_scoretrk.setText(displayStars(self.sli_scoretrk.value(), SCOR_TRACKS))
			if self.ScoreTrack != self.sli_scoretrk.value():
				self.btn_scoretrk.setVisible(True)
				listRows = []
				for ind in indexes:
					listRows.append(ind.row())
				nbselect = len(list(set(listRows)))
				if nbselect == 1:
					self.btn_scoretrk.setText('Update')
				else:
					self.btn_scoretrk.setText('Upd*' + str(nbselect))
			else:
				self.btn_scoretrk.setVisible(False)

	def onSelectThunbnailChanged(self, event, row):
		"""Change album infos."""
		self.currow = int(row)
		self.tbl_albums.setFocus()
		self.tbl_albums.selectRow(row)
		index = self.tableMdlAlb.index(row, 0)
		self.tbl_albums.scrollTo(index)
		self.displayAlbum()

	def onSelectListChanged(self, event,  indexes=None):
		"""Select Album."""
		indexes = self.tbl_albums.selectedIndexes()
		if len(indexes) > 0 and self.currow != self.tbl_albums.currentIndex().row():
			# unselect thunbnail
			for i in range(self.gridthunbnails.count()):
				if int(self.gridthunbnails.itemAt(i).widget().Name) == int(self.currow):
					self.gridthunbnails.itemAt(i).widget().setStyleSheet("border: 2px solid white;")
			self.currow = self.tbl_albums.currentIndex().row()
			self.displayAlbum()

	def onSelectTrackChanged(self, event, indexes=None):
		"""Select Track."""
		indexes = self.tbl_tracks.selectedIndexes()
		if len(indexes) > 0 and self.curtrk != self.tbl_tracks.currentIndex().row():
			self.curtrk = self.tbl_tracks.currentIndex().row()
			self.displaytrack()
			if self.playerAudio.player.state() != QMediaPlayer.PlayingState:
				self.playerAudio.currentPlaylist.setCurrentIndex(self.curtrk)
	
	def onAnchorClicked(self, url):
		"""Balises html title album clicked"""
		text = str(url.toString())
		if text.startswith('dbfunction://'):
			function = text.replace('dbfunction://','')
			print(function)
			param = function[1:]
			if function.startswith('a'):
				self.viewArtworks()
			elif function.startswith('y'):
				index = self.com_year.findText(param, Qt.MatchFixedString)
				if index >= 0:
					self.com_year.setCurrentIndex(index)
			elif function.startswith('l'):
				index = self.com_label.findText(param, Qt.MatchFixedString)
				if index >= 0:
					self.com_label.setCurrentIndex(index)
			elif function.startswith('s'):
				self.lin_search.setText(param)
				self.onFiltersChanged()
			#if hasattr(self,function):
			#	getattr(self,function)()
	
	def onPressCover(self,  event):
		"""Display large cover MD5."""
		if self.pathcov is not None:
			if self.pathcov[0:len(TEXT_NCO)] != TEXT_NCO:
				CoverViewGui(self.coveral, self.albumname, self.h_main, self.h_main)

	def viewArtworks(self):
		"""views artworks covers storage."""
		ArtworksGui(self.AlbumPath, self.albumname, self.pathcover, self.w_main, self.h_main, self.sizeTN)

	def onPressButtonEnrScoreAlbum(self):
		"""Update Score Album."""
		indexes = self.tbl_albums.selectedIndexes()
		if len(indexes) > 0:
			listRows = []
			for ind in indexes:
				listRows.append(ind.row())
			listRows = list(set(listRows))
			self.ScoreAlbum = self.sli_scorealb.value()
			self.lab_scorealb.setText(displayStars(self.sli_scorealb.value(), SCOR_ALBUMS))
			for ind in listRows:
				indalb = str(self.tableMdlAlb.getData(ind, 'ID_CD').value())
				# Mysql
				updateBaseScore(self.ScoreAlbum, indalb, getrequest('updatescorealbum', self.modsql))
		# Treeview
		self.tableMdlAlb.refresh()
		# Button
		self.btn_scorealb.setVisible(False)

	def onPressButtonEnrScoreTrack(self):
		"""Update Score Track."""
		indexes = self.tbl_tracks.selectedIndexes()
		if len(indexes) > 0:
			listRows = []
			for ind in indexes:
				listRows.append(ind.row())
			listRows = list(set(listRows))
			self.ScoreTrack = self.sli_scoretrk.value()
			self.lab_scoretrk.setText(displayStars(self.sli_scoretrk.value(), SCOR_TRACKS))
			for ind in listRows:
				indalb = str(self.tableMdlTrk.getData(ind, 'ID_TRACK').value())
				# Mysql
				updateBaseScore(self.ScoreTrack, indalb, getrequest('updatescoretrack', self.modsql))
		# Treeview
		self.tableMdlTrk.refresh()
		# Button
		self.btn_scoretrk.setVisible(False)

	def popUpBaseAlbums(self,  position):
		"""Menu Database."""
		self.menub.exec_(self.com_envt.mapToGlobal(position))

	def popUpCategoryAlbums(self,  position):
		"""Menu Combo Category."""
		self.menuc.exec_(self.com_category.mapToGlobal(position))

	def popUpTreeAlbums(self,  position):
		"""Menu Thunbnails."""
		indexes = self.tbl_albums.selectedIndexes()
		listRows = []
		for ind in indexes:
			listRows.append(ind.row())
		listRows = list(set(listRows))
		if len(listRows) == 1:
			self.currow = self.tbl_albums.currentIndex().row()
			self.displayAlbum()
			self.action_TAG.setEnabled(True)
			self.updateTextPopupAlbum(self.tbl_albums.viewport().mapToGlobal(position))
		else:
			if len(indexes) > 1:
				self.action_VIA.setEnabled(False)
				self.action_OPF.setEnabled(False)
				self.action_EXA.setText("Export " + displayCounters(len(listRows), 'Album')+"cover/csv...")
				self.action_UAP.setText("Update " + displayCounters(len(listRows), 'Album') + "...")
				self.action_TAG.setEnabled(False)
				self.menua.exec_(self.tbl_albums.viewport().mapToGlobal(position))

	def popUpTNAlbums(self,  position):
		"""Mennu Albums."""
		self.updateTextPopupAlbum(self.scrollArea.mapToGlobal(position))

	def updateTextPopupAlbum(self, position):
		if self.tableMdlAlb.getData(self.currow, 'Qty_covers').value() == 0 or not(path.exists(self.AlbumPath)):
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

	def getFolder(self):
		"""Open album folder."""
		openFolder(self.AlbumPath)

	def openTagScan(self):
		"""Open program TAGs. edit."""
		runCommand(TAGS_SCAN, self.AlbumPath)

	def buildInvent(self, category=None):
		"""Execute powershell Script update all albums infos."""
		if 'LOSSLESS' in self.envits:
			filescript = PWSH_SCRI.format(mod='LOSSLESS')
		else:
			filescript = PWSH_SCRI.format(mod='MP3')
		if category is not None:
			exeprocess, params = buildCommandPowershell(filescript, '-Envt', self.envits, '-Collections', category)
		else:
			exeprocess, params = buildCommandPowershell(filescript, '-Envt', self.envits)
		pro = ProcessGui(exeprocess, params, 'Update Base '+self.envits)
		pro.signalend.connect(lambda: self.connectEnvt(True))

	def importFoobar(self):
		"""Foobar2000 playlists operations."""
		# import fpl playlist to mysql DBFOOBAR
		numtracks = foobarMajDBFOOBAR(self, FOOB_PLAY)
		if numtracks == 0:
			QMessageBox.critical(self, 'Foobar2000 playlists operations', 'Problem import files fpl playlist from : '+FOOB_PLAY)
		else:
			# synchro score sql
			execSqlFile(self, FOOB_UPSC, 9)
		self.updateStatusBar('Foobar2000 playlists finished', 5000)

	def updateAlbums(self):
		"""Execute powershell Script update albums infos."""
		indexes = self.tbl_albums.selectedIndexes()
		if len(indexes) > 0:
			listRows = []
			for ind in indexes:
				listRows.append(ind.row())
			listRows = list(set(listRows))
			listSelect = []
			for ind in listRows:
				listSelect.append(str(self.tableMdlAlb.getData(ind, 'ID_CD').value()))
			exeprocess, params = buildCommandPowershell(PWSH_SCRU, '-listID_CD', ','.join(listSelect), '-Envt', self.envits)
			pro = ProcessGui(exeprocess, params, 'Update ' + displayCounters(len(listSelect), "Album "))
			pro.signalend.connect(lambda: self.connectEnvt(True))

	def createLocalBase(self):
		"""Create base Sqlite."""
		filename = BASE_SQLI.format(envt=self.envits+'_SQLITE')
		# remove if exist
		if path.isfile(filename):
			remove(filename)
		logname = QTime.currentTime().toString('yymmddhhmmss') + "_COPY_DATABASE_TO_SQLITE_" + self.envits + ".log"
		copyDatabaseInvent(self, self.dbbase,  filename, path.join(LOGS_PROG, logname))
		self.updateStatusBar("Create Database SQLite/nCreate Database SQLite :"+filename+" Sucessfull", 7000)

	def playMediasAlbum(self, event):
		"""play album tracks."""
		indexes = self.tbl_tracks.selectedIndexes()
		if len(indexes) > 0:
			# playing ? reset
			self.curtrk = self.tbl_tracks.currentIndex().row()
			self.homMed = self.tableMdlTrk.getMedias()
			self.playerAudio.addMedialist(self.homMed, self.curtrk)
			self.playerAudio.player.play()
	
	def exportAlbums(self):
		"""Export file cover or list albums select in grid."""
		indexes = self.tbl_albums.selectedIndexes()
		if len(indexes) > 0:
			filename = QFileDialog.getSaveFileName(self,
												"Export from CSV File list or cover jpeg Files",
												getcwd(),
												"Images (*.jpg);;CSV files (*.csv)")
			if filename is None:
				return
			filename = filename[0]
			extension = (path.splitext(filename))[1]
			# list select album
			listRows = []
			for ind in indexes:
				listRows.append(ind.row())
			listRows = list(set(listRows))
			if extension == '.csv':
				# extract file CSV
				with open(filename, "w") as csv_file:
					wr = writer(csv_file, delimiter=';', doublequote=True, quoting=QUOTE_ALL, lineterminator='\n')
					for ind in listRows:
						textRows = []
						for col in range(self.tableMdlAlb.columnCount()):
							textcol = self.tableMdlAlb.data(self.tableMdlAlb.index(ind, col))
							if isinstance(textcol, QDateTime):
								textcol = textcol.toString('dd/mm/yyyy hh:mm:ss')
							textRows.append(textcol)
						wr.writerow(textRows)
				openFolder(path.dirname(filename))
				self.statusBar().showMessage('Export csv list Albums /n Create file csv Sucessfull to :'+filename, 7000)
			elif extension == '.jpg':
				# extract base64\mysql to file JPEG
				for ind in listRows:
					filecover = path.join(path.dirname(filename), self.tableMdlAlb.getData(ind, 'Name').value())
					extension = ((self.tableMdlAlb.getData(ind, 'Cover').value())[-4:]).replace('.', '')
					filecover = filecover+'.'+extension
					buildFileCover(filecover, self.tableMdlAlb.getData(ind, 'MD5').value())
				self.statusBar().showMessage('Export covers Albums /n Create covers Sucessfull to :'+path.dirname(filename), 7000)
				openFolder(path.dirname(filename))


if __name__ == '__main__':
	app = QApplication(argv)
	DB = DBAlbumsMainGui()
	DB.show()
	rc = app.exec_()
	exit(rc)
