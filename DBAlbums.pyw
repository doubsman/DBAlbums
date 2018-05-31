#! /usr/bin/python
# coding: utf-8

""" DBAlbums History Version : Doubsman dev.
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
1.04 constantes
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

from sys import platform, argv, executable
from os import system, path, getcwd, name as osname, remove, walk, chdir
from tkinter import (Tk, Toplevel, Label, Button, Checkbutton, Entry, Canvas, Grid, 
					Frame, Scale, Menu, Text, StringVar, IntVar, FALSE, TRUE, 
					SOLID, FLAT, N, S, W, E, X, Y, RIGHT, LEFT, 
					BOTH, TOP, END, BOTTOM, VERTICAL, HORIZONTAL, INSERT, ALL)
from tkinter.filedialog import asksaveasfile
from tkinter.ttk import Treeview, Combobox, Scrollbar, Separator, Style
from tkinter.font import Font
from tkinter.messagebox import askyesno, showinfo
from multiprocessing import Process
from threading import Thread
from subprocess import Popen, PIPE
from queue import Queue, Empty
from pymysql import connect as connectmysql		#mysql
from sqlite3 import connect as connectsqlite3	#sqlite
from pypyodbc import connect as connectmssql	#sqlserver
from logging import DEBUG, basicConfig, info
from datetime import datetime
from time import sleep
from PIL import Image, ImageTk, ImageDraw, ImageFont
from csv import writer, QUOTE_ALL
from io import BytesIO
from base64 import b64decode, decodestring
from hashlib import md5
from configparser import ConfigParser
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist#, QMediaMetaData
from PyQt5.QtWidgets import (QApplication, QHBoxLayout,  QPushButton, QSlider, 
							QLabel, QMainWindow, QStyle, QWidget, QMessageBox)
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
							"FROM DBALBUMS ORDER BY Date_Insert DESC"
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
					"VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
	return request


###################################################################
# FUNCTIONS
def centerWindows(win):
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

def buildIco(Gui):
	"""Icon windows or linux/mac."""
	if "nt" == osname:
		#windows
		Gui.iconbitmap(WINS_ICO)
	else:
		#linux : os mac non prévu
		Gui.iconbitmap("@"+UNIX_ICO)
		#Gui.tk.call('wm', 'iconphoto', Gui._w, myico)

def initGuiTK(guiTK, w, h, resizew=False, resizeh=False, topmost=False):
	"""Size and center GUI tkinter."""
	guiTK.geometry("{w}x{h}".format(w=w,h=h))
	guiTK.resizable(width=resizew, height=resizeh)
	guiTK.minsize(width=w, height=h)
	guiTK.attributes('-topmost', topmost)
	buildIco(guiTK)
	centerWindows(guiTK)
	guiTK.focus_set()

def connectDatabase(envt):
	"""Connect base MySQL/Sqlite."""
	con = None
	# ENVT
	readIni = ConfigParser()
	readIni.read(FILE__INI)
	MODE_SQLI = readIni.get(envt, 'type')
	# Racine Media
	BASE_RAC = r'' + readIni.get(envt, 'raci')
	if MODE_SQLI == 'sqlite':
		try:
			# SQLITE
			con = connectsqlite3(BASE_SQLI.format(envt=envt))
		except:
			print('connect Sqlite Fail '+BASE_SQLI.format(envt=envt))
	if MODE_SQLI == 'mysql':
		BASE_SEV = readIni.get(envt, 'serv')
		BASE_USR = readIni.get(envt, 'user')
		BASE_PAS = readIni.get(envt, 'pass')
		BASE_NAM = readIni.get(envt, 'base')
		try:
			# MYSQL
			con = connectmysql( host=BASE_SEV, 
								user=BASE_USR, 
								passwd=BASE_PAS, 
								db=BASE_NAM,
								charset='utf8',
								use_unicode=True)
			#con.autocommit(True)
		except Exception:
			pass
			# SQLite: offline mode
			print('connect Mssql server Fail '+BASE_SEV+', change mode to SQLLite')
			MODE_SQLI = 'sqlite'
			con = connectsqlite3(BASE_SQLI.format(envt=(envt+'_SQLITE')))
	if MODE_SQLI == 'mssql':
		BASE_SEV = readIni.get(envt, 'serv')
		BASE_USR = readIni.get(envt, 'user')
		BASE_PAS = readIni.get(envt, 'pass')
		BASE_NAM = readIni.get(envt, 'base')
		try:
			# MSSQL
			con = connectmssql('Driver={SQL Server}; Server='+BASE_SEV+';Database='+BASE_NAM+';uid='+BASE_USR+';pwd='+BASE_PAS)
		except Exception:
			pass
			# SQLite: offline mode
			print('connect Mssql server Fail '+BASE_SEV+', change mode to SQLLite')
			MODE_SQLI = 'sqlite'
			con = connectsqlite3(BASE_SQLI.format(envt=(envt+'_SQLITE')))
	return con, MODE_SQLI, BASE_RAC

def copyDatabaseInvent(conMySQL, BaseNameSQLite, BarGauge, logname):
	basicConfig(filename=logname,
							filemode='a',
							format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
							datefmt='%H:%M:%S',
							level=DEBUG)
	info ('Create/Update Database '+BaseNameSQLite)
	BarGauge.open()
	con = connectsqlite3(BaseNameSQLite)
	NAME_TABL = "DBALBUMS"
	BarGauge.update(0.05, 'Create Table '+NAME_TABL+' in progress...')
	info ('Create '+NAME_TABL)
	Tabs =  buildTabFromRequest(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()    
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE DBALBUMS(ID_CD INTEGER PRIMARY KEY AUTOINCREMENT, MD5 TEXT, Family TEXT, Category TEXT, Position1 TEXT, Position2 TEXT, Name TEXT, Label TEXT, ISRC TEXT, Year TEXT, Qty_CD INT,Qty_Cue INT,Qty_CueERR INT, Qty_repMusic INT, Qty_Tracks INT, Qty_audio INT, Typ_Audio TEXT, Qty_repCover, Qty_covers, Cover TEXT, Path TEXT, Size INT, Duration TEXT, Length TEXT, Typ_Tag TEXT, Date_Insert DATETIME, Date_Modifs DATETIME, RHDD_Modifs DATETIME, Score INT, Statut TEXT)")
		cur.executemany("INSERT INTO DBALBUMS VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", Tabs)
		cur.execute("CREATE INDEX DBALBUMS_ndx_Date_Insert ON DBALBUMS(Date_Insert)")
		con.commit() 
	
	NAME_TABL = "DBTRACKS"
	BarGauge.update(0.25, 'Create Table '+NAME_TABL+' in progress...')
	info ('Create '+NAME_TABL)
	Tabs =  buildTabFromRequest(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()    
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE DBTRACKS(ID_CD INT,ID_TRACK INTEGER PRIMARY KEY AUTOINCREMENT, Family TEXT, Category TEXT, Position1 TEXT, Position2 TEXT, REP_Album TEXT, REP_Track TEXT,FIL_Track TEXT,TAG_Exten TEXT,TAG_Album TEXT, TAG_Albumartists TEXT, TAG_Year TEXT,TAG_Disc INT, TAG_Track INT,ODR_Track TEXT, TAG_Artists TEXT,TAG_Title TEXT,TAG_Genres TEXT,TAG_Duration TEXT,TAG_length TEXT,Score INT,Date_Insert DATETIME, Statut TEXT, FOREIGN KEY(ID_CD) REFERENCES DBALBUMS(ID_CD))")
		cur.executemany("INSERT INTO DBTRACKS VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", Tabs)
		cur.execute("CREATE INDEX DBTRACKS_ndx_idcd ON DBTRACKS(ID_CD)")
	con.commit() 
	
	NAME_TABL = "DBFOOBAR"
	BarGauge.update(0.5, 'Create Table '+NAME_TABL+' in progress...')
	info ('Create '+NAME_TABL)
	Tabs =  buildTabFromRequest(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE {t}(ID_FOO INTEGER PRIMARY KEY AUTOINCREMENT, MD5 TEXT, Name TEXT, Path TEXT, FIL_Track TEXT, Playlist TEXT, TAG_Album TEXT, TAG_Artists TEXT, TAG_Title TEXT, Date_insert TIMESTAMP DEFAULT CURRENT_TIMESTAMP)".format(t=NAME_TABL))
		cur.executemany("INSERT INTO {t} VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(t=NAME_TABL), Tabs)
		cur.execute("CREATE INDEX DBFOOBAR_ndx_FIL_Track ON DBFOOBAR(FIL_Track)")
	con.commit() 
	
	NAME_TABL = "DBFOOBOR"
	BarGauge.update(0.6, 'Create Table '+NAME_TABL+' in progress...')
	info ('Create '+NAME_TABL)
	Tabs =  buildTabFromRequest(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE {t}(FIL_Track TEXT, FIL_TrackM TEXT)".format(t=NAME_TABL))
		cur.executemany("INSERT INTO {t} VALUES(?, ?)".format(t=NAME_TABL), Tabs)
	con.commit() 
	
	NAME_TABL = "DBCOVERS"
	BarGauge.update(0.75, 'Create Table '+NAME_TABL+' in progress...')
	info ('Create '+NAME_TABL)
	Tabs =  buildTabFromRequest(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE {t}(MD5 TEXT, Cover64 BLOB, MiniCover64 BLOB)".format(t=NAME_TABL))
		cur.executemany("INSERT INTO {t} VALUES(?, ?, ?)".format(t=NAME_TABL), Tabs)
		cur.execute("CREATE UNIQUE INDEX DBCOVERS_ndx_md5 ON DBCOVERS(MD5)")
	con.commit() 
	
	NAME_TABL = "VW_AUTOCOMPLETION"
	BarGauge.update(0.9, 'Create Table '+NAME_TABL+' in progress...')
	info ('Create '+NAME_TABL)
	Tabs =  buildTabFromRequest(conMySQL, "SELECT * FROM "+NAME_TABL)
	with con:
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS {t}".format(t=NAME_TABL))
		cur.execute("CREATE TABLE {t}(ID_CD INT, Synthax TEXT)".format(t=NAME_TABL))
		cur.executemany("INSERT INTO {t} VALUES(?, ?)".format(t=NAME_TABL), Tabs)
	con.commit() 
	
	BarGauge.update(1, 'Create DataBase Completed: '+BaseNameSQLite)
	info("test")
	with con:
		cur = con.cursor()    
		cur.execute("SELECT * FROM VW_AUTOCOMPLETION;")
	con.commit()
	row = cur.fetchall()
	info(row[0])
	
	con.close()
	BarGauge.close()

def getListColumns(con, req, MODE_SQLI):
	"""List columns from request."""
	if MODE_SQLI == 'mssql':
		req = 'SELECT TOP 0 ' + req[7:]
	else:
		req = req[:-1] + " LIMIT 0"
	cur = con.cursor()
	cur.execute(req)
	col_names = list(map(lambda x: x[0], cur.description))
	cur.close()
	return col_names

def updateBaseScore(con, score, id, req):
	"""Maj Mysql table Albums."""
	req = req.format(score=score, id=id)
	with con.cursor() as curs:
		curs.execute(req)
	curs.close()
	con.commit()

def buildTabFromRequest(con, req):
	"""Select to memory list."""
	cur = con.cursor()
	cur.execute(req)
	rows = cur.fetchall()
	cur.close()
	return rows

def buildListFromRequest(con, req, joker=''):
	""""Select to Tuple memory list."""
	TLabs = buildTabFromRequest(con, req)
	TMods = []
	TMods.append(joker)
	for row in TLabs:
		TMods.append(''.join(map(str,row)))
		#TMods.insert(0,row[0])
	return TMods

def buildDictFromRequest(con, req):
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

def buildReqTCD(con, group, column, tableName, TDCName='TDC', TDCSum=1, LineSum=True, MODE_SQLI='mysql'):
	"""build request Pivot table compatible sqlite, mysql, SQLserver."""
	# Collections
	req = "SELECT `{column}` FROM {tableName} GROUP BY `{column}` ;".format(tableName=tableName,column=column)
	if MODE_SQLI == 'mssql': req = req.replace(' `',' [').replace('` ','] ')
	col_names = buildTabFromRequest(con, req)
	# sum/collections
	lstcols = ''
	ReqTDC = "(SELECT `{group}` AS '{TDCName}' ,\n".format(group=group,TDCName=TDCName)
	for col_name in col_names:
		ReqTDC += "    SUM(CASE WHEN `{column}` = '{col_name}' THEN {TDCSum} ELSE 0 END) AS `{col_name}` ,\n".format(column=column,TDCSum=TDCSum,col_name=col_name[0])
		lstcols+= " `{col_name}` ,".format(col_name=col_name[0])
	ReqTDC += "    SUM({TDCSum}) AS 'TOTAL' FROM {tableName} GROUP BY `{group}` \n".format(tableName=tableName,TDCSum=TDCSum,group=group)
	# sum global
	if LineSum:
		ReqTDC += " UNION \nSELECT 'TOTAL', \n"
		for col_name in col_names:
			ReqTDC += "    SUM(CASE WHEN `{column}` = '{col_name}' THEN {TDCSum} ELSE 0 END),\n".format(column=column,TDCSum=TDCSum,col_name=col_name[0])
		ReqTDC += "    SUM({TDCSum}) FROM {tableName}\n".format(tableName=tableName,TDCSum=TDCSum)
	# order by total is last line
	ReqTDC += ") tdc ORDER BY 'TOTAL';"
	# select column
	ReqTDC = "SELECT `"+TDCName+"` ,"+lstcols+" `TOTAL` FROM \n" + ReqTDC
	# replace ` for [] sqlserver
	if MODE_SQLI == 'mssql': ReqTDC = ReqTDC.replace(' `',' [').replace('` ','] ')
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
				bar.update(counter/nbop, "Exec :"+line.replace('--' ,''))
			continue
		statement = statement + line
		if len(line)>2 and line[-2] == ';':
			counter = counter +1
			try:
				cur.execute(statement)
				con.commit()
			except Exception as  e:
				print ("\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args)))
			statement = ""
	cur.close()
	bar.close()

def buildTree(frame, colNames, colWidth, line, scroll=False, align=W):
	"""Build Columns treeview."""
	tree = Treeview(frame, height=line, columns=colNames, show="headings")
	tree["columns"] = colNames
	counter = 0
	for col_name in colNames:
		tree.heading(col_name, text=col_name.title(),command=lambda c=col_name: treeviewSortColumn(tree, c, False))
		tree.column(col_name, minwidth=colWidth[counter], width=colWidth[counter], anchor=align)
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
	return tree

def treeviewSortColumn(tv, col, reverse):
	"""sort column treeview."""
	l = [(tv.set(k, col), k) for k in tv.get_children('')]
	l.sort(reverse=reverse)
	# rearrange items in sorted positions
	for index, (val, k) in enumerate(l):
		tv.move(k, '', index)
	# reverse sort next time
	tv.heading(col, command=lambda c=col: treeviewSortColumn(tv, c, not reverse))

def displayCounters(num = 0, text = '' ):
	"""format 0 000 + plural."""
	strtxt = " %s%s" % (text, "s"[num==1:])
	if num > 9999:
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

def buildCover(con, pathcover, md5, namerequest='cover'):
	"""Get base64 picture cover."""
	if pathcover[0:len(TEXT_NCO)] == TEXT_NCO: 
		# no cover : blank
		monimage = Image.open(PICT_NCO)
	else:
		# cover base64/mysql
		req = (getRequest(namerequest)).format(MD5=md5)
		try:
			coverb64 = buildTabFromRequest(con, req)
			monimage = Image.open(BytesIO(b64decode(coverb64[0][0])))
		except:
			pass
			showinfo(TITL_PROG,'Err thunbnail read :'+pathcover)
			monimage = Image.open(PICM_NCO)
	return (monimage)

def buildFileCover(con, filenamecover, md5):
	"""Build cover base64/mysql to file."""
	req = (getRequest('cover')).format(MD5=md5)
	coverb64 = buildTabFromRequest(con, req)
	cover = open(filenamecover, "wb")
	content = decodestring(coverb64[0][0])
	cover.write(content)
	cover.close()

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
	except:
		pass
		print('#problem : '+file_path)
	return(listfiles)

def foobarMajDBFOOBAR(con, BarGauge, folder):
	# fill DBFOOBAR
	footracks = foobarBuildTracksList(folder)
	numtracks = len(footracks)
	counter = 0
	BarGauge.open('import playlists ('+str(numtracks)+' Tracks) Foobar in progress...')
	request = getRequest('playlistfoobar')
	for footrack in footracks:
		with con.cursor() as curs:
			curs.execute(request, footrack)
			curs.close()
		con.commit()
		counter = counter +1
		BarGauge.update(counter/numtracks)
	BarGauge.close()
	return(numtracks)

def runCommand(prog, *argv):
	"""Execut a program no wait, no link."""
	command = [prog]
	for arg in argv:
		command += (arg,)
	Popen(command, close_fds=True)

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

def buildCommandPowershell(script, *argv):
	command = [r'powershell.exe',
				'-ExecutionPolicy', 'RemoteSigned',
				'-WindowStyle','Hidden',
				'-File', 
				script]
	for arg in argv:
		command += (arg,)
	return command


###################################################################
# PLAYER PQT5 V2
class playerAudioAlbum(QMainWindow):
	def __init__(self, listemedia, position=1, x=0, y=0):
		super().__init__()
		
		# Init main windows
		self.move(x, y)
		self.setFixedSize(700, 40)
		self.setWindowIcon(QIcon(WINS_ICO))
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setStyleSheet('QMainWindow{background-color: darkgray;border: 1px solid black;} ' \
						   'QMessageBox{background-color: darkgray;border: 1px solid black;}')
		
		# Init Player
		self.namemedia = ''
		self.currentPlaylist = QMediaPlaylist()
		self.player = QMediaPlayer()
		self.player.stateChanged.connect(self.qmp_stateChanged)
		self.player.positionChanged.connect(self.qmp_positionChanged)
		self.player.volumeChanged.connect(self.qmp_volumeChanged)
		self.player.durationChanged.connect(self.qmp_durationChanged)
		self.player.setVolume(60)
		
		
		# Init GUI
		centralWidget = QWidget()
		centralWidget.setLayout(self.addControls())
		self.setCentralWidget(centralWidget)
		self.show()
		self.infoBox = None
		
		# Add list medias
		self.listemedia = listemedia
		self.addMedialist()
		
		
		# Autoplay at position
		self.playHandler()
		self.currentPlaylist.setCurrentIndex(position-1)
		self.player.play()
	
	def addControls(self):
		# buttons
		self.playBtn = QPushButton()
		self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
		self.playBtn.setStyleSheet('border: 0px;')
		stopBtn = QPushButton()
		stopBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
		stopBtn.setStyleSheet('border: 0px;')
		prevBtn = QPushButton()
		prevBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
		prevBtn.setStyleSheet('border: 0px;')
		nextBtn = QPushButton()
		nextBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
		nextBtn.setStyleSheet('border: 0px;')
		volumeDescBtn = QPushButton('▼')
		volumeDescBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
		volumeDescBtn.setMaximumWidth(30)
		volumeDescBtn.setStyleSheet('border: 0px;')
		volumeIncBtn = QPushButton('▲')
		volumeIncBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
		volumeIncBtn.setMaximumWidth(40)
		volumeIncBtn.setStyleSheet('border: 0px;')
		infoBtn = QPushButton()
		infoBtn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
		infoBtn.setStyleSheet('border: 0px;')
		
		# seek slider
		self.seekSlider = QSlider(Qt.Horizontal, self)
		self.seekSlider.setMinimum(0)
		self.seekSlider.setMaximum(100)
		self.seekSlider.setTracking(False)
		
		# labels position start/end
		self.seekSliderLabel1 = QLabel('0:00')
		self.seekSliderLabel2 = QLabel('0:00')
		
		# layout
		controlArea = QHBoxLayout()
		controlArea.addWidget(prevBtn)
		controlArea.addWidget(self.playBtn)
		controlArea.addWidget(stopBtn)
		controlArea.addWidget(nextBtn)
		controlArea.addWidget(self.seekSliderLabel1)
		controlArea.addWidget(self.seekSlider)
		controlArea.addWidget(self.seekSliderLabel2)
		controlArea.addWidget(infoBtn)
		controlArea.addWidget(volumeDescBtn)
		controlArea.addWidget(volumeIncBtn)
		
		# link buttons to media
		self.seekSlider.sliderMoved.connect(self.seekPosition)
		self.playBtn.clicked.connect(self.playHandler)
		stopBtn.clicked.connect(self.stopHandler)
		volumeDescBtn.clicked.connect(self.decreaseVolume)
		volumeIncBtn.clicked.connect(self.increaseVolume)
		prevBtn.clicked.connect(self.prevItemPlaylist)
		nextBtn.clicked.connect(self.nextItemPlaylist)
		infoBtn.clicked.connect(self.displaySongInfo)
		
		return controlArea
	
	def playHandler(self):
		if self.player.state() == QMediaPlayer.PlayingState:
			self.player.pause()
			message = (' [Paused at position %s]'%self.seekSliderLabel1.text())
			self.setWindowTitle(self.namemedia+message)
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
			if self.player.volume()!= None:
				message = ' [Playing at Volume %d]'%self.player.volume()
				self.setWindowTitle(self.namemedia+message)
	
	def stopHandler(self):
		if self.player.state() == QMediaPlayer.PlayingState:
			self.stopState = True
			self.player.stop()
		elif self.player.state() == QMediaPlayer.PausedState:
			self.player.stop()
		elif self.player.state() == QMediaPlayer.StoppedState:
			pass
		self.setWindowTitle(self.namemedia+(' [Stopped]'))
	
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
			self.setWindowTitle(self.namemedia+message)
	
	def qmp_durationChanged(self, duration):
		self.seekSlider.setRange(0,duration)
		self.seekSliderLabel2.setText('%d:%02d'%(int(duration/60000),int((duration/1000)%60)))
		nummedia = self.currentPlaylist.mediaCount()
		curmedia = self.currentPlaylist.currentIndex()
		#artist = self.player.metaData(QMediaMetaData.Author)
		#tittle = self.player.metaData(QMediaMetaData.Title)
		self.namemedia = path.basename(self.listemedia[curmedia])
		self.namemedia = '[%02d/%02d'%(curmedia+1,nummedia) + '] "'+ self.namemedia + '"'
		self.setToolTip(self.namemedia)
		message = (' [Playing at Volume %d]'%(self.player.volume()))
		self.setWindowTitle(self.namemedia+message)
	
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
		for media in self.listemedia:
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

def playerProcessAudio(listmedia, position, x=0, y=0):
	app = QApplication(argv)
	player = playerAudioAlbum(listmedia, position, x, y)
	app.exec_()


###################################################################
# DRAG & DROP tkDND
class DnD:
	def __init__(self, tkroot):
		self._tkroot = tkroot
		tkroot.tk.eval('lappend auto_path {%s}' % TKDND_LIB)
		tkroot.tk.eval('package require tkdnd')
		# make self an attribute of the parent window for easy access in child classes
		tkroot.dnd = self
	
	def bindsource(self, widget, type=None, command=None, arguments=None, priority=None):
		'''Register widget as drag source; for details on type, command and arguments, see bindtarget().
		priority can be a value between 1 and 100, where 100 is the highest available priority (default: 50).
		If command is omitted, return the current binding for type; if both type and command are omitted,
		return a list of registered types for widget.'''
		command = self._generate_callback(command, arguments)
		tkcmd = self._generate_tkcommand('bindsource', widget, type, command, priority)
		res = self._tkroot.tk.eval(tkcmd)
		if type == None:
			res = res.split()
		return res
	
	def bindtarget(self, widget, type=None, sequence=None, command=None, arguments=None, priority=None):
		'''Register widget as drop target; type may be one of text/plain, text/uri-list, text/plain;charset=UTF-8
		(see the man page tkDND for details on other (platform specific) types);
		sequence may be one of '<Drag>', '<DragEnter>', '<DragLeave>', '<Drop>' or '<Ask>' ;
		command is the callback associated with the specified event, argument is an optional tuple of arguments
		that will be passed to the callback; possible arguments include: %A %a %b %C %c %D %d %L %m %T %t %W %X %x %Y %y
		(see the tkDND man page for details); priority may be a value in the range 1 to 100 ; if there are
		bindings for different types, the one with the priority value will be proceeded first (default: 50).
		If command is omitted, return the current binding for type, where sequence defaults to '<Drop>'.
		If both type and command are omitted, return a list of registered types for widget.'''
		command = self._generate_callback(command, arguments)
		tkcmd = self._generate_tkcommand('bindtarget', widget, type, sequence, command, priority)
		res = self._tkroot.tk.eval(tkcmd)
		if type == None:
			res = res.split()
		return res
	
	def clearsource(self, widget):
		'''Unregister widget as drag source.'''
		self._tkroot.tk.call('dnd', 'clearsource', widget)
	
	def cleartarget(self, widget):
		'''Unregister widget as drop target.'''
		self._tkroot.tk.call('dnd', 'cleartarget', widget)
	
	def drag(self, widget, actions=None, descriptions=None, cursorwindow=None, command=None, arguments=None):
		'''Initiate a drag operation with source widget.'''
		command = self._generate_callback(command, arguments)
		if actions:
			if actions[1:]:
				actions = '-actions {%s}' % ' '.join(actions)
			else:
				actions = '-actions %s' % actions[0]
		if descriptions:
			descriptions = ['{%s}'%i for i in descriptions]
			descriptions = '{%s}' % ' '.join(descriptions)
		if cursorwindow:
			cursorwindow = '-cursorwindow %s' % cursorwindow
		tkcmd = self._generate_tkcommand('drag', widget, actions, descriptions, cursorwindow, command)
		self._tkroot.tk.eval(tkcmd)
				
	def _generate_callback(self, command, arguments):
		'''Register command as tk callback with an optional list of arguments.'''
		cmd = None
		if command:
			cmd = self._tkroot._register(command)
			if arguments:
				cmd = '{%s %s}' % (cmd, ' '.join(arguments))
		return cmd
	
	def _generate_tkcommand(self, base, widget, *opts):
		'''Create the command string that will be passed to tk.'''
		tkcmd = 'dnd %s %s' % (base, widget)
		for i in opts:
			if i is not None:
				tkcmd += ' %s' % i
		return tkcmd


###################################################################
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


###################################################################
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
		self.canv = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=self.yscrlbr.set, width = canv_w, height = canv_h)
		self.canv.pack(side=LEFT, fill=BOTH, expand=TRUE, anchor=N)
		self.yscrlbr.config(command = self.canv.yview)
		
		# reset the view
		self.canv.xview_moveto(0)
		self.canv.yview_moveto(0)
		
		# creating a frame to inserto to canvas
		self.interior = Frame(self.canv, width = canv_w, height = canv_h)
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
		if self.interior.winfo_reqheight() != self.canv.winfo_height():
			# update the canvas's width to fit the inner frame
			#self.canv.config(height = self.interior.winfo_reqheight())
			None


###################################################################
class StatutProgressBar(Canvas):
	"""progress bar tkinter."""
	def __init__(self, parent, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)
		
		self.__font = Font(family=FONT_MAI, size=12)
		self.parent = parent
		self.__margin = 3
		self.__maintitle = self.__title = ''
	
	def message(self, title):
		self.delete(ALL)
		self.__maintitle = title
		self.create_text(self.__margin*2, self.__margin, text=self.__maintitle, font=self.__font, anchor=N+W)
		self.parent.update_idletasks()
	
	def open(self, title = 'Waiting Please...'):
		self.delete(ALL)
		self.__title = title
		self.create_text(self.__margin*2, self.__margin, text=title, font=self.__font, anchor=N+W)
		self.parent.update_idletasks()
	
	def update(self, ratio, title = ''):
		self.delete(ALL)
		self.create_rectangle(self.__margin, 0, self.winfo_width() * ratio, self.winfo_height(), fill=THUN_CO0)
		if title != '':
			self.__title = title
		self.create_text(self.__margin*2, self.__margin, text=self.__title, font=self.__font, anchor=N+W)
		self.parent.update_idletasks()
	
	def close(self):
		self.delete(ALL)
		self.create_text(self.__margin*2, self.__margin, text=self.__maintitle, font=self.__font, anchor=N+W)
		self.parent.update_idletasks()


###################################################################
# LOADING GUI
class LoadingGui(Toplevel):
	"""Fenetre loading."""
	def __init__(self , con, MODE_SQLI, sleeptime=1, w=400, h=200):
		Toplevel.__init__(self)
		# main loading gui
		self.linestabs = 6
		self.widthtabs = w - 150
		self.MODE_SQLI = MODE_SQLI
		initGuiTK(self, w, h+((self.linestabs)*13), True, False, True)
		self.overrideredirect(True)
		self.title("Loading Datas")
		self.bind("<F1>", self.hideLoadingGui)
		self.bind("<Escape>", self.hideLoadingGui)
		# frame logo + message
		customFont = Font(family=FONT_MAI, size=12)
		cadretittle = Frame(self, width=380, height=100)
		cadretittle.pack(fill=BOTH)
		# button quit
		btn_quit = Button(cadretittle, text='X', width=2, command = self.hideLoadingGui)
		btn_quit.pack(side=RIGHT, padx=0, pady=0, anchor=N+E)
		btn_quit.bind("<Enter>", lambda event, h=btn_quit: h.configure(bg=THUN_CO0))
		btn_quit.bind("<Leave>", lambda event, h=btn_quit: h.configure(bg="SystemButtonFace"))
		# logo
		monimage = Image.open(LOGO_PRG)
		monimage = monimage.resize((100, 100), Image.ANTIALIAS)
		photo = ImageTk.PhotoImage(monimage)
		prj_logo = Label(cadretittle, image = photo)
		prj_logo.image = photo
		prj_logo.pack(side=LEFT, padx=10, pady=10)
		# date modification base
		self.con = con
		basedate = (buildTabFromRequest(self.con, getRequest('datedatabase', MODE_SQLI)))[0][0]
		txt_message = MODE_SQLI + " Base \nlast modified :\n"+str(basedate)
		message = StringVar()
		message.set(TITL_PROG+"\nConnected "+txt_message+'.'*sleeptime)
		mes_label = Label(cadretittle, textvariable=message, font=customFont)
		mes_label.pack(side=LEFT, padx=5, pady=5)
		# 3*tabs stats
		self.cadrestats = Frame(self)
		self.cadrestats.pack(fill=BOTH)
		self.treestat1 = self.treestat2 = self.treestat3 = None
		self.scroll = Scrollbar(self.cadrestats, orient=VERTICAL)
		self.selectTreeTabDefault(None)
	
	def buildTreeStats(self, req):
		# build tree
		Tabs = buildTabFromRequest(self.con, req)
		col_names = getListColumns(self.con, req, self.MODE_SQLI)
		tree = buildTree(self.cadrestats, col_names, len(Tabs[0])* [int(self.widthtabs/len(Tabs[0]))], self.linestabs, False, E)
		# fill tree
		counter = 0
		for row in Tabs:
			# the last ligne
			if (counter + 1) == len(Tabs): 
				tag = 3
			else:
				tag = (counter%2)
			tree.insert("", counter, iid='row_%s'%counter, values=row, tag = tag)
			counter += 1
		return tree
	
	def displaytab(self, oldtab, newtab):
		if oldtab != None:
			if len(oldtab.get_children())> self.linestabs:
				self.scroll.pack_forget()
			oldtab.pack_forget()
		if len(newtab.get_children())> self.linestabs:
			self.scroll.pack(side=RIGHT, fill=Y, expand=False)
			self.scroll.config(command=newtab.yview)
			newtab.configure(yscrollcommand=self.scroll.set)
		newtab.pack(side=LEFT, anchor=W, fill=BOTH, expand=True)
		
	def selectTreeTabDefault(self, event):
		# build tab default
		if self.treestat1 == None:
			req = buildReqTCD(self.con, "Category" , "Family", "DBALBUMS", "ALBUMS", "1", True, self.MODE_SQLI)
			self.treestat1 = self.buildTreeStats(req)
			self.treestat1.bind("<Button-3>", self.selectTreeTabSize)
		self.displaytab(self.treestat3, self.treestat1)
		
	def selectTreeTabSize(self, event):
		# build tab size
		if self.treestat2 == None:
			req = buildReqTCD(self.con, "Category" , "Family", "DBALBUMS", "SIZE (GO)", "ROUND( `Size` /1024,1)", True, self.MODE_SQLI)
			self.treestat2 = self.buildTreeStats(req)
			self.treestat2.bind("<Button-3>", self.selectTreeTabYear)
		self.displaytab(self.treestat1, self.treestat2)
	
	def selectTreeTabYear(self, event):
		# build tab year
		if self.treestat3 == None:
			req = buildReqTCD(self.con, "Year" , "Category", "DBALBUMS", "YEARS", "1", True, self.MODE_SQLI)
			self.treestat3 = self.buildTreeStats(req)
			self.treestat3.bind("<Button-3>", self.selectTreeTabDefault)
		self.displaytab(self.treestat2,self.treestat3)
		
	def hideLoadingGui(self, event = None):
		self.withdraw()


###################################################################
# COVER b64 GUI
class CoverViewGui(Toplevel):
	"""Fenetre view cover."""
	def __init__(self, cover, namealbum, w=HEIG_MAIN, h=HEIG_MAIN):
		Toplevel.__init__(self)
		initGuiTK(self, w, h, False, False)
		width, height = cover.size
		self.title("{name} - [{w}x{h}] orignal size:[{wo}x{ho}]".format(w=w, h=h, name=namealbum, wo=str(width), ho=str(height)))
		cover = cover.resize((w, h), Image.ANTIALIAS)
		photo = ImageTk.PhotoImage(cover)
		label = Label(self, image = photo)
		label.image = photo
		label.bind("<Button-1>", lambda event:self.destroy())
		label.pack()


###################################################################
# ARTWORKS HDD GUI
class CoversArtWorkViewGui(Toplevel):
	"""Fenetre view cover."""
	def __init__(self, pathartworks, nametittle, createcover, w, h, tsize=WIDT_PICM):
		Toplevel.__init__(self)
		initGuiTK(self, w, h, True, True)
		self.title(TITL_PROG+" [view ArtWorks] : reading files covers...")
		self.labels = []
		self.monimage = None
		self.numlabel = None
		self.sizethun = tsize
		
		# build list covers
		self.nametittle = nametittle
		fileslist = list(getListFiles(pathartworks, MASKCOVER))
		self.numbersCov = len(fileslist)
		self.pathartworks = pathartworks
		
		# build labels thunbnails
		self.frameThunbnails = VerticalScrolledFrame(self , w , self.sizethun+4)
		self.frameThunbnails.bind("<Configure>",self.resizeMainGui)
		self.frameThunbnails.pack(side=TOP, anchor=W, fill=BOTH, padx=5, pady=5)
		self.listartwork = []
		self.listimage = []
		maxCol = int(w/self.sizethun)
		curRow = curCol = cptIte = 0
		self.update_idletasks()
		for filelist in fileslist:
			monimage = Image.open(filelist)
			self.listimage.append(monimage)
			monimage = monimage.resize((self.sizethun, self.sizethun), Image.ANTIALIAS)
			photo = ImageTk.PhotoImage(monimage)
			label = Label(self.frameThunbnails.interior, image = photo, text=filelist)
			label.image = photo
			self.listartwork.append(label)
			label.grid(row=curRow,column=curCol)
			self.update_idletasks()
			label.bind("<Button-1>", lambda event,a=cptIte: self.onSelectThunbnail(event,a))
			label.bind("<Enter>", lambda event: event.widget.config(relief=SOLID))
			label.bind("<Leave>", lambda event: event.widget.config(relief=FLAT))
			self.labels.append(label)
			# build large cover
			if cptIte==0: 
				# build cover
				self.framecover = Frame(self)
				self.framecover.pack(side=TOP, anchor=W, fill=BOTH, expand=TRUE)
				self.cover = Label(self.framecover, background=THUN_CO0)
				self.cover.pack(side=TOP, fill=BOTH, expand=TRUE)
				self.aMenu = Menu(self.framecover, tearoff=0)
				self.aMenu.add_command(label="Open Folder...", command=lambda c=self.pathartworks: openFolder(c))
				self.aMenu.add_command(label="Create cover file...", command=self.createFileCover)
				self.cover.bind("<Button-3>", self.popupThunbnail)
				# create cover option only if no cover file
				if createcover[0:len(TEXT_NCO)] != TEXT_NCO:
					self.aMenu.entryconfig(1, state="disabled")
				# display first artvork
				self.onSelectThunbnail(None, 0)
			# count thunbnails
			cptIte = cptIte + 1
			# position
			curCol = curCol + 1
			if curCol == maxCol:
				curCol = 0
				curRow = curRow + 1
	
	def onSelectThunbnail(self, event, numlabel):
		curlabel = self.listartwork[numlabel]
		self.filelist = curlabel.cget('text')
		self.monimage = self.listimage[numlabel]
		self.numlabel = numlabel
		# display artwork
		width, height, new_width, new_height = self.resizeImage(self.winfo_width(), self.winfo_height()-self.sizethun+4)
		photo = ImageTk.PhotoImage(self.monimage)
		self.cover.configure(image = photo)
		self.cover.image = photo
		# next
		self.cover.bind("<Button-1>", lambda event,a=(0 if self.numbersCov==numlabel+1 else numlabel+1): self.onSelectThunbnail(event,a))
		# windows
		self.title(TITL_PROG+" : [view ArtWorks: "+self.nametittle+'] {c}/{n} "{name}" A[{w}x{h}] O[{wo}x{ho}]'.format(c=str(numlabel+1), 
																		 n=str(len(self.listartwork)), 
																		 w=new_width, 
																		 h=new_height, 
																		 name=path.basename(self.filelist), 
																		 wo=str(width), 
																		 ho=str(height)))
		self.update_idletasks()
	
	def resizeImage(self, wmax, hmax):
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
	
	def resizeMainGui(self, event):
		# update display thunbnails
		if len(self.labels)>0:
			w = self.winfo_width()
			h = self.winfo_height()
			self.frameThunbnails.config(width=w, height=h)
			maxCol = int(self.winfo_width()/self.sizethun)
			Grid.columnconfigure(self.frameThunbnails.interior, maxCol, weight=1)
			curRow = curCol = 0
			for labelt in self.labels:
				labelt.grid(row=curRow,column=curCol)
				# position
				curCol = curCol + 1
				if curCol == maxCol:
					curCol = 0
					curRow = curRow + 1
		# update size cover
		if self.monimage != None:
			self.onSelectThunbnail(None, self.numlabel)
	
	def popupThunbnail(self, event):
		self.aMenu.post(event.x_root, event.y_root)
	
	def createFileCover(self):
		file_exten = path.splitext(self.filelist)[1][1:]
		path_cover = path.join(path.dirname(self.filelist), 'cover.' +file_exten )
		self.title("create file {name} ".format(name=path.basename(path_cover)))
		self.monimage.save(path_cover)


###################################################################
# CONSOL EXECUTION SCRIPT
class DisplaySubprocessGui(Toplevel):
	def __init__(self, eCommand, title, w=WIDT_MAIN, h=600):
		Toplevel.__init__(self)
		initGuiTK(self, w, h, True, True)
		self.title(title+' : waiting...')
		customFont = Font(family=FONT_CON, size=8)
		self.textarea = Text(self, wrap='word', state='disabled', height=49, width=200, bg='black', fg='snow', font=customFont)
		ysb = Scrollbar(self, orient=VERTICAL)
		ysb.config(command=self.textarea.yview)
		self.endline = True
		ysb.bind("<Button-1>", self.endlineKO)
		ysb.bind("<ButtonRelease-1>", self.endlineOK)
		ysb.pack(side=RIGHT, fill=Y)
		self.textarea.configure(yscrollcommand=ysb.set)
		self.textarea.tag_config("com", foreground="green2")
		self.textarea.tag_config("nfo", foreground="magenta")
		self.textarea.tag_config("err", foreground="red2")
		self.textarea.pack(ipadx=4, padx=4, ipady=4, pady=4, fill=BOTH, expand=TRUE)
		self.btnquit = Button(self, text="Kill", width=15, command=self.quitDisplaySubprocessGui)
		self.btnquit.pack(side=BOTTOM, anchor=E, padx=4, pady=5)
		# launch process
		self.textarea.configure(state='normal')
		self.textarea.insert('end', ' '.join(eCommand) + '\n', 'nfo')
		self.textarea.configure(state='disabled')
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
				self.title(self.title+' : completed')
				self.btnquit.configure(text="Quit")
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
				self.update_idletasks()
				# display no more than one line per 10 milliseconds
				break 
		 # schedule next update
		self.after(10, self.update, q)
	
	def iter_except(self, function, exception):
		"""Works like builtin 2-argument `iter()`, but stops on `exception`."""
		try:
			while True:
				yield function()
		except exception:
			return
	
	def quitDisplaySubprocessGui(self):
		self.process.kill() # exit (zombie!)
		self.destroy()


###################################################################
###################################################################
# MAIN GUI
###################################################################
class DBAlbumsMainGui(Tk):
	"""Fenetre principale."""
	MARG_GENE = 5 
	MARG_THUN = 4
	WIDT_COMB = 15
	WIDT_BUTN = 2
	WIDT_PICM = WIDT_PICM
	HEIG_LHUN = HEIG_LHUN
	
	def __init__(self , parent):
		Tk.__init__(self , parent)
		self.parent = parent
		
		### MAIN DEFINITION
		self.tk.call('encoding', 'system', 'utf-8')
		# init size main
		self.protocol("WM_DELETE_WINDOW", self.quitDBAlbumsMain)
		self.squarethunbnails = WIDT_PICM
		self.nblinethunbnails = HEIG_LHUN
		self.heightgridalbums = HEIG_LTAB
		self.heightmainwindow = HEIG_MAIN
		self.width_mainwindow = WIDT_MAIN
		self.heightthunbnails = self.nblinethunbnails * (self.squarethunbnails+DBAlbumsMainGui.MARG_THUN)
		self.coef = 1
		# minimize ? height main windows
		if self.winfo_screenheight() < self.heightmainwindow:
			# one line for thunbnails
			self.nblinethunbnails = 1
			self.heightthunbnails = self.nblinethunbnails * (self.squarethunbnails+DBAlbumsMainGui.MARG_THUN)
			self.heightmainwindow = self.heightmainwindow - (self.squarethunbnails+DBAlbumsMainGui.MARG_THUN)
			if self.winfo_screenheight() < self.heightmainwindow:
				# 5 lines for grig
				self.heightgridalbums = 5
				self.heightmainwindow = self.heightmainwindow - (5*20)
		# size & center position
		initGuiTK(self, self.width_mainwindow, self.heightmainwindow, True, True)
		
		### NO DISPLAY MAIN GUI
		self.withdraw()
		
		### DRAG & DROP
		if platform == "win32":
			dnd = DnD(self)
			dnd.bindtarget(self, 'text/uri-list', '<Drop>', self.dropAddFolders, ('%A', '%a', '%T', '%W', '%X', '%Y', '%x', '%y','%D'))
		
		### STYLE
		s=Style()
		s.theme_use('clam')
		
		### INIT VAR
		self.con = None
		self.Envs = None
		self.labels = []
		self.tplay = None
		self.CurentAlbum = None
		self.Curalbmd5 = None
		self.CurentTrack = None
		self.homeMedias = None
		self.thunbnailNoMiniCover = Image.open(PICM_NCO)
		
		### BUILD GUI
		self.buildGui()
		
		### BIND GUI
		self.bind("<F1>", self.showloadingWin)
		self.bind("<F5>", lambda e:self.connectEnvtBase(True))
		self.bind("<F11>", self.changeDisplayNoList)
		self.bind("<Shift-MouseWheel>", self.zoomChange)
		self.frameThunbnails.bind("<Configure>", self.resizeframeThunbnails)
		self.ligne_texte.bind("<Return>", lambda e:self.getSearchAlbums())
		self.Combostyle.bind("<<ComboboxSelected>>",  lambda e:self.getSearchAlbums())
		self.Combofamily.bind("<<ComboboxSelected>>",  lambda e:self.getSearchAlbums())
		self.Combolabelm.bind("<<ComboboxSelected>>",  lambda e:self.getSearchAlbums())
		self.Comboyearc.bind("<<ComboboxSelected>>",  lambda e:self.getSearchAlbums())
		self.combo.bind("<<ComboboxSelected>>", lambda e:self.connectEnvtBase())
		self.Combostyle.bind("<Button-3>", self.popupcategory)
		self.combo.bind("<Button-3>", self.popupbase)
		self.tree.bind("<Button-3>", self.popuptreealbum)
		self.tree.bind("<<TreeviewSelect>>", self.onTreeSelectAlbum)
		self.labcover.bind("<Button-1>", self.onPressCover)
		self.treealb.bind("<Double-1>", self.onDoubleClickTrack)
		self.treealb.bind("<<TreeviewSelect>>", self.onSelectTrack)
		
		#### DISABLED OPTIONS for OS linux: no powershell, foobar, tagscan
		if platform == "darwin" or platform == 'linux':
			self.bMenu.entryconfig(2, state="disabled") #Update Base (powershell)
			self.bMenu.entryconfig(4, state="disabled") #Import Foobar Playlists
			self.cMenu.entryconfig(0, state="disabled") #Update Category Base (powershell)
			self.aMenu.entryconfig(3, state="disabled") #Update Album (powershell)
			self.aMenu.entryconfig(4, state="disabled") #TagScan
		
		#### LOADING ENVT
		self.connectEnvtBase()
		
		#### DISPLAY MAIN GUI
		self.update()
		self.deiconify()
	
	def buildGui(self):
		margin = DBAlbumsMainGui.MARG_GENE
		widthcombos = DBAlbumsMainGui.WIDT_COMB
		widthbutton = DBAlbumsMainGui.WIDT_BUTN
		self.customFont = Font(family=FONT_MAI, size=12)
		self.zoomfont = Font(family=FONT_MAI, size=8)
		#### SAISIE
		self.cadresaisie = Frame(self)
		self.cadresaisie.pack(fill=BOTH)
		# Label
		labelDir = Label(self.cadresaisie, text="Search")
		labelDir.pack(side=LEFT, padx=margin, pady=margin)
		# ligne de saisie
		self.var_searchtext_value = StringVar(None)
		self.ligne_texte = AutocompleteEntry(self.cadresaisie, textvariable=self.var_searchtext_value, width=(4*margin))
		self.ligne_texte.pack(side=LEFT, pady=margin)
		# button clear
		btn_clear = Button(self.cadresaisie, text='✖', width=widthbutton, command = self.clearSearchAlbums)
		btn_clear.pack(side="left", pady=margin)
		# button search
		btn_search = Button(self.cadresaisie, text='➜', width=widthbutton, command = self.getSearchAlbums)
		btn_search.pack(side=LEFT, pady=margin)
		# + search in tracks
		self.searchtracks = IntVar()
		self.searchtracks.set(0)
		Checkbutton(self.cadresaisie, text="In Tracks", variable = self.searchtracks, command= self.searchInTrackChange).pack(side=LEFT, padx=margin, pady=margin)
		# combo Category
		self.Combostyle_value = StringVar()
		self.Combostyle = Combobox(self.cadresaisie, textvariable=self.Combostyle_value, state='readonly', width = widthcombos)
		self.Combostyle.pack(side=LEFT, padx=margin, pady=margin)
		self.Combostyle['values'] = DISP_CJOKER
		self.Combostyle.current(0)
		# popup category
		self.cMenu = Menu(self.cadresaisie, tearoff=0)
		self.cMenu.add_command(label="Update Category (powershell)...", command=lambda c=self.Combostyle.get(): self.buildInvent(c))
		# combo Family
		self.Combofamily_value = StringVar()
		self.Combofamily = Combobox(self.cadresaisie, textvariable=self.Combofamily_value, state='readonly', width = widthcombos)
		self.Combofamily.pack(side=LEFT, padx=margin, pady=margin)
		self.Combofamily['values'] = DISP_CJOKER
		self.Combofamily.current(0)
		# combo Label
		self.Combolabelm_value = StringVar()
		self.Combolabelm = Combobox(self.cadresaisie, textvariable=self.Combolabelm_value, state='readonly', width = widthcombos)
		self.Combolabelm.pack(side=LEFT, padx=margin, pady=margin)
		self.Combolabelm['values'] = DISP_CJOKER
		self.Combolabelm.current(0)
		# combo year
		self.Comboyearc_value = StringVar()
		self.Comboyearc = Combobox(self.cadresaisie, textvariable=self.Comboyearc_value, state='readonly', width = widthcombos)
		self.Comboyearc.pack(side=LEFT, padx=margin, pady=margin)
		self.Comboyearc.pack(side=LEFT, padx=margin, pady=margin)
		self.Comboyearc['values'] = DISP_CJOKER
		self.Comboyearc.current(0)
		# combo environments
		self.combo_value = StringVar()
		self.combo = Combobox(self.cadresaisie, textvariable=self.combo_value, state='readonly', width = widthcombos)
		self.combo.pack(side=RIGHT, padx=margin, pady=margin)
		self.combo['values'] = NAME_EVT
		self.combo.current(CURT_EVT)
		# button display
		self.btn_display = Button(self.cadresaisie, text='≠', width=widthbutton, command = self.changeDisplayNoList)
		self.btn_display.pack(side=RIGHT, pady=margin)
		Separator(self ,orient=HORIZONTAL).pack(side=TOP, fill=BOTH)
		# display zoom %
		self.canvdiszoomp = Canvas(self.cadresaisie, width = 30, height = 25)
		self.canvdiszoomp.pack(side=RIGHT, anchor=W, pady=margin , padx=2)
		# popup menu base
		self.bMenu = Menu(self.cadresaisie, tearoff=0)
		self.bMenu.add_command(label="Show Informations  [F1]", command=self.showloadingWin)
		self.bMenu.add_command(label="Reload base Albums [F5]", command=lambda: self.connectEnvtBase(True))
		self.bMenu.add_command(label="Update Base (powershell)...", command=self.buildInvent)
		self.bMenu.add_command(label="Create sqlite database", command=self.CreateLocalBase)
		self.bMenu.add_command(label="Import Foobar Playlists, Update Score...", command=self.importFoobar)
		self.bMenu.add_command(label="Edit %s..." % FILE__INI, command=lambda e = EDIT_TEXT, f = FILE__INI : runCommand(e, f))
		self.bMenu.add_command(label="Open Logs Folder...", command=lambda l=LOGS_PROG : openFolder(l))
		
		#### LIST ALBUMS
		# thunbnails
		self.frameThunbnails = VerticalScrolledFrame(self , self.width_mainwindow , self.heightthunbnails)
		self.frameThunbnails.pack(side=TOP, anchor=N+W, fill=BOTH, expand=FALSE)
		# list albums
		self.framealbumlist = Frame(self)
		self.framealbumlist.pack(side=TOP, anchor=W, fill=BOTH, expand=TRUE)
		self.tree = buildTree(self.framealbumlist, A_COLNAME, A_C_WIDTH, self.heightgridalbums, True)
		self.tree.pack(side=TOP, anchor=W, expand=TRUE, fill=BOTH)
		# popup menu album
		self.aMenu = Menu(self.framealbumlist, tearoff=0)
		self.aMenu.add_command(label="View ArtWorks...", command=self.viewArtWorks)
		self.aMenu.add_command(label="Open Folder...", command=self.getFolder)
		self.aMenu.add_command(label="Export Album...", command=self.exportAlbums)
		self.aMenu.add_command(label="Update Album...", command=self.updateAlbums)
		self.aMenu.add_command(label="Edit Tags (TagScan)...", command=self.openTagScan)
		
		#### INFOS ALBUM 
		# COVER
		self.cadrealbum = Frame(self)
		self.cadrealbum.pack(side=TOP, anchor=W, fill=BOTH, expand=FALSE)
		self.labcover = Label(self.cadrealbum)
		self.labcover.pack(side=LEFT)
		# SET BLANK COVERS
		monimage = buildCover(' ', TEXT_NCO, ' ')
		monimage = monimage.resize((COVE_SIZ, COVE_SIZ), Image.ANTIALIAS)
		photo = ImageTk.PhotoImage(monimage)
		self.labcover.configure(image = photo)
		self.labcover.image = photo
		# ALBUM NAME
		self.cadrelabelalb = Frame(self.cadrealbum)
		self.cadrelabelalb.pack(fill=BOTH, side=TOP)
		self.stralbumname = StringVar()
		self.labelalb = Label(self.cadrelabelalb ,textvariable=self.stralbumname ,justify=LEFT ,font=self.customFont)
		self.labelalb.pack(side=LEFT, padx=margin)
		# SCORE ALBUM
		self.posalbum_scale = Scale( self.cadrelabelalb,
										command=self.modifyScoreAlbum, 
										showvalue=0, 
										from_=0, 
										to=len(SCOR_ALBUMS)-1, 
										length=100,
										orient='horizontal')
		self.posalbum_scale.pack(side=RIGHT, padx=margin*3, pady=margin)
		self.ScoAlbumlb = StringVar()
		self.scorealbum_label = Label(self.cadrelabelalb, textvariable=self.ScoAlbumlb, font=self.customFont)
		self.btn_enrscralb = Button(self.cadrelabelalb, text='Update', command = self.onPressButtonEnrScoreAlbum)
		self.scorealbum_label.pack(side=RIGHT, padx=margin, pady=margin)
		# TRACKS
		self.treealb = buildTree(self.cadrealbum, T_COLNAME, T_C_WIDTH, 15, True)
		self.treealb.pack(side=BOTTOM, anchor=W, fill=BOTH, padx=0, pady=0)
		# SCORE TRACK
		self.cadrescoretrack = Frame(self)
		self.cadrescoretrack.pack(side=TOP, fill=BOTH)
		self.postrack_scale = Scale( self.cadrescoretrack,
										command=self.modifyScoreTrack, 
										showvalue=0, 
										from_=0, 
										to=len(SCOR_TRACKS)-1, 
										length=100,
										orient='horizontal')
		self.postrack_scale.pack(side=RIGHT, padx=margin*3, pady=margin)
		self.ScoTracklb = StringVar()
		self.scoretrack_label = Label(self.cadrescoretrack, textvariable=self.ScoTracklb, font=self.customFont)
		self.scoretrack_label.pack(side=RIGHT, padx=margin, pady=margin)
		self.btn_enrscrtrk = Button(self.cadrescoretrack, text='Update', command = self.onPressButtonEnrScoreTrack)
		
		#### STATUS BAR
		self.cadrStatusBar = Frame(self)
		self.cadrStatusBar.pack(fill=BOTH, anchor=S+W, side=BOTTOM)
		Separator(self.cadrStatusBar ,orient=HORIZONTAL).pack(side=TOP, fill=BOTH)
		self.statusBar = StatutProgressBar(self.cadrStatusBar, width=self.width_mainwindow-(margin*2), height=26)
		self.statusBar.pack(fill=BOTH, anchor=S+W, side=BOTTOM)
	
	def resizeframeThunbnails(self, event):
		if len(self.labels)>0:
			w = self.winfo_width()
			h = self.winfo_height()
			self.frameThunbnails.config(width=w, height=h)
			maxCol = int(self.winfo_width()/(self.squarethunbnails+DBAlbumsMainGui.MARG_THUN))
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
	
	def displayThunbnails(self, new=True, deb=0, fin=THUN_DIS):
		if new:
			# delete all labels thunbnails
			for labelt in self.labels:
				labelt.destroy()
			self.labels[:] = []
			self.frameThunbnails.canv.yview_moveto(0)
		else:
			# delete 2 labels endof before add more
			self.labels[len(self.labels)-1].destroy()
			self.labels[len(self.labels)-2].destroy()
			self.labels = self.labels[:-2]
		self.statusBar.open("Loading covers albums in progress...")
		self.displayZoom(True)
		numAlb = len(self.tree.get_children())
		numCov = min(fin,len(self.tree.get_children()))-deb
		maxCol = int(self.winfo_width()/(self.squarethunbnails+DBAlbumsMainGui.MARG_THUN))
		Grid.columnconfigure(self.frameThunbnails.interior, maxCol, weight=1)
		curRow = curCol = cptIte = 0
		for curItem in self.tree.get_children():
			if cptIte >= deb and cptIte <= fin:
				curLign = self.tree.item(curItem)
				pathcover = curLign['values'][A_POSITIO.index('Cover')]
				albumname = curLign['values'][A_POSITIO.index('Name')]
				# no cover or no display thunbnails covers (thnail_nod = 1)
				if THUN_NOD == 0 or pathcover == TEXT_NCO:
					if THUN_NOD == 0:pathcover = TEXT_NCO
					monimage = self.thunbnailNoMiniCover
				else:
					Curalbmd5 = curLign['values'][A_POSITIO.index('MD5')]
					monimage = buildCover(self.con, pathcover, Curalbmd5, 'minicover')
				label = self.buildThunbnail(pathcover, albumname.replace(' - ','\n'), monimage, curItem)
				label.grid(row=curRow,column=curCol)
				label.bind("<Button-1>", lambda event,a=curItem: self.onSelectThunbnail(event,a))
				label.bind("<Button-3>", self.popupthunbnailsalbum)
				self.labels.append(label)
				self.statusBar.update((cptIte-deb+1)/numCov)
			# count thunbnails
			cptIte = cptIte + 1
			# position
			curCol = curCol + 1
			if curCol == maxCol:
				curCol = 0
				curRow = curRow + 1
				self.update_idletasks()
			# end max display, labels for more
			if cptIte==fin:
				# add for add more thunbnails
				monimage = Image.open(THUN_DBA)
				label = self.buildThunbnail(THUN_DBA, "{n} covers display max \n Click for more +{f}...".format(n=str(fin),f=str(fin+fin) if (fin+fin)<(numAlb-fin) else str(numAlb-fin)), monimage, 'endof')
				label.grid(row=curRow,column=curCol)
				label.bind("<Button-1>", lambda e: self.displayThunbnails(False,fin,fin+fin))
				self.labels.append(label)
				# add for all thunbnails
				curCol = curCol + 1
				if curCol == maxCol:
					curCol = 0
					curRow = curRow + 1
				label = self.buildThunbnail(THUN_DBA, "{n} covers display max \n Click for all +{f}...".format(n=str(fin),f=str(numAlb-fin)), monimage, 'endof')
				label.grid(row=curRow,column=curCol)
				label.bind("<Button-1>", lambda e: self.displayThunbnails(False,fin,numAlb-fin+1))
				self.labels.append(label)
				break
		self.displayZoom(False)
		self.statusBar.close()
		#print(str(cptIte)+'*covers')
	
	def buildThunbnail(self, pathcover, texte, monimage, curItem):
		"""Build label image thunbnails."""
		width, height = monimage.size
		if width != self.squarethunbnails or height != self.squarethunbnails:
			monimage = monimage.resize((self.squarethunbnails, self.squarethunbnails), Image.ANTIALIAS)
		# no cover, add blank
		if pathcover[0:len(TEXT_NCO)] == TEXT_NCO or pathcover==THUN_DBA: 
			# add text infos
			draw = ImageDraw.Draw(monimage)
			h = 30 
			if '\n' in texte:
				texte = texte.split('\n')
				texte = texte[0]+"\n"+texte[1]
			draw.rectangle(((4,(self.squarethunbnails-h)/2),(self.squarethunbnails-4,((self.squarethunbnails-h)/2)+h)), fill=THUN_CO0)
			try:
				font = ImageFont.truetype(FONT_MAI.lower() + '.ttf', 12)
			except:
				font = ImageFont.truetype("FreeMono.ttf", 10)
			draw.text((6,((self.squarethunbnails-h)/2)+4), texte, font=font, fill=THUN_CO1)
		photo = ImageTk.PhotoImage(monimage)
		label = Label(self.frameThunbnails.interior, image=photo, text=curItem)
		label.image = photo
		label.bind("<Enter>", lambda event: event.widget.config(relief=SOLID))
		label.bind("<Leave>", lambda event: event.widget.config(relief=FLAT))
		return label
	
	def onSelectThunbnail(self, event, curItem):
		"""Display album infos."""
		self.CurentAlbum = curItem
		# select item
		self.tree.selection_set(self.CurentAlbum)
		# scroll
		self.tree.see(self.CurentAlbum)
		# cursor
		self.tree.focus(self.CurentAlbum)
	
	def clearSearchAlbums(self):
		"""Clear search, combos."""
		# reset text search + in track
		self.var_searchtext_value.set('')
		self.searchtracks.set(0)
		# reset combos
		self.Combostyle.current(0)
		self.Combofamily.current(0)
		self.Combolabelm.current(0)
		self.Comboyearc.current(0)
		self.getSearchAlbums()
	
	def searchInTrackChange(self):
		"""Rerun search + in track."""
		if self.var_searchtext_value.get():
			self.getSearchAlbums()
	
	def onPressCover(self, event):
		"""Display large cover MD5."""
		if self.pathcover[0:len(TEXT_NCO)] != TEXT_NCO:
			monimage = buildCover(self.con, self.pathcover, self.Curalbmd5)
			CoverViewGui(monimage, self.albumname, self.heightmainwindow, self.heightmainwindow)
	
	def onTreeSelectAlbum(self, event):
		"""Display album infos + ."""
		if self.tree.get_children():
			self.tree.focus()
			self.CurentAlbum = self.tree.focus()
			self.getInfosAlbum(self.CurentAlbum)
			# find thunbnails label + format + scroll
			nblindisp = int(self.frameThunbnails.winfo_height()/self.squarethunbnails)
			nbcoldisp = int(self.winfo_width()/self.squarethunbnails)
			nbthudisp = nbcoldisp*nblindisp
			fraction = int(round((len(self.labels)/nbcoldisp) + 0.5)) / nblindisp
			fraction = float(1 / fraction)
			counter = 0
			for labelt in self.labels:
				if labelt.cget("text") == self.CurentAlbum:
					labelt.config(bg=THUN_SE2)
					curfra = int((counter) / nbthudisp) * fraction
					self.frameThunbnails.canv.yview_moveto(curfra)
				else:
					labelt.config(bg=THUN_SE1)
				counter = counter + 1
	
	def onSelectTrack(self, event):
		"""Select track."""
		if self.treealb.get_children():
			self.treealb.focus()
			self.CurentTrack = self.treealb.focus()
			self.getInfosTrack(self.CurentTrack)
	
	def onDoubleClickTrack(self, event):
		"""Play track."""
		if self.treealb.get_children():
			self.playerMedias()
	
	def onPressButtonEnrScoreAlbum(self):
		"""Update Score Album."""
		self.ScoreAlbum = self.posalbum_scale.get()
		self.ScoAlbumlb.set(displayStars(self.ScoreAlbum, SCOR_ALBUMS))
		# Mysql
		updateBaseScore(self.con, self.ScoreAlbum, self.Id_CD, getRequest('updatescorealbum', self.MODE_SQLI))
		# Treeview
		self.tree.set(self.CurentAlbum, column=A_POSITIO.index('Score'), value=self.ScoreAlbum*'★')
		# Button
		self.btn_enrscralb.pack_forget()
	
	def onPressButtonEnrScoreTrack(self):
		"""Update Score Track."""
		self.ScoreTrack = self.postrack_scale.get()
		self.ScoTracklb.set(displayStars(self.ScoreTrack, SCOR_TRACKS))
		# Mysql
		updateBaseScore(self.con, self.ScoreTrack, self.ID_TRACK, getRequest('updatescoretrack', self.MODE_SQLI))
		# Treeview
		self.treealb.set(self.CurentTrack, column=T_POSITIO.index('Score'), value=self.ScoreTrack*'★')
		# Button
		self.btn_enrscrtrk.pack_forget()
	
	def modifyScoreAlbum(self, event):
		"""Modify Score Album."""
		self.ScoAlbumlb.set(displayStars(self.posalbum_scale.get(), SCOR_ALBUMS))
		if self.ScoreAlbum != self.posalbum_scale.get():
			self.btn_enrscralb.pack(side=RIGHT, padx=5, pady=5)
		else:
			self.btn_enrscralb.pack_forget()
	
	def modifyScoreTrack(self, event):
		"""Modify Score Track, Add button."""
		self.ScoTracklb.set(displayStars(self.postrack_scale.get(), SCOR_TRACKS))
		if self.ScoreTrack != self.postrack_scale.get():
			self.btn_enrscrtrk.pack(side=RIGHT, padx=5, pady=5)
		else:
			self.btn_enrscrtrk.pack_forget()
	
	def popupbase(self, event):
		"""Menu Base."""
		self.bMenu.post(event.x_root, event.y_root)
	
	def popupcategory(self, event):
		"""Menu Combo Category."""
		if self.Combostyle.current()==0:
			self.cMenu.entryconfig(0, state="disabled")
		else:
			self.cMenu.entryconfig(0, label=("Update Category " + self.Combostyle.get() + " (powershell)..."), 
										command=lambda c=self.Combostyle.get(): self.buildInvent(c))
		self.cMenu.post(event.x_root, event.y_root)
	
	def popupthunbnailsalbum(self, event):
		"""Menu Thunbnails."""
		curItem = event.widget.cget('text')
		self.CurentAlbum = curItem
		self.tree.selection_set(self.CurentAlbum)
		self.tree.see(self.CurentAlbum)
		self.tree.focus(self.CurentAlbum)
		# maj infos albums
		self.getInfosAlbum(self.CurentAlbum, True)
		# maj combo popup menu
		self.updateTextPopupAlbum(event)
	
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
			self.getInfosAlbum(self.CurentAlbum, True)
			self.aMenu.entryconfig(4, state="normal")
			self.updateTextPopupAlbum(event)
		else:
			# select x item
			if len(ListeSelect) > 1 :
				self.aMenu.entryconfig(0, state="disabled")
				self.aMenu.entryconfig(1, state="disabled")
				self.aMenu.entryconfig(2, label="Export "+ displayCounters(len(ListeSelect), 'Album')+"cover/csv...")
				self.aMenu.entryconfig(3, label="Update "+ displayCounters(len(ListeSelect), 'Album') +"...")
				self.aMenu.entryconfig(4, state="disabled")
				self.aMenu.post(event.x_root, event.y_root)
	
	def updateTextPopupAlbum(self, event):
		curLign = self.tree.item(self.CurentAlbum)
		if curLign['values'][A_POSITIO.index('Qty_covers')] == 0 or not(path.exists(self.AlbumPath)):
			self.aMenu.entryconfig(0, state="disabled")
		else:
			self.aMenu.entryconfig(0, state="normal")
		# path exist ?
		if not(path.exists(self.AlbumPath)):
			self.aMenu.entryconfig(1, state="disabled")
		else:
			self.aMenu.entryconfig(1, state="normal")
		self.aMenu.entryconfig(2, label="Export cover/csv '"+ self.albumname[:15] + "...'")
		self.aMenu.entryconfig(3, label="Update Album (powershell): "+ self.albumname[:15] + "...")
		self.aMenu.post(event.x_root, event.y_root)
		
	def connectEnvtBase(self, refresh = False):
		"""Connect Base Environnement."""
		if self.Envs != self.combo_value.get() or refresh:
			# Mysql
			self.Envs = self.combo_value.get()
			if self.con: self.con.close()
			self.condat = datetime.now().strftime('%H:%M:%S')
			self.con, self.MODE_SQLI, self.homeMedias = connectDatabase(self.Envs)
			# debut loading
			self.loadingWin = LoadingGui(self.con, self.MODE_SQLI, 0)
			# mode sqllite, no create base
			if self.MODE_SQLI == 'sqlite':
				self.bMenu.entryconfig(3, state="disabled")
			else:
				self.bMenu.entryconfig(3, state="normal")
			# auto-completion
			completion_list = buildListFromRequest(self.con, getRequest('autocompletion', self.MODE_SQLI))
			self.ligne_texte.set_completion_list(completion_list)
			# title
			self.title('{prog} : Connected base {database} [{mode}] at {heure}'.format(prog = TITL_PROG,
																			mode=self.MODE_SQLI,
																			database = self.Envs,
																			 heure = self.condat))
			# mount table albums in memory
			self.Tabs = buildTabFromRequest(self.con, getRequest('albumslist', self.MODE_SQLI))
			# reset combos
			self.Combostyle.current(0)
			self.Combofamily.current(0)
			self.Combolabelm.current(0)
			self.Comboyearc.current(0)
			# all albums to treeview
			self.getSearchAlbums(refresh)
			# Hide loading
			self.loadingWin.withdraw()
	
	def getSearchAlbums(self, refresh = False):
		"""Search Albums."""
		txt_search = self.var_searchtext_value.get()
		# SEARCH IN TRACKS
		if self.searchtracks.get() == 1:
			# build list id contains text search
			lst_id = buildTabFromRequest(self.con, (getRequest('tracksinsearch', self.MODE_SQLI)).format(search=txt_search))
			lst_id = list(lst_id)
			counter = 0
			while counter < len(lst_id):
				lst_id[counter] = lst_id[counter][0]
				counter = counter + 1
		else:
			lst_id = []
		# DELETE TREEVIEW
		self.tree.delete(*self.tree.get_children())
		self.update_idletasks()
		# insert
		liststyle = []
		listfamil = []
		listlabel = []
		listeyear = []
		counter = cpt_trk = cpt_cds = cpt_siz = cpt_len = 0
		for row in self.Tabs:
			# find text entry ?
			if  txt_search.lower() in row[A_POSITIO.index('Name')].lower() or txt_search.lower() in row[A_POSITIO.index('Label')].lower() or row[A_POSITIO.index('ID_CD')] in lst_id:
				# Category ok ?
				if (self.Combostyle_value.get() != DISP_CJOKER and row[A_POSITIO.index('Category')] == self.Combostyle_value.get()) or (self.Combostyle_value.get() == DISP_CJOKER):
					# Family ok ?
					if (self.Combofamily_value.get() != DISP_CJOKER and row[A_POSITIO.index('Family')] == self.Combofamily_value.get()) or (self.Combofamily_value.get() == DISP_CJOKER):
						# Label ok ?
						if (self.Combolabelm_value.get() != DISP_CJOKER and row[A_POSITIO.index('Label')] == self.Combolabelm_value.get()) or (self.Combolabelm_value.get() == DISP_CJOKER):
							# year ok ?
							if (self.Comboyearc_value.get() != DISP_CJOKER and row[A_POSITIO.index('Year')] == self.Comboyearc_value.get()) or (self.Comboyearc_value.get() == DISP_CJOKER):
								# FILL TREEVIEW
								self.tree.insert("", counter, iid=row[A_POSITIO.index('ID_CD')], values=row, tag = (counter%2))
								# SCORE DISPLAY
								self.tree.set(row[A_POSITIO.index('ID_CD')], column=A_POSITIO.index('Score'), value=row[A_POSITIO.index('Score')]*'★')
								# FILL LISTS COMBOS
								if row[A_POSITIO.index('Category')] not in liststyle:
									liststyle.append(row[A_POSITIO.index('Category')])
								if row[A_POSITIO.index('Family')] not in listfamil:
									listfamil.append(row[A_POSITIO.index('Family')])
								if row[A_POSITIO.index('Label')] not in listlabel:
									listlabel.append(row[A_POSITIO.index('Label')]) 
								if row[A_POSITIO.index('Year')] not in listeyear:
									listeyear.append(row[A_POSITIO.index('Year')])
								# MODIFICATIONS DISPLAY ALBUM NAME, LABEL, ISRC
								albumname = row[A_POSITIO.index('Name')]
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
								self.tree.set(row[A_POSITIO.index('ID_CD')], column=A_POSITIO.index('Name'), value=albumname)
								if row[A_POSITIO.index('Label')]=='':
									self.tree.set(row[A_POSITIO.index('ID_CD')], column=A_POSITIO.index('Label'), value=label)
								if row[A_POSITIO.index('ISRC')]=='':
									self.tree.set(row[A_POSITIO.index('ID_CD')], column=A_POSITIO.index('ISRC'), value=isrc)
								# COUNTERS
								counter += 1
								cpt_cds += row[A_POSITIO.index('Qty_CD')]
								cpt_trk += row[A_POSITIO.index('Qty_Tracks')]
								cpt_siz += row[A_POSITIO.index('Size')]
								cpt_len += sum(int(x) * 60 ** i for i,x in enumerate(reversed(row[A_POSITIO.index('Length')].split(":"))))
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
		self.displayThunbnails()
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
			self.statusBar.message("Search Result \"{sch}\" :  {alb} | {trk} | {cds} | {siz} | {dur} ".format(sch = (txt_search if len(txt_search)>0 else 'all'),
																						alb = displayCounters(counter, 'Album'),
																						cds =  displayCounters(cpt_cds, 'CD'),
																						trk = displayCounters(cpt_trk, 'Track'),
																						siz = txt_siz,
																						dur = txt_dur))
		else:
			self.statusBar.message("Search Result \"{sch}\" : nothing".format(sch = self.ligne_texte.get()))
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
		self.getInfosAlbum(self.CurentAlbum, refresh)
		# focus
		self.ligne_texte.focus_set()
	
	def getInfosAlbum(self, curItem, refresh = False):
		"""Display album infos select."""
		# if treeview not empty or album different or optiontrack
		if self.tree.get_children():
			curLign = self.tree.item(curItem)
			if  curLign['values'][A_POSITIO.index('MD5')] != self.Curalbmd5 or refresh:
				# DEL LIST TRACKS
				self.treealb.delete(*self.treealb.get_children())
				# MAJ ALBUM INFO
				self.Curalbmd5 = curLign['values'][A_POSITIO.index('MD5')]
				self.pathcover = convertUNC(curLign['values'][A_POSITIO.index('Cover')])
				self.albumname = curLign['values'][A_POSITIO.index('Name')]
				self.ScoreAlbum = len(curLign['values'][A_POSITIO.index('Score')])
				self.AlbumPath = convertUNC(curLign['values'][A_POSITIO.index('Path')])
				self.Id_CD = curItem
				self.CurentAlbum = curItem
				# MAJ SCORE ALBUM
				self.posalbum_scale.config(state='normal')
				# FILL TREE ALBUMS
				counter = cpt_len = 0
				req = (getRequest('trackslist', self.MODE_SQLI)).format(id=self.Id_CD)
				tracks = buildTabFromRequest(self.con, req)
				for track in tracks:
					# SEARCH IN TRACKS
					if self.searchtracks.get() == 1 and (self.var_searchtext_value.get().lower() in track[A_POSITIO.index('Category')].lower() or self.var_searchtext_value.get().lower() in track[A_POSITIO.index('Family')].lower()):
						tag = '2'
					else:
						tag = str(counter%2)
					self.treealb.insert("", counter, iid=track[T_POSITIO.index('ID_TRACK')], values = track, tag = tag)
					# SCORE DISPLAY
					self.treealb.set(track[T_POSITIO.index('ID_TRACK')], column=T_POSITIO.index('Score'), value=track[T_POSITIO.index('Score')]*'★')
					counter += 1
					cpt_len += sum(int(x) * 60 ** i for i,x in enumerate(reversed(track[3].split(":"))))
				# first line by defaut
				if counter > 0: self.CurentTrack = self.treealb.get_children()[0]
				# extract infos label
				albumnamet, infoslabel = albumNameExtract(self.albumname, str(curLign['values'][A_POSITIO.index('Label')]), 
																		str(curLign['values'][A_POSITIO.index('ISRC')]),
																		str(curLign['values'][A_POSITIO.index('Qty_CD')]))
				# MAJ ALBUM NAME
				txt_album = albumnamet + "\n{year} • {tracks} • {dur} • {cd} • {art}\n{lab}".format(year=str(curLign['values'][A_POSITIO.index('Year')]),
																		tracks = displayCounters(counter, 'track'),
																		dur = displayCounters(int(((cpt_len/60)*10)/10),'min'),
																		cd = displayCounters(curLign['values'][A_POSITIO.index('Qty_CD')], 'CD'),
																		art = displayCounters(curLign['values'][A_POSITIO.index('Qty_covers')], 'ArtWork'),
																		lab = infoslabel)
				self.stralbumname.set(txt_album)
		else:
			# MAJ ALBUM INFO
			self.Curalbmd5 = None
			self.pathcover = TEXT_NCO
			self.albumname = None
			self.ScoreAlbum = 0
			self.Id_CD = None
			self.CurentAlbum = None
			self.AlbumPath = None
			self.CurentTrack = None
			# DEL LIST TRACKS
			self.treealb.delete(*self.treealb.get_children())
			# DISABLED SCORE
			self.posalbum_scale.config(state='disabled')
			# NO ALBUM NAME
			self.stralbumname.set('No Album Selected')
		# MAJ SCORE ALB
		self.posalbum_scale.set(self.ScoreAlbum)
		self.ScoAlbumlb.set(displayStars(self.ScoreAlbum, SCOR_ALBUMS))
		# MAJ COVERS
		monimage = buildCover(self.con, self.pathcover , self.Curalbmd5)
		monimage = monimage.resize((COVE_SIZ, COVE_SIZ), Image.ANTIALIAS)
		photo = ImageTk.PhotoImage(monimage)
		self.labcover.configure(image = photo)
		self.labcover.image = photo
		# MAJ TRACK INFO
		self.getInfosTrack(self.CurentTrack)
	
	def getInfosTrack(self, curItem):
		"""Display track infos select."""
		if self.treealb.get_children():
			curLign = self.treealb.item(curItem)
			#self.treealb.selection_set(curItem)
			#self.treealb.focus(curItem)
			self.ScoreTrack = len(curLign['values'][T_POSITIO.index('Score')])
			self.ID_TRACK = curItem
			self.CurentTrack = curItem
			# ENABLED SCORE
			self.postrack_scale.config(state='normal')
		else:
			self.ScoreTrack = 0
			self.ID_TRACK = None
			self.CurentTrack = None
			# DISABLED SCORE
			self.postrack_scale.config(state='disabled')
		# MAJ SCORE ALB
		self.postrack_scale.set(self.ScoreTrack)
		self.ScoTracklb.set(displayStars(self.ScoreTrack, SCOR_TRACKS))
	
	def getFolder(self):
		"""Open album folder."""
		openFolder(self.AlbumPath)
	
	def openTagScan(self):
		"""Open program TAGs. edit """
		runCommand(TAGS_SCAN, self.AlbumPath)
	
	def changeDisplayNoList(self, event=None):
		"""Enlarge thunbnails display, no grid."""
		self.framealbumlist.pack_forget()
		self.frameThunbnails.pack(expand=TRUE)
		# reconfigure commands
		self.btn_display.configure(text='≡', command=self.reinitDisplay)
		self.bind("<F11>", self.reinitDisplay)
	
	def reinitDisplay(self, event=None):
		"""Reinit display thunbnails + grid."""
		self.frameThunbnails.pack_forget()
		self.cadrealbum.pack_forget()
		self.cadrescoretrack.pack_forget()
		self.cadrStatusBar.pack_forget()
		# replace thunbnails + grid
		self.frameThunbnails.pack(side=TOP, anchor=W, fill=BOTH, expand=FALSE)
		self.framealbumlist.pack(side=TOP, anchor=W, fill=BOTH, expand=TRUE)
		self.cadrealbum.pack(side=TOP, anchor=W, fill=BOTH, expand=FALSE)
		self.cadrescoretrack.pack(side=TOP, fill=BOTH)
		self.cadrStatusBar.pack(side=BOTTOM, anchor=S+W, fill=BOTH)
		# reconfigure commands
		self.btn_display.configure(text='≠', command=self.changeDisplayNoList)
		self.bind("<F11>", self.changeDisplayNoList)
	
	def zoomChange(self, event):
		"""Change current Zoom coefficient."""
		step = 1/4
		nbstep = 3
		if event.delta > 0 and self.coef >= step: 
			self.coef -= step
		elif event.delta < 0 and self.coef <= 1+(nbstep*step): 
			self.coef += step
		self.squarethunbnails = int(DBAlbumsMainGui.WIDT_PICM*self.coef)
		# default 
		if self.coef < 1-(nbstep*step) or self.coef > 1+(nbstep*step):
			self.coef = 1
			self.squarethunbnails = DBAlbumsMainGui.WIDT_PICM
		# display thunbnails
		self.displayThunbnails()
	
	def displayZoom(self, display):
		"""Display current Zoom coefficient."""
		if display:
			self.canvdiszoomp.create_rectangle(0, 0, self.canvdiszoomp.winfo_width() , self.canvdiszoomp.winfo_height(), fill="black")
			#self.canvdiszoomp.create_oval(0, 0, self.canvdiszoomp.winfo_width() , self.canvdiszoomp.winfo_height(), fill="black")
			self.canvdiszoomp.create_text(self.canvdiszoomp.winfo_width()/2, self.canvdiszoomp.winfo_height()/2, text=str(int(self.coef*100))+'%', font=self.zoomfont, fill="green yellow")
		else:
			self.canvdiszoomp.delete(ALL)
	
	def playerMedias(self):
		"""Player Audio thread pyQT5."""
		# track selected
		self.curLign = self.treealb.item(self.CurentTrack)
		fileselect = path.join(self.curLign['values'][T_POSITIO.index('REP_Track')], self.curLign['values'][T_POSITIO.index('FIL_Track')])
		# build list medias & position track selected
		lismedia = []
		position = 1
		for SelItem in self.treealb.get_children():
			file = path.join(self.treealb.item(SelItem)['values'][T_POSITIO.index('REP_Track')], self.treealb.item(SelItem)['values'][T_POSITIO.index('FIL_Track')])
			if file == fileselect:
				curentposition = position
			lismedia.append(convertUNC(file))
			position += 1
		# actif audio process, close
		try:
			if self.tplay.is_alive():
				self.tplay.terminate()
				self.tplay.close()
				sleep(0.1)
		except Exception:
			pass
		# process player audio
		self.tplay = Process(target = playerProcessAudio, args = (lismedia, curentposition, self.winfo_x()+3, self.winfo_y()+self.winfo_height()-43))
		self.tplay.daemon = True
		self.tplay.start()
		
	def exportAlbums(self):
		"""Export file cover or list albums select in grid."""
		fileprop = datetime.now().strftime('%Y%m%d%H%M%S') + "_Albums.csv"
		filename = asksaveasfile(mode='w', 
								 initialdir = getcwd(), 
								 initialfile = fileprop, 
								 defaultextension = ".csv", 
								 filetypes = [('CSV Files', '.csv'), ('Image files', '.jpg')], 
								 title = "Export from CSV File list or cover jpeg Files")
		if filename is None: return
		extension = path.splitext(filename.name)[1][1:]
		ListeSelect = self.tree.selection()
		# extract file CSV
		if extension == 'csv':
			wr = writer(filename, delimiter=';', doublequote=True, quoting=QUOTE_ALL, lineterminator='\n')
			for SelItem in ListeSelect:
				Album = self.tree.item(SelItem)
				wr.writerow(Album['values'])
			filename.close()
			showinfo('Export csv list Albums','Create file csv Sucessfull to :'+filename)
			openFolder(path.dirname(filename))
		# extract base64\mysql to file JPEG 
		if extension == 'jpg':
			filename.close()
			remove(filename.name)
			for SelItem in ListeSelect:
				Album = self.tree.item(SelItem)
				filecover = path.join(path.dirname(filename.name), Album['values'][A_POSITIO.index('Name')])
				extension = path.splitext(Album['values'][A_POSITIO.index('Cover')])[1][1:]
				filecover = QUOTE_ALL
				buildFileCover(self.con, filecover, Album['values'][A_POSITIO.index('MD5')])
			showinfo('Export covers Albums','Create covers Sucessfull to :'+path.dirname(filename.name))
			openFolder(path.dirname(filename.name))
	
	def showloadingWin(self, event=None):
		"""Display stats base"""
		if self.loadingWin.state() == 'withdrawn':
			self.loadingWin.update()
			self.loadingWin.deiconify()
			self.loadingWin.focus_set()
		else:
			self.loadingWin.withdraw()
	
	def CreateLocalBase(self):
		"""Create base Sqlite."""
		filename = BASE_SQLI.format(envt=self.Envs+'_SQLITE')
		# remove if exist
		if path.isfile(filename):
			remove(filename)
		logname = datetime.now().strftime("%Y%m%d%H%M%S") + "_COPY_DATABASE_TO_SQLITE_" + self.Envs + ".log"
		copyDatabaseInvent(self.con, filename, self.statusBar, path.join(LOGS_PROG, logname))
		showinfo("Create Database SQLite", "Create Database SQLite :"+filename+" Sucessfull", icon='info')
	
	def importFoobar(self):
		"""Foobar2000 playlists operations."""
		# import fpl playlist to mysql DBFOOBAR
		numtracks = foobarMajDBFOOBAR(self.con, self.statusBar, FOOB_PLAY)
		# synchro score sql
		execSqlFile(self.con, self.statusBar, FOOB_UPSC , 9)
		showinfo("Import Playlists Foobar 2000", "Import & Synchro Score Sucessfull: "+str(numtracks)+" Tracks in base", icon='info')
	
	def updateAlbums(self):
		"""Execute powershell Script update albums infos."""
		ListeSelect = self.tree.selection()
		eCommand = buildCommandPowershell(PWSH_SCRU, '-listID_CD', ','.join(ListeSelect), '-Envt', self.Envs)
		#print(eCommand)
		DisplaySubprocessGui( eCommand, 'Update '+ displayCounters(len(ListeSelect), "Album "))
	
	def buildInvent(self, category = None):
		"""Execute powershell Script update all albums infos."""
		if 'LOSSLESS' in self.Envs:
			filescript = PWSH_SCRI.format(mod='LOSSLESS')
		else:
			filescript = PWSH_SCRI.format(mod='MP3')
		if category != None:
			eCommand = buildCommandPowershell(filescript, '-Envt', self.Envs, '-Collections', category)
		else:
			eCommand = buildCommandPowershell(filescript, '-Envt', self.Envs)
		#print(eCommand)
		DisplaySubprocessGui(eCommand, 'Update Base '+self.Envs)
		#self.connectEnvtBase(True)
	
	def viewArtWorks(self):
		"""views artworks covers storage."""
		CoversArtWorkViewGui(self.AlbumPath, self.albumname, self.pathcover, self.heightmainwindow,  self.heightmainwindow, self.squarethunbnails)
	
	def dropAddFolders(self, action, actions, type, win, X, Y, x, y, data):
		""" Drag & Drop Folder for Add Powershell script."""
		listfolders = []
		badlist = []
		for addfolder in data[1:-1].split('} {'):
			addfolder = r''+addfolder.replace('/','\\')
			addfolder = convertUNC(addfolder)
			if addfolder.startswith(convertUNC(self.homeMedias)):
				listfolders.append(addfolder)
			else:
				badlist.append(addfolder)
		if len(badlist)>0 and len(listfolders) == 0:
			showinfo("Drag & Drop Folders: bad selection", badlist, icon='warning')
		if len(listfolders) > 0:
			title = 'Add/Update '+displayCounters(len(listfolders),'Album')+' to database '+self.Envs
			if askyesno(title, listfolders):
				eCommand = buildCommandPowershell(PWSH_SCRA, '-AlbumReps', ','.join(listfolders), '-Envt', self.Envs)
				DisplaySubprocessGui(eCommand, title)
	
	def quitDBAlbumsMain(self):
		"""Exit program."""
		#close player processing ?
		try:
			if self.tplay.is_alive():
				self.tplay.terminate()
				self.tplay.close()
				self.tplay.join()
		except Exception:
			pass
		self.con.close()
		self.destroy()
		self.quit()


###################################################################
# MAIN MINI GUI
class DBAlbumsMainMiniGui(Tk):
	"""Version Mini."""
	width  = 400
	height = 300
	heightcover = 1024 # cover
	def __init__(self , parent):
		Tk.__init__(self , parent)
		self.parent = parent
		self.tk.call('encoding', 'system', 'utf-8')
		self.protocol("WM_DELETE_WINDOW", self.quitDBAlbumsMainMini)
		# Dimensions
		initGuiTK(self, DBAlbumsMainMiniGui.width, DBAlbumsMainMiniGui.height, True, True)
		self.title(TITL_PROG)
		# Style
		s=Style()
		s.theme_use('clam')
		# Line of entry
		cdr_search = Frame(self)
		cdr_search.pack(fill=BOTH)
		labelDir=Label(cdr_search, text="Search ")
		labelDir.pack(side=LEFT, padx=5, pady=5)
		self.var_searchtext_value = StringVar(None)
		ligne_texte = AutocompleteEntry(cdr_search, textvariable=self.var_searchtext_value, width=30)
		ligne_texte.bind("<Return>", self.searchMySQL)
		ligne_texte.focus()
		ligne_texte.pack(side=LEFT, padx=5, pady=5)
		btn_clear = Button(cdr_search, text='✖', width=2, command = self.clearSearchAlbums)
		btn_clear.pack(side=LEFT, padx=0, pady=5)
		btn_sear = Button(cdr_search, text='➜', width=2,command= self.searchMySQL)
		btn_sear.pack(side=LEFT, padx=5, pady=5)
		# Treeview 
		cdr_tabtree = Frame(self)
		cdr_tabtree.pack(fill=BOTH, expand=TRUE)
		self.tree = buildTree(cdr_tabtree,  A_COLNAME, A_C_WIDTH, 10, True)
		self.tree.bind("<Double-1>", self.onPressCover)
		self.tree.pack(side=TOP, anchor=W, fill=BOTH, expand=TRUE)
		# Result
		cdr_result = Frame(self)
		cdr_result.pack(fill=BOTH)
		self.Resultat = StringVar()
		labelRes=Label(cdr_result, textvariable=self.Resultat)
		labelRes.pack(side=LEFT, padx=5, pady=5)
		# cnx 
		self.con, self.MODE_SQLI, self.homeMedias = connectDatabase('LOSSLESS')
		# auto-completion
		completion_list = buildListFromRequest(self.con, getRequest('autocompletion', self.MODE_SQLI))
		ligne_texte.set_completion_list(completion_list)
		# fill list albums
		self.Tabs = buildTabFromRequest(self.con, getRequest('albumslist', self.MODE_SQLI))
		# go
		self.searchMySQL()
	
	def searchMySQL(self, event=None):
		self.tree.delete(*self.tree.get_children())
		counter = 0
		txt_search = self.var_searchtext_value.get()
		for row in self.Tabs:
			if  txt_search.lower() in row[A_POSITIO.index('Name')].lower() or txt_search.lower() in row[A_POSITIO.index('Label')].lower():
				self.tree.insert("", counter, iid=row[A_POSITIO.index('ID_CD')], values=row, tag = (counter%2))
				counter += 1
		self.Resultat.set('find ' + str(counter) + ' Album(s)')
	
	def clearSearchAlbums(self):
		self.var_searchtext_value.set('')
		self.searchMySQL()
		
	def onPressCover(self, event):
		"""Display cover MD5."""
		if self.tree.get_children():
			CurentAlbum = self.tree.identify('item',event.x,event.y)
			curLign = self.tree.item(CurentAlbum)
			self.Curalbmd5 = curLign['values'][A_POSITIO.index('MD5')]
			self.pathcover = convertUNC(curLign['values'][A_POSITIO.index('Cover')])
			self.albumname = curLign['values'][A_POSITIO.index('Name')]
			if self.pathcover[0:len(TEXT_NCO)] != TEXT_NCO:
				monimage = buildCover(self.con, self.pathcover, self.Curalbmd5)
				CoverViewGui( monimage, self.albumname, DBAlbumsMainMiniGui.heightcover, DBAlbumsMainMiniGui.heightcover)
				
	def quitDBAlbumsMainMini(self):
		"""Exit."""
		self.con.close()
		self.destroy()
		self.quit()


###################################################################
# START
if __name__ == "__main__":
	# Version MINI/ NORMAL ?
	#argv.append('MINI') #TEST
	if len(argv)>1:
		if argv[1] == 'MINI':
			TITL_PROG = TITL_PROG.replace('DBAlbums','DBAlbums mini')
			app = DBAlbumsMainMiniGui(None)
		else:
			print('bad parameter '+argv[1])
	else:
		app = DBAlbumsMainGui(None)
	app.mainloop()
