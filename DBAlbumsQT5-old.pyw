#!/usr/bin/env python
# -*- coding: utf-8 -*-

# compiler .ui
# pyuic5 file.ui -o Ui_main_file.py

from sys import platform, argv, executable
from os import system, path, chdir
#from time import sleep
from PIL import ImageTk, ImageDraw, ImageFont
from base64 import b64decode
from configparser import ConfigParser
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox, 
							QAbstractItemView, QLineEdit, QLabel, QMainWindow, QWidget, QMessageBox, QListWidget, QListWidgetItem, QTableView)#QSlider, QStyle,  QAction,
# Gui QtDesigner
from Ui_DBALBUMS import Ui_MainWindow


###################################################################
# CONSTANTS
# path
if getattr(system, 'frozen', False):
	# frozen
	PATH_PROG = path.dirname(executable)
else:
	# unfrozen
	PATH_PROG = path.realpath(path.dirname(argv[0]))
	#PATH_PROG = path.dirname(__file__)
TKDND_LIB = path.join(PATH_PROG,'lib','tkdnd2.8') #Dnd
chdir(PATH_PROG) # working directory
LOGS_PROG = path.join(PATH_PROG, 'LOG')
BASE_SQLI = path.join(PATH_PROG, 'LOC', "Invent_{envt}.db")
PWSH_SCRI = path.join(PATH_PROG, 'PS1', "BUILD_INVENT_{mod}.ps1")
PWSH_SCRU = path.join(PATH_PROG, 'PS1', "UPDATE_ALBUMS.ps1")
PWSH_SCRA = path.join(PATH_PROG, 'PS1', "ADD_ALBUMS.ps1")
FOOB_UPSC = path.join(PATH_PROG, 'SQL', "DBAlbums_FOOBAR_UPADTESCORE.sql")
MASKCOVER = ('.jpg','.jpeg','.png','.bmp','.tif','.bmp','.tiff')
# Read File DBAlbums.ini
FILE__INI = 'DBAlbums.ini'
readIni = ConfigParser()
readIni.read(FILE__INI)
# GUI
VERS_PROG   = readIni.get('dbalbums', 'prog_build')
TITL_PROG   = "♫ DBAlbums v{v} (2017)".format(v=VERS_PROG)
WIDT_MAIN   = readIni.getint('dbalbums', 'wgui_width')
HEIG_MAIN   = readIni.getint('dbalbums', 'wgui_heigh')
WIDT_PICM   = readIni.getint('dbalbums', 'thun_csize')
HEIG_LHUN   = readIni.getint('dbalbums', 'thnail_nbl')
HEIG_THUN   = HEIG_LHUN * (WIDT_PICM+4)
HEIG_LTAB   = readIni.getint('dbalbums', 'tagrid_nbl')
DISP_CJOKER = readIni.get('dbalbums', 'text_joker')
TEXT_NCO    = readIni.get('dbalbums', 'text_nocov')
WINS_ICO    = readIni.get('dbalbums', 'wins_icone')
UNIX_ICO    = readIni.get('dbalbums', 'unix_icone')
LOGO_PRG    = readIni.get('dbalbums', 'progr_logo')
PICT_NCO    = readIni.get('dbalbums', 'pict_blank')
PICM_NCO    = readIni.get('dbalbums', 'picm_blank')
ENVT_DEF    = readIni.get('dbalbums', 'envt_deflt')
TREE_CO0    = readIni.get('dbalbums', 'color0_lin')
TREE_CO1    = readIni.get('dbalbums', 'color1_lin')
TREE_CO2    = readIni.get('dbalbums', 'color2_lin')
TREE_CO3    = readIni.get('dbalbums', 'color3_lin')
THUN_CO0    = readIni.get('dbalbums', 'color0_thu')
THUN_CO1    = readIni.get('dbalbums', 'color1_thu')
THUN_SE1    = readIni.get('dbalbums', 'color0_sel')
THUN_SE2    = readIni.get('dbalbums', 'color1_sel')
THUN_DBA    = readIni.get('dbalbums', 'picm_endof')
THUN_DIS    = readIni.getint('dbalbums', 'thnail_dis')
THUN_NOD    = readIni.getint('dbalbums', 'thnail_nod')
COVE_SIZ    = readIni.getint('dbalbums', 'covers_siz')
FONT_MAI    = readIni.get('dbalbums', 'font00_ttx')
FONT_CON    = readIni.get('dbalbums', 'font01_ttx')
# PROGS LINKS
TAGS_SCAN = r'' + readIni.get('programs', 'tagscan')
FOOB_PLAY = r'' + readIni.get('programs', 'foobarP')
if platform == "darwin" or platform == 'linux':
	EDIT_TEXT = r'' + readIni.get('programs', 'txt_lin')
	LOGS_PROG = r""+LOGS_PROG.replace('\\\\','/').replace('\\','/')
	BASE_SQLI = r""+BASE_SQLI.replace('\\\\','/').replace('\\','/')
else:
	EDIT_TEXT = r'' + readIni.get('programs', 'txt_win')
# LIST SCORE
SCOR_ALBUMS = {}
for envt in readIni['score']:
	SCOR_ALBUMS.update({int(envt) : readIni.get('score',envt)})
SCOR_TRACKS = SCOR_ALBUMS
# LIST ENVT
NAME_EVT = []
for envt in readIni['environments']:
	envtname = readIni.get('environments',envt)
	if envtname == ENVT_DEF:
		CURT_EVT = len(NAME_EVT)
	NAME_EVT.append(readIni.get('environments',envt))

### definition list albums
# columns position 0-19
A_POSITIO = (	'Category', 'Family', 'Name', 'Label', 'ISRC',
				'Qty_Tracks', 'Qty_CD', 'Year', 'Length', 'Size',
				'Score', 'Qty_covers', 'Date_Insert', 'Date_Modifs', 'Position',
				'Typ_Tag', 'Path', 'Cover', 'MD5', 'ID_CD')
# columns grid name
A_COLNAME = (	'Category', 'Family', 'Name', 'Label', 'ISRC',
				'Trk', 'CD', 'Year', 'Time', 'Size',
				'Score', 'Pic', 'Add', 'Modified', 'Position',
				'Tag', 'Path', 'Cover', 'MD5')
# treeview columns width
A_C_WIDTH = (	60, 90, 250, 100, 80,
				30, 30, 40, 50, 40,
				45, 30, 67, 67, 250,
				30, 200, 200, 200)
### definition list tracks
# columns position 0-8
T_POSITIO = (	'ODR_Track', 'TAG_Artists', 'TAG_Title', 'TAG_length',
				'Score', 'TAG_Genres', 'FIL_Track', 'REP_Track', 'ID_TRACK')
# columns grid name
T_COLNAME = (	'N°', 'Artist', 'Title', 'Time',
				'Score', 'Style', 'File', 'Folder')
# treeview columns width
T_C_WIDTH = (	50, 150, 200, 60,
				45, 70, 250, 250)

class MyTableModel(QSqlQueryModel): 
    def __init__(self, datain, headerdata, parent=None, *args): 
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QSqlQueryModel.__init__(self, parent, *args) 
        self.arraydata = datain
        self.headerdata = headerdata
 
    def rowCount(self, parent): 
        return len(self.arraydata) 
 
    def columnCount(self, parent): 
        return len(self.arraydata[0]) 
 
    def data(self, index, role): 
        if not index.isValid(): 
            return QVariant() 
        elif role != Qt.DisplayRole: 
            return QVariant() 
        return QVariant(self.arraydata[index.row()][index.column()]) 

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))        
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))

###################################################################
# DBAlbums pyQT5
class DBAlbumsMainGui(QMainWindow):
	def __init__(self):
		super().__init__()
		
		# Init main windows
		self.setWindowTitle(TITL_PROG)
		#self.setFixedSize(WIDT_MAIN, HEIG_MAIN)
		self.resize(WIDT_MAIN, HEIG_MAIN)
		self.setWindowIcon(QIcon(WINS_ICO))
		self.setStyleSheet('QMainWindow{background-color: darkgray;border: 1px solid black;} ' \
						   'QMessageBox{background-color: darkgray;border: 1px solid black;}')
		
		# center
		qtRectangle = self.frameGeometry()
		centerPoint = QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())
		
		# Init GUI
		centralWidget = QWidget(self)
		centralWidget.setLayout(self.addControls())
		self.setCentralWidget(centralWidget)
		self.show()
		
		self.labels = []
		self.modelstalb = None
				
		#Connect to Database
		db=QSqlDatabase.addDatabase("QMYSQL")
		db.setHostName("doubbigstation")
		db.setDatabaseName("Invent")
		db.setUserName("admInvent")
		db.setPassword("MwRbBR2HA8PFQjuu")
		if db.open():
			self.statusBar().showMessage('Connected.')
			#Dispalying Data from MySql Db inTree View
			A_REQUEST = "SELECT Category, Family, Name, Label, ISRC, `Year`, Length, Qty_CD AS `CD`, " \
						"Qty_Tracks AS Trks, Qty_covers AS Pic, Score As SCR, Size, Typ_Tag AS Tag, " \
						"Date_Insert AS `Add`, Date_Modifs AS `Modified`, " \
						"CONCAT(Position1,'\\\\',Position2) AS Position, " \
						"Path, Cover, `MD5`, ID_CD AS ID " \
						"FROM DBALBUMS ORDER BY Date_Insert DESC"
			tablemodel=QSqlQueryModel()
			tablemodel.setQuery(A_REQUEST)
			self.treelstalb.setModel(tablemodel) 
			self.treelstalb.resizeColumnsToContents()
			self.treelstalb.resizeRowsToContents()
			self.treelstalb.setSelectionBehavior(QAbstractItemView.SelectRows)
			self.modelstalb = self.treelstalb.model()
			self.treelstalb.selectRow(0)
			#QSortFilterSqlQueryModel *model = new QSortFilterSqlQueryModel(this);
			#model->setQuery("SELECT u.id, u.name, c.name FROM users AS u LEFT JOIN cities AS c ON (u.city_id = c.id)");
			#model->setFilterColumn("u.name"); // will filter by user name
			#model->setFilterFlags(Qt::MatchStartsWith);
			#model->setFilter("Iv");
			#model->select();
			# DISPLAY THUNBNAILS
			self.displayThunbnails()
		else:
			print('caca')
			
		# Binds
		#self.treelstalb.selectRow().connect(self.onSelectList())
		#self.treelstalb.selectRow.connect(lambda: QTimer.singleShot(0, self.onSelectList))

		
		
	def addControls(self):
		self.labelsear = QLabel('Search')
		self.labelsear.setFixedWidth(80)
		self.txtsearch = QLineEdit()
		self.txtsearch.setFixedWidth(200)
		self.txtsearch.setObjectName("TextSearch")
		self.txtsearch.setText("")
		self.butnclear = QPushButton('✖')
		self.butnclear.setFixedWidth(20)
		self.butnsearc = QPushButton('➜')
		self.butnsearc.setFixedWidth(20)
		self.combostyl = QComboBox()
		self.combostyl.addItems([DISP_CJOKER])
		self.combostyl.setFixedWidth(80)
		self.combofami = QComboBox()
		self.combofami.addItems([DISP_CJOKER])
		self.combofami.setFixedWidth(80)
		self.combolabl = QComboBox()
		self.combolabl.addItems([DISP_CJOKER])
		self.combolabl.setFixedWidth(80)
		self.comboYear = QComboBox()
		self.comboYear.addItems([DISP_CJOKER])
		self.comboYear.setFixedWidth(80)
		self.butndispl = QPushButton('≠')
		self.butndispl.setFixedWidth(20)
		self.comboEnvt = QComboBox()
		self.comboEnvt.clear()
		self.comboEnvt.addItems(NAME_EVT)
		self.comboEnvt.setFixedWidth(160)
		#currentIndexChanged.connect(self.selectionchange)
		
		self.framethunb = QListWidget()
		self.framethunb.resize(self.frameGeometry().width(),HEIG_THUN*2)
		#self.framethunb.setMinimumSize(self.frameGeometry().width(),HEIG_THUN*2)
		self.framethunb.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.framethunb.sizeHintForColumn(HEIG_THUN)
		self.framethunb.sizeHintForRow(HEIG_THUN)
		#self.framethunb.setSelectionRectVisible(True)
		#self.framethunb.setResizeMode(QListWidget.Adjust)

		
		self.treelstalb = QTableView()
		self.treelstalb.setAlternatingRowColors(True)
		self.treelstalb.setShowGrid(True)
		self.treelstalb.setSortingEnabled(True)
		
		self.treelstalb.setStyleSheet("alternate-background-color: rgb(209, 209, 209)"
										"; background-color: rgb(244, 244, 244);")
		#self.treelstalb.resize(int(self.frameGeometry().width()/WIDT_PICM), 10)
		
		self.labelcover = QLabel()
		pixmap = QPixmap(PICM_NCO)
		self.labelcover.setPixmap(pixmap)
		self.labelcover.setScaledContents(True)
		self.labeltitle = QLabel('Title')
		self.treelsttrk = QTableView()
		self.treelsttrk.setAlternatingRowColors(True)
		self.treelsttrk.setShowGrid(True)
		self.treelsttrk.setSortingEnabled(True)
		self.treelsttrk.setSelectionBehavior(QAbstractItemView.SelectRows)
		
		# layout
		# bar commands
		controlHead = QHBoxLayout()
		controlHead.setAlignment(Qt.AlignTop)
		controlHead.addWidget(self.labelsear)
		controlHead.addWidget(self.txtsearch)
		controlHead.addWidget(self.butnclear)
		controlHead.addWidget(self.butnsearc)
		controlHead.addWidget(self.combostyl)
		controlHead.addWidget(self.combofami)
		controlHead.addWidget(self.combolabl)
		controlHead.addWidget(self.comboYear)
		controlEnvt = QHBoxLayout()
		controlEnvt.setAlignment(Qt.AlignRight)
		controlEnvt.addWidget(self.butndispl)
		controlEnvt.addWidget(self.comboEnvt)
		controlComm = QHBoxLayout()
		controlComm.addLayout(controlHead)
		controlComm.addLayout(controlEnvt)
		# thunbnails
		self.controlThun = QGridLayout(self.framethunb)
		# tab
		controlList = QHBoxLayout()
		controlList.setAlignment(Qt.AlignTop)
		controlList.addWidget(self.treelstalb)
		# cover + titre + list tracks
		controlCove = QHBoxLayout()
		controlCove.setAlignment(Qt.AlignTop)
		controlCove.addWidget(self.labelcover)
		controlTitl = QVBoxLayout()
		controlTitl.setAlignment(Qt.AlignTop)
		controlTitl.addWidget(self.labeltitle)
		controlTitl.addWidget(self.treelsttrk)
		controlAlbm = QHBoxLayout()
		controlAlbm.addLayout(controlCove)
		controlAlbm.addLayout(controlTitl)
		# global
		controlArea = QVBoxLayout()
		controlArea.setAlignment(Qt.AlignTop)
		controlArea.addLayout(controlComm)
		controlArea.addWidget(self.framethunb)
		controlArea.addLayout(controlList)
		controlArea.addLayout(controlAlbm)
		
		# link buttons to media
		#self.playBtn.clicked.connect(self.playHandler)
		#stopBtn.clicked.connect(self.stopHandler)
		#volumeDescBtn.clicked.connect(self.decreaseVolume)
		#volumeIncBtn.clicked.connect(self.increaseVolume)
		#prevBtn.clicked.connect(self.prevItemPlaylist)
		#nextBtn.clicked.connect(self.nextItemPlaylist)
		#infoBtn.clicked.connect(self.displaySongInfo)
		
		return controlArea
	
	def displayThunbnails(self, new=True, deb=0, fin=THUN_DIS):
		if new:
			# delete all labels thunbnails
			for labelt in self.labels:
				labelt.destroy()
			self.labels[:] = []
			#self.framethunb.canv.yview_moveto(0) ###########
		else:
			# delete 2 labels endof after add more
			self.labels[len(self.labels)-1].destroy()
			self.labels[len(self.labels)-2].destroy()
			self.labels = self.labels[:-2]
		#self.statusBar.open("Loading covers albums in progress...")
		
		numCov = self.modelstalb.rowCount()
		maxCol = int(self.frameGeometry().width()/WIDT_PICM)
		curRow = curCol = cptIte = 0
		for row in range(self.modelstalb.rowCount()):
			if cptIte >= deb and cptIte <= fin:
				curItem = int(self.modelstalb.data(self.modelstalb.index(row, A_POSITIO.index('ID_CD'))))
				index = self.modelstalb.index(row, A_POSITIO.index('Cover'))
				pathcover = self.modelstalb.data(index)
				index = self.modelstalb.index(row, A_POSITIO.index('Name'))
				albumname = self.modelstalb.data(index)
				# no cover or no display thunbnails covers (thnail_nod = 1)
				if THUN_NOD == 0 or pathcover == TEXT_NCO:
					if THUN_NOD == 0:pathcover = TEXT_NCO
					monimage = QPixmap(PICM_NCO)
				else:
					index = self.modelstalb.index(row, A_POSITIO.index('MD5'))
					Curalbmd5 = self.modelstalb.data(index)
					monimage = self.buildCover(pathcover, Curalbmd5, 'minicover')
				label = self.buildThunbnail(pathcover, albumname.replace(' - ','\n'), monimage, row)
				label.mousePressEvent = (lambda event:self.onSelectThunbnailChanged(event))
				label.mouseEnter = (lambda event,a=row: self.onSelectThunbnail(event,a))
				label.Name = curItem
				label.setStyleSheet("border: 2px solid white")
				#label.rightClicked.connect(lambda: print('clicked')) #self.popupthunbnailsalbum
				self.controlThun.addWidget(label, curRow+1, curCol+1)
				self.labels.append(label)
				#label.bind("<Enter>", lambda event: event.widget.setStyleSheet("border: 1px solid black"))
				#label.bind("<Leave>", lambda event: event.widget.setStyleSheet("border: 0px"))
				#self.statusBar.update((cptIte-deb)/disCov)
			# count thunbnails
			cptIte = cptIte + 1
			#print(type(self.labels))
			# position
			curCol = curCol + 1
			if curCol == maxCol:
				curCol = 0
				curRow = curRow + 1
			# max display, labels for more
			if cptIte==fin:
				# add for add more thunbnails
				monimage = QPixmap(THUN_DBA)
				label = self.buildThunbnail(THUN_DBA, "{n} covers display max \n Click for more +{f}...".format(n=str(fin),f=str(fin+fin) if (fin+fin)<(numCov-fin) else str(numCov-fin)), monimage, 'endof')
				self.controlThun.addWidget(label, curRow+1, curCol+1)
				#label.bind("<Button-1>", lambda e: self.displayThunbnails(False,fin,fin+fin))
				#label.bind("<Enter>", lambda event: event.widget.config(relief=SOLID))
				#label.bind("<Leave>", lambda event: event.widget.config(relief=FLAT))
				self.labels.append(label)
				# add for all thunbnails
				curCol = curCol + 1
				if curCol == maxCol:
					curCol = 0
					curRow = curRow + 1
				label = self.buildThunbnail(THUN_DBA, "{n} covers display max \n Click for all +{f}...".format(n=str(fin),f=str(numCov-fin)), monimage, 'endof')
				self.controlThun.addWidget(label, curRow+1, curCol+1)
				#label.bind("<Button-1>", lambda e: self.displayThunbnails(False,fin,numCov-fin+1))
				#label.bind("<Enter>", lambda event: event.widget.config(relief=SOLID))
				#label.bind("<Leave>", lambda event: event.widget.config(relief=FLAT))
				self.labels.append(label)
				break
		#self.statusBar.close()
		#print(str(cptIte)+'*covers')
	
	def buildThunbnail(self, pathcover, texte, monimage, curItem):
		# no cover, add blank
		if pathcover[0:len(TEXT_NCO)] == TEXT_NCO or pathcover==THUN_DBA: 
			# add text infos
			draw = ImageDraw.Draw(monimage)
			#w, h = draw.textsize(texte)
			w, h = WIDT_PICM, 30 
			if '\n' in texte:
				texte = texte.split('\n')
				texte = texte[0]+"\n"+texte[1]
			draw.rectangle(((4,(WIDT_PICM-h)/2),(WIDT_PICM-4,((WIDT_PICM-h)/2)+h)), fill=THUN_CO0)
			try:
				font = ImageFont.truetype(FONT_MAI.lower() + '.ttf', 12)
			except:
				font = ImageFont.truetype("FreeMono.ttf", 10)
			draw.text((6,((WIDT_PICM-h)/2)+4), texte, font=font, fill=THUN_CO1)
			photo = ImageTk.PhotoImage(monimage)
		label = QLabel()
		label.setPixmap(monimage)
		label.setScaledContents(True)
		
		return(label)
		
	def buildCover(con, pathcover, md5, namerequest='cover'):
		"""Get base64 picture cover."""
		if namerequest=='cover':
			request = "SELECT Cover64 FROM DBCOVERS WHERE MD5='{MD5}'"
		else:
			request = "SELECT MiniCover64 FROM DBCOVERS WHERE MD5='{MD5}'"
		if pathcover[0:len(TEXT_NCO)] == TEXT_NCO: 
			# no cover : blank
			monimage = QPixmap(PICT_NCO)
		else:
			# cover base64/mysql
			try:
				query = QSqlQuery()
				query.exec_(request.format(MD5=str(md5)))
				query.first()
				query.clear
				covermd5 = query.value(0)
				cover = b64decode(covermd5)
				monimage = QPixmap()
				monimage.loadFromData(cover)
			except:
				pass
				QMessageBox(TITL_PROG,' : err thunbnail read :'+pathcover)
				monimage = QPixmap(PICT_NCO)
		return (monimage)
	
	def onSelectThunbnailChanged(self, event):
		"""Display album infos."""
		print(self.controlThun.currentItem().text())
		print(self.controlThun.row(myListWidget.currentItem()))
		print(self.controlThun.checkState()) # if it is a checkable item
		print(self.controlThun.currentItem().toolTip().toString())
		print(self.controlThun.currentItem().whatsThis().toString())
		# select item
		#self.treelstalb.selectRow(row)
	
	def onSelectList(self, event=None):
		"""Display album infos + ."""
		currow = self.treelstalb.currentIndex().row()
		if self.treelstalb.currentIndex():
			print(currow)
			if self.modelstalb != None and self.treelstalb.currentIndex().row() > 0:
				if self.modelstalb.rowCount() > 1:
					self.CurentAlbum = int(self.modelstalb.data(self.modelstalb.index(currow, A_POSITIO.index('ID_CD'))))
					items = self.framethunb.findItems(self.CurentAlbum, Qt.MatchRegExp)
					for item in items:
						print (item)
					print(self.modelstalb.index(currow, A_POSITIO.index('ID_CD')))
					self.CurentAlbum = int(self.modelstalb.data(self.modelstalb.index(currow, A_POSITIO.index('ID_CD'))))
					for labelt in self.labels:
						if labelt.Name == self.CurentAlbum:
							labelt.setStyleSheet("border: 2px solid red")
						else:
							labelt.setStyleSheet("border: 2px solid white")

		
if __name__ == '__main__':
	app = QApplication(argv)
	DB = DBAlbumsMainGui()
	app.exec_()
