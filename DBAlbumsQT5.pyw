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
from os import system, path, getcwd, walk, remove
from base64 import b64decode
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont, QTextCursor, QColor
from PyQt5.QtCore import (Qt, QVariant, QDir, pyqtSlot, pyqtSignal, QUrl, QProcess, QIODevice, QTime, 
						QDateTime, QRect, QCryptographicHash, QSettings, QtInfoMsg, QtWarningMsg, 
						QtCriticalMsg, QtFatalMsg, qInstallMessageHandler, qDebug, QSize) # , QAbstractTableModel
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QLabel, QMainWindow, QProgressBar, QPushButton,
							QTextEdit, QFileDialog, QMessageBox, QMenu, QStyle, QSlider,  QWidget, QSizePolicy, 
							QGridLayout, QVBoxLayout, QHBoxLayout, QCompleter, QScrollArea, QFrame, QLayout)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist # , QMediaMetaData

# dev ext https://github.com/rr-/fpl_reader
from fpl_reader import read_playlist 
# Gui QtDesigner
from Ui_DBALBUMS import Ui_MainWindow
from Ui_DBLOADING import Ui_LoadingWindow
# compiler .ui sans Eric6: pyuic5 file.ui -o Ui_main_file.py

""" DBAlbums History Version : Doubsman dev.
1.46 passage QT5
1.45 version MINI + zoom thunbnails, corrections bugs + test
1.44 drag and drop folders, super class python3
1.43 loading refont, artwork player resize, optimize thunbnail, powershell 1.11
1.42 refont list grid, add album powershell by select folder, jauge v2
1.41 add connexion sqlserver, store requests, gui whith no connect
1.40 100% compatible Linux Debian 9 + simplication autocompletion
1.39 last modified + update only category powershell
1.38 treeview link thunbnails + upgrade / help .ini
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
1.18 Execution Powershell script BUILD_INVENT.ps1 + BUILD_INVENT_updateAlbum.ps1
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
1.04 constants
1.02 export csv
1.01 gestion covers
1.00 search base INVENT mysql TEST/PRODUCTION (05/2016)."""

""" INSTALLATION
for Python 3.6.0 installation modules for Windows
	pip install pymysql (mysql)
	pip install pypyodbc (sql server)
	pip install pillow
	pip install pyQT5
	pip install pyqtdeploy
	pip install cx_Freeze
	extract N:\_INVENT\DBAlbums\LIB\fpl_reader-master.zip
	python.exe setup.py install
for Python 3 installation modules for Debian9
	su
	apt-get install python3-pymysql
	apt-get install python3-pip
	apt-get install python3-tk
	apt-get install python3-pil
	apt-get install python3-pil.imagetk
	pip3 install SIP
	pip3 install pyqt5 python-qt4-sql
	apt-get install libqt5multimedia5-plugins
	pip3 install pypyodbc
	extract /HOMERSTATION/_LossLess/_INVENT/DBAlbums/LIB/fpl_reader-master.zip
		python3.exe setup.py install
"""

""" MOUNT VOLUME LINUX DEBIAN
# Debian9 Mount volume Music HOMERSTATION
Add Hostname /etc/hosts
	Terminal:	su
	mousepad /etc/hosts
	add line:
	192.168.0.250 HOMERSTATION
install network package
	Terminal:	su
	apt-get install sudo
	apt-get install cifs-utils
	apt-get install gvfs-backends
	apt-get install net-tools
	# Add this repo to the /etc/apt/source.list file
	deb ftp://ftp.debian.org/debian stable contrib non-free
	apt-get update
	apt-get install ttf-mscorefonts-installer
create folder mount
	Terminal:	su
	mkdir -p /HOMERSTATION/_LossLess
	chmod 777 /HOMERSTATION/_LossLess
Create credential File:
	Terminal:	su
	mousepad  /home/misterdoubs/.smbhomercred
		username=HomerMusic
		password=Mus1c4Me
		domain=WORKGROUP
	chmod 600 /home/misterdoubs/.smbhomercred
Add mount:
	Terminal:	su
	mousepad /etc/fstab
	add line:
	//192.168.0.250/_LossLess /HOMERSTATION/_LossLess cifs _netdev,users,noauto,users,credentials=/home/misterdoubs/.smbmusiccred
test:
	mount /HOMERSTATION/_LossLess/
"""

# ##################################################################
# CONSTANTS
# path
if getattr(system, 'frozen', False):
	# frozen
	PATH_PROG = path.dirname(executable)
else:
	# unfrozen
	PATH_PROG = path.realpath(path.dirname(argv[0]))
	# PATH_PROG = path.dirname(__file__)
# chdir(PATH_PROG) 
QDir.setCurrent(PATH_PROG) # working directory
LOGS_PROG = path.join(PATH_PROG, 'LOG')
BASE_SQLI = path.join(PATH_PROG, 'LOC', "DBALBUMS_{envt}.db")
PWSH_SCRI = path.join(PATH_PROG, 'PS1', "BUILD_INVENT_{mod}.ps1")
PWSH_SCRU = path.join(PATH_PROG, 'PS1', "UPDATE_ALBUMS.ps1")
PWSH_SCRA = path.join(PATH_PROG, 'PS1', "ADD_ALBUMS.ps1")
FOOB_UPSC = path.join(PATH_PROG, 'SQL', "DBAlbums_FOOBAR_UPADTESCORE.sql")
MASKCOVER = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.bmp', '.tiff')

# ##################################################################
# Read File DBAlbums.ini
FILE__INI = 'DBAlbums.ini'
configini = QSettings(FILE__INI, QSettings.IniFormat)
configini.beginGroup('dbalbums')
VERS_PROG = configini.value('prog_build')
TITL_PROG   = "♫ DBAlbums v{v} (2017)".format(v=VERS_PROG)
WIDT_MAIN   = int(configini.value('wgui_width'))
HEIG_MAIN   = int(configini.value('wgui_heigh'))
WIDT_PICM   = int(configini.value('thun_csize'))
HEIG_LHUN   = int(configini.value('thnail_nbl'))
HEIG_LTAB   = int(configini.value('tagrid_nbl'))
DISP_CJOKER = configini.value('text_joker')
TEXT_NCO    = configini.value('text_nocov')
WINS_ICO    = configini.value('wins_icone')
UNIX_ICO    = configini.value('unix_icone')
LOGO_PRG    = configini.value('progr_logo')
PICT_NCO    = configini.value('pict_blank')
PICM_NCO    = configini.value('picm_blank')
ENVT_DEF    = configini.value('envt_deflt')
TREE_CO0    = configini.value('color0_lin')
TREE_CO1    = configini.value('color1_lin')
TREE_CO2    = configini.value('color2_lin')
TREE_CO3    = configini.value('color3_lin')
THUN_CO0    = configini.value('color0_thu')
THUN_CO1    = configini.value('color1_thu')
THUN_SE1    = configini.value('color0_sel')
THUN_SE2    = configini.value('color1_sel')
THUN_DBA    = configini.value('picm_endof')
THUN_DIS    = int(configini.value('thnail_dis'))
THUN_NOD    = int(configini.value('thnail_nod'))
COVE_SIZ    = int(configini.value('covers_siz'))
FONT_MAI    = configini.value('font00_ttx')
FONT_CON    = configini.value('font01_ttx')
configini.endGroup()
# PROGS LINKS
configini.beginGroup('programs')
TAGS_SCAN = r'' + configini.value('tagscan')
FOOB_PLAY = r'' + configini.value('foobarP')
if platform == "darwin" or platform == 'linux':
	EDIT_TEXT = r'' + configini.value('txt_lin')
	LOGS_PROG = r""+LOGS_PROG.replace('\\\\', '/').replace('\\', '/')
	BASE_SQLI = r""+BASE_SQLI.replace('\\\\', '/').replace('\\', '/')
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
	print('qt_message_handler: line: {l}, func: {f}(), file: {i}'.format(l=context.line,
																		 f=context.function,
																		 i=context.file))
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

# ##################################################################
# STORE REQUESTS
def getRequest(name, MODE_SQLI = None):
	# autocompletion VW_DBCOMPLETION
	if name == 'autocompletion':
		if MODE_SQLI == 'mssql':
			request = "SELECT TOP 1000 Synthax FROM VW_AUTOCOMPLETION GROUP BY Synthax ORDER BY COUNT(*) DESC;"
		else:
			request = "SELECT Synthax FROM VW_AUTOCOMPLETION GROUP BY Synthax ORDER BY COUNT(*) DESC LIMIT 1000;"
	# date modification base
	if name == 'datedatabase':
		request = "SELECT MAX(datebase) FROM (SELECT MAX(Date_insert) AS datebase FROM DBALBUMS UNION SELECT MAX(Date_Modifs) FROM DBALBUMS ) FUS;"
	# list albums DBALBUMS
	if name == 'albumslist':
		request = 	"SELECT Category, Family, Name, Label, ISRC, " \
					"Qty_Tracks, Qty_CD, Year, Length, Size, " \
					"Score, Qty_covers, Date_Insert, Date_Modifs, "
		if MODE_SQLI == 'sqlite':
			request = request + "Position1 || '\\' || Position2 AS Position, "
		if MODE_SQLI == 'mysql':
			request = request + "CONCAT(Position1,'\\\\',Position2) AS Position, "
		if MODE_SQLI == 'mssql':
			request = request + "Position1+'\'+Position2 AS Position, "
		request = request +" Typ_Tag, Path, Cover, MD5, ID_CD AS ID " \
							"FROM DBALBUMS WHERE 1=1 ORDER BY Date_Insert DESC"
	# list tracks
	if name == 'trackslist':
		request = "SELECT ODR_Track, TAG_Artists, TAG_Title, TAG_length, " \
					"Score, TAG_Genres, FIL_Track, REP_Track, ID_TRACK  " \
					"FROM DBTRACKS WHERE ID_CD={id} ORDER BY REP_Track, ODR_Track"
	# search in track
	if name == 'tracksinsearch':
		request =  "SELECT ID_CD AS ID FROM DBTRACKS AS TRK WHERE TAG_Artists like '%{search}%' OR TAG_Title like '%{search}%' GROUP BY ID_CD"
	# cover base64
	if name == 'cover':
		request = "SELECT Cover64 FROM DBCOVERS WHERE MD5='{MD5}'"
	# minicover base64
	if name == 'minicover':
		request = "SELECT MiniCover64 FROM DBCOVERS WHERE MD5='{MD5}'"
	# update Sore Album
	if name == 'updatescorealbum':
		request = "UPDATE DBALBUMS SET Score={score} WHERE ID_CD={id}"
	# update Sore Track
	if name == 'updatescoretrack':
		request = "UPDATE DBTRACKS SET Score={score} WHERE ID_TRACK={id}"
	# insert playlist foobar
	if name == 'playlistfoobar':
		request = "INSERT INTO DBFOOBAR (Playlist, Path, FIL_Track, Name , MD5, TAG_Album, TAG_Artists, TAG_Title) " \
					"VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
	if MODE_SQLI == 'mssql': 
		request = request.replace(' `',' [').replace('` ','] ')
	return request

def copyDatabaseInvent(parent, db,  BaseNameSQLite, logname):
	"""create SqlLite Database."""	
	qDebug('Process Creation Database Sqlite '+BaseNameSQLite)
	parent.updateGaugeBar(0, 'Process Creation Database Sqlite '+BaseNameSQLite)
	# create sqlite database
	cnxlite = 'CREA'
	dblite = QSqlDatabase.addDatabase("QSQLITE", cnxlite)
	dblite.setDatabaseName(BaseNameSQLite)
	if dblite.isValid():
		boolcon = dblite.open()
		if boolcon:
			parent.updateGaugeBar(0.05)
			tablename = "DBALBUMS"
			qDebug('Create '+tablename)
			reqcreate = "CREATE TABLE DBALBUMS(ID_CD INTEGER PRIMARY KEY AUTOINCREMENT, MD5 TEXT, Family TEXT, " \
						"Category TEXT, Position1 TEXT, Position2 TEXT, Name TEXT, Label TEXT, ISRC TEXT, " \
						"Year TEXT, Qty_CD INT, Qty_Cue INT, Qty_CueERR INT, Qty_repMusic INT, Qty_Tracks INT, " \
						"Qty_audio INT, Typ_Audio TEXT, Qty_repCover, Qty_covers, Cover TEXT, Path TEXT, Size INT, " \
						"Duration TEXT, Length TEXT, Typ_Tag TEXT, Date_Insert DATETIME, Date_Modifs DATETIME, RHDD_Modifs DATETIME, Score INT, Statut TEXT)"
			reqinsert = "INSERT INTO DBALBUMS VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
			reqindexe = "CREATE INDEX DBALBUMS_ndx_Date_Insert ON DBALBUMS(Date_Insert)"
			copytable(db, dblite, tablename, reqcreate, reqinsert, reqindexe)
			parent.updateGaugeBar(0.20)
			tablename = "DBTRACKS"
			qDebug('Create '+tablename)
			reqcreate = "CREATE TABLE DBTRACKS(ID_CD INT,ID_TRACK INTEGER PRIMARY KEY AUTOINCREMENT, Family TEXT, " \
						"Category TEXT, Position1 TEXT, Position2 TEXT, REP_Album TEXT, REP_Track TEXT,FIL_Track TEXT, " \
						"TAG_Exten TEXT,TAG_Album TEXT, TAG_Albumartists TEXT, TAG_Year TEXT,TAG_Disc INT, TAG_Track INT, " \
						"ODR_Track TEXT, TAG_Artists TEXT,TAG_Title TEXT,TAG_Genres TEXT,TAG_Duration TEXT,TAG_length TEXT, " \
						"Score INT,Date_Insert DATETIME, Statut TEXT, FOREIGN KEY(ID_CD) REFERENCES DBALBUMS(ID_CD))"
			reqinsert = "INSERT INTO DBTRACKS VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )"
			reqindexe = "CREATE INDEX DBTRACKS_ndx_idcd ON DBTRACKS(ID_CD)"
			copytable(db, dblite, tablename, reqcreate, reqinsert, reqindexe)
			parent.updateGaugeBar(0.40)
			tablename = "DBFOOBAR"
			qDebug('Create '+tablename)
			reqcreate = "CREATE TABLE {t}(ID_FOO INTEGER PRIMARY KEY AUTOINCREMENT, MD5 TEXT, Name TEXT, Path TEXT, " \
						"FIL_Track TEXT, Playlist TEXT, TAG_Album TEXT, TAG_Artists TEXT, TAG_Title TEXT, " \
						"Date_insert TIMESTAMP DEFAULT CURRENT_TIMESTAMP)".format(t=tablename)
			reqinsert = "INSERT INTO {t} VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(t=tablename)
			reqindexe = "CREATE INDEX DBFOOBAR_ndx_FIL_Track ON DBFOOBAR(FIL_Track)"
			copytable(db, dblite, tablename, reqcreate, reqinsert, reqindexe)
			parent.updateGaugeBar(0.60)
			tablename = "DBFOOBOR"
			qDebug('Create '+tablename)
			reqcreate = "CREATE TABLE {t}(FIL_Track TEXT, FIL_TrackM TEXT)".format(t=tablename)
			reqinsert = "INSERT INTO {t} VALUES( ?, ?)".format(t=tablename)
			copytable(db, dblite, tablename, reqcreate, reqinsert)
			parent.updateGaugeBar(0.75)
			tablename = "DBCOVERS"
			qDebug('Create '+tablename)
			reqcreate = "CREATE TABLE {t}(MD5 TEXT, Cover64 BLOB, MiniCover64 BLOB)".format(t=tablename)
			reqinsert = "INSERT INTO {t} VALUES( ?, ?, ?)".format(t=tablename)
			reqindexe = "CREATE UNIQUE INDEX DBCOVERS_ndx_md5 ON DBCOVERS(MD5)"
			copytable(db, dblite, tablename, reqcreate, reqinsert, reqindexe)
			parent.updateGaugeBar(0.9)
			tablename = "VW_AUTOCOMPLETION"
			qDebug('Create '+tablename)
			reqcreate = "CREATE TABLE {t}(ID_CD INT, Synthax TEXT)".format(t=tablename)
			reqinsert = "INSERT INTO {t} VALUES( ?, ?)".format(t=tablename)
			copytable(db, dblite, tablename, reqcreate, reqinsert)
			# remove database sqlite
			db.removeDatabase(cnxlite)
			parent.updateGaugeBar(1)			
		else:
			qDebug('no create', BaseNameSQLite)
	parent.gaugeBar.setVisible(False)

def copytable(dbsrc, dbdes, tablename, reqcreate, reqinsert, reqindexe=None):
	"""Copy table. Create+Datas+Index."""
	querylite = QSqlQuery(None, dbdes)
	query = QSqlQuery(None, dbsrc)
	# drop
	querylite.exec_("DROP TABLE {t}".format(t=tablename))
	if not querylite.exec_(): qDebug(10*' '+"drop "+querylite.lastError().text())
	# create
	querylite.exec_(reqcreate)
	if not querylite.exec_(): qDebug(10*' '+"create "+querylite.lastError().text())
	# datas
	query.exec_("SELECT * FROM "+tablename)
	while query.next():
		querylite.prepare(reqinsert)
		for indcol in range(query.record().count()):
			querylite.bindValue(indcol, query.value(indcol))
		if not querylite.exec_(): 
			qDebug(tablename+"10*' ' "+querylite.lastError().text())
			listparam = list(querylite.boundValues().values())
			for i in range(len(listparam)):	qDebug(10*' ', i, listparam[i])
	# index
	if reqindexe!=None:
		querylite.exec_(reqindexe)
		if not querylite.exec_(): qDebug(10*' '+":index "+querylite.lastError().text())
	querylite.clear
	query.clear

def centerWidget(widget):
	"""Center Widget."""
	qtRectangle = widget.frameGeometry()
	centerPoint = QDesktopWidget().availableGeometry().center()
	qtRectangle.moveCenter(centerPoint)
	widget.move(qtRectangle.topLeft())

def displayCounters(num = 0, text = '' ):
	"""format 0 000 + plural."""
	strtxt=" %s%s" % (text, "s"[num==1:])
	if num>9999:
		strnum = '{0:,}'.format(num).replace(",", " ")
	else:
		strnum = str(num)
	return (strnum + strtxt)

def displayStars(star, scorelist):
	"""scoring."""
	max = len(scorelist)-1
	txt_score =  scorelist[star]
	return (txt_score+'  '+star*'★'+(max-star)*'☆')

def albumNameExtract(name, label, isrc, nbcd):
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
		infoslabel = infoslabel[:-3]
		albumnamet = name
	albumnamet = albumnamet.replace('('+nbcd+'CD)','').replace(nbcd+'CD','')
	return (albumnamet, infoslabel)	

def logit(dat, filename):
  rt=open(filename,"a")
  rt.write(dat+"\n")
  rt.close()
  
def buildCommandPowershell(script, *argv):
	"""Build command PowerShell."""
	command = [r'-ExecutionPolicy', 'Unrestricted',
				'-WindowStyle','Hidden',
				'-File', 
				script]
	for arg in argv:
		command += (arg,)
	return 'powershell.exe', command
	
def runCommand(prog, *argv):
	"""Execut a program no wait, no link."""
	argums = []
	for arg in argv:
		argums += (arg,)
	p = QProcess()
	# print(prog, argums)
	p.startDetached(prog, argums)

def openFolder(path):
	"""Open File Explorer."""
	if platform == "win32":
		runCommand('explorer', path)
	elif platform == "darwin":
		runCommand('open', path)
	elif platform == 'linux':
		runCommand('xdg-open', path)

def convertUNC(path):
	""" convert path UNC to linux."""
	# open file unc from Linux (mount \HOMERSTATION\_lossLess)
	if (platform == "darwin" or platform == 'linux') and path.startswith(r'\\'):
		path = r""+path.replace('\\\\','/').replace('\\','/')
	return(path)

def getListFiles(folder, masks):
	"""Build files list."""
	for folderName, subfolders, filenames in walk(folder):
		if subfolders:
			for subfolder in subfolders:
				getListFiles(subfolder, masks)
		for filename in filenames:
			for xmask in masks:
				if filename[-4:].lower() in xmask:
					yield path.join(folderName,filename)

def getFile(folder, file_name):
	"""open file playlist foobar 2000."""
	with open(path.join(folder, file_name), 'rb') as handle:
		return handle.read()

def foobarBuildTracksList(folder):
	"""build list of playlists foobar 2000."""
	trackslist = []
	playfiles = list(getListFiles(folder,(".fpl",)))
	for playfile in playfiles:
		trackslist += foobargetListFilesFromPlaylist(playfile)
	return(trackslist)

def foobargetListFilesFromPlaylist(file_path):
	folder = path.dirname(file_path)
	file_name = path.basename(file_path)
	listfiles = []
	try:
		playlistcontent = read_playlist(getFile(folder, file_name))
		for lfile in playlistcontent.tracks:
			playlist = file_path
			audiofil = str(lfile.file_name[7:], 'utf-8')
			albumnam = audiofil.split('\\')[-2]
			albummd5 = QCryptographicHash.hash(albumnam.encode('utf-8'),QCryptographicHash.Md5).toHex()
			albummd5 = (albummd5.data()).decode('utf-8').upper()
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
		listfiles.append((path.basename(playlist), path.dirname(audiofil), path.basename(audiofil), albumnam, albummd5, TAG_Album, TAG_Artists, TAG_Title))
	except BaseException as e:
		pass
		#logger.error('Failed' + str(e))
		qDebug('#problem : '+file_path)
		qDebug('Failed' + str(e))
	return(listfiles)

def foobarMajDBFOOBAR(parent, folder):
	# fill DBFOOBAR
	footracks = foobarBuildTracksList(folder)
	numtracks = len(footracks)
	counter = 0
	parent.updateGaugeBar(0, "Crowse playlists fooBar 2000")
	request = getRequest('playlistfoobar')
	for footrack in footracks:
		query = QSqlQuery()
		query.prepare(request)
		pos = 0
		for colval in footrack:
			query.bindValue(pos, colval)
			pos += 1
		if not query.exec_():
			errorText = query.lastError().text()
			qDebug(request, errorText)
			numtracks = 0
			break
		query.clear
		counter += 1
		parent.updateGaugeBar(counter/numtracks)
	return(numtracks)

def connectDatabase(envt):
	"""Connect base MySQL/Sqlite."""
	configini.beginGroup(envt)
	MODE_SQLI = configini.value('typb')
	BASE_RAC = r'' +configini.value('raci')
	boolcon = False
	if MODE_SQLI == 'sqlite':
		db=QSqlDatabase.addDatabase("QSQLITE")
		db.setDatabaseName(BASE_SQLI.format(envt=envt))
		if not db.isValid():
			qDebug(envt+' problem no valid database')
	else:
		BASE_SEV = configini.value('serv')
		BASE_USR = configini.value('user')
		BASE_PAS = configini.value('pass')
		BASE_NAM = configini.value('base')
		BASE_PRT = int(configini.value('port'))
		configini.endGroup()
		if MODE_SQLI == 'mysql':
			db=QSqlDatabase.addDatabase("QMYSQL")
		elif MODE_SQLI == 'mssql':
			db=QSqlDatabase.addDatabase("QODBC")
		db.setHostName(BASE_SEV)
		db.setDatabaseName(BASE_NAM)
		db.setUserName(BASE_USR)
		db.setPassword(BASE_PAS)
		db.setPort(BASE_PRT)
	if db.isValid():
		boolcon = db.open()
	else:
		qDebug(envt+' problem for open database')
	return boolcon, db, MODE_SQLI, BASE_RAC

def execSqlFile(parent, sql_file, nbop):
	"""Exec script SQL file..."""
	#cur = con.cursor()
	statement = ""
	counter = 0
	parent.updateGaugeBar(0,"Exececution script SQL file"+sql_file)
	for line in open(sql_file):
		if line[0:2] == '--':
			if line[0:3] == '-- ':
				parent.updateGaugeBar(counter/nbop, "Exec :"+line.replace('--' ,''))
			continue
		statement = statement + line
		if len(line)>2 and line[-2] == ';':
			counter = counter +1
			query = QSqlQuery()
			query.exec_(statement)
			if not query.exec_():
				errorText = query.lastError().text()
				qDebug(query.lastQuery())
				qDebug(errorText)
				break
			query.clear
			statement = ""
	
def buildTabFromRequest(req):
	"""Select to memory list."""
	autoList = []
	query = QSqlQuery(req)
	query.exec_(req)
	while query.next():
		autoList.append(query.value(0))
	query.clear
	return autoList

def buildFileCover(filenamecover, md5):
	"""Build cover base64/mysql to file."""
	request = (getRequest('cover')).format(MD5=md5)
	coverb64 = buildTabFromRequest(request)[0]
	cover = b64decode(coverb64)
	filecover = open(filenamecover, "wb")
	filecover.write(cover)
	filecover.close()

def updateBaseScore(score, id, req):
	"""Maj Mysql table Albums."""
	req = req.format(score=score, id=id)
	query = QSqlQuery()
	query.exec_(req)
	query.clear

def buildReqTCD(group, column, tableName, TDCName='TDC', TDCSum=1, LineSum=True, MODE_SQLI='mysql'):
	"""build request Pivot table compatible sqlite, mysql, SQLserver."""
	# Collections
	req = "SELECT `{column}` FROM {tableName} GROUP BY `{column}` ;".format(tableName=tableName,column=column)
	if MODE_SQLI == 'mssql': req = req.replace(' `',' [').replace('` ','] ')
	col_names = buildTabFromRequest(req)
	# sum/collections
	lstcols = ''
	ReqTDC = "(SELECT `{group}` AS '{TDCName}' ,\n".format(group=group,TDCName=TDCName)
	for col_name in col_names:
		ReqTDC += "    SUM(CASE WHEN `{column}` = '{col_name}' THEN {TDCSum} ELSE 0 END) AS `{col_name}` ,\n".format(column=column,TDCSum=TDCSum,col_name=col_name)
		lstcols+= " `{col_name}` ,".format(col_name=col_name)
	ReqTDC += "    SUM({TDCSum}) AS 'TOTAL' FROM {tableName} GROUP BY `{group}` \n".format(tableName=tableName,TDCSum=TDCSum,group=group)
	# sum global
	if LineSum:
		ReqTDC += " UNION \nSELECT 'TOTAL', \n"
		for col_name in col_names:
			ReqTDC += "    SUM(CASE WHEN `{column}` = '{col_name}' THEN {TDCSum} ELSE 0 END),\n".format(column=column,TDCSum=TDCSum,col_name=col_name)
		ReqTDC += "    SUM({TDCSum}) FROM {tableName}\n".format(tableName=tableName,TDCSum=TDCSum)
	# order by total is last line
	ReqTDC += ") tdc ORDER BY 'TOTAL';"
	# select column
	ReqTDC = "SELECT `"+TDCName+"` ,"+lstcols+" `TOTAL` FROM \n" + ReqTDC
	# replace ` for [] sqlserver
	if MODE_SQLI == 'mssql': ReqTDC = ReqTDC.replace(' `',' [').replace('` ','] ')
	return ReqTDC

# ##################################################################
class TNLabel(QLabel):
	def __init__(self, parent, monimage,  size,  row, **kwargs):
		super(TNLabel,  self).__init__(parent, **kwargs)
		self.parent = parent
		# label
		self.setPixmap(monimage)
		self.setFixedSize(size, size)
		self.setStyleSheet("border: 2px solid white")
		self.Name = row
		
	@pyqtSlot()
	def enterEvent(self, QEvent):
		# here the code for mouse hover
		self.setStyleSheet("border: 2px solid black")
		
	@pyqtSlot()
	def leaveEvent(self, QEvent):
		# here the code for mouse leave
		self.setStyleSheet("border: 2px solid white")

# ##################################################################
class ModelTbl(QSqlQueryModel):
	def __init__(self, parent, req, gridname,  colsname, colswrapper):
		super(ModelTbl, self).__init__(parent)
		self.parent = parent
		self.myindex = colswrapper
		self.columns = colsname
		self.req = req
		self.grid = gridname
		self.setQuery(self.req)
		# set columns name + size
		numcol = 0
		for colname in self.columns:
			self.setHeaderData(numcol, Qt.Horizontal, colname);
			numcol += 1
	
	def setFilter(self,  colname,  value):
		self.req = self.req.replace('1=1', '1=1 AND '+colname+"='"+value+"'")
		self.setQuery(self.req)
		#self.displayThunbnails()
	
	def refresh(self):
		self.setQuery(self.req)
		
	def datacombos(self, column):
		list = []
		for row in range(self.rowCount()):
			index = self.index(row, self.columns.index(column))
			curItem = self.data(index)
			if curItem not in list:
				list.append(str(curItem))
		list.sort(reverse=True)
		list = [DISP_CJOKER] + list
		return list
		
	def listmodel(self):
		if self.rowCount()>0:
			for index in range(len(self.columns)):
				curItem = self.data(self.index(0, index))
				qDebug(index, self.myindex[index], curItem)
	
	def getData(self, row, colname):
		if self.rowCount()>0:
			return QVariant(self.data(self.index(row, self.myindex.index(colname))))
		return QVariant()
		
	def getSum(self, colname):
		if self.rowCount()>0:
			total = 0
			for row in range(self.rowCount()):
				value = self.data(self.index(row, self.myindex.index(colname)))
				if isinstance(value, int)==False:
					if len(value.split(':'))>1:
						value = sum(int(x) * 60 ** i for i,x in enumerate(reversed(value.split(':'))))
				total += int(value)
			return total
		return QVariant()
		
	def getMedias(self):
		if self.rowCount()>0:
			listmedia = []
			for row in range(self.rowCount()):
				file = path.join(self.data(self.index(row, self.myindex.index('REP_Track'))), self.data(self.index(row, self.myindex.index('FIL_Track'))))
				listmedia.append(convertUNC(file))
		return listmedia
	
	def replaceThunbnails(self, sizeTN, oldsizeTN):
		"""Modify size thunbnails"""
		# replace labels thunbnails
		numCov = self.grid.count()
		if numCov>1:
			oldmaxCol = int(self.parent.frameGeometry().width()/(oldsizeTN+4))
			maxCol = int(self.parent.frameGeometry().width()/(sizeTN+4))
			curRow = curCol = cptIte = oldcurRow = oldcurCol = 0
			for row in range(numCov):
				if self.grid.itemAtPosition(oldcurRow, oldcurCol)!=0:
					# capture and clear label gridlayout
					layoutitem = self.grid.takeAt(cptIte)
					label = layoutitem.widget()
					self.grid.removeWidget(label)
					# resize
					label.setFixedSize(sizeTN, sizeTN)
					mypixmap = label.pixmap()
					if mypixmap.size().width()!=sizeTN or mypixmap.size().height()!=sizeTN:
						mypixmap = mypixmap.scaled(sizeTN, sizeTN, Qt.IgnoreAspectRatio, Qt.FastTransformation)
					label.setPixmap(mypixmap)
					# replace
					self.grid.addWidget(label, curRow, curCol)
				# position old next
				oldcurRow += 1
				if oldcurCol == oldmaxCol:
					oldcurCol = 0
					oldcurRow += 1
				# position next
				curCol += 1
				if curCol == maxCol:
					curCol = 0
					curRow += 1
	
	def displayThunbnails(self, new=True, deb=0, fin=THUN_DIS):
		if new:
			# clear thunbnails
			while self.grid.count()>0:
				layoutitem = self.grid.takeAt(0)
				self.grid.removeWidget(layoutitem.widget())
				layoutitem.widget().deleteLater()
		else:
			# delete 2 labels endof before add more
			if self.grid.count()>0:
				layoutitem = self.grid.takeAt(self.grid.count()-1)
				self.grid.removeWidget(layoutitem.widget())
				layoutitem.widget().deleteLater()
				layoutitem = self.grid.takeAt(self.grid.count()-1)
				self.grid.removeWidget(layoutitem.widget())
				layoutitem.widget().deleteLater()
		sizeTN = self.parent.sizeTN
		self.parent.updateGaugeBar(0, "Create thunbnails...")
		numAlb = self.rowCount()
		numCov = min(fin,numAlb)-deb
		maxCol = int(self.parent.frameGeometry().width()/(sizeTN+4))
		curRow = 0
		curCol = 0
		cptIte = 0
		for row in range(numAlb):
			if cptIte >= deb and cptIte <= fin:
				index = self.index(row, self.myindex.index('Cover'))
				pathcover = self.data(index)
				index = self.index(row, self.myindex.index('Name'))
				albumname = self.data(index)
				# no cover or no display thunbnails covers (thnail_nod = 1)
				if THUN_NOD == 0 or pathcover == TEXT_NCO:
					if THUN_NOD == 0:pathcover = TEXT_NCO
					monimage = QPixmap(PICM_NCO)
					monimage = self.buildTextThunbnail(pathcover, albumname.replace(' - ','\n'), monimage, sizeTN)
				else:
					index = self.index(row, self.myindex.index('MD5'))
					Curalbmd5 = self.data(index)
					monimage = self.buildCover(pathcover, Curalbmd5, sizeTN, 'minicover')
				label = TNLabel(self.parent, monimage, sizeTN,  row)
				label.mousePressEvent = (lambda event, r=row:self.parent.onSelectThunbnailChanged(event,  r))
				self.grid.addWidget(label, curRow, curCol)
				self.parent.updateGaugeBar((cptIte-deb+1)/numCov)
			cptIte = cptIte + 1
			# position
			curCol = curCol + 1
			if curCol == maxCol:
				curCol = 0
				curRow = curRow + 1
				self.parent.update()
			# max display, labels for more
			if cptIte==fin:
				# add for add more thunbnails
				monimage = QPixmap(THUN_DBA)
				monimage = self.buildTextThunbnail(THUN_DBA, "{n} covers display max \n Click for more +{f}...".format(n=str(fin),f=str(fin+fin) if (fin+fin)<(numAlb-fin) else str(numAlb-fin)), monimage, sizeTN)
				label = TNLabel(self.parent, monimage, sizeTN,  999999)
				label.mousePressEvent = (lambda e, d=fin, f=fin+fin: self.displayThunbnails(False,d,f))
				self.grid.addWidget(label, curRow, curCol)
				# add for all thunbnails
				curCol = curCol + 1
				if curCol == maxCol:
					curCol = 0
					curRow = curRow + 1
				monimage = QPixmap(THUN_DBA)
				monimage = self.buildTextThunbnail(THUN_DBA, "{n} covers display max \n Click for all +{f}...".format(n=str(fin),f=str(numAlb-fin)), monimage, sizeTN)
				label = TNLabel(self.parent, monimage, sizeTN,  999999)
				label.mousePressEvent = (lambda e, d=fin, f=numAlb-fin+1: self.displayThunbnails(False,d,f))
				self.grid.addWidget(label, curRow, curCol)
				self.parent.updateGaugeBar(1)
				break
		self.parent.updateGaugeBar(1)
		
	def buildTextThunbnail(self, pathcover, texte, monimage, sizeTN):
		# no cover, add blank
		if pathcover[0:len(TEXT_NCO)] == TEXT_NCO or pathcover==THUN_DBA: 
			# add text infos
			painter = QPainter(monimage)
			painter.setRenderHint(QPainter.Antialiasing)
			painter.drawPixmap(QRect(0, 0, monimage.width(), monimage.width()), monimage)
			painter.fillRect(QRect(5, sizeTN/3, sizeTN-5, sizeTN/3), Qt.black)
			painter.setPen(Qt.white)
			painter.setFont(QFont(FONT_MAI, 8))
			painter.drawText(QRect(0, 0, sizeTN, sizeTN), Qt.AlignCenter, texte)
			painter.end()
		return monimage
		
	def buildCover(self, pathcover, md5, sizeTN, namerequest='cover'):
		"""Get base64 picture cover."""
		request = (getRequest(namerequest)).format(MD5=md5)
		if pathcover[0:len(TEXT_NCO)] == TEXT_NCO: 
			# no cover : blank
			monimage = QPixmap(PICT_NCO)
		else:
			# cover base64/mysql
			try:
				coverb64 = buildTabFromRequest(request)[0]
				cover = b64decode(coverb64)
				monimage = QPixmap()
				monimage.loadFromData(cover)
			except:
				pass
				QMessageBox(self, TITL_PROG,' : err thunbnail read :'+pathcover)
				monimage = QPixmap(PICT_NCO)
		if monimage.width()!=sizeTN or monimage.height()!=sizeTN:
			qDebug('resize picture')
			monimage= monimage.scaled(sizeTN, sizeTN, Qt.IgnoreAspectRatio, Qt.FastTransformation)
		return (monimage)

# ##################################################################
class ProcessGui(QWidget):
	def __init__(self, process, params, title, w=WIDT_MAIN, h=HEIG_MAIN-150, parent=None):
		super(ProcessGui, self).__init__(parent)
		self.title = title
		self.resize(w,h)
		self.setWindowIcon(QIcon(WINS_ICO))
		self.setWindowTitle(title+' : waiting...')
		self.plainTextOut = QTextEdit(self)
		self.plainTextOut.setStyleSheet("background-color: black;color:white;")
		self.plainTextOut.setReadOnly(True)
		self.btn_quit = QPushButton('Kill')
		self.btn_quit.setMaximumWidth(80)
		self.btn_quit.clicked.connect(lambda e:self.destroy())
		font = QFont()
		font.setFamily(FONT_CON)
		font.setFixedPitch(True)
		font.setPointSize(8)
		self.levelcolors = [Qt.white, Qt.green, Qt.magenta, Qt.red]
		self.plainTextOut.setFont(font)
		labtn = QHBoxLayout()
		labtn.addStretch()
		labtn.addWidget(self.btn_quit)
		layout = QVBoxLayout()
		layout.addWidget(self.plainTextOut)
		layout.addLayout(labtn)
		self.setLayout(layout)
		centerWidget(self)
		self.show()
		# run process
		self.normalOutputWritten('|'+process+' '+' '.join(params) + '\n')
		self.process = QProcess()
		self.process.setProcessChannelMode(QProcess.MergedChannels)
		self.process.readyReadStandardOutput.connect(self.WorkReply)
		self.process.finished.connect(self.WorkFinished)
		self.process.start(process, params, QIODevice.ReadWrite)
		self.process.waitForStarted()

	def normalOutputWritten(self, line):
		# set level line
		if line.startswith('*') or ('****' in line):
			level = 1
		elif (line.lstrip()).startswith('|') or ('(U)' in line) or ('(N)' in line):
			level = 2
		elif 'error:' in line:
			level = 3
		else:
			level = 0
		# set color
		self.plainTextOut.setTextColor(QColor(self.levelcolors[level]))
		# display
		cursor = self.plainTextOut.textCursor()
		cursor.movePosition(QTextCursor.End)
		#cursor.insertText(line)
		self.plainTextOut.append(line.rstrip())
		self.plainTextOut.setTextCursor(cursor)
		self.plainTextOut.ensureCursorVisible()	
	
	@pyqtSlot()
	def WorkReply(self):
		"""Outpout to Gui"""
		data = self.process.readAllStandardOutput().data()
		ch = data.decode('cp850').rstrip()
		self.normalOutputWritten(ch)

	@pyqtSlot()
	def WorkFinished(self):
		"""End of processus."""
		if self.process!=None:
			self.process.readyReadStandardOutput.disconnect()
			self.process.finished.disconnect()
			self.normalOutputWritten('Process Finished...')
			self.setWindowTitle(self.title+' : Finished...')
			self.btn_quit.setText('Quit')

# ##################################################################
class CoverViewGui(QWidget):
	def __init__(self, cover, namealbum, w=HEIG_MAIN, h=HEIG_MAIN, parent=None):
		super(CoverViewGui, self).__init__(parent)
		self.resize(w, h)
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags(Qt.WindowTitleHint)
		self.setWindowFlags(Qt.WindowSystemMenuHint)
		self.setWindowFlags(Qt.WindowCloseButtonHint)
		self.setWindowIcon(QIcon(WINS_ICO))
		self.setWindowTitle("{name} - [{w}x{h}] orignal size:[{wo}x{ho}]".format(w=w, h=h, name=namealbum, wo=str(cover.width()), ho=str(cover.height())))
		centerWidget(self)
		covdi= cover.scaled(w, h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
		label = QLabel(self)
		label.setPixmap(covdi)
		label.mousePressEvent = lambda e:self.destroy()
		posit = QGridLayout(self)
		posit.setContentsMargins(0, 0, 0, 0)
		posit.addWidget(label, 0, 0)
		self.setLayout(posit)
		self.show()
	
	@pyqtSlot()
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape: 
			self.destroy()

# ##################################################################
class ArtworksGui(QWidget):
	def __init__(self, pathartworks, nametittle, createcover, w, h, sizeTN=WIDT_PICM, parent=None):
		super(ArtworksGui, self).__init__(parent)
		self.resize(w,h)
		self.setWindowIcon(QIcon(WINS_ICO))
		self.setWindowTitle(TITL_PROG+" [view ArtWorks] : reading files covers...")
		self.setStyleSheet('QWidget{background-color: darkgray} ' \
						   'QLabel{background-color: darkgray;}')
		self.height = h
		self.mycover = None
		self.sizethun = sizeTN
		self.scrollAreaWidgetthunbnails = QWidget(self)
		self.scrollArea = QScrollArea()
		self.scrollArea.setSizeIncrement(QSize(sizeTN+4, sizeTN+4))
		self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.scrollArea.setMinimumSize(QSize(8*(self.sizethun+4), 155))
		self.gridthunbnails = QGridLayout()
		self.gridthunbnails.setContentsMargins(5, 5, 5, 5)
		self.labelcover = QLabel()
		self.labelcover.setAlignment(Qt.AlignCenter)
		self.labelcover.setMinimumSize(QSize(self.width()-40, self.height-(self.gridthunbnails.rowCount()*(self.sizethun+4))-70))
		self.labelcover.enterEvent = self.onSelectCover
		self.labelcover.setContextMenuPolicy(Qt.CustomContextMenu)
		self.labelcover.customContextMenuRequested.connect(self.popUpMenu)
		# popup albums 
		self.menua = QMenu()
		self.action_OFC = self.menua.addAction("Open Folder...", lambda c=pathartworks: openFolder(c))
		self.action_COV = self.menua.addAction("Create cover file...", self.createFileCover)
		# create cover option only if no cover file
		if createcover[0:len(TEXT_NCO)] != TEXT_NCO:
			self.action_COV.setEnabled(False)
		self.line = QFrame(self)
		self.line.setFrameShape(QFrame.HLine)
		self.line.setFrameShadow(QFrame.Sunken)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.labelcover.setSizePolicy(sizePolicy)
		labelcgrid = QGridLayout()
		labelcgrid.setContentsMargins(5, 5, 5, 5)
		labelcgrid.addWidget(self.labelcover)
		labelcgrid.setSizeConstraint(QLayout.SetFixedSize)
		self.gridthunbnails.setContentsMargins(3, 5, -1, 5)
		self.gridthunbnails.setSpacing(2)
		self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetthunbnails)
		self.gridLayout_2.addLayout(self.gridthunbnails, 0, 0, 1, 1)

		self.scrollArea.setWidget(self.scrollAreaWidgetthunbnails)
		layout = QVBoxLayout(self)
		layout.addWidget(self.scrollAreaWidgetthunbnails)
		layout.addWidget(self.line)
		layout.addStretch(1)
		layout.addLayout(labelcgrid)
		self.setLayout(layout)
		centerWidget(self)
		self.show()

		# build list covers
		self.nametittle = nametittle
		self.fileslist = list(getListFiles(pathartworks, MASKCOVER))
		self.pathartworks = pathartworks
		self.filelist = self.fileslist[0]

		maxCol = int(w/self.sizethun)
		curRow = curCol = 0
		# build thunbnails
		cpt = 0
		for filelist in self.fileslist:
			mycover = QPixmap(filelist)
			mythunb = mycover.scaled(sizeTN, sizeTN, Qt.IgnoreAspectRatio, Qt.FastTransformation)
			label = TNLabel(self, mythunb, sizeTN,  filelist)
			label.mousePressEvent = (lambda event,  n=cpt:self.onSelectThunbnailChanged(event, n))
			self.gridthunbnails.addWidget(label, curRow, curCol)
			cpt += 1
			# position
			curCol += 1
			if curCol == maxCol:
				curCol = 0
				curRow += 1
		# build large cover
		self.numpic = 0
		self.onSelectThunbnailChanged(None, self.numpic)
				
	@pyqtSlot()
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape: 
			self.destroy()
		elif event.key() == Qt.Key_Left:
			self.onSelectThunbnailChanged(None, (self.numpic-1) % len(self.fileslist))
		elif event.key() == Qt.Key_Right:
			self.onSelectThunbnailChanged(None, (self.numpic+1) % len(self.fileslist))
	
	@pyqtSlot()
	def resizeEvent(self, event):
		if self.gridthunbnails.count()>0:
			self.replaceThunbnails(self.sizethun, self.sizethun)
			self.onSelectThunbnailChanged(None, self.numpic)
		
	def popUpMenu(self,  position):
		self.menua.exec_(self.labelcover.mapToGlobal(position))
	
	def onSelectThunbnailChanged(self, event, numpic):
		"""Display picture"""
		self.filelist = self.fileslist[numpic]
		self.numpic = numpic
		self.mycover = QPixmap(self.filelist)
		width, height, new_width, new_height = self.resizeImage(self.width()-40, self.height-(self.gridthunbnails.rowCount()*(self.sizethun+4))-70, self.mycover)
		dicover = self.mycover.scaled(new_width, new_height, Qt.IgnoreAspectRatio, Qt.FastTransformation)
		self.labelcover.setPixmap(dicover)
		self.setWindowTitle(TITL_PROG+" : [view ArtWorks: "+self.nametittle+'] {c}/{n} "{name}" A[{w}x{h}] O[{wo}x{ho}]'.format(c=str(numpic), 
																		 n=str(len(self.fileslist)), 
																		 w=new_width, 
																		 h=new_height, 
																		 name=path.basename(self.filelist), 
																		 wo=str(width), 
																		 ho=str(height)))
		self.onSelectCover()
	
	def onSelectCover(self,  event=None):
		# unselect/select thunbnail 
		for i in range(self.gridthunbnails.count()): 
			if self.gridthunbnails.itemAt(i).widget().Name == self.filelist:
				self.gridthunbnails.itemAt(i).widget().setStyleSheet("border: 2px solid red;")
			else:
				self.gridthunbnails.itemAt(i).widget().setStyleSheet("border: 2px solid white;")
		
	def replaceThunbnails(self, sizeTN, oldsizeTN):
		# replace labels thunbnails
		numCov = self.gridthunbnails.count()
		if numCov>1:
			oldmaxCol = int(self.frameGeometry().width()/(oldsizeTN+4))
			maxCol = int(self.frameGeometry().width()/(sizeTN+4))
			curRow = curCol = cptIte = oldcurRow = oldcurCol = 0
			for row in range(numCov):
				if self.gridthunbnails.itemAtPosition(oldcurRow, oldcurCol)!=0:
					# capture and clear label gridlayout
					layoutitem = self.gridthunbnails.takeAt(cptIte)
					label = layoutitem.widget()
					self.gridthunbnails.removeWidget(label)
					# resize
					label.setFixedSize(sizeTN, sizeTN)
					mypixmap = label.pixmap()
					if mypixmap.size().width()!=sizeTN or mypixmap.size().height()!=sizeTN:
						mypixmap = mypixmap.scaled(sizeTN, sizeTN, Qt.IgnoreAspectRatio, Qt.FastTransformation)
					label.setPixmap(mypixmap)
					# replace
					self.gridthunbnails.addWidget(label, curRow, curCol)
				# position old next
				oldcurRow += 1
				if oldcurCol == oldmaxCol:
					oldcurCol = 0
					oldcurRow += 1
				# position next
				curCol += 1
				if curCol == maxCol:
					curCol = 0
					curRow += 1
	
	def resizeImage(self, wmax, hmax, pic):
		# measures
		width, height = pic.size().width(), pic.size().height()
		# resize
		if ((wmax/width)<(hmax/height)):
			new_width  = wmax
			new_height = int(new_width * height / width)
		else:
			new_height = hmax
			new_width  = int(new_height * width / height)
		return(width, height, new_width, new_height)
		
	def createFileCover(self):
		file_exten = path.splitext(self.filelist)[1][1:]
		path_cover = path.join(path.dirname(self.filelist), 'cover.' +file_exten )
		self.setWindowTitle("create file {name} ".format(name=path.basename(path_cover)))
		self.mycover.save(path_cover)

# ##################################################################
class DBloadingGui(QWidget,Ui_LoadingWindow):
	def __init__(self, modsql, parent=None): 
		super(DBloadingGui,self).__init__(parent)
		self.setupUi(self)
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags(Qt.SplashScreen)
		centerWidget(self)
		# font
		font = QFont()
		font.setFamily(FONT_MAI)
		font.setFixedPitch(True)
		font.setPointSize(14)
		self.lab_logo.setFont(font)
		# tab1
		req = buildReqTCD("Category" , "Family", "DBALBUMS", "ALBUM", "1", True, modsql)
		self.buildTab(req, self.tableWid1)
		# tab2
		req = buildReqTCD("Category" , "Family", "DBALBUMS", "SIZE (GO)", "ROUND( `Size` /1024,1)", True, modsql)
		self.buildTab(req, self.tableWid2)
		# tab3
		req = buildReqTCD("Year" , "Category", "DBALBUMS", "YEAR", "1", True, modsql)
		self.buildTab(req, self.tableWid3)
		self.tableWid3.setColumnWidth(0, 38)
		# message
		basedate = buildTabFromRequest(getRequest('datedatabase', modsql))[0]
		if modsql=='sqlite':
			txt_message = modsql + " Base \nlast modified :\n"+str(basedate)
		else:
			txt_message = modsql + " Base \nlast modified :"+basedate.toString('hh:mm:ss')
		self.lab_logo.setText(TITL_PROG+"\nConnected "+txt_message)
		# quit
		self.btn_quit.clicked.connect(lambda:self.hide())
		self.show()
	
	def buildTab(self,  req, tab):
		model = QSqlQueryModel(self)
		model.setQuery(req)
		tab.setModel(model)
		tab.resizeColumnsToContents()
		tab.resizeRowsToContents()
		tab.verticalHeader().setVisible(False)
		tab.verticalHeader().setStretchLastSection(True)
		tab.horizontalHeader().setStretchLastSection(True)
	
	@pyqtSlot()
	def keyPressEvent(self, event):
		if event.key()==Qt.Key_Escape or event.key()==Qt.Key_F1:
			self.hide()

# ##################################################################
class DBAlbumsMainGui(QMainWindow,Ui_MainWindow): 
	# default value
	WIDT_PICM = WIDT_PICM
	HEIG_MAIN = HEIG_MAIN
	WIDT_MAIN = WIDT_MAIN
	COVE_SIZ  = COVE_SIZ
	COEF_ZOOM = 100
	
	def __init__(self, parent=None): 
		super(DBAlbumsMainGui,self).__init__(parent)
		self.setupUi(self)
		
		self.envits = None				# environment
		self.dbbase = None				# database connect
		self.modsql = None				# type database
		self.currow = None  			# row tab current album
		self.curAlb = None				# ID current album
		self.curMd5 = None  			# MD5 current album
		self.pathcov= None				# cover current album
		self.curTrk = None				# ID current track
		self.homMed = None				# playlist player
		self.rootDk = None				# root colume music
		self.infoBox= None				# message box
		self.maintitle = 'Loading...'	# status bar main message
		self.coveral= QPixmap(PICT_NCO)	# current cover album
		# zoom
		self.cuzoom = DBAlbumsMainGui.COEF_ZOOM
		self.sizeTN = DBAlbumsMainGui.WIDT_PICM
		self.h_main = DBAlbumsMainGui.HEIG_MAIN
		self.w_main = DBAlbumsMainGui.WIDT_MAIN
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
		
		# center
		centerWidget(self)
		
		self.setWindowTitle(TITL_PROG)
		self.resize(self.w_main, self.h_main)
		self.setWindowIcon(QIcon(WINS_ICO))
		self.setStyleSheet('QMainWindow{background-color: #D9D9D9;border: 1px solid black;} ' \
						   'QStatusBar{background-color: #D9D9D9;border: 1px solid black;}')
		
		# init combos Envt
		self.com_envt.addItems(NAME_EVT)
		self.com_envt.setCurrentIndex(CURT_EVT)
		
		# init scrore
		self.sli_scorealb.setMinimum(0)
		self.sli_scorealb.setMaximum(len(SCOR_ALBUMS)-1)
		self.btn_scorealb.setVisible(False)
		self.sli_scorealb.setValue(0)
		self.sli_scoretrk.setMinimum(0)
		self.sli_scoretrk.setMaximum(len(SCOR_TRACKS)-1)
		self.btn_scoretrk.setVisible(False)
		self.sli_scoretrk.setValue(0)
		
		# tab list no header row
		self.tbl_albums.verticalHeader().setVisible(False)
		self.tbl_tracks.verticalHeader().setVisible(False)
		
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
		self.menub.addAction("Edit %s..." % FILE__INI, lambda e=EDIT_TEXT, f=FILE__INI : runCommand(e, f))
		self.menub.addAction("Open Logs Folder...", lambda l=LOGS_PROG : openFolder(l))
		# popup albums 
		self.menua = QMenu()
		self.action_VIA = self.menua.addAction("View ArtWorks...", self.viewArtworks)
		self.action_OPF = self.menua.addAction("Open Folder...", self.getFolder)
		self.action_EXA = self.menua.addAction("Export Album...", self.exportAlbums)
		self.action_UAP = self.menua.addAction("Update Album...", self.updateAlbums)
		self.action_TAG = self.menua.addAction("Edit Tags (TagScan)...", self.openTagScan)
		
		# init player
		self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
		self.stopBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
		self.prevBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
		self.nextBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
		self.volumeDescBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
		self.volumeIncBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
		self.infoBtn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
		self.namemedia = ''
		self.currentPlaylist = QMediaPlaylist()
		self.player = QMediaPlayer()
		self.player.stateChanged.connect(self.qmp_stateChanged)
		self.player.positionChanged.connect(self.qmp_positionChanged)
		self.player.volumeChanged.connect(self.qmp_volumeChanged)
		self.player.durationChanged.connect(self.qmp_durationChanged)
		self.player.setVolume(60)
		self.seekSlider.setTracking(False)
		self.seekSliderLabel1.setText('0:00')
		self.seekSliderLabel2.setText('0:00')
		
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
		self.labelcover.mousePressEvent = self.onPressCover
		self.sli_scorealb.valueChanged.connect(self.onModifyScoreAlbum)
		self.sli_scoretrk.valueChanged.connect(self.onModifyScoreTrack)
		self.btn_scorealb.clicked.connect(self.onPressButtonEnrScoreAlbum)
		self.btn_scoretrk.clicked.connect(self.onPressButtonEnrScoreTrack)
		# link buttons to media player
		self.seekSlider.sliderMoved.connect(self.seekPosition)
		self.playBtn.clicked.connect(self.playHandler)
		self.stopBtn.clicked.connect(self.stopHandler)
		self.volumeDescBtn.clicked.connect(self.decreaseVolume)
		self.volumeIncBtn.clicked.connect(self.increaseVolume)
		self.prevBtn.clicked.connect(self.prevItemPlaylist)
		self.nextBtn.clicked.connect(self.nextItemPlaylist)
		self.infoBtn.clicked.connect(self.displaySongInfo)
		
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
		min = DBAlbumsMainGui.COEF_ZOOM-(nbstep*abs(degre.y()))
		max = DBAlbumsMainGui.COEF_ZOOM+(nbstep*abs(degre.y()))
		if self.cuzoom < min or self.cuzoom > max:
			self.cuzoom = DBAlbumsMainGui.COEF_ZOOM
			self.sizeTN = DBAlbumsMainGui.WIDT_PICM
		# redisplay zoom thunbnails
		if self.sizeTN<oldsizeTN:
			# resize
			self.tableMdlAlb.replaceThunbnails(self.sizeTN, oldsizeTN)
		elif self.sizeTN>oldsizeTN:
			# rebuild
			self.tableMdlAlb.displayThunbnails()
	
	@pyqtSlot()
	def resizeEvent(self, event):
		if self.gridthunbnails.count()>0:
			self.tableMdlAlb.replaceThunbnails(self.sizeTN, self.sizeTN)
	
	@pyqtSlot()
	def closeEvent(self, event):
		"""Quit."""
		response = QMessageBox.question(self, "Confirmation", "Exit DBAlbums ?",QMessageBox.Yes,QMessageBox.No)
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
		if category!=DISP_CJOKER and category!=None:
			print('category Filter')
			self.tableMdlAlb.setFilter('Category', self.com_category.currentText())
			print("Category   : "+str(self.com_category.currentText())+"'")
			print("txt search : "+self.lin_search.text())
			#print("search In  : "+(self.chb_searchtracks.isChecked()))
	
	def updateStatusBar(self, message, t=0): 
		self.statusBar().showMessage(message, t)

	def updateGaugeBar(self, purcent, message=None, t=0): 
		if message!=None:
			self.updateStatusBar(message, t)
		self.gaugeBar.setValue(purcent)
		self.update()
		if purcent==1:
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
				self.coveral= QPixmap(PICT_NCO)
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
				self.setWindowTitle('{prog} : Connected base {base} [{mode}] at {hour}'.format(prog = TITL_PROG,
																								mode =self.modsql,
																								base = self.envits,
																								hour = curdate))
				# fill model/tree albums list/thunbnails
				req = getRequest('albumslist', self.modsql)
				self.tableMdlAlb = ModelTbl(self, req, self.gridthunbnails, A_COLNAME, A_POSITIO)
				self.tbl_albums.setModel(self.tableMdlAlb)
				self.tbl_albums.resizeColumnsToContents()
				self.tbl_albums.resizeRowsToContents()
				# data ?
				if self.tableMdlAlb.rowCount()>0:				
					# fill combos
					self.com_category.addItems(self.tableMdlAlb.datacombos('Category'))
					self.com_family.addItems(self.tableMdlAlb.datacombos('Family'))
					self.com_label.addItems(self.tableMdlAlb.datacombos('Label'))
					self.com_year.addItems(self.tableMdlAlb.datacombos('Year'))
					# fill thunbnails
					self.tableMdlAlb.displayThunbnails()
					# autocompletion list
					autoList = buildTabFromRequest(getRequest('autocompletion', self.modsql))
					self.com_autcom = QCompleter(autoList, self.lin_search)
					self.com_autcom.setCaseSensitivity(Qt.CaseInsensitive)
					self.lin_search.setCompleter(self.com_autcom)
					# select default row
					if not refresh:
						self.currow = 0
					self.tbl_albums.selectRow(self.currow)
					if self.focusWidget()==self.tbl_albums:
						self.tbl_albums.setFocus()
					else:
						self.lin_search.setFocus()
					# display album
					self.currow = self.tbl_albums.currentIndex().row()
					self.displayAlbum()
					# build message
					txt_siz = str(int(self.tableMdlAlb.getSum('Size')/1024)) +' Go'
					cpt_len = self.tableMdlAlb.getSum('Length')
					cpt_cds = self.tableMdlAlb.getSum('Qty_CD')
					cpt_trk = self.tableMdlAlb.getSum('Qty_Tracks')
					if int(((cpt_len/60/60)/24)*10)/10 < 1:
						# seoncd -> Hours
						txt_len = str(int(((cpt_len/60/60))*10)/10) + ' Hours'
					else:
						# seoncd -> Days
						txt_len = str(int(((cpt_len/60/60)/24)*10)/10) + ' Days'
					message = "Search Result \"{sch}\" :  {alb} | {trk} | {cds} | {siz} | {dur}".format(alb = displayCounters(self.tableMdlAlb.rowCount(), 'Album'),
																										cds =  displayCounters(cpt_cds, 'CD'),
																										trk = displayCounters(cpt_trk, 'Track'),
																										siz = txt_siz,
																										dur = txt_len, 
																										sch = '{sch}')
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
					self.coveral= QPixmap(PICT_NCO)
					self.labelcover.setPixmap(self.coveral)
					# init scrore
					self.sli_scorealb.setValue(0)
					self.sli_scoretrk.setValue(0)
				# display message
				txt_sch = (self.lin_search.text() if len(self.lin_search.text())>0 else 'all')
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
				curthu=self.gridthunbnails.itemAt(i).widget()
				break
		# move scroll to widget
		self.scrollArea.ensureWidgetVisible(curthu)
		
		# fill tracks
		req = (getRequest('trackslist', self.modsql)).format(id=self.curAlb)
		self.tableMdlTrk = ModelTbl(self, req, None, T_COLNAME, T_POSITIO)
		self.tbl_tracks.setModel(self.tableMdlTrk) 
		self.tbl_tracks.resizeColumnsToContents()
		self.tbl_tracks.resizeRowsToContents()

		# fill label
		counter = self.tableMdlAlb.rowCount()
		cpt_len = self.tableMdlTrk.getSum('TAG_length')
		albumnamet, infoslabel = albumNameExtract(self.albumname, str(self.tableMdlAlb.getData(self.currow, 'Label').value()), 
																str(self.tableMdlAlb.getData(self.currow, 'ISRC').value()),
																str(self.tableMdlAlb.getData(self.currow, 'Qty_CD').value()))
		txt_album = albumnamet + "\n{year} • {tracks} • {dur} • {cd} • {art}\n{lab}".format(year=str(self.tableMdlAlb.getData(self.currow, 'Year').value()),
																tracks = displayCounters(counter, 'track'),
																dur = displayCounters(int(((cpt_len/60)*10)/10),'min'),
																cd = displayCounters(self.tableMdlAlb.getData(self.currow, 'Qty_CD').value(), 'CD'),
																art = displayCounters(self.tableMdlAlb.getData(self.currow, 'Qty_covers').value(), 'ArtWork'),
																lab = infoslabel)
		self.lab_album.setText(txt_album)
				
		# fill score album
		self.sli_scorealb.setValue(self.ScoreAlbum)
		self.lab_scorealb.setText(displayStars(self.ScoreAlbum, SCOR_ALBUMS))
		
		# fill cover
		self.pathcov = self.tableMdlAlb.getData(self.currow, 'Cover').value()
		self.coveral = self.tableMdlAlb.buildCover(self.pathcov, self.curMd5, DBAlbumsMainGui.COVE_SIZ)
		pixmap = QPixmap(self.coveral)
		self.labelcover.setPixmap(pixmap)
		
		# fill play medias only is not playing
		if self.player.state() != QMediaPlayer.PlayingState:
			if self.currentPlaylist.mediaCount()>0:
				self.player.stop()
				self.stopHandler()
				self.currentPlaylist.removeMedia(0, self.currentPlaylist.mediaCount())
			self.curtrk = self.tbl_tracks.currentIndex().row()
			self.homMed = self.tableMdlTrk.getMedias()
			self.addMedialist()
			self.currentPlaylist.setCurrentIndex(self.curtrk)
			self.playHandler()
		
		# select track default
		if self.tableMdlTrk.rowCount()>0:
			self.tbl_tracks.selectRow(0)
			self.curTrk = 0
		self.displaytrack()
	
	def displaytrack(self):
		"""Display info current select track."""
		if self.tableMdlTrk.rowCount()>0:
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
			else:
				self.btn_scorealb.setVisible(False)
	
	def onModifyScoreTrack(self,  event):
		"""Modify Score Track."""
		indexes = self.tbl_tracks.selectedIndexes()
		if len(indexes) > 0:
			self.lab_scoretrk.setText(displayStars(self.sli_scoretrk.value(), SCOR_TRACKS))
			if self.ScoreTrack != self.sli_scoretrk.value():
				self.btn_scoretrk.setVisible(True)
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

	def onSelectTrackChanged(self, event,  indexes=None):
		"""Select Track."""
		indexes = self.tbl_tracks.selectedIndexes()
		if len(indexes) > 0 and self.curtrk != self.tbl_tracks.currentIndex().row():
			self.curtrk = self.tbl_tracks.currentIndex().row()
			self.currentPlaylist.setCurrentIndex(self.curtrk)
			self.displaytrack()

	def onPressCover(self,  event):
		"""Display large cover MD5."""
		if self.pathcov!=None:
			if self.pathcov[0:len(TEXT_NCO)] != TEXT_NCO:
				CoverViewGui(self.coveral, self.albumname, self.h_main, self.h_main)
				
	def viewArtworks(self):
		"""views artworks covers storage."""
		ArtworksGui(self.AlbumPath, self.albumname, self.pathcover, self.h_main, self.h_main, self.sizeTN)
		
	def onPressButtonEnrScoreAlbum(self):
		"""Update Score Album."""
		self.ScoreAlbum = self.sli_scorealb.value()
		self.lab_scorealb.setText(displayStars(self.sli_scorealb.value(), SCOR_ALBUMS))
		# Mysql
		updateBaseScore(self.ScoreAlbum, self.curAlb, getRequest('updatescorealbum', self.modsql))
		# Treeview
		self.tableMdlAlb.refresh()
		# Button
		self.btn_scorealb.setVisible(False)
	
	def onPressButtonEnrScoreTrack(self):
		"""Update Score Track."""
		self.ScoreTrack = self.sli_scoretrk.value()
		self.lab_scoretrk.setText(displayStars(self.sli_scoretrk.value(), SCOR_TRACKS))
		# Mysql
		updateBaseScore(self.ScoreTrack, self.curtrk, getRequest('updatescoretrack', self.modsql))
		# Treeview
		self.tableMdlTrk.refresh()
		# Button
		self.btn_scoretrk.setVisible(False)
	
	def playMediasAlbum(self, event):
		"""play album tracks."""
		indexes = self.tbl_tracks.selectedIndexes()
		if len(indexes) > 0:
			# playing ? reset
			if self.currentPlaylist.mediaCount()>0:
				self.player.stop()
				self.stopHandler()
				self.currentPlaylist.removeMedia(0, self.currentPlaylist.mediaCount())
			self.curtrk = self.tbl_tracks.currentIndex().row()
			self.homMed = self.tableMdlTrk.getMedias()
			self.addMedialist()
			self.currentPlaylist.setCurrentIndex(self.curtrk)
			self.playHandler()
			self.player.play()
	
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
		if len(listRows)==1:
			self.currow = self.tbl_albums.currentIndex().row()
			self.displayAlbum()
			self.action_TAG.setEnabled(True)
			self.updateTextPopupAlbum(self.tbl_albums.viewport().mapToGlobal(position))
		else:
			if len(indexes)>1:
				self.action_VIA.setEnabled(False)
				self.action_OPF.setEnabled(False)
				self.action_EXA.setText("Export "+ displayCounters(len(listRows), 'Album')+"cover/csv...")
				self.action_UAP.setText("Update "+ displayCounters(len(listRows), 'Album') +"...")
				self.action_TAG.setEnabled(False)
				self.menua.exec_(self.tbl_albums.viewport().mapToGlobal(position))
	
	def popUpTNAlbums(self,  position):
		"""Mennu Albums."""
		self.updateTextPopupAlbum(self.scrollArea.mapToGlobal(position))

	def updateTextPopupAlbum(self, position):
		if self.tableMdlAlb.getData(self.currow, 'Qty_covers').value()==0 or not(path.exists(self.AlbumPath)):
			self.action_VIA.setEnabled(False)
		else:
			self.action_VIA.setEnabled(True)
		# path exist ?
		if not(path.exists(self.AlbumPath)):
			self.action_OPF.setEnabled(False)
		else:
			self.action_OPF.setEnabled(True)
		self.action_EXA.setText("Export cover/csv '"+ self.albumname[:15] + "...'")
		self.action_UAP.setText("Update Album (powershell): "+ self.albumname[:15] + "...")
		self.menua.exec_(position)
	
	def getFolder(self):
		"""Open album folder."""
		openFolder(self.AlbumPath)
		
	def openTagScan(self):
		"""Open program TAGs. edit """
		runCommand(TAGS_SCAN, self.AlbumPath)
		
	def buildInvent(self, category=None):
		"""Execute powershell Script update all albums infos."""
		if 'LOSSLESS' in self.envits:
			filescript = PWSH_SCRI.format(mod='LOSSLESS')
		else:
			filescript = PWSH_SCRI.format(mod='MP3')
		if category != None:
			exeprocess, params = buildCommandPowershell(filescript, '-Envt', self.envits, '-Collections', category)
		else:
			exeprocess, params = buildCommandPowershell(filescript, '-Envt', self.envits)
		ProcessGui(exeprocess, params, 'Update Base '+self.envits)

	def importFoobar(self):
		"""Foobar2000 playlists operations."""
		# import fpl playlist to mysql DBFOOBAR
		numtracks = foobarMajDBFOOBAR(self, FOOB_PLAY)
		if numtracks == 0:
			QMessageBox.critical(self, 'Foobar2000 playlists operations', 'Problem import files fpl playlist from : '+FOOB_PLAY)
		else:
			# synchro score sql
			execSqlFile(self, FOOB_UPSC , 9)
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
			ProcessGui(exeprocess, params, 'Update '+ displayCounters(len(listSelect), "Album "))
			self.statusBar().showMessage('Foobar2000 playlists finished', 7000)
	
	def createLocalBase(self):
		"""Create base Sqlite."""
		filename = BASE_SQLI.format(envt=self.envits+'_SQLITE')
		# remove if exist
		if path.isfile(filename): 
			remove(filename)
		logname = QTime.currentTime().toString('yymmddhhmmss') + "_COPY_DATABASE_TO_SQLITE_" + self.envits + ".log"
		copyDatabaseInvent(self, self.dbbase,  filename, path.join(LOGS_PROG, logname))
		self.updateStatusBar("Create Database SQLite/nCreate Database SQLite :"+filename+" Sucessfull", 7000)
	
	def exportAlbums(self):
		"""Export file cover or list albums select in grid."""
		indexes = self.tbl_albums.selectedIndexes()
		if len(indexes) > 0:
			filename = QFileDialog.getSaveFileName(self, 
												"Export from CSV File list or cover jpeg Files", 
												getcwd(), 
												"Images (*.jpg);;CSV files (*.csv)")
			if filename==None: return
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
			elif extension=='.jpg':
				# extract base64\mysql to file JPEG 
				for ind in listRows:
					filecover = path.join(path.dirname(filename), self.tableMdlAlb.getData(ind, 'Name').value())
					extension = ((self.tableMdlAlb.getData(ind, 'Cover').value())[-4:]).replace('.','')
					filecover = filecover+'.'+extension
					buildFileCover(filecover, self.tableMdlAlb.getData(ind, 'MD5').value())	
				self.statusBar().showMessage('Export covers Albums /n Create covers Sucessfull to :'+path.dirname(filename), 7000)
				openFolder(path.dirname(filename))
	
	# player Audio functions	
	def playHandler(self):
		if self.player.state() == QMediaPlayer.PlayingState:
			self.player.pause()
			message = (' [Paused at position %s]'%self.seekSliderLabel1.text())
			self.updateStatusBar(self.namemedia+message)
		else:
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
			if self.player.volume()!= None and self.player.state() == QMediaPlayer.PlayingState:
				message = ' [Volume %d]'%self.player.volume()
				self.updateStatusBar(self.namemedia+message)
	
	def stopHandler(self):
		if self.player.state() == QMediaPlayer.PlayingState:
			self.stopState = True
			self.player.stop()
		elif self.player.state() == QMediaPlayer.PausedState:
			self.player.stop()
		elif self.player.state() == QMediaPlayer.StoppedState:
			pass
		if self.player.volume()!= None and self.player.state() == QMediaPlayer.PlayingState:
			self.updateStatusBar(self.namemedia+(' [Stopped]'))
	
	def qmp_stateChanged(self):
		if self.player.state() == QMediaPlayer.StoppedState:
			self.player.stop()
		# buttons icon play/pause change
		if self.player.state() == QMediaPlayer.PlayingState:
			self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
		else:
			self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
	
	def qmp_positionChanged(self, position):
		# update position slider
		self.seekSlider.setValue(position)
		# update the text label
		self.seekSliderLabel1.setText('%d:%02d'%(int(position/60000),int((position/1000)%60)))
	
	def seekPosition(self, position):
		sender = self.sender()
		if isinstance(sender,QSlider):
			if self.player.isSeekable():
				self.player.setPosition(position)
	
	def qmp_volumeChanged(self):
		if self.player.volume()!=None:
			message = (' [Playing at Volume %d]'%(self.player.volume()))
			if self.namemedia!='':
				self.updateStatusBar(self.namemedia+message)
			else:
				self.updateStatusBar("Initialisation player "+message, 5000)
		
	def qmp_durationChanged(self, duration):
		self.seekSlider.setRange(0,duration)
		self.seekSliderLabel2.setText('%d:%02d'%(int(duration/60000),int((duration/1000)%60)))
		nummedia = self.currentPlaylist.mediaCount()
		curmedia = self.currentPlaylist.currentIndex()
		#artist = self.player.metaData(QMediaMetaData.Author)
		#tittle = self.player.metaData(QMediaMetaData.Title)
		self.namemedia = path.basename(self.homMed[curmedia])
		self.namemedia = '[%02d/%02d'%(curmedia+1,nummedia) + '] "'+ self.namemedia + '"'
		self.playBtn.setToolTip(self.namemedia)
		message = (' [Playing at Volume %d]'%(self.player.volume()))
		if self.player.volume()!=None and self.player.state() == QMediaPlayer.PlayingState:
			self.updateStatusBar(self.namemedia+message)
	
	def increaseVolume(self):
		vol = self.player.volume()
		vol = min(vol+5,100)
		self.player.setVolume(vol)
	
	def decreaseVolume(self):
		vol = self.player.volume()
		vol = max(vol-5,0)
		self.player.setVolume(vol)
	
	def prevItemPlaylist(self):
		self.player.playlist().previous()
		if self.currentPlaylist.currentIndex()==-1:
			self.player.playlist().previous()
	
	def nextItemPlaylist(self):
		self.player.playlist().next()
		if self.currentPlaylist.currentIndex()==-1:
			self.player.playlist().next()
	
	def addMedialist(self):
		for media in self.homMed:
			self.currentPlaylist.addMedia(QMediaContent(QUrl.fromLocalFile(media)))
	
	def displaySongInfo(self):
		# extract datas
		metaDataKeyList = self.player.availableMetaData()
		fullText = '<table class="tftable" border="0">'
		for key in metaDataKeyList:
			value = str(self.player.metaData(key)).replace("'","").replace("[","").replace("]","")
			if key=='Duration':
				value = '%d:%02d'%(int(int(value)/60000),int((int(value)/1000)%60))
			fullText = fullText + '<tr><td>' + key + '</td><td>' + value + '</td></tr>'
		fullText = fullText + '</table>'
		# re-init
		if self.infoBox != None:
			self.infoBox.destroy()
		# infos box
		self.infoBox = QMessageBox(self)
		self.infoBox.setWindowTitle('Detailed Song Information')
		self.infoBox.setTextFormat(Qt.RichText)
		self.infoBox.addButton('OK',QMessageBox.AcceptRole)
		self.infoBox.setText(fullText)
		self.infoBox.show()

if __name__ == '__main__':
	app = QApplication(argv)
	DB = DBAlbumsMainGui()
	DB.show()
	rc = app.exec_() 
	exit(rc)

