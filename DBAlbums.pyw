#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" DBAlbums History Version : Doubsman dev.
1.37 New player QT5 v2 (vol+playlist) + multiprocessing
1.36 Enlarge Display thunbnails + bugs closing
1.35 centralisation functions player/create sqlite3 / create exe via cx_freeze
1.34 link tree id <-> mysql id / Full Screen
1.33 mass update albums + autoincrement id + theme
1.32 import playlist foobar v2 + dynamic combos 
1.31 DBAlbums.ini
1.30 import playlist foobar
1.29 GetExist -> DBAlbums
1.28 fixed bugs + status bar
1.27 combos label/year + fast speed viewer artworks
1.26 viewer artworks
1.25 gestion import tkinter + stats loading
1.24 thunbnails + mousewheel + popup
1.23 thunbnails link treeview
1.22 thunbnails view
1.21 Tagscan + sdtout powershell
1.20 Artworks viewer
1.19 integration Powershell script
1.18 Execution Powershell script BUILD_INVENT.ps1 + BUILD_INVENT_UPDATEALBUM.ps1
1.17 base sqllite (create base + offline mode)
1.16 score album + track
1.15 player music pyQT5
1.14 stats + play music 
1.13 best performance mysql
1.12 fusion gui albmus/tracks windows
1.11 fixed bugs
1.10 refresh buttons + tdc loading
1.09 extract cover mysql/base64 to file
1.08 adaptation python 2.7 (py2exe) et 3.5.2
1.07 combos category/family
1.06 adaptation Ubuntu + base64
1.05 autocompletion
1.04 constantes
1.02 export csv
1.01 gestion covers
1.00 search base INVENT mysql TEST/PRODUCTION
"""

""" # python 3.6.0 installation modules
pip install pymysql
pip install pillow
pip install pyQT5
extract N:\_INVENT\DBAlbums\LIB\fpl_reader-master.zip
python.exe setup.py install
pip install cx_Freeze
"""
from sys import platform, stdout, argv, executable
from os import system, path, getcwd, name, remove, walk
from tkinter import (Tk, Toplevel, Label, Button, Checkbutton, Entry, Canvas, Grid, 
					Frame, Scale, Menu, Text, StringVar, IntVar, FALSE, TRUE, 
					RIDGE, SUNKEN, SOLID, FLAT, N, S, W, E, X, Y, RIGHT, LEFT, 
					BOTH, TOP, END, BOTTOM, VERTICAL, HORIZONTAL, INSERT, ALL)
from tkinter.filedialog import asksaveasfile
from tkinter.ttk import Treeview, Combobox, Scrollbar, Separator, Style
from tkinter.font import Font
from multiprocessing import Process
from subprocess import check_call, call, Popen, PIPE
from queue import Queue, Empty
from pymysql import connect as connectmysql
from sqlite3 import connect as connectsqlite3
from logging import DEBUG, basicConfig, info
from datetime import datetime
from time import sleep
from PIL import Image, ImageTk, ImageDraw, ImageFont
from csv import writer, QUOTE_ALL
from io import BytesIO
from base64 import b64decode, decodestring, b64encode
from hashlib import md5
from configparser import ConfigParser
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist, QMediaMetaData
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QSlider, 
							QLabel, QMainWindow, QStyle, QWidget, QAction, QMessageBox)
from fpl_reader import read_playlist # dev ext https://github.com/rr-/fpl_reader


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
LOGS_PROG = path.join(PATH_PROG, 'LOG')
BASE_SQLI = path.join(PATH_PROG, 'LOC', "Invent_{envt}.db")
PWSH_SCRI = path.join(PATH_PROG, 'PS1', "BUILD_INVENT_{mod}.ps1")
PWSH_SCRU = path.join(PATH_PROG, 'PS1', "UPDATEALBUMS.ps1")
FOOB_UPSC = path.join(PATH_PROG, 'SQL', "DBAlbums_FOOBAR_UPADTESCORE.sql")
MASKCOVER = ('.jpg','.jpeg','.png','.bmp','.tif','.bmp','.tiff')
# Read File DBAlbums.ini
FILE__INI = 'DBAlbums.ini'
readIni = ConfigParser()
readIni.read(FILE__INI)
# GUI
VERS_PROG = readIni.get('dbalbums', 'version')
TITL_PROG = "DBAlbums v{v} (2017)".format(v=VERS_PROG)
WIDT_MAIN = readIni.getint('dbalbums', 'gui_width')
HEIG_MAIN = readIni.getint('dbalbums', 'gui_height')
WIDT_PICM = readIni.getint('dbalbums', 'thunb_size')
DISP_CJOKER = readIni.get('dbalbums', 'text_joker')
TEXT_NCO = readIni.get('dbalbums', 'text_nocov')
WINS_ICO = readIni.get('dbalbums', 'wins_icone')
UNIX_ICO = readIni.get('dbalbums', 'unix_icone')
PICT_NCO = readIni.get('dbalbums', 'pict_blank')
PICM_NCO = readIni.get('dbalbums', 'picm_blank')
ENVT_DEF = readIni.get('dbalbums', 'envt_deflt')
TREE_CO0 = readIni.get('dbalbums', 'color0_lin')
TREE_CO1 = readIni.get('dbalbums', 'color1_lin')
TREE_CO2 = readIni.get('dbalbums', 'color2_lin')
TREE_CO3 = readIni.get('dbalbums', 'color3_lin')
THUN_CO0 = readIni.get('dbalbums', 'color0_thu')
THUN_CO1 = readIni.get('dbalbums', 'color1_thu')
THUN_SIZ = readIni.getint('dbalbums', 'thnail_siz')
THUN_DIS = readIni.getint('dbalbums', 'thnail_dis')
THUN_DBA = readIni.get('dbalbums', 'picm_endof')
COVE_SIZ = readIni.getint('dbalbums', 'covers_siz')
# PROG
TAGS_SCAN = r'' + readIni.get('programs', 'tagscan')
FOOB_PLAY = r'' + readIni.get('programs', 'foobarP')
EDIT_TEXT = r'' + readIni.get('programs', 'notepad')
# SCORE
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

#  columns position
A_POSITIO = {'Category'		: 0, 'Family'		: 1,
			'Name'			: 2, 'Label'		: 3,
			'ISRC'			: 4, 'Year'			: 5,
			'Length'		: 6, 'Qty_CD'		: 7,
			'Qty_Tracks'	: 8, 'Qty_covers'	: 9,
			'Score'			: 10, 'Size'		: 11,
			'Typ_Tag'		: 12,'Position'		: 13,
			'Date_Insert'	: 14,'Date_Modifs'	: 15,
			'Path'			: 16,'Cover'		: 17,
			'MD5'			: 18,'ID_CD' 		: 19}
T_POSITIO = {'ODR_Track'	: 0, 'TAG_Artists'	: 1, 
			 'TAG_Title'	: 2, 'TAG_length'	: 3, 
			 'Score'		: 4, 'TAG_Genres'	: 5, 
			 'FIL_Track'	: 6, 'REP_Track'	: 7, 
			 'ID_TRACK'		: 8}
#  treeview columns width
A_C_WIDTH = (60,60,250,100,80,40,50,30,30,30,30,30,30,67,67,200,200,200,200)
T_C_WIDTH = (50,150,200,60,30,70,200,200)

# REQUESTS
#  autocompletion VW_DBCOMPLETION
S_REQUEST = "SELECT Synthax FROM VW_DBCOMPLETLISTPUB ORDER BY Synthax"
#  list albums mysql DBALBUMS
A_REQUEST = "SELECT Category, Family, Name, Label, ISRC, `Year`, Length, Qty_CD AS `CD`, " \
			"Qty_Tracks AS Trks, Qty_covers AS Pic, Score As SCR, Size, Typ_Tag AS Tag, " \
			"Date_Insert AS `Add`, Date_Modifs AS `Modified`, " \
			"CONCAT(Position1,'\\\\',Position2) AS Position, " \
			"Path, Cover, `MD5`, ID_CD AS ID " \
			"FROM DBALBUMS ORDER BY Date_Insert DESC"
#  list albums sqllite DBALBUMS
Z_REQUEST = "SELECT Category, Family, Name, Label, ISRC, `Year`, Length, Qty_CD AS `CD`, " \
			"Qty_Tracks AS Trks, Qty_covers AS Pic, Score As SCR, Size, Typ_Tag AS Tag, " \
			"Date_Insert AS `Add`, Date_Modifs AS `Modified`, " \
			"Position1 || '\\' || Position2 AS Position, " \
			"Path, Cover, `MD5`, ID_CD AS ID " \
			"FROM DBALBUMS ORDER BY Date_Insert DESC"
#  list tracks mysql/sqllite
T_REQUEST = "SELECT ODR_Track AS `N°`, TAG_Artists AS Artist, TAG_Title AS Tittle, TAG_length AS Length, " \
			"Score As SCR, TAG_Genres AS `Style`, FIL_Track AS File, REP_Track AS Folder, ID_TRACK AS `ID`  " \
			"FROM DBTRACKS WHERE ID_CD={id} ORDER BY REP_Track, ODR_Track"
#  cover blob
C_REQUEST = "SELECT `MD5`, `Cover64` FROM DBCOVERS WHERE `MD5`='{MD5}'"
M_REQUEST = "SELECT `MD5`, `MiniCover64` FROM DBCOVERS WHERE `MD5`='{MD5}'"
#  search tracks
B_REQUEST = "SELECT ID_CD AS ID FROM DBTRACKS AS TRK WHERE TAG_Artists like '%{search}%' OR TAG_Title like '%{search}%' GROUP BY ID_CD"
#  Update Sore Album
U_REQUEST = "UPDATE DBALBUMS SET `Score`={score} WHERE `ID_CD`={id}"
#  Update Score Track
V_REQUEST = "UPDATE DBTRACKS SET `Score`={score} WHERE `ID_TRACK`={id}"
#  insert playlist foobar
F_REQUEST = "INSERT INTO DBFOOBAR (Playlist, Path, FIL_Track, Name , MD5, TAG_Album, TAG_Artists, TAG_Title) " \
			"VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"


###################################################################
# PLAYER PQT5 V2
class playerAudioAlbum(QMainWindow):
	def __init__(self, listemedia, position=1, x=0, y=0):
		super().__init__()
		
		#Init main windows
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.move(x, y)
		self.setFixedSize(400, 100)
		self.setWindowIcon(QIcon(WINS_ICO))
		
		#Init Player
		self.currentPlaylist = QMediaPlaylist()
		self.player = QMediaPlayer()
		self.userAction = -1			#0- stopped, 1- playing 2-paused
		self.player.stateChanged.connect(self.qmp_stateChanged)
		self.player.positionChanged.connect(self.qmp_positionChanged)
		self.player.volumeChanged.connect(self.qmp_volumeChanged)
		self.player.durationChanged.connect(self.qmp_durationChanged)
		self.player.setVolume(60)
		#Add Status bar
		self.statusBar().showMessage('No Media :: %d'%self.player.volume())
		
		#Init GUI
		centralWidget = QWidget()
		centralWidget.setLayout(self.addControls())
		self.setCentralWidget(centralWidget)
		self.show()
		
		#Add media
		self.listemedia = listemedia
		self.addMedialist()
		
		#Autoplay
		self.playHandler()
		self.currentPlaylist.setCurrentIndex(position-1)
		self.player.play()
	
	def addControls(self):
		controlArea = QVBoxLayout()
		seekSliderLayout = QHBoxLayout()
		controls = QHBoxLayout()
		
		#creating buttons
		self.playBtn = QPushButton()
		self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
		stopBtn = QPushButton()
		stopBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
		prevBtn = QPushButton()
		prevBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
		nextBtn = QPushButton()
		nextBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
		volumeDescBtn = QPushButton('-')
		volumeDescBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
		volumeIncBtn = QPushButton('+')
		volumeIncBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
		infoBtn = QPushButton('Tags...')
		infoBtn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
		
		#creating seek slider
		self.seekSlider = QSlider(Qt.Horizontal, self)
		self.seekSlider.setMinimum(0)
		self.seekSlider.setMaximum(100)
		self.seekSlider.setTracking(False)
		self.seekSlider.sliderMoved.connect(self.seekPosition)
		
		self.seekSliderLabel1 = QLabel('00:00')
		self.seekSliderLabel2 = QLabel('00:00')
		seekSliderLayout.addWidget(self.seekSliderLabel1)
		seekSliderLayout.addWidget(self.seekSlider)
		seekSliderLayout.addWidget(self.seekSliderLabel2)
		
		#Add link buttons media
		self.playBtn.clicked.connect(self.playHandler)
		stopBtn.clicked.connect(self.stopHandler)
		volumeDescBtn.clicked.connect(self.decreaseVolume)
		volumeIncBtn.clicked.connect(self.increaseVolume)
		prevBtn.clicked.connect(self.prevItemPlaylist)
		nextBtn.clicked.connect(self.nextItemPlaylist)
		infoBtn.clicked.connect(self.displaySongInfo)
		
		#Adding to the horizontal layout
		controls.addWidget(prevBtn)
		controls.addWidget(self.playBtn)
		controls.addWidget(stopBtn)
		controls.addWidget(nextBtn)
		
		controls.addWidget(volumeDescBtn)
		controls.addWidget(volumeIncBtn)
		controls.addWidget(infoBtn)
		
		#Adding to the vertical layout
		controlArea.addLayout(seekSliderLayout)
		controlArea.addLayout(controls)
		return controlArea
	
	def playHandler(self):
		if self.player.state() == QMediaPlayer.PlayingState:
			self.userAction = 2
			self.statusBar().showMessage('Paused %s at position %s at Volume %d'%\
						(self.player.metaData(QMediaMetaData.Title),\
						self.seekSliderLabel1.text(),\
						self.player.volume()))
			self.player.pause()
		else:
			self.userAction = 1
			self.statusBar().showMessage('Playing at Volume %d'%self.player.volume())
			if self.player.state() == QMediaPlayer.StoppedState :
				if self.player.mediaStatus() == QMediaPlayer.NoMedia:
					if self.currentPlaylist.mediaCount() != 0:
						self.player.setPlaylist(self.currentPlaylist)
				elif self.player.mediaStatus() == QMediaPlayer.LoadedMedia:
					self.player.play()
				elif self.player.mediaStatus() == QMediaPlayer.BufferedMedia:
					self.player.play()
			elif self.player.state() == QMediaPlayer.PlayingState:
				pass
			elif self.player.state() == QMediaPlayer.PausedState:
				self.player.play()
			
	def stopHandler(self):
		self.userAction = 0
		self.statusBar().showMessage('Stopped at Volume %d'%(self.player.volume()))
		if self.player.state() == QMediaPlayer.PlayingState:
			self.stopState = True
			self.player.stop()
		elif self.player.state() == QMediaPlayer.PausedState:
			self.player.stop()
		elif self.player.state() == QMediaPlayer.StoppedState:
			pass
		
	def qmp_stateChanged(self):
		if self.player.state() == QMediaPlayer.StoppedState:
			self.player.stop()
		#buttons icon play/pause change
		if self.player.state() == QMediaPlayer.PlayingState:
			self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
		else:
			self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
	
	def qmp_positionChanged(self, position):
		#update position slider
		self.seekSlider.setValue(position)
		#update the text label
		self.seekSliderLabel1.setText('%d:%02d'%(int(position/60000),int((position/1000)%60)))
	
	def seekPosition(self, position):
		sender = self.sender()
		if isinstance(sender,QSlider):
			if self.player.isSeekable():
				self.player.setPosition(position)
	
	def qmp_volumeChanged(self):
		msg = self.statusBar().currentMessage()
		msg = msg[:-2] + str(self.player.volume())
		self.statusBar().showMessage(msg)
	
	def qmp_durationChanged(self, duration):
		self.seekSlider.setRange(0,duration)
		self.seekSliderLabel2.setText('%d:%02d'%(int(duration/60000),int((duration/1000)%60)))
		nummedia = self.currentPlaylist.mediaCount()
		curmedia = self.currentPlaylist.currentIndex()+1
		#artist = self.player.metaData(QMediaMetaData.Author)
		#tittle = self.player.metaData(QMediaMetaData.Title)
		namemedia = path.basename(self.listemedia[self.currentPlaylist.currentIndex()])
		self.setWindowTitle('[%02d/%02d'%(curmedia,nummedia)+'] '+namemedia)
	
	def increaseVolume(self):
		vol = self.player.volume()
		vol = min(vol+5,100)
		self.player.setVolume(vol)
	
	def decreaseVolume(self):
		vol = self.player.volume()
		vol = max(vol-5,0)
		self.player.setVolume(vol)
	
	def addMedialist(self):
		for media in self.listemedia:
			self.currentPlaylist.addMedia(QMediaContent(QUrl.fromLocalFile(media)))
	
	def displaySongInfo(self):
		#extract datas
		metaDataKeyList = self.player.availableMetaData()
		fullText = '<table class="tftable" border="0">'
		for key in metaDataKeyList:
			value = str(self.player.metaData(key)).replace("'","").replace("[","").replace("]","")
			fullText = fullText + '<tr><td>' + key + '</td><td>' + value + '</td></tr>'
		fullText = fullText + '</table>'
		#Box
		infoBox = QMessageBox(self)
		infoBox.setWindowTitle('Detailed Song Information')
		infoBox.setTextFormat(Qt.RichText)
		infoBox.setText(fullText)
		infoBox.addButton('OK',QMessageBox.AcceptRole)
		infoBox.show()
	
	def prevItemPlaylist(self):
		self.player.playlist().previous()
		if self.currentPlaylist.currentIndex()==-1:
			self.player.playlist().previous()
	
	def nextItemPlaylist(self):
		self.player.playlist().next()
		if self.currentPlaylist.currentIndex()==-1:
			self.player.playlist().next()
	
def playerProcessAudio(listmedia, position, x=0, y=0):
	app = QApplication(argv)
	app.setStyleSheet('QMainWindow{background-color: darkgray;border: 1px solid black;}')
	player = playerAudioAlbum(listmedia, position, x, y)
	app.exec_()

###################################################################
# FUNCTIONS
def CenterWindows(win):
	"""centers a tkinter window
	:param win: the root or Toplevel window to center."""
	win.update_idletasks()
	width = win.winfo_width()
	frm_width = win.winfo_rootx() - win.winfo_x()
	win_width = width + 2 * frm_width
	height = win.winfo_height()
	titlebar_height = win.winfo_rooty() - win.winfo_y()
	win_height = height + titlebar_height + frm_width
	x = win.winfo_screenwidth() // 2 - win_width // 2
	y = win.winfo_screenheight() // 2 - win_height // 2
	win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
	win.deiconify()

def ConnectInvent(envt):
	"""Connect base MySQL/Sqlite."""
	con = None
	# ENVT
	readIni = ConfigParser()
	readIni.read(FILE__INI)
	BASE_SEV = readIni.get(envt, 'serv')
	BASE_USR = readIni.get(envt, 'user')
	BASE_PAS = readIni.get(envt, 'pass')
	BASE_NAM = readIni.get(envt, 'base')
	try:
		# MYSQL
		MODE_SQLI = False
		con = connectmysql( host=BASE_SEV, 
							user=BASE_USR, 
							passwd=BASE_PAS, 
							db=BASE_NAM,
							charset='utf8',
							use_unicode=True)
		#con.autocommit(True)
	except Exception:
		pass
		# SQLite: offline
		print("SQLLite: mode offline")
		MODE_SQLI = True
		con = connectsqlite3(BASE_SQLI.format(envt=envt))
	
	return con, MODE_SQLI

def CopyDatabaseInvent(conMySQL, BaseNameSQLite, BarGauge, logname):
	basicConfig(filename=logname,
							filemode='a',
							format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
							datefmt='%H:%M:%S',
							level=DEBUG)
	info ('Create/Update Database '+BaseNameSQLite)
	BarGauge.open()
	con = connectsqlite3(BaseNameSQLite)
	NAME_TABL = "DBALBUMS"
	BarGauge.update(0.05)
	BarGauge.settitle('Create Table '+NAME_TABL+' in progress...')
	info ('Create '+NAME_TABL)
	Tabs =  BuildTabFromRequest(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()    
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE DBALBUMS(ID_CD INTEGER PRIMARY KEY AUTOINCREMENT, MD5 TEXT, Family TEXT, Category TEXT, Position1 TEXT, Position2 TEXT, Name TEXT, Label TEXT, ISRC TEXT, Year TEXT, Qty_CD INT,Qty_Cue INT,Qty_CueERR INT, Qty_repMusic INT, Qty_Tracks INT, Qty_audio INT, Typ_Audio TEXT, Qty_repCover, Qty_covers, Cover TEXT, Path TEXT, Size INT, Duration TEXT, Length TEXT, Typ_Tag TEXT, Date_Insert DATETIME, Date_Modifs DATETIME, RHDD_Modifs DATETIME, Score INT, Statut TEXT)")
		cur.executemany("INSERT INTO DBALBUMS VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", Tabs)
		cur.execute("CREATE INDEX DBALBUMS_ndx_Date_Insert ON DBALBUMS(Date_Insert)")
		con.commit() 
	
	NAME_TABL = "DBTRACKS"
	BarGauge.update(0.25)
	BarGauge.settitle('Create Table '+NAME_TABL+' in progress...')
	info ('Create '+NAME_TABL)
	Tabs =  BuildTabFromRequest(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()    
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE DBTRACKS(ID_CD INT,ID_TRACK INTEGER PRIMARY KEY AUTOINCREMENT, Family TEXT, Category TEXT, Position1 TEXT, Position2 TEXT, REP_Album TEXT, REP_Track TEXT,FIL_Track TEXT,TAG_Exten TEXT,TAG_Album TEXT, TAG_Albumartists TEXT, TAG_Year TEXT,TAG_Disc INT, TAG_Track INT,ODR_Track TEXT, TAG_Artists TEXT,TAG_Title TEXT,TAG_Genres TEXT,TAG_Duration TEXT,TAG_length TEXT,Score INT,Date_Insert DATETIME, Statut TEXT, FOREIGN KEY(ID_CD) REFERENCES DBALBUMS(ID_CD))")
		cur.executemany("INSERT INTO DBTRACKS VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", Tabs)
		cur.execute("CREATE INDEX DBTRACKS_ndx_idcd ON DBTRACKS(ID_CD)")
	con.commit() 
	
	NAME_TABL = "DBFOOBAR"
	BarGauge.update(0.5)
	BarGauge.settitle('Create Table '+NAME_TABL+' in progress...')
	info ('Create '+NAME_TABL)
	Tabs =  BuildTabFromRequest(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE {t}(ID_FOO INTEGER PRIMARY KEY AUTOINCREMENT, MD5 TEXT, Name TEXT, Path TEXT, FIL_Track TEXT, Playlist TEXT, TAG_Album TEXT, TAG_Artists TEXT, TAG_Title TEXT, Date_insert TIMESTAMP DEFAULT CURRENT_TIMESTAMP)".format(t=NAME_TABL))
		cur.executemany("INSERT INTO {t} VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(t=NAME_TABL), Tabs)
		cur.execute("CREATE INDEX DBFOOBAR_ndx_FIL_Track ON DBFOOBAR(FIL_Track)")
	con.commit() 
	
	NAME_TABL = "DBFOOBOR"
	BarGauge.update(0.6)
	BarGauge.settitle('Create Table '+NAME_TABL+' in progress...')
	info ('Create '+NAME_TABL)
	Tabs =  BuildTabFromRequest(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE {t}(FIL_Track TEXT, FIL_TrackM TEXT)".format(t=NAME_TABL))
		cur.executemany("INSERT INTO {t} VALUES(?, ?)".format(t=NAME_TABL), Tabs)
	con.commit() 
	
	NAME_TABL = "DBCOVERS"
	BarGauge.update(0.75)
	BarGauge.settitle('Create Table '+NAME_TABL+' in progress...')
	info ('Create '+NAME_TABL)
	Tabs =  BuildTabFromRequest(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE {t}(MD5 TEXT, Cover64 BLOB, MiniCover64 BLOB)".format(t=NAME_TABL))
		cur.executemany("INSERT INTO {t} VALUES(?, ?, ?)".format(t=NAME_TABL), Tabs)
		cur.execute("CREATE UNIQUE INDEX DBCOVERS_ndx_md5 ON DBCOVERS(MD5)")
	con.commit() 
	
	NAME_TABL = "VW_DBCOMPLETLISTPUB"
	BarGauge.update(0.9)
	BarGauge.settitle('Create Table '+NAME_TABL+' in progress...')
	info ('Create '+NAME_TABL)
	Tabs =  BuildTabFromRequest(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE {t}(Synthax TEXT)".format(t=NAME_TABL))
		cur.executemany("INSERT INTO {t} VALUES(?)".format(t=NAME_TABL), Tabs)
	con.commit() 
	
	BarGauge.update(1)
	BarGauge.settitle('Create DataBase Completed: '+BaseNameSQLite)
	info("test")
	with con:
		cur = con.cursor()    
		cur.execute("SELECT * FROM VW_DBCOMPLETLISTPUB;")
	con.commit()
	row = cur.fetchall()
	info (row[0])
	
	con.close()
	BarGauge.close()

def GetListColumns(con, req, rowid):
	"""List columns from request MySQL/Sqlite."""
	req = req + " LIMIT 0"
	cur = con.cursor()
	cur.execute(req)
	col_names = list(map(lambda x: x[0], cur.description))
	cur.close()
	# no id key in list columns ?
	if rowid != None: col_names.remove(rowid)
	return col_names

def UpdateBaseScore(con, score, id, req):
	"""Maj Mysql table Albums."""
	req = req.format(score=score, id=id)
	with con.cursor() as curs:
		curs.execute(req)
	curs.close()
	con.commit()

def BuildTabFromRequest(con, req):
	"""Select Mysql/Sqlite to memory list."""
	cur = con.cursor()    
	cur.execute(req)
	rows = cur.fetchall()
	cur.close()
	return rows

def BuildDictFromRequest(con, req):
	"""Select Mysql to memory object dict."""
	with con.cursor() as curs:
		curs.execute(req)
	col_names = [desc[0] for desc in curs.description]
	while True:
		row = curs.fetchone()
		if row is None:
			break
		row_dict = dict(zip(col_names, row))
		yield row_dict

def BuildReqTCD(con, group, column, tableName, TDCName="TDC", TDCSum="1", LineSum=False):
	"""Pivot table Mysql/SQLite."""
	# Collections
	req = """SELECT `{column}` FROM {tableName} GROUP BY `{column}`;""".format(tableName=tableName,column=column)
	col_names = BuildTabFromRequest(con, req)
	# sum/collections
	ReqTDC = """SELECT * FROM (SELECT `{group}` AS '{TDCName}',""".format(group=group,TDCName=TDCName)
	for col_name in col_names:
		ReqTDC += """SUM(CASE WHEN `{column}` = '{col_name}' THEN {TDCSum} ELSE 0 END) AS `{col_name}`,""".format(column=column,TDCSum=TDCSum,col_name=col_name[0])
	ReqTDC += """SUM({TDCSum}) AS `Total` FROM {tableName} GROUP BY `{group}` ORDER BY `{group}` DESC) ALB""".format(tableName=tableName,TDCSum=TDCSum,group=group)
	# sum
	if LineSum:
		ReqTDC += """ UNION SELECT 'TOTAL',"""
		for col_name in col_names:
			ReqTDC += """SUM(CASE WHEN {column} = '{col_name}' THEN {TDCSum} ELSE 0 END),""".format(column=column,TDCSum=TDCSum,col_name=col_name[0])
		ReqTDC += """SUM({TDCSum}) FROM {tableName}""".format(tableName=tableName,TDCSum=TDCSum)
	#ReqTDC += """ ORDER BY TOTAL"""
	return ReqTDC

def execSqlFile(con, bar, sql_file, nbop):
	"""Exec script SQL file..."""
	cur = con.cursor()
	statement = ""
	counter = 0
	bar.open()
	for line in open(sql_file):
		if line[0:2] == '--':
			if line[0:3] == '-- ':
				bar.settitle("Exec :"+line.replace('--' ,''))
			continue
		statement = statement + line
		if len(line)>2 and line[-2] == ';':
			counter = counter +1
			try:
				cur.execute(statement)
				con.commit()
			except (OperationalError, ProgrammingError) as e:
				print ("\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args)))
			bar.update(counter/nbop)
			statement = ""
	bar.close()
	cur.close()

def BuildTree(con, frame, req, colWidth, line, rowid=None, scroll=False, align=W):
	"""Build Columns treeview."""
	col_names = GetListColumns(con, req, rowid)
	tree = Treeview(frame, height=line, columns=col_names, show="headings")
	tree["columns"] = col_names
	counter = 0
	for col_name in col_names:
		tree.heading(col_name, text=col_name.title(),command=lambda c=col_name: TreeviewSortColumn(tree, c, False))
		tree.column(col_name,width=colWidth[counter], anchor=align)
		counter += 1
	tree.tag_configure('0', background=TREE_CO0)
	tree.tag_configure('1', background=TREE_CO1)
	tree.tag_configure('2', background=TREE_CO2)
	tree.tag_configure('3', background=TREE_CO3)
	if scroll:
		ysb = Scrollbar(frame, orient=VERTICAL)
		ysb.pack(side=RIGHT, fill=Y)
		ysb.config(command=tree.yview)
		xsb = Scrollbar(frame, orient=HORIZONTAL)
		xsb.pack(side=BOTTOM, fill=X)
		xsb.config(command=tree.xview)
		tree.configure(yscrollcommand=ysb.set,xscrollcommand=xsb.set)
	return (tree)

def TreeviewSortColumn(tv, col, reverse):
	"""sort column treeview."""
	l = [(tv.set(k, col), k) for k in tv.get_children('')]
	l.sort(reverse=reverse)
	# rearrange items in sorted positions
	for index, (val, k) in enumerate(l):
		tv.move(k, '', index)
	# reverse sort next time
	tv.heading(col, command=lambda	c=col: TreeviewSortColumn(tv, c, not reverse))

def BuildListFromRequest(con, req, joker=''):
	"""" fill combo tkinter."""
	TLabs = BuildTabFromRequest(con, req)
	TMods = []
	TMods.append(joker)
	for row in TLabs:
		TMods.append(''.join(map(str,row)))
		#TMods.insert(0,row[0])
	return (TMods)

def DisplayCounters(num = 0, text = '' ):
	"""format 0 000 + plural."""
	strtxt = " %s%s" % (text, "s"[num==1:])
	if num > 9999:
		strnum = '{0:,}'.format(num).replace(",", " ")
	else:
		strnum = str(num)
	return (strnum + strtxt)

def DisplayStars(star, scorelist):
	"""scoring."""
	max = len(scorelist)-1
	txt_score =  scorelist[star]
	return (txt_score+'  '+star*'★'+(max-star)*'☆')

def AlbumNameExtract(name, label, isrc, nbcd):
	"""buil label name & album name."""
	infoslabel = ""
	if label!="":
		infoslabel = label + ' • '
	if isrc!="":
		infoslabel += isrc + ' • '
	if '[' in name:
		infosalbum = name[name.find('[')+1:name.find(']')]
		albumnamet = name.replace('['+infosalbum+']','')
		infoslabel += infosalbum.replace('-',' • ')
	else:
		albumnamet = name
	albumnamet = albumnamet.replace('('+nbcd+'CD)','').replace(nbcd+'CD','')
	return (albumnamet, infoslabel)

def BuildIco(Gui):
	"""Icon windows or linux/mac."""
	if "nt" == name:
		#windows
		Gui.iconbitmap(WINS_ICO)
	else:
		#linux : os mac non prévu
		myico = ImageTk.PhotoImage(file=UNIX_ICO)
		Gui.tk.call('wm', 'iconphoto', Gui._w, myico)

def BuildCover(con, pathcover, md5):
	"""Get base64 picture cover mysql/sqlite."""
	if pathcover[0:len(TEXT_NCO)] == TEXT_NCO: 
		# no cover
		monimage = Image.open(PICT_NCO)
	else:
		# cover base64/mysql
		req = C_REQUEST.format(MD5=md5)
		Tableau = BuildTabFromRequest(con, req)
		if len(Tableau) == 0 or Tableau[0][1]== None:
			monimage = Image.open(PICM_NCO)
			print('err '+pathcover) #############
		else:
			monimage = Image.open(BytesIO(b64decode(Tableau[0][1])))
	return (monimage)

def BuildMiniCover(con, pathcover, md5):
	"""Get base64 picture cover mysql/sqlite."""
	if pathcover[0:len(TEXT_NCO)] == TEXT_NCO: 
		# no cover
		monimage = Image.open(PICM_NCO)
	else:
		# cover base64/mysql
		req = M_REQUEST.format(MD5=md5)
		Tableau = BuildTabFromRequest(con, req)
		if len(Tableau) == 0 or Tableau[0][1]== None:
			monimage = Image.open(PICM_NCO)
			print('err '+pathcover) #############
		else:
			monimage = Image.open(BytesIO(b64decode(Tableau[0][1])))
	return (monimage)

def BuildFileCover(con, namefile, pathcover, md5):
	"""Build cover base64/mysql to file."""
	#no cover
	if pathcover[0:len(TEXT_NCO)] != TEXT_NCO: 
		#mysql
		req = C_REQUEST.format(MD5=md5)
		Tableau = BuildTabFromRequest(con, req)
		extension = path.splitext(pathcover)[1][1:]
		filecover = namefile+'.'+extension
		cover = open(filecover, "wb")
		content = decodestring(Tableau[0][1])
		cover.write(content)
		cover.close()

def GetListFiles(folder, masks):
	"""Build files list."""
	for folderName, subfolders, filenames in walk(folder):
		if subfolders:
			for subfolder in subfolders:
				GetListFiles(subfolder, masks)
		for filename in filenames:
			for xmask in masks:
				if filename[-4:] in xmask:
					yield path.join(folderName,filename)

def GetFile(folder, file_name):
	"""open file playlist foobar 2000."""
	with open(path.join(folder, file_name), 'rb') as handle:
		return handle.read()

def foobarBuildTracksList(folder):
	"""build list of playlists foobar 2000."""
	trackslist = []
	playfiles = list(GetListFiles(folder,(".fpl",)))
	for playfile in playfiles:
		print(playfile)
		trackslist += foobarGetListfilesFromPlaylist(playfile)
	return(trackslist)

def foobarGetListfilesFromPlaylist(file_path):
	folder = path.dirname(file_path)
	file_name = path.basename(file_path)
	playlistcontent = read_playlist(GetFile(folder, file_name))
	listfiles = []
	for lfile in playlistcontent.tracks:
		playlist = file_path
		audiofil = str(lfile.file_name[7:], 'utf-8')
		albumnam = audiofil.split('\\')[-2]
		albummd5 = md5(albumnam.encode('utf-8')).hexdigest()
		TAG_Album = ''
		TAG_Artists = ''
		TAG_Title = ''
		try:
			TAG_Album = lfile.primary_keys[b"album"]
			TAG_Artists = lfile.primary_keys[b"artist"]
			TAG_Title = lfile.primary_keys[b"title"]
		except:
			pass
		# add list Playlist, Path, FIL_Track, Name , MD5, TAGartist, TABalbum, TAGtitle
		listfiles.append((path.basename(playlist), path.dirname(audiofil), path.basename(audiofil) , albumnam, albummd5, TAG_Album, TAG_Artists, TAG_Title)) 
	return(listfiles)

def foobarMajDBFOOBAR(con, bar, folder):
	# fill DBFOOBAR
	footracks = foobarBuildTracksList(folder)
	numtracks = len(footracks)
	counter = 0
	bar.open()
	bar.settitle('import playlists ('+str(numtracks)+' Tracks) Foobar in progress...')
	for footrack in footracks:
		with con.cursor() as curs:
			curs.execute(F_REQUEST, footrack)
			curs.close()
		con.commit()
		counter = counter +1
		bar.update(counter/numtracks)
	bar.settitle('importation playlist Foobar 2000 terminated')
	bar.close()
	return(numtracks)

def OpenComand(progra, params):
	"""Execute une commande system."""
	command = """{tprogra} "{tparams}" """.format(tprogra=progra,tparams=params)
	system(command)

def RunProgExecWin(prog, *argv):
	"""Execut a program no wait, no link."""
	Command = [prog]
	for arg in argv:
		Command += (arg,)
	Popen(Command, close_fds=True)

# opening-a-folder-in-explorer-nautilus-mac-thingie
if platform == 'darwin':
	def openFolder(path):
		check_call(['open', '--', path])
elif platform == 'linux2':
	def openFolder(path):
		check_call(['xdg-open', '--', path])
elif platform == 'win32':
	def openFolder(path):
		OpenComand('explorer', path)

def BuildCommandPowershell(script, *argv):
	Command = [r'powershell.exe',
				'-ExecutionPolicy', 'RemoteSigned',
				'-WindowStyle','Hidden',
				'-File', 
				script]
	for arg in argv:
		Command += (arg,)
	return Command

def getFileNameWithoutExtension(path):
	return path.split('\\').pop().split('/').pop().rsplit('.', 1)[0]

# auto-completion
tk_umlauts=['odiaeresis', 'adiaeresis', 'udiaeresis', 'Odiaeresis', 'Adiaeresis', 'Udiaeresis', 'ssharp']
class AutocompleteEntry(Entry):
	"""
	Subclass of tkinter.Entry that features autocompletion.
	To enable autocompletion use set_completion_list(list) to define
	a list of possible strings to hit.
	To cycle through hits use down and up arrow keys.
	"""
	def set_completion_list(self, completion_list):
		self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
		self._hits = []
		self._hit_index = 0
		self.position = 0
		self.bind('<KeyRelease>', self.handle_keyrelease)

	def autocomplete(self, delta=0):
		"""autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits"""
		if delta: # need to delete selection otherwise we would fix the current position
				self.delete(self.position, END)
		else: # set position to end so selection starts where textentry ended
				self.position = len(self.get())
		# collect hits
		_hits = []
		for element in self._completion_list:
				if element.lower().startswith(self.get().lower()):	# Match case-insensitively
						_hits.append(element)
		# if we have a new hit list, keep this in mind
		if _hits != self._hits:
				self._hit_index = 0
				self._hits=_hits
		# only allow cycling if we are in a known hit list
		if _hits == self._hits and self._hits:
				self._hit_index = (self._hit_index + delta) % len(self._hits)
		# now finally perform the auto completion
		if self._hits:
				self.delete(0,END)
				self.insert(0,self._hits[self._hit_index])
				self.select_range(self.position,END)

	def handle_keyrelease(self, event):
		"""event handler for the keyrelease event on this widget"""
		if event.keysym == "BackSpace":
				self.delete(self.index(INSERT), END)
				self.position = self.index(END)
		if event.keysym == "Left":
				if self.position < self.index(END): # delete the selection
						self.delete(self.position, END)
				else:
						self.position = self.position-1 # delete one character
						self.delete(self.position, END)
		if event.keysym == "Right":
				self.position = self.index(END) # go to end (no selection)
		if event.keysym == "Down":
				self.autocomplete(1) # cycle to next hit
		if event.keysym == "Up":
				self.autocomplete(-1) # cycle to previous hit
		if len(event.keysym) == 1 or event.keysym in tk_umlauts:
				self.autocomplete()

class VerticalScrolledFrame(Frame):
	"""A pure Tkinter scrollable frame that actually works!
	* Use the 'interior' attribute to place widgets inside the scrollable frame
	* Construct and pack/place/grid normally
	* This frame only allows vertical scrolling
	"""
	def __init__(self, parent, canv_w , canv_h , *args, **kwargs):
		super().__init__(parent, *args, **kwargs)
		
		self.parent = parent
		# create a canvas object and a vertical scrollbar 
		self.yscrlbr = Scrollbar(self)
		self.yscrlbr.pack(fill=Y, side=RIGHT, expand=FALSE)
		self.canv = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=self.yscrlbr.set, width = canv_w, heigh = canv_h)
		self.canv.pack(side=LEFT, fill=BOTH, expand=TRUE)
		self.yscrlbr.config(command = self.canv.yview)
		
		# reset the view
		self.canv.xview_moveto(0)
		self.canv.yview_moveto(0)
		
		# creating a frame to inserto to canvas
		self.interior = Frame(self.canv, width = canv_w, heigh = canv_h)
		self.canv.create_window(0, 0, window = self.interior, anchor=N+W)
		self.interior.bind('<Configure>', self._configure_window)  
		self.interior.bind('<Enter>', self._bound_to_mousewheel)
		self.interior.bind('<Leave>', self._unbound_to_mousewheel)

	def _bound_to_mousewheel(self, event):
		self.canv.bind_all("<MouseWheel>", self._on_mousewheel)

	def _unbound_to_mousewheel(self, event):
		self.canv.unbind_all("<MouseWheel>") 

	def _on_mousewheel(self, event):
		self.canv.yview_scroll(int(-1*(event.delta/120)), "units")

	def _configure_window(self, event):
		# update the scrollbars to match the size of the inner frame
		size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
		self.canv.config(scrollregion='0 0 %s %s' % size)
		if self.interior.winfo_reqwidth() != self.canv.winfo_width():
			# update the canvas's width to fit the inner frame
			self.canv.config(width = self.interior.winfo_reqwidth())
		#if self.interior.winfo_reqheight() != self.canv.winfo_height():
			# update the canvas's width to fit the inner frame
			#self.canv.config(height = self.interior.winfo_reqheight())

class ProgressBar():
	"""progress bar tkinter."""
	def __init__(self, width=400, height=30):
		self.__root = Tk()
		self.__root.geometry("{w}x{h}".format(w=width+5,h=height+5))
		self.__root.resizable(False, False)
		self.__root.attributes('-topmost', True)
		self.__root.attributes("-toolwindow", 1)
		self.__root.protocol('WM_DELETE_WINDOW', self.hide)
		self.__root.title('Wait please...')
		BuildIco(self.__root)
		CenterWindows(self.__root)
		self.__canvas = Canvas(self.__root, width=width, height=height)
		self.__canvas.grid()
		self.__width = width
		self.__height = height
		
	def hide(self):
		self.__root.withdraw()
		
	def settitle(self, title):
		self.__root.title(title)
	
	def open(self):
		self.__root.deiconify()
		self.__root.focus_set()
	
	def close(self):
		self.__root.withdraw()
	
	def update(self, ratio):
		self.__canvas.delete(ALL)
		self.__canvas.create_rectangle(0, 0, self.__width , self.__height)
		self.__canvas.create_rectangle(0, 0, self.__width * ratio, self.__height, fill=THUN_CO0)
		self.__root.update()
		self.__root.focus_set()


###################################################################
# LOADING GUI
class LoadingGui():
	"""Fenetre loading."""
	def __init__(self , MyTopLevel, con, MODE_SQLI, sleeptime=0, w=400, h=200):
		self.MyTopLevel = MyTopLevel
		self.MyTopLevel.geometry("{w}x{h}".format(w=w,h=h))
		self.MyTopLevel.attributes('-topmost', True)
		BuildIco(self.MyTopLevel)
		self.MyTopLevel.title("Loading Datas")
		self.MyTopLevel.resizable(width=False, height=False)
		self.MyTopLevel.overrideredirect(True)
		self.MyTopLevel.bind("<F1>", self.HideLoadingGui)
		self.MyTopLevel.bind("<Escape>", self.HideLoadingGui)
		self.MyTopLevel.bind("<Button-1>", self.HideLoadingGui)
		# logo + message
		customFont = Font(family="Calibri", size=14)
		cadretittle = Frame(self.MyTopLevel, width=380, height=100)
		cadretittle.pack(fill=BOTH)
		monimage = Image.open(UNIX_ICO)
		monimage = monimage.resize((100, 100), Image.ANTIALIAS)
		photo = ImageTk.PhotoImage(monimage)
		prj_label = Label(cadretittle, image = photo)
		prj_label.image = photo
		prj_label.pack(side=LEFT, padx=10, pady=10)
		if MODE_SQLI:
			txt_message = "SQLite Base (mode offline)"
		else:
			txt_message = "Mysql Base"
		message = StringVar()
		message.set(TITL_PROG+"\nConnected "+txt_message+'.'*sleeptime)
		mes_label = Label(cadretittle, textvariable=message, font=customFont)
		mes_label.pack(side=LEFT, padx=5, pady=5)
		# 2*tabs stats
		self.con = con
		self.w = w
		self.h = h
		self.cadrestats = Frame(self.MyTopLevel)
		self.cadrestats.pack(fill=BOTH)
		req = BuildReqTCD(con, "Category" , "Family", "DBALBUMS", "ALBUMS", "1", True)
		self.treestat1 = self.BuildTreeStats(req)
		self.treestat1.bind("<Button-3>", self.ChangeTree1)
		self.treestat1.pack(side=TOP, anchor=W, fill=BOTH, padx=5, pady=5)
		req = BuildReqTCD(con, "Category" , "Family", "DBALBUMS", "SIZE (GO)", "ROUND(`Size`/1024,1)", True)
		self.treestat2 = self.BuildTreeStats(req)
		self.treestat2.bind("<Button-3>", self.ChangeTree2)
		req = BuildReqTCD(con, "Year" , "Category", "DBALBUMS", "YEARS", "1", True)
		self.treestat3 = self.BuildTreeStats(req, 30)
		self.treestat3.bind("<Button-3>", self.ChangeTree3)
		self.ysb = Scrollbar(self.cadrestats, orient=VERTICAL)
		self.ysb.config(command=self.treestat3.yview)
		self.treestat3.configure(yscrollcommand=self.ysb.set)
		# windows
		self.MyTopLevel.update_idletasks()
		# waiting
		counter = sleeptime
		while counter != 0:
			sleep(1)
			counter -= 1
			message.set(TITL_PROG+"\nConnected "+txt_message+'.'*counter + ' '*(sleeptime-counter))
			self.MyTopLevel.update_idletasks()
	
	def BuildTreeStats(self, req, colwidth=50):
		Tabs = BuildTabFromRequest(self.con, req)
		# ajust window height
		#linestabs = max(6 , len(Tabs))
		linestabs = 6
		self.MyTopLevel.geometry("{w}x{h}".format(w=self.w,h=self.h+((linestabs+1)*17)))
		CenterWindows(self.MyTopLevel)
		# build tree
		tree = BuildTree(self.con, self.cadrestats, req, len(Tabs[0])* [colwidth], linestabs, None, False, E) #(50,50,50,50,50)
		# fill tree
		counter = 0
		for row in Tabs:
			tag = (counter%2)
			if (counter + 1) == len(Tabs): tag = 3
			tree.insert("", counter, iid='row_%s'%counter, values=row, tag = tag)
			counter += 1
		return(tree)
	
	def ChangeTree1(self, event):
		self.treestat1.pack_forget()
		self.treestat2.pack(side=TOP, anchor=W, fill=BOTH, padx=5, pady=5)
		
	def ChangeTree2(self, event):
		self.treestat2.pack_forget()
		self.ysb.pack(side=RIGHT, fill=Y)
		self.treestat3.pack(side=TOP, anchor=W, fill=BOTH, padx=5, pady=5)
		
	def ChangeTree3(self, event):
		self.treestat3.pack_forget()
		self.ysb.pack_forget()
		self.treestat1.pack(side=TOP, anchor=W, fill=BOTH, padx=5, pady=5)
		
		
	def HideLoadingGui(self, event):
		self.MyTopLevel.withdraw()

# COVER GUI
class CoverViewGui():
	"""Fenetre view cover."""
	def __init__(self, master, monimage, namealbum,  w=HEIG_MAIN, h=HEIG_MAIN):
		# Windows
		self.master = master
		self.master.geometry("{w}x{h}".format(w=w,h=h))
		self.master.attributes('-topmost', True)
		self.master.resizable(width=False, height=False)
		BuildIco(self.master)
		CenterWindows(self.master)
		
		width, height = monimage.size
		self.master.title("{name} - [{w}x{h}] orignal size:[{wo}x{ho}]".format(w=w, h=h, name=namealbum, wo=str(width), ho=str(height)))
		monimage = monimage.resize((w, h), Image.ANTIALIAS)
		photo = ImageTk.PhotoImage(monimage)
		label = Label(self.master, image = photo)
		label.image = photo
		label.bind("<Button-1>", self.QuitCoverViewGui)
		label.pack()
	
	def QuitCoverViewGui(self, event):
		self.master.destroy()


class CoversArtWorkViewGui():
	"""Fenetre view cover."""
	def __init__(self, master, pathartworks, nametittle, modecreate=None):
		# Windows
		self.master = master
		self.master.geometry("{w}x{h}".format(w=WIDT_MAIN,h=HEIG_MAIN))
		#self.master.attributes('-topmost', True)
		self.master.title(TITL_PROG+" [view ArtWorks] : reading files covers...")
		self.master.resizable(width=False, height=False)
		BuildIco(self.master)
		CenterWindows(self.master)
		
		# build list covers
		self.nametittle = nametittle
		fileslist = list(GetListFiles(pathartworks, MASKCOVER))
		self.numbersCov = len(fileslist)
		self.pathartworks = pathartworks
		
		# build labels thunbnails
		self.frameThunbnails = VerticalScrolledFrame(self.master , WIDT_MAIN , WIDT_PICM+4)
		self.frameThunbnails.pack(side=TOP, anchor=W, fill=BOTH, padx=5, pady=5)
		self.listartwork = []
		self.listimage = []
		maxCol = int(WIDT_MAIN/WIDT_PICM)
		curRow = curCol = cptIte = 0
		self.master.update_idletasks()
		for filelist in fileslist:
			monimage = Image.open(filelist)
			self.listimage.append(monimage)
			monimage = monimage.resize((WIDT_PICM, WIDT_PICM), Image.ANTIALIAS)
			photo = ImageTk.PhotoImage(monimage)
			label = Label(self.frameThunbnails.interior, image = photo, text=filelist)
			label.image = photo
			self.listartwork.append(label)
			label.grid(row=curRow,column=curCol)
			self.master.update_idletasks()
			label.bind("<Button-1>", lambda event,a=cptIte: self.OnSelectThunbnail(event,a))
			label.bind("<Enter>", lambda event: event.widget.config(relief=SOLID))
			label.bind("<Leave>", lambda event: event.widget.config(relief=FLAT))
			# build large cover
			if cptIte==0: 
				# build cover
				self.framecover = Frame(self.master)
				self.framecover.pack(side=TOP, anchor=W, fill=BOTH)
				self.cover = Label(self.framecover, background=THUN_CO0)
				self.cover.pack(side=TOP, fill=BOTH, expand=TRUE)
				self.aMenu = Menu(self.framecover, tearoff=0)
				self.aMenu.add_command(label="Open Folder...", command=self.OpenFolder)
				self.aMenu.add_command(label="Create cover file...", command=self.CreateFileCover)
				self.cover.bind("<Button-3>", self.popupThunbnail)
				# create cover option only if no cover file
				if modecreate[0:len(TEXT_NCO)] != TEXT_NCO:
					self.aMenu.entryconfig(1, state="disabled")
				# display first artvork
				self.OnSelectThunbnail(None, 0)
			# count thunbnails
			cptIte = cptIte + 1
			# position
			curCol = curCol + 1
			if curCol == maxCol:
				curCol = 0
				curRow = curRow + 1

	def OnSelectThunbnail(self, event, numlabel):
		curlabel = self.listartwork[numlabel]
		self.filelist = curlabel.cget('text')
		self.monimage = self.listimage[numlabel]
		# display artwork
		width, height, new_width, new_height = self.ResizeImage(WIDT_MAIN, HEIG_MAIN-WIDT_PICM+4)
		photo = ImageTk.PhotoImage(self.monimage)
		self.cover.configure(image = photo)
		self.cover.image = photo
		# next
		self.cover.bind("<Button-1>", lambda event,a=(0 if self.numbersCov==numlabel+1 else numlabel+1): self.OnSelectThunbnail(event,a))
		# windows
		self.master.title(TITL_PROG+" : [view ArtWorks: "+self.nametittle+'] {c}/{n} "{name}" A[{w}x{h}] O[{wo}x{ho}]'.format(c=str(numlabel+1), 
																		 n=str(len(self.listartwork)), 
																		 w=new_width, 
																		 h=new_height, 
																		 name=path.basename(self.filelist), 
																		 wo=str(width), 
																		 ho=str(height)))
		self.master.update_idletasks()
	
	def ResizeImage(self, wmax, hmax):
		# measures
		width, height = self.monimage.size
		# resize
		if ((wmax/width)<(hmax/height)):
			new_width  = wmax
			new_height = int(new_width * height / width)
		else:
			new_height = hmax
			new_width  = int(new_height * width / height)
		self.monimage = self.monimage.resize((new_width, new_height), Image.ANTIALIAS)
		return(width, height, new_width, new_height)
	
	def popupThunbnail(self, event):
		self.aMenu.post(event.x_root, event.y_root)
	
	def OpenFolder(self):
		openFolder(self.pathartworks)
		
	def CreateFileCover(self):
		file_pictu = getFileNameWithoutExtension(self.filelist)
		file_exten = path.splitext(self.filelist)[1][1:]
		path_cover = path.join(path.dirname(self.filelist), 'cover.' +file_exten )
		self.master.title("create file {name} ".format(name=path.basename(path_cover)))
		self.monimage.save(path_cover)


class DisplaySubprocessGui():
	def __init__(self, master, eCommand, title):
		# Windows 
		self.master = master
		self.title = title
		self.master.title(self.title+' : waiting...')
		self.master.geometry("{w}x{h}".format(w=WIDT_MAIN,h=600))
		self.master.resizable(width=False, height=False)
		BuildIco(self.master)
		CenterWindows(self.master)
		# Gui
		customFont = Font(family="Lucida Console", size=8)
		self.textarea = Text(self.master, wrap='word', state='disabled', height=49, width=200, bg='black', fg='snow', font=customFont)
		ysb = Scrollbar(self.master, orient=VERTICAL)
		ysb.config(command=self.textarea.yview)
		self.endline = True
		ysb.bind("<Button-1>", self.endlineKO)
		ysb.bind("<ButtonRelease-1>", self.endlineOK)
		ysb.pack(side=RIGHT, fill=Y)
		self.textarea.configure(yscrollcommand=ysb.set)
		self.textarea.tag_config("com", foreground="green2")
		self.textarea.tag_config("nfo", foreground="magenta")
		self.textarea.tag_config("err", foreground="red2")
		self.textarea.pack(ipadx=4, padx=4, ipady=4, pady=4, fill=BOTH)
		self.button = Button(master, text="Kill", width=15, command=self.QuitDisplaySubprocessGui)
		self.button.pack(side=BOTTOM, anchor=E, padx=4, pady=5)
		# launch process
		self.process = Popen(eCommand, stdout=PIPE, stderr=PIPE)
		# launch thread for output
		q = Queue(maxsize=1024)  # limit output buffering (may stall subprocess)
		t = Thread(target=self.reader_thread, args=[q])
		t.daemon = True # close pipe if GUI process exits
		t.start()
		# start update Gui
		self.update(q) 
	
	def endlineOK(self, event):
		self.endline = True
	
	def endlineKO(self, event):
		self.endline = False
	
	def reader_thread(self, q):
		"""Read subprocess output and put it into the queue."""
		try:
			with self.process.stdout as pipe:
				for line in iter(pipe.readline, b''):
					q.put(line)
		finally:
			q.put(None)
	
	def update(self, q):
		"""Update GUI with items from the queue."""
		for line in self.iter_except(q.get_nowait, Empty):
			if line is None:
				# end buffer
				self.master.title(self.title+' : completed')
				self.button.configure(text="Quit")
				# err
				self.textarea.configure(state='normal')
				self.textarea.insert('end', self.process.stderr.read().decode('cp850'), 'err')
				self.textarea.see('end')
				self.textarea.configure(state='disabled')
				return
			else:
				# update GUI
				self.textarea.configure(state='normal')
				line = line.decode('cp850')
				# colors tags
				if line.startswith('*') or ('****' in line):
					ltag = 'com'
				else:
					if (line.lstrip()).startswith('|') or ('(U)' in line) or ('(N)' in line):
						ltag = 'nfo'
					else:
						if 'error:' in line:
							ltag = 'err'
						else:
							ltag = None
				self.textarea.insert('end', line, ltag)
				if self.endline:
					self.textarea.see('end')
				self.textarea.configure(state='disabled')
				self.master.update_idletasks()
				# display no more than one line per 10 milliseconds
				break 
		 # schedule next update
		self.master.after(10, self.update, q)
	
	def iter_except(self, function, exception):
		"""Works like builtin 2-argument `iter()`, but stops on `exception`."""
		try:
			while True:
				yield function()
		except exception:
			return
	
	def QuitDisplaySubprocessGui(self):
		self.process.kill() # exit (zombie!)
		self.master.destroy()

# MAIN GUI
class CoverMainGui(Tk):
	"""Fenetre principale."""
	def __init__(self , master):
		# WINDOWS
		Tk.__init__(self , master)
		self.master = master
		self.title(TITL_PROG +' : initialisation...')
		# Icone
		BuildIco(self)
		# dimensions
		self.resizable(width=True, height=True)
		self.geometry("{w}x{h}".format(w=WIDT_MAIN, h=HEIG_MAIN))
		self.minsize(width=WIDT_MAIN, height=HEIG_MAIN)
		self.protocol("WM_DELETE_WINDOW", self.QuitDBAlbums)
		CenterWindows(self)
		self.bind("<F5>", self.RefreshBase)
		self.bind("<F1>", self.showloadingWin)
		self.bind("<F11>", self.ChangeDisplayNoList)
		self.withdraw()
		# Style
		s=Style()
		s.theme_use('clam')
		
		### INIT VAR
		self.labels = []
		self.Envs = None
		self.tplay = None
		self.CurentAlbum = None
		self.curalbmd5 = None
		self.CurentTrack = None
		
		#### INIT CONNECT
		self.con = None
		self.con, self.MODE_SQLI = ConnectInvent(NAME_EVT[CURT_EVT])
		
		### DISPLAY GUI
		self.displaygui()
		
		#### LOADING ENVT
		self.ConnectEnvt()
		
		#### INIT PROGRESS BAR
		self.bargauge = ProgressBar()
		self.bargauge.close()
	
	def displaygui(self):
		#### SAISIE
		self.cadresaisie = Frame(self)
		self.cadresaisie.pack(fill=BOTH)
		# Label
		labelDir = Label(self.cadresaisie, text="Search")
		labelDir.pack(side="left", padx=5, pady=5)
		# ligne de saisie
		self.var_texte = StringVar(None)
		self.ligne_texte = AutocompleteEntry(self.cadresaisie, textvariable=self.var_texte, width=27)
		self.ligne_texte.bind("<Return>", self.OnPressEnter)
		self.ligne_texte.focus_set()
		self.ligne_texte.pack(side="left", padx=5, pady=5)
		# + search tracks
		self.searchtracks = IntVar()
		self.searchtracks.set(0)
		Checkbutton(self.cadresaisie, text="In Tracks", variable = self.searchtracks).pack(side=LEFT,padx=5,pady=5)
		# buttons
		btn_search = Button(self.cadresaisie, text='Search...', width=19, command = self.GetSearchAlbums)
		btn_search.pack(side="left", padx=5, pady=5)
		# combo Category
		self.Combostyle_value = StringVar()
		self.Combostyle = Combobox(self.cadresaisie, textvariable=self.Combostyle_value, state='readonly')
		self.Combostyle.bind("<<ComboboxSelected>>", self.OnPressEnter)
		self.Combostyle.pack(side="left", padx=5, pady=5)
		self.Combostyle['values'] = DISP_CJOKER
		self.Combostyle.current(0)
		# combo Family
		self.Combofamily_value = StringVar()
		self.Combofamily = Combobox(self.cadresaisie, textvariable=self.Combofamily_value, state='readonly')
		self.Combofamily.bind("<<ComboboxSelected>>", self.OnPressEnter)
		self.Combofamily.pack(side="left", padx=5, pady=5)
		self.Combofamily['values'] = DISP_CJOKER
		self.Combofamily.current(0)
		# combo Label
		self.Combolabelm_value = StringVar()
		self.Combolabelm = Combobox(self.cadresaisie, textvariable=self.Combolabelm_value, state='readonly')
		self.Combolabelm.bind("<<ComboboxSelected>>", self.OnPressEnter)
		self.Combolabelm.pack(side="left", padx=5, pady=5)
		self.Combolabelm['values'] = DISP_CJOKER
		self.Combolabelm.current(0)
		# combo year
		self.Comboyearc_value = StringVar()
		self.Comboyearc = Combobox(self.cadresaisie, textvariable=self.Comboyearc_value, state='readonly')
		self.Comboyearc.bind("<<ComboboxSelected>>", self.OnPressEnter)
		self.Comboyearc.pack(side="left", padx=5, pady=5)
		self.Comboyearc['values'] = DISP_CJOKER
		self.Comboyearc.current(0)
		# combo environments
		self.combo_value = StringVar()
		self.combo = Combobox(self.cadresaisie, textvariable=self.combo_value, state='readonly')
		self.combo['values'] = NAME_EVT
		self.combo.current(CURT_EVT)
		# popup menu base
		self.bMenu = Menu(self.cadresaisie, tearoff=0)
		self.bMenu.add_command(label="Show Informations  [F1]", command=self.showloadingWin)
		self.bMenu.add_command(label="Reload base Albums [F5]", command=self.RefreshBase)
		self.bMenu.add_command(label="Update Base (powershell)...", command=self.BuildInvent)
		self.bMenu.add_command(label="Create sqlite database", command=self.CreateLocalBase)
		self.bMenu.add_command(label="Import Foobar Playlists, Update Score...", command=self.ImportFoobar)
		self.bMenu.add_command(label="Edit %s..." % FILE__INI, command=self.EditINI)
		self.bMenu.add_command(label="Open Logs Folder...", command=self.GetFolderLogs)
		self.combo.bind("<<ComboboxSelected>>", self.OnComboEnvtChange)
		self.combo.bind("<Button-3>", self.popupbase)
		self.combo.pack(side=RIGHT, padx=15, pady=5)
		Separator(self.master ,orient=HORIZONTAL).pack(side=TOP, fill=BOTH)
		
		#### LIST ALBUMS
		# thunbnails
		#self.frameThunbnails = VerticalScrolledFrame(self.master , None, None)#WIDT_MAIN ,WIDT_PICM*2+3*2)
		self.frameThunbnails = VerticalScrolledFrame(self.master , WIDT_MAIN ,(WIDT_PICM*2)+8)
		self.frameThunbnails.pack(side=TOP, anchor=W, fill=BOTH, expand=FALSE)
		self.frameThunbnails.bind("<Configure>",self.resizeframeThunbnails)
		# list
		self.framealbumlist = Frame(self)
		self.framealbumlist.pack(side=TOP, anchor=W, fill=BOTH, expand=FALSE)
		# tree : compatibilité sqllite
		self.tree = BuildTree(self.con, self.framealbumlist, (Z_REQUEST if self.MODE_SQLI else A_REQUEST), A_C_WIDTH, 10, 'ID', True)
		# popup menu album
		self.aMenu = Menu(self.framealbumlist, tearoff=0)
		self.aMenu.add_command(label="View ArtWorks...", command=self.ViewArtWorks)
		self.aMenu.add_command(label="Open Folder...", command=self.GetFolder)
		self.aMenu.add_command(label="Export Album...", command=self.ExportAlbums)
		self.aMenu.add_command(label="Update Album...", command=self.UpdateAlbum)
		self.aMenu.add_command(label="Edit Tags (TagScan)...", command=self.OpenTagScan)
		self.aMenu.add_command(label="No Display list [F11]", command=self.ChangeDisplayNoList)
		self.tree.bind("<Button-3>", self.popuptreealbum)
		self.tree.bind("<<TreeviewSelect>>", self.OnTreeSelectAlbum)
		self.tree.pack(side=TOP, anchor=W, padx=0, pady=0, expand=TRUE, fill=BOTH)
		
		#### INFOS ALBUM 
		# COVER
		self.cadrealbum = Frame(self)
		self.cadrealbum.pack(side=TOP, anchor=W, fill=BOTH, expand=FALSE)
		self.labcover = Label(self.cadrealbum)
		self.labcover.pack(side=LEFT, padx=0, pady=0)
		self.labcover.bind("<Button-1>", self.OnPressCover)
		# BLANK COVERS
		monimage = BuildCover(' ', TEXT_NCO, ' ')
		monimage = monimage.resize((COVE_SIZ, COVE_SIZ), Image.ANTIALIAS)
		photo = ImageTk.PhotoImage(monimage)
		self.labcover.configure(image = photo)
		self.labcover.image = photo
		# ALBUM NAME
		self.customFont = Font(family="Calibri", size=12)
		self.cadrelabelalb = Frame(self.cadrealbum)
		self.cadrelabelalb.pack(fill=BOTH, side=TOP)
		self.stralbumname = StringVar()
		self.labelalb = Label( self.cadrelabelalb, textvariable=self.stralbumname, justify = LEFT, font=self.customFont)
		self.labelalb.pack(side=LEFT, padx=10, pady=0)
		# SCORE ALBUM
		self.posalbum_scale = Scale( self.cadrelabelalb,
										command=self.ModifyScoreAlbum, 
										showvalue=0, 
										from_=0, 
										to=len(SCOR_ALBUMS)-1, 
										length=100,
										orient='horizontal')
		self.posalbum_scale.pack(side=RIGHT, padx=15, pady=5)
		self.ScoAlbumlb = StringVar()
		self.scorealbum_label = Label(self.cadrelabelalb, textvariable=self.ScoAlbumlb, font=self.customFont)
		self.btn_enrscralb = Button(self.cadrelabelalb, text='Update', command = self.OnPressButtonEnrScoreAlbum)
		self.scorealbum_label.pack(side=RIGHT, padx=5, pady=5)
		self.ScoreAlbum = 0
		# TRACKS
		self.treealb = BuildTree(self.con, self.cadrealbum, T_REQUEST.format(id=0), T_C_WIDTH, 15, 'ID', True)
		# popup menu track
		self.tMenu = Menu(self.cadrealbum, tearoff=0)
		self.treealb.bind("<Double-1>", self.OnDoubleClickTrack)
		self.treealb.bind("<<TreeviewSelect>>", self.OnSelectTrack)
		self.treealb.pack(side=BOTTOM, anchor=W, fill=BOTH, padx=0, pady=0)
		# SCORE TRACK
		self.cadrescoretrack = Frame(self)
		self.cadrescoretrack.pack(side=TOP, fill=BOTH)
		self.postrack_scale = Scale( self.cadrescoretrack,
										command=self.ModifyScoreTrack, 
										showvalue=0, 
										from_=0, 
										to=len(SCOR_TRACKS)-1, 
										length=100,
										orient='horizontal')
		self.postrack_scale.pack(side=RIGHT, padx=15, pady=5)
		self.ScoTracklb = StringVar()
		self.scoretrack_label = Label(self.cadrescoretrack, textvariable=self.ScoTracklb, font=self.customFont)
		self.scoretrack_label.pack(side=RIGHT, padx=5, pady=5)
		self.btn_enrscrtrk = Button(self.cadrescoretrack, text='Update', command = self.OnPressButtonEnrScoreTrack)
		self.ScoreTrack = 0
		
		# Status Bar
		self.StatusBar = Frame(self)
		self.StatusBar.pack(fill=BOTH, anchor=S+W, side=BOTTOM)
		self.MessageInfo = StringVar()
		self.MessageInfo_label = Label(self.StatusBar, textvariable=self.MessageInfo, anchor=W, font=self.customFont, bd=1, relief=SUNKEN)
		self.MessageInfo_label.pack(fill=X, padx=5, pady=5)
	
	def resizeframeThunbnails(self, event):
		if len(self.labels)>0:
			w = self.winfo_width()
			h = self.winfo_height()
			self.frameThunbnails.config(width=w, height=h)
			self.frameThunbnails.canv.yview_moveto(0)
			numCov = len(self.labels)
			maxCol = int(self.winfo_width()/WIDT_PICM)
			Grid.columnconfigure(self.frameThunbnails.interior, maxCol, weight=1)
			curRow = curCol = 0
			for labelt in self.labels:
				labelt.grid(row=curRow,column=curCol)
				# position
				curCol = curCol + 1
				if curCol == maxCol:
					curCol = 0
					curRow = curRow + 1
					self.update_idletasks()
	
	def DisplayThunbnails(self, new=True, deb=0, fin=THUN_SIZ):
		if new:
			# delete
			for labelt in self.labels:
				labelt.destroy()
			self.frameThunbnails.canv.yview_moveto(0)
		else:
			# del label for more
			self.labels[len(self.labels)-1].destroy()
			self.labels[len(self.labels)-2].destroy()
		numCov = len(self.tree.get_children())
		maxCol = int(self.winfo_width()/WIDT_PICM)
		Grid.columnconfigure(self.frameThunbnails.interior, maxCol, weight=1)
		if (numCov-deb)<(fin-deb):
			disCov = (numCov-deb)
		else:
			disCov = (fin-deb)
		if not new: 
			self.bargauge.open()
			self.bargauge.settitle("Create albums cover in progress...")
		curRow = curCol = cptIte = 0
		for curItem in self.tree.get_children():
			if cptIte >= deb and cptIte <= fin:
				curLign = self.tree.item(curItem)
				curalbmd5 = curLign['values'][A_POSITIO['MD5']]
				pathcover = curLign['values'][A_POSITIO['Cover']]
				albumname = curLign['values'][A_POSITIO['Name']]
				# no display thunbnails covers
				if THUN_DIS == 0: pathcover = TEXT_NCO
				monimage = BuildMiniCover(self.con, pathcover, curalbmd5)
				label = self.BuildThunbnail(pathcover, albumname.replace(' - ','\n'), monimage, curItem)
				label.grid(row=curRow,column=curCol)
				label.bind("<Button-1>", lambda event,a=curItem: self.OnSelectThunbnail(event,a))
				label.bind("<Button-3>", self.popupthunbnailsalbum)
				label.bind("<Enter>", lambda event: event.widget.config(relief=SOLID))
				label.bind("<Leave>", lambda event: event.widget.config(relief=FLAT))
				self.labels.append(label)
				if not new: self.bargauge.update((cptIte-deb)/disCov)
			# count thunbnails
			cptIte = cptIte + 1
			# position
			curCol = curCol + 1
			if curCol == maxCol:
				curCol = 0
				curRow = curRow + 1
				self.update_idletasks()
			# max display, labels for more
			if cptIte==fin:
				# add for add more thunbnails
				monimage = Image.open(THUN_DBA)
				label = self.BuildThunbnail(THUN_DBA, "{n} covers display max \n Click for more +{f}...".format(n=str(fin),f=str(fin+fin) if (fin+fin)<(numCov-fin) else str(numCov-fin)), monimage, None)
				label.grid(row=curRow,column=curCol)
				label.bind("<Button-1>", lambda e: self.DisplayThunbnails(False,fin,fin+fin))
				label.bind("<Enter>", lambda event: event.widget.config(relief=SOLID))
				label.bind("<Leave>", lambda event: event.widget.config(relief=FLAT))
				self.labels.append(label)
				# add for all thunbnails
				curCol = curCol + 1
				if curCol == maxCol:
					curCol = 0
					curRow = curRow + 1
				label = self.BuildThunbnail(THUN_DBA, "{n} covers display max \n Click for all +{f}...".format(n=str(fin),f=str(numCov-fin)), monimage, None)
				label.grid(row=curRow,column=curCol)
				label.bind("<Button-1>", lambda e: self.DisplayThunbnails(False,fin,numCov-fin+1))
				label.bind("<Enter>", lambda event: event.widget.config(relief=SOLID))
				label.bind("<Leave>", lambda event: event.widget.config(relief=FLAT))
				self.labels.append(label)
				break
		if not new: self.bargauge.close()
		#print(str(cptIte)+'*covers')
	
	def BuildThunbnail(self, pathcover, texte, monimage, curItem):
		try:
			font = ImageFont.truetype("calibri.ttf", 12)
		except:
			font = ImageFont.truetype("arial.ttf", 10)
		# two first line
		if pathcover[0:len(TEXT_NCO)] == TEXT_NCO or pathcover==THUN_DBA: 
			# add text infos
			draw = ImageDraw.Draw(monimage)
			#w, h = draw.textsize(texte)
			w, h = WIDT_PICM, 30 
			if '\n' in texte:
				texte = texte.split('\n')
				texte = texte[0]+"\n"+texte[1]
			draw.rectangle(((4,(WIDT_PICM-h)/2),(WIDT_PICM-4,((WIDT_PICM-h)/2)+h)), fill=THUN_CO0)
			draw.text((6,((WIDT_PICM-h)/2)+4), texte, font=font, fill=THUN_CO1)
		photo = ImageTk.PhotoImage(monimage)
		label = Label(self.frameThunbnails.interior, image = photo, text= curItem)
		label.image = photo
		return(label)
	
	def OnSelectThunbnail(self, event, curItem):
		"""Display album infos."""
		self.CurentAlbum = curItem
		# select item
		self.tree.selection_set(self.CurentAlbum)
		# scroll
		self.tree.see(self.CurentAlbum)
		# cursor
		self.tree.focus(self.CurentAlbum)
	
	def OnComboEnvtChange(self, event):
		self.ConnectEnvt()
	
	def OnPressEnter(self, event):
		self.GetSearchAlbums()
	
	def OnPressCover(self, event):
		"""Affiche la pochette de l'album."""
		if self.pathcover[0:len(TEXT_NCO)] != TEXT_NCO:
			self.coverWin = Toplevel(self.master)
			monimage = BuildCover(self.con, self.pathcover, self.curalbmd5)
			CoverViewGui(self.coverWin, monimage, self.albumname)
	
	def OnTreeSelectAlbum(self, event):
		"""Display album infos."""
		if self.tree.get_children():
			self.tree.focus()
			self.CurentAlbum = self.tree.focus()
			self.GetInfosAlbum(self.CurentAlbum)
	
	def OnSelectTrack(self, event):
		if self.treealb.get_children():
			self.treealb.focus()
			self.CurentTrack = self.treealb.focus()
			self.GetInfosTrack(self.CurentTrack)
	
	def OnDoubleClickTrack(self, event):
		if self.treealb.get_children():
			self.playmedia()
	
	def OnPressButtonEnrScoreAlbum(self):
		"""MAJ Score Album."""
		# var
		self.ScoreAlbum = self.posalbum_scale.get()
		self.ScoAlbumlb.set(DisplayStars(self.ScoreAlbum, SCOR_ALBUMS))
		# Mysql
		UpdateBaseScore(self.con, self.ScoreAlbum, self.Id_CD, U_REQUEST)
		# Treeview
		self.tree.set(self.CurentAlbum, column=A_POSITIO['Score'], value=self.ScoreAlbum)
		# Button
		self.btn_enrscralb.pack_forget()
	
	def OnPressButtonEnrScoreTrack(self):
		"""MAJ Score Track."""
		# var
		self.ScoreTrack = self.postrack_scale.get()
		self.ScoTracklb.set(DisplayStars(self.ScoreTrack, SCOR_TRACKS))
		# Mysql
		UpdateBaseScore(self.con, self.ScoreTrack, self.ID_TRACK, V_REQUEST)
		# Treeview
		self.treealb.set(self.CurentTrack, column=T_POSITIO['Score'], value=self.ScoreTrack)
		# Button
		self.btn_enrscrtrk.pack_forget()
	
	def ModifyScoreAlbum(self, event):
		"""Modify Score Album."""
		self.ScoAlbumlb.set(DisplayStars(self.posalbum_scale.get(), SCOR_ALBUMS))
		if self.ScoreAlbum != self.posalbum_scale.get():
			self.btn_enrscralb.pack(side=RIGHT, padx=5, pady=5)
		else:
			self.btn_enrscralb.pack_forget()
	
	def ModifyScoreTrack(self, event):
		"""Modify Score Track."""
		self.ScoTracklb.set(DisplayStars(self.postrack_scale.get(), SCOR_TRACKS))
		if self.ScoreTrack != self.postrack_scale.get():
			self.btn_enrscrtrk.pack(side=RIGHT, padx=5, pady=5)
		else:
			self.btn_enrscrtrk.pack_forget()
	
	def popupbase(self, event):
		"""Mennu Base."""
		if self.MODE_SQLI:
			self.aMenu.entryconfig(3, state="disabled")
		else:
			self.aMenu.entryconfig(3, state="normal")
		self.bMenu.post(event.x_root, event.y_root)
	
	def popupthunbnailsalbum(self, event):
		"""Mennu Thunbnails."""
		curItem = event.widget.cget('text')
		self.CurentAlbum = curItem
		self.tree.selection_set(self.CurentAlbum)
		self.tree.see(self.CurentAlbum)
		self.tree.focus(self.CurentAlbum)
		# maj infos albums
		self.GetInfosAlbum(self.CurentAlbum, True)
		curLign = self.tree.item(curItem)
		if curLign['values'][A_POSITIO['Qty_covers']] == 0 or not(path.exists(self.AlbumPath)):
			self.aMenu.entryconfig(0, state="disabled")
		else:
			self.aMenu.entryconfig(0, state="normal")
		self.aMenu.entryconfig(3, label="Update Album (powershell): "+ self.albumname[:15] + "...")
		self.aMenu.post(event.x_root, event.y_root)
	
	def popuptreealbum(self, event):
		"""Mennu Album."""
		# maj selection : only for one selection
		ListeSelect = self.tree.selection()
		if len(ListeSelect) == 1 :
			# select item
			self.CurentAlbum = self.tree.identify('item',event.x,event.y)
			self.tree.selection_set(self.CurentAlbum)
			self.tree.focus(self.CurentAlbum)
			# maj infos albums
			self.GetInfosAlbum(self.CurentAlbum, True)
			curLign = self.tree.item(self.CurentAlbum)
			if curLign['values'][A_POSITIO['Qty_covers']] == 0 or not(path.exists(self.AlbumPath)):
				self.aMenu.entryconfig(0, state="disabled")
			else:
				self.aMenu.entryconfig(0, state="normal")
			self.aMenu.entryconfig(1, state="normal")
			self.aMenu.entryconfig(2, label="Export cover/csv '"+ self.albumname[:15] + "...'")
			self.aMenu.entryconfig(3, label="Update Album '"+ self.albumname[:15] + "...'")
			self.aMenu.entryconfig(4, state="normal")
			self.aMenu.post(event.x_root, event.y_root)
		else:
			# select x item
			if len(ListeSelect) > 1 :
				self.aMenu.entryconfig(0, state="disabled")
				self.aMenu.entryconfig(1, state="disabled")
				self.aMenu.entryconfig(2, label="Export "+ DisplayCounters(len(ListeSelect), 'Album')+"cover/csv...")
				self.aMenu.entryconfig(3, label="Update "+ DisplayCounters(len(ListeSelect), 'Album') +"...")
				self.aMenu.entryconfig(4, state="disabled")
				self.aMenu.post(event.x_root, event.y_root)
	
	def QuitMain(self):
		"""Exit."""
		# connection close
		self.con.close()
		self.destroy()
	
	def ConnectEnvt(self, refresh = False):
		"""Connect Base Environnement."""
		if self.Envs != self.combo_value.get() or refresh:
			# Mysql
			self.Envs = self.combo_value.get()
			if self.con: self.con.close()
			self.condat = datetime.now().strftime('%H:%M:%S')
			self.con, self.MODE_SQLI = ConnectInvent(self.Envs)
			# debut loading
			self.loadingWin = Toplevel(self)
			LoadingGui(self.loadingWin, self.con, self.MODE_SQLI, 0)
			# auto-completion
			completion_list = BuildListFromRequest(self.con, S_REQUEST)
			self.ligne_texte.set_completion_list(completion_list)
			# tittle
			if self.MODE_SQLI:
				self.title(TITL_PROG + ' : offline mode SQLite local at '+self.condat)
			else:
				self.title('{prog} : online base "{database}" at {heure}'.format(prog = TITL_PROG,
																			 database = self.Envs,
																			 heure = self.condat))
			# mount table albums in memory
			self.Tabs = BuildTabFromRequest(self.con, (Z_REQUEST if self.MODE_SQLI else A_REQUEST))
			# reset combos
			self.Combostyle.current(0)
			self.Combofamily.current(0)
			self.Combolabelm.current(0)
			self.Comboyearc.current(0)
			# all albums to treeview
			self.GetSearchAlbums(refresh)
			# Hide loading
			self.loadingWin.withdraw()
			# display main
			self.update()
			self.deiconify()
	
	def GetSearchAlbums(self, refresh = False):
		"""Search Albums."""
		self.config(cursor="watch")
		txt_search = self.var_texte.get()
		# SEARCH IN TRACKS
		if self.searchtracks.get() == 1:
			lst_id = BuildTabFromRequest(self.con, B_REQUEST.format(search=txt_search))
		else:
			lst_id = []
		# THUNBNAILS
		# delete collection
		for labelt in self.labels:
			labelt.destroy()
		self.labels = []
		self.frameThunbnails.canv.yview_moveto(0)
		# TREEVIEW
		# del
		if self.tree.get_children():
			for i in self.tree.get_children():
				self.tree.delete(i)
		self.update_idletasks()
		# insert
		liststyle = []
		listfamil = []
		listlabel = []
		listeyear = []
		counter = cpt_trk = cpt_cds = cpt_siz = cpt_len = 0
		for row in self.Tabs:
			# find text entry ?
			if  txt_search.lower() in row[A_POSITIO['Name']].lower() or txt_search.lower() in row[A_POSITIO['Label']].lower() or self.SearchInTracksSQL(lst_id,row[A_POSITIO['ID_CD']]):
				# Category ok ?
				if (self.Combostyle_value.get() != DISP_CJOKER and row[A_POSITIO['Category']] == self.Combostyle_value.get()) or (self.Combostyle_value.get() == DISP_CJOKER):
					# Family ok ?
					if (self.Combofamily_value.get() != DISP_CJOKER and row[A_POSITIO['Family']] == self.Combofamily_value.get()) or (self.Combofamily_value.get() == DISP_CJOKER):
						# Label ok ?
						if (self.Combolabelm_value.get() != DISP_CJOKER and row[A_POSITIO['Label']] == self.Combolabelm_value.get()) or (self.Combolabelm_value.get() == DISP_CJOKER):
							# year ok ?
							if (self.Comboyearc_value.get() != DISP_CJOKER and row[A_POSITIO['Year']] == self.Comboyearc_value.get()) or (self.Comboyearc_value.get() == DISP_CJOKER):
								# FILL TREEVIEW
								self.tree.insert("", counter, iid=row[A_POSITIO['ID_CD']], values=row, tag = (counter%2))
								# FILL LISTS COMBOS
								if row[A_POSITIO['Category']] not in liststyle:
									liststyle.append(row[A_POSITIO['Category']])
								if row[A_POSITIO['Family']] not in listfamil:
									listfamil.append(row[A_POSITIO['Family']])
								if row[A_POSITIO['Label']] not in listlabel:
									listlabel.append(row[A_POSITIO['Label']]) 
								if row[A_POSITIO['Year']] not in listeyear:
									listeyear.append(row[A_POSITIO['Year']])
								# MODIFICATIONS DISPLAY ALBUM NAME, LABEL, ISRC
								albumname = row[A_POSITIO['Name']]
								label = isrc = None
								if len(albumname.split('['))==2 and albumname[0]!='[':
									label = albumname.split('[')[1].split(']')[0]
									albumname = albumname.split('[')[0]
									if len(label.split(' - '))==2:
										isrc = label.split(' - ')[1]
										label = label.split(' - ')[0]
									else:
										# LABEL OR ISRC (digit?)
										if any(char.isdigit() for char in label):
											isrc = label
											label = ''
									# FILL LISTS COMBOS LABEL EXTRA
									if label not in listlabel:
										listlabel.append(label)
								self.tree.set(row[A_POSITIO['ID_CD']], column=A_POSITIO['Name'], value=albumname)
								if row[A_POSITIO['Label']]=='':
									self.tree.set(row[A_POSITIO['ID_CD']], column=A_POSITIO['Label'], value=label)
								if row[A_POSITIO['ISRC']]=='':
									self.tree.set(row[A_POSITIO['ID_CD']], column=A_POSITIO['ISRC'], value=isrc)
								# COUNTERS
								counter += 1
								cpt_cds += row[A_POSITIO['Qty_CD']]
								cpt_trk += row[A_POSITIO['Qty_Tracks']]
								cpt_siz += row[A_POSITIO['Size']]
								cpt_len += sum(int(x) * 60 ** i for i,x in enumerate(reversed(row[A_POSITIO['Length']].split(":"))))
		# FILL COMBOS IF NO SELECT
		if self.Combostyle_value.get() == DISP_CJOKER:
			liststyle.sort(reverse=True)
			self.Combostyle['values'] = [DISP_CJOKER,] + liststyle
		if self.Combofamily_value.get() == DISP_CJOKER:
			listfamil.sort()
			self.Combofamily['values'] = [DISP_CJOKER,] + listfamil
		if self.Combolabelm_value.get() == DISP_CJOKER:
			listlabel.sort()
			self.Combolabelm['values'] = [DISP_CJOKER,] + listlabel
		if self.Comboyearc_value.get() == DISP_CJOKER:
			listeyear.sort(reverse=True)
			self.Comboyearc['values'] = [DISP_CJOKER,] + listeyear
		# DISPLAY THUNBNAILS
		self.DisplayThunbnails()
		# DISPLAY STATS SEARCH
		if counter > 0:
			# info size
			txt_siz = str(int(cpt_siz/1024)) +' Go'
			# info time
			if int(((cpt_len/60/60)/24)*10)/10 < 1:
				# seoncd -> Hours
				txt_dur = str(int(((cpt_len/60/60))*10)/10) + ' Hours'
			else:
				# seoncd -> Days
				txt_dur = str(int(((cpt_len/60/60)/24)*10)/10) + ' Days'
			self.MessageInfo.set("Search Result \"{sch}\" :  {alb} | {trk} | {cds} | {siz} | {dur} ".format(sch = (txt_search if len(txt_search)>0 else 'all'),
																						alb = DisplayCounters(counter, 'Album'),
																						cds =  DisplayCounters(cpt_cds, 'CD'),
																						trk = DisplayCounters(cpt_trk, 'Track'),
																						siz = txt_siz,
																						dur = txt_dur))
		else:
			self.MessageInfo.set("Search Result \"{sch}\" : nothing".format(sch = self.ligne_texte.get()))
		if self.tree.get_children():
			# first line by defaut
			if not(refresh): 
				self.CurentAlbum = self.tree.get_children()[0]
			try:
				self.tree.selection_set(self.CurentAlbum)
			except:
				pass
				self.CurentAlbum = self.tree.get_children()[0]
				self.tree.selection_set(self.CurentAlbum)
			self.tree.focus(self.CurentAlbum)
		# MAJ ALBUMS INFOS
		self.GetInfosAlbum(self.CurentAlbum, refresh)
		# focus
		self.ligne_texte.focus_set()
		self.config(cursor="")
		
	def SearchInTracksSQL(self, lst_id, cur_id):
		# SEARCH TRACKS
		if self.searchtracks.get() == 1:
			for elt in lst_id:
				if str(cur_id).lower() in str(elt).lower():
					return True
		return False
		
	def GetInfosAlbum(self, curItem, refresh = False):
		# if treeview not empty or album different or optiontrack
		if self.tree.get_children():
			curLign = self.tree.item(curItem)
			if  curLign['values'][A_POSITIO['MD5']] != self.curalbmd5 or refresh:
				# MAJ ALBUM INFO
				self.curalbmd5 = curLign['values'][A_POSITIO['MD5']]
				self.pathcover = curLign['values'][A_POSITIO['Cover']]
				self.albumname = curLign['values'][A_POSITIO['Name']]
				self.ScoreAlbum = curLign['values'][A_POSITIO['Score']]
				self.AlbumPath = curLign['values'][A_POSITIO['Path']]
				self.Id_CD = curItem
				self.CurentAlbum = curItem
				# MAJ SCORE ALBUM
				self.posalbum_scale.set(self.ScoreAlbum)
				self.ScoAlbumlb.set(DisplayStars(self.ScoreAlbum, SCOR_ALBUMS))
				self.posalbum_scale.config(state='normal')
				# MAJ LIST TRACKS
				if self.treealb.get_children():
					for i in self.treealb.get_children():
						self.treealb.delete(i)
				req = T_REQUEST.format(id=self.Id_CD)
				counter = cpt_len = 0
				tracks = BuildTabFromRequest(self.con, req)
				for track in tracks:
					# SEARCH IN TRACKS
					if self.searchtracks.get() == 1 and (self.var_texte.get().lower() in track[A_POSITIO['Category']].lower() or self.var_texte.get().lower() in track[A_POSITIO['Family']].lower()):
						tag = '2'
					else:
						tag = str(counter%2)
					self.treealb.insert("", counter, iid=track[T_POSITIO['ID_TRACK']], values = track, tag = tag)
					counter += 1
					cpt_len += sum(int(x) * 60 ** i for i,x in enumerate(reversed(track[3].split(":"))))
				# first line by defaut
				if counter > 0: self.CurentTrack = self.treealb.get_children()[0]
				# extract infos label
				albumnamet, infoslabel = AlbumNameExtract(self.albumname, str(curLign['values'][A_POSITIO['Label']]), 
																		str(curLign['values'][A_POSITIO['ISRC']]),
																		str(curLign['values'][A_POSITIO['Qty_CD']]))
				# MAJ ALBUM NAME
				txt_album = albumnamet + "\n{year} • {tracks} • {dur} • {cd} • {art}\n{lab}".format(year=str(curLign['values'][A_POSITIO['Year']]),
																		tracks = DisplayCounters(counter, 'track'),
																		dur = DisplayCounters(int(((cpt_len/60)*10)/10),'min'),
																		cd = DisplayCounters(curLign['values'][A_POSITIO['Qty_CD']], 'CD'),
																		art = DisplayCounters(curLign['values'][A_POSITIO['Qty_covers']], 'ArtWork'),
																		lab = infoslabel)
				self.stralbumname.set(txt_album)
				# MAJ COVERS
				monimage = BuildCover(self.con, self.pathcover, self.curalbmd5)
				monimage = monimage.resize((COVE_SIZ, COVE_SIZ), Image.ANTIALIAS)
				photo = ImageTk.PhotoImage(monimage)
				self.labcover.configure(image = photo)
				self.labcover.image = photo
		else:
			# MAJ ALBUM INFO
			self.curalbmd5 = None
			self.pathcover = None
			self.albumname = None
			self.ScoreAlbum = 0
			self.Id_CD = None
			self.CurentAlbum = None
			self.AlbumPath = None
			self.CurentTrack = None
			# INI SCORE
			self.posalbum_scale.set(self.ScoreAlbum)
			self.ScoAlbumlb.set(DisplayStars(self.ScoreAlbum, SCOR_ALBUMS))
			self.posalbum_scale.config(state='disabled')
			# DEL LIST TRACKS
			if self.treealb.get_children():
				for i in self.treealb.get_children():
					self.treealb.delete(i)
			# NO ALBUM NAME
			self.stralbumname.set('')
			# BLANK COVERS
			monimage = BuildCover(' ', TEXT_NCO, ' ')
			monimage = monimage.resize((COVE_SIZ, COVE_SIZ), Image.ANTIALIAS)
			photo = ImageTk.PhotoImage(monimage)
			self.labcover.configure(image = photo)
			self.labcover.image = photo
		# MAJ TRACK INFO
		self.GetInfosTrack(self.CurentTrack)
	
	def GetInfosTrack(self, curItem):
		if self.treealb.get_children():
			curLign = self.treealb.item(curItem)
			#self.treealb.selection_set(curItem)
			#self.treealb.focus(curItem)
			self.ScoreTrack = curLign['values'][T_POSITIO['Score']]
			self.ID_TRACK = curItem
			self.CurentTrack = curItem
			# MAJ SCORE
			self.postrack_scale.set(self.ScoreTrack)
			self.ScoTracklb.set(DisplayStars(self.ScoreTrack, SCOR_TRACKS))
			self.postrack_scale.config(state='normal')
		else:
			self.ScoreTrack = 0
			self.ID_TRACK = None
			self.CurentTrack = None
			self.postrack_scale.set(self.ScoreTrack)
			self.ScoTracklb.set(DisplayStars(self.ScoreTrack, SCOR_TRACKS))
			self.postrack_scale.config(state='disabled')
	
	def GetFolder(self):
		"""Ouvre dossier album dans l'explorateur."""
		openFolder(self.AlbumPath)
	
	def GetFolderLogs(self):
		"""Ouvre dossier logs dans l'explorateur."""
		openFolder(LOGS_PROG)
	
	def OpenTagScan(self):
		"""Ouvre program edit TAGs."""
		RunProgExecWin(TAGS_SCAN, self.AlbumPath)
	
	def EditINI(self):
		"""Edit INI FILE."""
		RunProgExecWin(EDIT_TEXT, FILE__INI)
	
	def ChangeDisplayNoList(self, event=None):
		"""modifiy thunbnails display."""
		self.framealbumlist.pack_forget()
		self.frameThunbnails.pack(expand=TRUE)
		self.aMenu.entryconfig(5, label="Display list [F11]", command=self.ReinitDisplay)
		self.bind("<F11>", self.ReinitDisplay)
	
	def ReinitDisplay(self, event=None):
		self.frameThunbnails.pack_forget()
		self.cadrealbum.pack_forget()
		self.cadrescoretrack.pack_forget()
		self.StatusBar.pack_forget()
		
		self.frameThunbnails.pack(side=TOP, anchor=W, fill=BOTH, expand=FALSE)
		self.framealbumlist.pack(side=TOP, anchor=W, fill=BOTH, expand=FALSE)
		self.cadrealbum.pack(side=TOP, anchor=W, fill=BOTH, expand=FALSE)
		self.cadrescoretrack.pack(side=TOP, fill=BOTH)
		self.StatusBar.pack(side=BOTTOM, anchor=S+W, fill=BOTH)
		self.aMenu.entryconfig(7, label="No Display list [F11]", command=self.ChangeDisplayNoList)
		self.bind("<F11>", self.ChangeDisplayNoList)
	
	def playmedia(self):
		"""Player Audio thread pyQT5."""
		self.curLign = self.treealb.item(self.CurentTrack)
		lismedia = []
		fileselect = path.join(self.curLign['values'][T_POSITIO['REP_Track']], self.curLign['values'][T_POSITIO['FIL_Track']])
		position = 1
		for SelItem in self.treealb.get_children():
			file = path.join(self.treealb.item(SelItem)['values'][T_POSITIO['REP_Track']], self.treealb.item(SelItem)['values'][T_POSITIO['FIL_Track']])
			if file == fileselect:
				curentposition = position
			lismedia.append(file)
			position += 1
		# first exec
		try:
			if self.tplay.is_alive():
				self.tplay.terminate()
				sleep(0.1)
		except Exception:
			pass
		self.tplay = Process(target = playerProcessAudio, args = (lismedia, curentposition, self.winfo_x()+3, self.winfo_y()+self.winfo_height()-130))
		self.tplay.start()
		
	def ExportAlbums(self):
		fileprop = datetime.now().strftime('%Y%m%d%H%M%S') + "_Albums.csv"
		filename = asksaveasfile(mode='w', 
								 initialdir = getcwd(), 
								 initialfile = fileprop, 
								 defaultextension = ".csv", 
								 filetypes = [('CSV Files', '.csv'), ('Image files', '.jpg')], 
								 title = "Export from CSV File")
		if filename is None: return
		extension = path.splitext(filename.name)[1][1:]
		ListeSelect = self.tree.selection()
		# extract file CSV
		if extension == 'csv':
			print ('create CSV')
			wr = writer(filename, delimiter=';', doublequote=True, quoting=QUOTE_ALL, lineterminator='\n')
			for SelItem in ListeSelect:
				Album = self.tree.item(SelItem)
				print ('Export: '+Album['values'][A_POSITIO['Name']])
				wr.writerow(Album['values'])
			filename.close()
		# extract base64\mysql to file JPEG 
		if extension == 'jpg':
			filename.close()
			print ('create JPGs')
			for SelItem in ListeSelect:
				Album = self.tree.item(SelItem)
				filecover = path.join(path.dirname(filename.name), Album['values'][A_POSITIO['Name']])
				print ('Extract: '+filecover)
				BuildFileCover(self.con, filecover,Album['values'][A_POSITIO['MD5']], Album['values'][A_POSITIO['Score']])
			remove(filename.name)
	
	def showloadingWin(self, event=None):
		"""Display stats base"""
		self.loadingWin.update()
		self.loadingWin.deiconify()
		self.loadingWin.focus_set()
	
	def RefreshBase(self, event=None):
		"""Recharge environnement."""
		self.ConnectEnvt(True)
	
	def CreateLocalBase(self):
		"""Create base Sqlite."""
		filename = BASE_SQLI.format(envt=self.Envs)
		if path.isfile(filename):
			remove(filename)
		logname = datetime.now().strftime("%Y%m%d%H%M%S") + "_CopyDatabaseToSqlite_" + self.Envs + ".log"
		CopyDatabaseInvent(self.con, filename, self.bargauge, path.join(LOGS_PROG, logname))
		self.MessageInfo.set("Create Database SQLite :"+filename+" Sucessfull")
	
	def ImportFoobar(self):
		"""Foobar2000 playlists operations."""
		# import fpl playlist to mysql DBFOOBAR
		numtracks = foobarMajDBFOOBAR(self.con, self.bargauge, FOOB_PLAY)
		self.MessageInfo.set("Import Sucessfull Playlists Foobar 2000: "+str(numtracks)+" Tracks in base")
		# synchro score sql
		execSqlFile(self.con, self.bargauge, FOOB_UPSC , 9)
		self.MessageInfo.set("Synchro Score Sucessfull Playlists Foobar 2000")
	
	def UpdateAlbum(self):
		"""Execute powershell Script update albums infos."""
		ListeSelect = self.tree.selection()
		self.GUIUpdateAlbum = Toplevel(self.master)
		eCommand = BuildCommandPowershell(PWSH_SCRU, '-listID_CD', ','.join(ListeSelect), '-Envt', self.Envs)
		print(eCommand)
		DisplaySubprocessGui(self.GUIUpdateAlbum, eCommand, 'Update '+ DisplayCounters(len(ListeSelect), "Album "))
	
	def BuildInvent(self):
		"""Execute powershell Script update all albums infos."""
		self.GUIBuildInvent = Toplevel(self.master)
		if 'LOSSLESS' in self.Envs:
			filescript = PWSH_SCRI.format(mod='LOSSLESS')
		else:
			filescript = PWSH_SCRI.format(mod='MP3')
		eCommand = BuildCommandPowershell(filescript, '-Envt', self.Envs)
		print(eCommand)
		DisplaySubprocessGui(self.GUIBuildInvent, eCommand, 'Update Base '+self.Envs)
		#self.ConnectEnvt(True)
	
	def ViewArtWorks(self):
		"""views covers storage."""
		self.coverWin = Toplevel(self.master)
		curLign = self.tree.item(self.CurentAlbum)
		if curLign['values'][A_POSITIO['Qty_covers']] == 1:
			# only cover
			monimage = BuildCover(self.con, self.pathcover, self.curalbmd5)
			CoverViewGui(self.coverWin, monimage, self.albumname)
		else:
			# view artworks
			CoversArtWorkViewGui(self.coverWin, self.AlbumPath, self.albumname, self.pathcover)
	
	def QuitDBAlbums(self):
		#close player processing ?
		try:
			if self.tplay.is_alive():
				self.tplay.terminate()
				sleep(0.1)
		except Exception:
			pass
		#close sql
		self.con.close()
		self.destroy()


###################################################################
# START
if __name__ == "__main__":
	app = CoverMainGui(None)
	app.mainloop()
