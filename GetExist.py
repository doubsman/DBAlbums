#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GetExist History Version
#  1.21 Tagscan + sdtout powershell
#  1.20 Artworks viewer
#  1.19 integration Powershell script
#  1.18 Execute Powershell script BUILD_INVENT.ps1 + BUILD_INVENT_UPDATEALBUM.ps1
#  1.17 base sqllite (create base + offline mode)
#  1.16 score album + track
#  1.15 player music pyQT5
#  1.14 stats + play music 
#  1.13 best performance mysql
#  1.12 fusion gui albmus/tracks windows
#  1.11 fixed bugs
#  1.10 refresh buttons + tdc loading
#  1.09 extract cover mysql/base64 to file
#  1.08 adaptation python 2.7 (py2exe) et 3.5.2
#  1.07 combos category/family
#  1.06 adaptation Ubuntu + base64
#  1.05 autocompletion
#  1.04 constantes
#  1.02 export csv
#  1.01 gestion covers
#  1.00 search base INVENT mysql TEST/PRODUCTION

# python 2.7
#import Tkinter
#from Tkinter import *
#import ttk
#import tkFont
#import tkFileDialog
#import datetime

# python 3.5.2
# python3 -m pip install pymysql
import sys
import tkinter as tk
from tkinter import * #Tk, Label, Entry, Canvas, Frame, StringVar
from tkinter.filedialog import asksaveasfile
from tkinter.ttk import Treeview, Combobox, Scrollbar
from tkinter.font import Font
from threading import Thread
from os import system, path, getcwd, name, remove, walk
from pymysql import connect as connectmysql
from sqlite3 import connect as connectsqlite3
from subprocess import check_call, call, Popen, PIPE
from datetime import datetime
from PIL import Image, ImageTk
from csv import writer, QUOTE_ALL
from io import BytesIO
from base64 import b64decode, decodestring
from time import sleep
# functions
from GetExistPlayer import PlayerProcess
from GetExistCopyDatabaseToSqlite import CopyDatabaseInvent


###################################################################
# CONSTANTS
VERS_PROG = '1.21'
TITL_PROG = "DB Albums v{v} (2016)".format(v=VERS_PROG)
PATH_PROG = path.dirname(__file__)
LOGS_PROG = path.join(PATH_PROG, 'Logs')
# TAG
TAGS_SCAN = '\\\\HOMERSTATION\_Synchro\_Apps_Portables\\tagscan_6.0.4\Tagscan.exe'
# LOCAL SQLLITE
BASE_SQLI = path.join(PATH_PROG, 'local', "Invent_{envt}.db")
# INVENT POWERSHELL
PWSH_SCRI = path.join(PATH_PROG, 'PS1', "BUILD_INVENT_{mod}.ps1")
PWSH_SCRU = path.join(PATH_PROG, 'PS1', "UPDATEALBUM.ps1")
# EXT COVERS
MASKCOVERS = ('.jpg','.jpeg','.png','.bmp','.tif','.bmp')
# SCORE ALBUMS
SCOR_ALBUMS = { 0 : 'not listened',
				1 : 'listened',
				2 : 'Less 3 tracks well',
				3 : 'More 3 tracks well',
				4 : 'top',
				5 : 'best'}
# SCORE TRACKS
SCOR_TRACKS = { 0 : 'not listened',
				1 : 'listened',
				2 : 'top',
				3 : 'best'}
# GUI
WIDT_MAIN = 1280
HEIG_MAIN = 1024
# mysql
# PRODS
SERV_PROD = 'homerstation'
USER_PROD = 'AdmInvent'
PASS_PROD = 'JMctOz7a6TWnrJHB86pL'
BASE_PROD = 'Invent'
SERV_MP3S = 'homerstation'
USER_MP3S = 'admInventMP3'
PASS_MP3S = 'nuDbC6spVZxtkKC8'
BASE_MP3S = 'InventMP3'
# TEST
SERV_TEST = 'doubbigstation'
USER_TEST = 'admInvent'
PASS_TEST = 'MwRbBR2HA8PFQjuu'
BASE_TEST = 'Invent'
SERV_MP3T = 'doubbigstation'
USER_MP3T = 'admInvent'
PASS_MP3T = 'MwRbBR2HA8PFQjuu'
BASE_MP3T = 'MP3'
# gui
NAME_EVT = ('LOSSLESS', 'MP3', 'LOSSLESS_TEST', 'MP3_TEST')
CURT_EVT = 3 # 0 LOSSLESS
WINS_ICO = "GetExist.ico"
UNIX_ICO = 'GetExist.png'
PICT_NCO = 'cd-blank.gif'
TEXT_NCO = 'No Picture'
TREE_CO0 = 'gray85'
TREE_CO1 = 'gray90'
TREE_CO2 = 'lightSteelBlue1'
TREE_CO3 = 'snow'
# REQS
# combo Category
D_REQUEST = "SELECT '*' AS Category UNION SELECT Category from DBALBUMS group by Category"
# combo Family
E_REQUEST = "SELECT '*' AS Family UNION SELECT Family from DBALBUMS group by Family"
### ALBUMS
#  request mysql
A_REQUEST = "SELECT ID_CD AS ID, Category, Family, Name, Label, ISRC, `Year`, Size, Length, Qty_CD AS `CD`, Qty_Tracks AS Trks, Qty_covers AS Pic, Score As SCR, Typ_Tag AS Tag, CONCAT(Position1,'\\\\',Position2) AS Position, Path, Cover, `MD5`, Date_Insert AS `Add`, Date_Modifs AS `Modified` FROM DBALBUMS ORDER BY Date_Insert DESC"
#  request sqllite
Z_REQUEST = "SELECT ID_CD AS ID, Category, Family, Name, Label, ISRC, `Year`, Size, Length, Qty_CD AS `CD`, Qty_Tracks AS Trks, Qty_covers AS Pic, Score As SCR, Typ_Tag AS Tag, Position1 || '\\' || Position2 AS Position, Path, Cover, `MD5`, Date_Insert AS `Add`, Date_Modifs AS `Modified` FROM DBALBUMS ORDER BY Date_Insert DESC"
#  request autocompletion: artists + labels
S_REQUEST = "SELECT Synthax FROM VW_DBCOMPLETION ORDER BY Synthax"
#  request Update Sore Album
U_REQUEST = "UPDATE DBALBUMS SET `Score`={score} WHERE `ID_CD`={id}"
#  columns position
A_POSITIO = {'ID_CD' 		: 0, 'Category'		: 1, 
			 'Family'		: 2, 'Name'			: 3,
			 'Label'		: 4, 'ISRC'			: 5, 
			 'Year'			: 6, 'Size'			: 7, 
			 'Length'		: 8, 'Qty_CD'		: 9,
			 'Qty_Tracks'	: 10, 'Qty_covers'	: 11,
			 'Score'		: 12, 'Typ_Tag'		: 13,
			 'Position'		: 14, 'Path'		: 15,
			 'Cover'		: 16, 'MD5'			: 17,
			 'Date_Insert'	: 18, 'Date_Modifs'	: 19}
#  treeview columns width
A_C_WIDTH = (40,60,60,270,90,60,40,35,50,25,25,30,30,30,80,200,200,200,67,67)
### TRACKS
#  request mysql/sqllite
T_REQUEST = "SELECT ODR_Track AS `N°`, TAG_Artists AS Artist, TAG_Title AS Tittle, TAG_length AS Length, Score As SCR, TAG_Genres AS `Style`, FIL_Track AS File, REP_Track AS Folder, ID_TRACK AS `ID` FROM DBTRACKS WHERE ID_CD={id} ORDER BY ODR_Track"
#  request search tracks
B_REQUEST = "SELECT ID_CD AS ID FROM DBTRACKS AS TRK WHERE TAG_Artists like '%{search}%' OR TAG_Title like '%{search}%' GROUP BY ID_CD"
#  Update Sore Track
V_REQUEST = "UPDATE DBTRACKS SET `Score`={score} WHERE `ID_TRACK`={id}"
#  columns position
T_POSITIO = {'ODR_Track'	: 0, 'TAG_Artists'	: 1, 
			 'TAG_Title'	: 2, 'TAG_length'	: 3, 
			 'Score'		: 4, 'TAG_Genres'	: 5, 
			 'FIL_Track'	: 6, 'REP_Track'	: 7, 
			 'ID_TRACK'		: 8}
#  treeview columns width
T_C_WIDTH = (50,150,200,60,30,70,200,200,50)
### COVERS
#  cover blob
C_REQUEST = "SELECT `MD5`, `Cover64` FROM DBCOVERS WHERE `MD5`='{MD5}'"


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
	if envt == 'LOSSLESS':
		server = SERV_PROD
		userdb = USER_PROD
		namedb = BASE_PROD
		passdb = PASS_PROD
	else: 
		if envt == 'MP3':
			server = SERV_MP3S
			userdb = USER_MP3S
			namedb = BASE_MP3S
			passdb = PASS_MP3S
		else:
			if envt == 'MP3_TEST':
				server = SERV_MP3T
				userdb = USER_MP3T
				namedb = BASE_MP3T
				passdb = PASS_MP3T
			else:
				if envt == 'LOSSLESS_TEST':
					server = SERV_TEST
					userdb = USER_TEST
					namedb = BASE_TEST
					passdb = PASS_TEST
				else:
					server = SERV_TEST
					userdb = USER_TEST
					namedb = BASE_TEST
					passdb = PASS_TEST
	try:
		# MYSQL
		MODE_SQLI = False
		con = connectmysql( host=server, 
							user=userdb, 
							passwd=passdb, 
							db=namedb,
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

def GetListColumns(con, req):
	"""List columns from request MySQL/Sqlite."""
	req = req + " LIMIT 0"
	cur = con.cursor()    
	cur.execute(req)
	col_names = list(map(lambda x: x[0], cur.description))
	cur.close()
	return col_names

def SelectTOTab(con, req):
	"""Select Mysql/Sqlite to memory list."""
	cur = con.cursor()    
	cur.execute(req)
	rows = cur.fetchall()
	cur.close()
	return rows

def SelectTODict(con, req):
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
	col_names = SelectTOTab(con, req)
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

def UpdateBaseScore(con, score, id, req):
	"""Maj Mysql table Albums."""
	req = req.format(score=score, id=id)
	with con.cursor() as curs:
		curs.execute(req)
	curs.close()
	con.commit()

def CreateListCompletion(con, req=S_REQUEST):
	"""list for utocompletion."""
	Tabs = SelectTOTab(con, req)
	completion_list = []
	for row in Tabs:
		completion_list.insert(0,row[0])
	return completion_list

def TreeviewSortColumn(tv, col, reverse):
	"""sort column treeview."""
	l = [(tv.set(k, col), k) for k in tv.get_children('')]
	l.sort(reverse=reverse)
	# rearrange items in sorted positions
	for index, (val, k) in enumerate(l):
		tv.move(k, '', index)
	# reverse sort next time
	tv.heading(col, command=lambda	c=col: TreeviewSortColumn(tv, c, not reverse))

def BuildTree(con, cadreresult, req, colWidth, line=15, scroll=False):
	"""Build Columns treeview."""
	col_names = GetListColumns(con, req)
	tree = Treeview(cadreresult, height=line, columns=col_names, show="headings")
	tree["columns"] = col_names
	counter = 0
	for col_name in col_names:
		tree.heading(col_name, text=col_name.title(),command=lambda c=col_name: TreeviewSortColumn(tree, c, False))
		tree.column(col_name,width=colWidth[counter])
		counter += 1
	tree.tag_configure('0', background=TREE_CO0)
	tree.tag_configure('1', background=TREE_CO1)
	tree.tag_configure('2', background=TREE_CO2)
	tree.tag_configure('3', background=TREE_CO3)
	if scroll:
		ysb = Scrollbar(cadreresult, orient=VERTICAL)
		ysb.pack(side=tk.RIGHT, fill=tk.Y)
		ysb.config(command=tree.yview)
		xsb = Scrollbar(cadreresult, orient=tk.HORIZONTAL)
		xsb.pack(side=tk.BOTTOM, fill=tk.X)
		xsb.config(command=tree.xview)
		tree.configure(yscrollcommand=ysb.set,xscrollcommand=xsb.set)
	return (tree)

def DisplayCounters(num = 0, text = '' ):
	"""format 0 000 + plural."""
	strtxt = " %s%s" % (text, "s"[num==1:])
	if num > 9999:
		strnum = '{0:,}'.format(num).replace(",", " ")
	else:
		strnum = str(num)
	return (strnum + strtxt)

def DisplayStars(star, scorelist):
	max = len(scorelist)-1
	txt_score =  scorelist[star]
	return(txt_score+'  '+star*'★'+(max-star)*'☆')

def BuildIco(Gui):
	"""Icon windows or linux/mac."""
	if "nt" == name:
		#windows
		Gui.iconbitmap(WINS_ICO)
	else:
		#linux : os mac non prévu
		myico = PhotoImage(file=UNIX_ICO)
		Gui.tk.call('wm', 'iconphoto', Gui._w, myico)

def BuildCover(con, pathcover, md5):
	"""Get base64 picture cover mysql/sqlite."""
	if pathcover[0:len(TEXT_NCO)] == TEXT_NCO: 
		# no cover
		monimage = Image.open(PICT_NCO)
	else:
		# cover base64/mysql
		req = C_REQUEST.format(MD5=md5)
		Tableau = SelectTOTab(con, req)
		monimage = Image.open(BytesIO(b64decode(Tableau[0][1])))
	return (monimage)

def BuildFileCover(con, namefile, pathcover, md5):
	"""Build cover base64/mysql to file."""
	#no cover
	if pathcover[0:len(TEXT_NCO)] != TEXT_NCO: 
		#mysql
		req = C_REQUEST.format(MD5=md5)
		Tableau = SelectTOTab(con, req)
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
			if filename[-4:] in masks:
				yield path.join(folderName,filename)

def OpenComand(progra, params):
	"""Execute une commande system."""
	command = """{tprogra} "{tparams}" """.format(tprogra=progra,tparams=params)
	system(command)

# opening-a-folder-in-explorer-nautilus-mac-thingie
if sys.platform == 'darwin':
	def openFolder(path):
		check_call(['open', '--', path])
elif sys.platform == 'linux2':
	def openFolder(path):
		check_call(['xdg-open', '--', path])
elif sys.platform == 'win32':
	def openFolder(path):
		OpenComand('explorer', path)

def ExcecutePowershell(script, *argv):
	Command = [r'powershell.exe',
				'-ExecutionPolicy', 'RemoteSigned',
				'-File', 
				script]
	for arg in argv:
		Command += (arg,)
	p = Popen(Command, stdin=sys.stdout, stdout=sys.stdout, stderr=sys.stdout)
	return p
	#out, err = p.communicate()
	#returncode = p.wait()
	#print (returncode)
	#print (out)

def BuildCommandPowershell(script, *argv):
	Command = [r'powershell.exe',
				'-ExecutionPolicy', 'RemoteSigned',
				'-File', 
				script]
	for arg in argv:
		Command += (arg,)
	return Command

def getFileNameWithoutExtension(path):
	return path.split('\\').pop().split('/').pop().rsplit('.', 1)[0]

# auto-completion
tk_umlauts=['odiaeresis', 'adiaeresis', 'udiaeresis', 'Odiaeresis', 'Adiaeresis', 'Udiaeresis', 'ssharp']
class AutocompleteEntry(tk.Entry):
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
				self.delete(self.position, tk.END)
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
				self.delete(0,tk.END)
				self.insert(0,self._hits[self._hit_index])
				self.select_range(self.position,tk.END)

	def handle_keyrelease(self, event):
		"""event handler for the keyrelease event on this widget"""
		if event.keysym == "BackSpace":
				self.delete(self.index(tk.INSERT), tk.END)
				self.position = self.index(tk.END)
		if event.keysym == "Left":
				if self.position < self.index(tk.END): # delete the selection
						self.delete(self.position, tk.END)
				else:
						self.position = self.position-1 # delete one character
						self.delete(self.position, tk.END)
		if event.keysym == "Right":
				self.position = self.index(tk.END) # go to end (no selection)
		if event.keysym == "Down":
				self.autocomplete(1) # cycle to next hit
		if event.keysym == "Up":
				self.autocomplete(-1) # cycle to previous hit
		if len(event.keysym) == 1 or event.keysym in tk_umlauts:
				self.autocomplete()


###################################################################
# LOADING GUI
class LoadingGui():
	"""Fenetre loading."""
	def __init__(self , MyTopLevel, con, MODE_SQLI, sleeptime=0):
		self.MyTopLevel = MyTopLevel
		self.MyTopLevel.geometry("400x290")
		self.MyTopLevel.attributes('-topmost', True)
		CenterWindows(self.MyTopLevel)
		BuildIco(self.MyTopLevel)
		self.MyTopLevel.title("Loading Datas")
		self.MyTopLevel.resizable(width=False, height=False)
		self.MyTopLevel.overrideredirect(True)
		# messages
		customFont = Font(family="Calibri", size=14)
		cadretittle = tk.Frame(self.MyTopLevel, width=380, height=50, bd=3, relief=SUNKEN)
		cadretittle.pack(fill=tk.BOTH)
		cadretittle.bind("<Button-1>", self.HideLoadingGui)
		monimage = Image.open(UNIX_ICO)
		monimage = monimage.resize((100, 100), Image.ANTIALIAS)
		photo = ImageTk.PhotoImage(monimage)
		prj_label = tk.Label(cadretittle, image = photo)
		prj_label.image = photo
		prj_label.pack(side=tk.LEFT, padx=10, pady=10)
		message = StringVar()
		if MODE_SQLI:
			txt_message = "SQLite Base (mode offline)"
		else:
			txt_message = "Mysql Base"
		message.set(TITL_PROG+"\nConnected "+txt_message+'.'*sleeptime)
		mes_label = tk.Label(cadretittle, textvariable=message, font=customFont)
		mes_label.pack(side=tk.LEFT, padx=5, pady=5)
		# stats
		MAX_LINES = 6
		cadrestats = tk.Frame(self.MyTopLevel)
		cadrestats.pack(fill=tk.BOTH)
		req = BuildReqTCD(con, "Category" , "Family", "DBALBUMS", "BASE ALBUMS", "1", True)
		treeload = BuildTree(con, cadrestats, req, (50,50,50,50,50), MAX_LINES)
		Tabs = SelectTOTab(con, req)
		counter = 0
		for row in Tabs:
			tag = (counter%2)
			if (counter + 1) == len(Tabs): tag = 3
			treeload.insert("", counter, iid='Row_%s'%counter, values=row, tag = tag)
			counter += 1
		# add scrollbar ?
		if counter > MAX_LINES:
			ysb = Scrollbar(cadrestats, orient=VERTICAL)
			ysb.pack(side=tk.RIGHT, fill=tk.Y)
			ysb.config(command=treeload.yview)
			treeload.configure(yscrollcommand=ysb.set)
		treeload.pack(side=tk.TOP, anchor=tk.W, fill=tk.BOTH, padx=5, pady=5)
		# windows
		self.MyTopLevel.update_idletasks()
		# waiting
		counter = sleeptime
		while counter != 0:
			sleep(1)
			counter -= 1
			message.set(TITL_PROG+"\nConnected "+txt_message+'.'*counter + ' '*(sleeptime-counter))
			self.MyTopLevel.update_idletasks()
		
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
		#self.master.overrideredirect(True)
		
		width, height = monimage.size
		self.master.title("{name} - [{w}x{h}] orignal size:[{wo}x{ho}]".format(w=w, h=h, name=namealbum, wo=str(width), ho=str(height)))
		monimage = monimage.resize((w, h), Image.ANTIALIAS)
		photo = ImageTk.PhotoImage(monimage)
		label = tk.Label(self.master, image = photo)
		label.image = photo
		label.bind("<Button-1>", self.QuitCoverViewGui)
		label.pack()
	
	def QuitCoverViewGui(self, event):
		self.master.destroy()

class CoversViewGui():
	"""Fenetre view covers."""
	def __init__(self, master, pathalbum, namealbum):
		# Windows
		self.master = master
		self.master.attributes('-topmost', True)
		self.master.resizable(width=False, height=False)
		BuildIco(self.master)
		self.master.title("reading files covers...")
		# build list covers
		self.namealbum = namealbum
		self.fileslist = list(GetListFiles(pathalbum, MASKCOVERS))
		self.numbersCov = len(self.fileslist)
		self.counterCov = 0
		self.label = tk.Label(self.master)
		self.label.bind("<Button-3>", self.nextCov)
		self.label.bind("<Button-1>", self.QuitCoversViewGui)
		self.label.pack()
		self.master.bind("<Control-Key-c>", self.MakeCover)
		self.nextCov(None)
	
	def nextCov(self, event):
		"""next file covers."""
		self.currentCov = self.fileslist[self.counterCov]
		self.monimage = Image.open(self.currentCov)
		# measures
		width, height = self.monimage.size
		new_height = height
		new_width = width
		if width>WIDT_MAIN or height>HEIG_MAIN:
			# resize
			if (width-WIDT_MAIN) > (height-HEIG_MAIN):
				new_width  = WIDT_MAIN
				new_height = int(new_width * height / width)
			else:
				new_height = HEIG_MAIN
				new_width  = int(new_height * width / height)
			self.monimage = self.monimage.resize((new_width, new_height), Image.ANTIALIAS)
		# windows
		self.master.title("{c}/{n} - {name}  - {w}x{h}<{wo}x{ho}".format(c=(self.counterCov+1), n=(self.numbersCov), w=new_width, h=new_height, name=path.basename(self.currentCov), wo=str(width), ho=str(height)))
		self.master.geometry("{w}x{h}".format(w=new_width,h=new_height))
		CenterWindows(self.master)
		# cover
		self.covers = ImageTk.PhotoImage(self.monimage)
		self.label.configure(image = self.covers)
		self.label.image = self.covers
		# next cover
		self.counterCov += 1
		if self.counterCov == self.numbersCov:
			self.counterCov = 0
	
	def MakeCover(self, event):
		file_pictu = getFileNameWithoutExtension(self.currentCov)
		path_cover = self.currentCov.replace(file_pictu,'cover')
		self.monimage.save(path_cover)
	
	def QuitCoversViewGui(self, event):
		self.master.destroy()

class DisplaySubprocessGui():
	def __init__(self, master, eCommand, title):
		# Windows 
		self.master = master
		self.master.title(title)
		self.master.geometry("{w}x{h}".format(w=WIDT_MAIN,h=600))
		self.master.attributes('-topmost', True)
		self.master.resizable(width=False, height=False)
		BuildIco(self.master)
		CenterWindows(self.master)

		# Gui
		customFont = Font(family="Lucida Console", size=8)
		textarea = tk.Text(master, wrap='word', state='disabled', height=49, width=200, bg='black', fg='green', font=customFont)
		ysb = Scrollbar(master, orient=tk.VERTICAL)
		ysb.config(command=textarea.yview)
		ysb.pack(side=tk.RIGHT, fill=tk.Y)
		textarea.configure(yscrollcommand=ysb.set)
		textarea.pack(ipadx=4, padx=4, ipady=4, pady=4, fill=tk.BOTH)
		button = tk.Button(master, text="Kill", width=15, command=self.QuitDisplaySubprocessGui)
		button.pack(side=tk.BOTTOM, padx=4, pady=4)
		
		# launch process + output
		self.process = Popen(eCommand, stdout=PIPE, stderr=PIPE)
		for line in iter(self.process.stdout.readline, b''):
			#sys.stdout.write(str(line))
			textarea.configure(state='normal')
			textarea.insert('end', line.decode('cp850'))
			textarea.see('end')
			textarea.configure(state='disabled')
			self.master.update_idletasks()
		button.configure(text="Quit")
		
	def QuitDisplaySubprocessGui(self):
		self.process.kill() # exit (zombie!)
		self.master.destroy()

# MAIN GUI
class CoverMainGui(tk.Tk):
	"""Fenetre principale."""
	def __init__(self , master):
		tk.Tk.__init__(self , master)
		self.master = master
		self.title(TITL_PROG +' : initialisation...')
		# Icone
		BuildIco(self)
		self.resizable(width=True, height=False)
		self.geometry("{w}x{h}".format(w=WIDT_MAIN, h=HEIG_MAIN))
		CenterWindows(self)
		
		# media
		self.tplay = None
		
		#### SAISIE
		cadresaisie = tk.Frame(self)
		cadresaisie.pack(fill=tk.BOTH)
		# Label
		labelDir = tk.Label(cadresaisie, text="Search")
		labelDir.pack(side="left", padx=5, pady=5)
		# ligne de saisie
		self.var_texte = tk.StringVar(None)
		self.ligne_texte = AutocompleteEntry(cadresaisie, textvariable=self.var_texte, width=30)
		self.ligne_texte.bind("<Return>", self.OnPressEnter)
		self.ligne_texte.focus_set()
		self.ligne_texte.pack(side="left", padx=5, pady=5)
		# + search tracks
		self.searchtracks = IntVar()
		self.searchtracks.set(0)
		Checkbutton(cadresaisie, text="In Tracks", variable = self.searchtracks).pack(side=LEFT,padx=5,pady=5)
		# Style
		self.style_value = tk.StringVar()
		self.style = Combobox(cadresaisie, textvariable=self.style_value, state='readonly')
		self.style.pack(side="left", padx=5, pady=5)
		# Family
		self.family_value = tk.StringVar()
		self.family = Combobox(cadresaisie, textvariable=self.family_value, state='readonly')
		self.family.pack(side="left", padx=5, pady=5)
		# buttons
		btn_search = tk.Button(cadresaisie, text='Search', width=15, command = self.GetSearchAlbums)
		btn_search.pack(side="left", padx=5, pady=5)
		# combo
		self.combo_value = tk.StringVar()
		self.combo = Combobox(cadresaisie, textvariable=self.combo_value, state='readonly')
		self.combo['values'] = NAME_EVT
		self.combo.current(CURT_EVT)
		# popup menu base
		self.bMenu = tk.Menu(cadresaisie, tearoff=0)
		self.bMenu.add_command(label="Show infos", command=self.showloadingWin)
		self.bMenu.add_command(label="Refresh", command=self.RefreshBase)
		self.bMenu.add_command(label="Update (powershell)...", command=self.BuildInvent)
		self.bMenu.add_command(label="Create Local base (sqlite)", command=self.CreateLocalBase)
		self.combo.bind("<<ComboboxSelected>>", self.OnComboChange)
		self.combo.bind("<Button-3>", self.popupbase)
		self.combo.pack(side=tk.RIGHT, padx=15, pady=5)
		
		#### CONNECT
		self.con = None
		self.Envs = self.combo_value.get()
		self.con, self.MODE_SQLI = ConnectInvent(self.Envs)
		
		#### LIST ALBUMS
		self.cadreresult = tk.Frame(self)
		self.cadreresult.pack(fill=tk.BOTH)
		# tree : compatibilité sqllite
		self.tree = BuildTree(self.con, self.cadreresult, (Z_REQUEST if self.MODE_SQLI else A_REQUEST), A_C_WIDTH, 22, True)
		# popup menu album
		self.aMenu = tk.Menu(self.cadreresult, tearoff=0)
		self.aMenu.add_command(label="View ArtWorks...", command=self.ViewArtWorks)
		self.aMenu.add_command(label="Open Folder...", command=self.GetFolder)
		self.aMenu.add_command(label="Export Select Album(s) to...", command=self.ExportAlbums)
		self.aMenu.add_command(label="Update Album...", command=self.UpdateAlbum)
		self.aMenu.add_command(label="Open TagScan...", command=self.OpenTagScan)
		self.tree.bind("<<TreeviewSelect>>", self.SelectTree)
		self.tree.bind("<Button-3>", self.popupalbum)
		self.tree.pack(side=tk.TOP, anchor=tk.W, fill=tk.BOTH, padx=5, pady=5)
		
		#### INFOS ALBUM 
		# COVER
		self.cadrealbum = tk.Frame(self)
		self.cadrealbum.pack(fill=tk.BOTH)
		self.labcover = tk.Label(self.cadrealbum)
		self.labcover.pack(side=LEFT, padx=5, pady=5)
		self.labcover.bind("<Button-1>", self.OnPressCover)
		# BLANK COVERS
		monimage = BuildCover(' ', TEXT_NCO, ' ')
		monimage = monimage.resize((400, 400), Image.ANTIALIAS)
		photo = ImageTk.PhotoImage(monimage)
		self.labcover.configure(image = photo)
		self.labcover.image = photo
		# ALBUM NAME
		self.customFont = Font(family="Calibri", size=12)
		self.cadrelabelalb = tk.Frame(self.cadrealbum)
		self.cadrelabelalb.pack(fill=tk.BOTH, side=tk.TOP)
		self.stralbumname = tk.StringVar()
		self.labelalb = Label( self.cadrelabelalb, textvariable=self.stralbumname, justify = tk.LEFT, font=self.customFont)
		self.labelalb.pack(side=tk.LEFT, padx=0, pady=5)
		# SCORE ALBUM
		self.posalbum_scale = tk.Scale( self.cadrelabelalb,
										command=self.ModifyScoreAlbum, 
										showvalue=0, 
										from_=0, 
										to=len(SCOR_ALBUMS)-1, 
										length=100,
										orient='horizontal')
		self.posalbum_scale.pack(side=tk.RIGHT, padx=15, pady=5)
		self.ScoAlbumlb = tk.StringVar()
		self.scorealbum_label = Label(self.cadrelabelalb, textvariable=self.ScoAlbumlb, font=self.customFont)
		self.btn_enrscralb = tk.Button(self.cadrelabelalb, text='Save', command = self.OnPressButtonEnrScoreAlbum)
		self.scorealbum_label.pack(side=tk.RIGHT, padx=5, pady=5)
		# TRACKS
		self.treealb = BuildTree(self.con, self.cadrealbum, T_REQUEST.format(id=0), T_C_WIDTH, 15, True)
		# popup menu track
		self.tMenu = tk.Menu(self.cadrealbum, tearoff=0)
		self.treealb.bind("<Double-1>", self.OnDoubleClickTrack)
		self.treealb.bind("<<TreeviewSelect>>", self.SelectTreeAlb)
		self.treealb.pack(side=tk.BOTTOM, anchor=tk.W, fill=tk.BOTH, padx=5, pady=5)
		# SCORE TRACK
		self.cadrescoretrack = tk.Frame(self)
		self.cadrescoretrack.pack(fill=tk.BOTH, side=tk.TOP)
		self.MessageInfo = tk.StringVar()
		self.MessageInfo_label = Label(self.cadrescoretrack, textvariable=self.MessageInfo, font=self.customFont)
		self.MessageInfo_label.pack(side=tk.LEFT, padx=5, pady=5)
		self.postrack_scale = tk.Scale( self.cadrescoretrack,
										command=self.ModifyScoreTrack, 
										showvalue=0, 
										from_=0, 
										to=len(SCOR_TRACKS)-1, 
										length=100,
										orient='horizontal')
		self.postrack_scale.pack(side=tk.RIGHT, padx=15, pady=5)
		self.ScoTracklb = tk.StringVar()
		self.scoretrack_label = Label(self.cadrescoretrack, textvariable=self.ScoTracklb, font=self.customFont)
		self.scoretrack_label.pack(side=tk.RIGHT, padx=5, pady=5)
		self.btn_enrscrtrk = tk.Button(self.cadrescoretrack, text='Save', command = self.OnPressButtonEnrScoreTrack)
		
		#### BUTTONS
		cadrebottom = tk.Frame(self)
		cadrebottom.pack(fill=tk.BOTH)
		#self.btn_extras = tk.Button(cadrebottom, text='R&D...', width=15, command = self.Extras, state=tk.DISABLED)
		#self.btn_extras.pack(side=tk.LEFT, padx=5, pady=5)
		btn_quitpr = tk.Button(cadrebottom, text="Quit", width=15, command = self.QuitMain).pack(side=tk.RIGHT, padx=20, pady=5)
		
		#### LOADING ENVT
		self.CurentAlbum = None
		self.CurentTrack = None
		self.curalbmd5 = None
		self.Envs = None
		self.ConnectEnvt()
	
	def OnComboChange(self, event):
		self.ConnectEnvt()
	
	def OnPressEnter(self, event):
		self.GetSearchAlbums()
	
	def OnPressCover(self, event):
		"""Affiche la pochette de l'album."""
		self.coverWin = tk.Toplevel(self.master)
		monimage = BuildCover(self.con, self.pathcover, self.curalbmd5)
		CoverViewGui(self.coverWin, monimage, self.albumname)
	
	def SelectTree(self, event):
		if self.tree.get_children():
			self.tree.focus()
			self.CurentAlbum = self.tree.focus()
			self.GetInfosAlbum(self.CurentAlbum)
	
	def SelectTreeAlb(self, event):
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
		UpdateBaseScore(self.con, self.ScoreTrack, self.Id_TRACK, V_REQUEST)
		# Treeview
		self.treealb.set(self.CurentTrack, column=T_POSITIO['Score'], value=self.ScoreTrack)
		# Button
		self.btn_enrscrtrk.pack_forget()
	
	def ModifyScoreAlbum(self, event):
		self.ScoAlbumlb.set(DisplayStars(self.posalbum_scale.get(), SCOR_ALBUMS))
		if self.ScoreAlbum != self.posalbum_scale.get():
			self.btn_enrscralb.pack(side=tk.RIGHT, padx=5, pady=5)
		else:
			self.btn_enrscralb.pack_forget()
	
	def ModifyScoreTrack(self, event):
		self.ScoTracklb.set(DisplayStars(self.postrack_scale.get(), SCOR_TRACKS))
		if self.ScoreTrack != self.postrack_scale.get():
			self.btn_enrscrtrk.pack(side=tk.RIGHT, padx=5, pady=5)
		else:
			self.btn_enrscrtrk.pack_forget()
	
	def popupalbum(self, event):
		# maj selection : only for one selection
		ListeSelect = self.tree.selection()
		if len(ListeSelect) == 1 :
			self.CurentAlbum = self.tree.identify('item',event.x,event.y)
			self.tree.selection_set(self.CurentAlbum)
			self.tree.focus(self.CurentAlbum)
			self.GetInfosAlbum(self.CurentAlbum, True)
		if self.tree.get_children():
			curLign = self.tree.item(self.CurentAlbum)
			if curLign['values'][A_POSITIO['Qty_covers']] == 0 or not(path.exists(self.AlbumPath)):
				self.aMenu.entryconfig(0, state="disabled")
			else:
				self.aMenu.entryconfig(0, state="normal")
			self.aMenu.entryconfig(3, label="Update (powershell) Album : "+ self.albumname[:15] + "...")
			self.aMenu.post(event.x_root, event.y_root)
	
	def popupbase(self, event):
		self.bMenu.post(event.x_root, event.y_root)
	
	def QuitMain(self):
		# connection close
		self.con.close()
		self.destroy()
	
	def ConnectEnvt(self, refresh = False):
		if self.Envs != self.combo_value.get() or refresh:
			# Mysql
			self.Envs = self.combo_value.get()
			if self.con: self.con.close()
			self.condat = datetime.now().strftime('%H:%M:%S')
			self.con, self.MODE_SQLI = ConnectInvent(self.Envs)
			# debut loading
			self.loadingWin = tk.Toplevel(self)
			LoadingGui(self.loadingWin, self.con, self.MODE_SQLI, 0)
			# auto-completion
			completion_list = CreateListCompletion(self.con)
			self.ligne_texte.set_completion_list(completion_list)
			# tittle
			if self.MODE_SQLI:
				self.title(TITL_PROG + ' : offline mode SQLite local at '+self.condat)
			else:
				self.title('{prog} : connected {database} at {heure}'.format(prog = TITL_PROG,
																			 database = self.Envs,
																			 heure = self.condat))
			# montage table mysql en memoire
			self.Tabs = SelectTOTab(self.con, (Z_REQUEST if self.MODE_SQLI else A_REQUEST))
			# init combos
			self.style['values'] = SelectTOTab(self.con, D_REQUEST)
			self.style.bind("<<ComboboxSelected>>", self.OnPressEnter)
			self.style.current(0)
			self.family['values'] = SelectTOTab(self.con, E_REQUEST)
			self.family.bind("<<ComboboxSelected>>", self.OnPressEnter)
			self.family.current(0)
			# first line by defaut
			if not(refresh):
				self.CurentAlbum = 'Row_0'
			# all albums to treeview
			self.GetSearchAlbums(refresh)
			#self.tree.selection_set(self.CurentAlbum)
			# Hide loading
			self.loadingWin.withdraw()
	
	def GetSearchAlbums(self, refresh = False):
		"""Search Albums."""
		self.config(cursor="wait")
		txt_search = self.var_texte.get()
		# SEARCH IN TRACKS
		if self.searchtracks.get() == 1:
			lst_id = SelectTOTab(self.con, B_REQUEST.format(search=txt_search))
		else:
			lst_id = []
		# TREEVIEW
		# del
		if self.tree.get_children():
			for i in self.tree.get_children():
				self.tree.delete(i)
		# insert
		counter = cpt_trk = cpt_cds = cpt_siz = cpt_len = 0
		for row in self.Tabs:
			# on cherche la chaine saisie ou search tracks
			if txt_search.lower() in row[A_POSITIO['Name']].lower() or txt_search.lower() in row[A_POSITIO['Label']].lower() or self.SearchInTracksSQL(lst_id,row[A_POSITIO['ID_CD']]):
				# Category ok ?
				if (self.style_value.get() != '*' and row[A_POSITIO['Category']] == self.style_value.get()) or (self.style_value.get() == '*') :
					# Family ok ?
					if (self.family_value.get() != '*' and row[A_POSITIO['Family']] == self.family_value.get()) or (self.family_value.get() == '*') :
						self.tree.insert("", counter, iid='Row_%s'%counter, values=row, tag = (counter%2))
						counter += 1
						cpt_cds += row[A_POSITIO['Qty_CD']]
						cpt_trk += row[A_POSITIO['Qty_Tracks']]
						cpt_siz += row[A_POSITIO['Size']]
						cpt_len += sum(int(x) * 60 ** i for i,x in enumerate(reversed(row[A_POSITIO['Length']].split(":"))))
		
		# DISPLAY STATS SEARCH
		if counter > 0:
			# info size
			if int((cpt_siz/1024/1024)*10)/10 < 1:
				# Mo -> Go
				txt_siz = str(int((cpt_siz/1024)*10)/10) +' Go'
			else:
				# Mo -> To
				txt_siz = str(int((cpt_siz/1024/1024)*10)/10) +' To'
			# info time
			if int(((cpt_len/60/60)/24)*10)/10 < 1:
				# seoncd -> Hours
				txt_dur = str(int(((cpt_len/60/60))*10)/10) + ' Hours'
			else:
				# seoncd -> Days
				txt_dur = str(int(((cpt_len/60/60)/24)*10)/10) + ' Days'
			self.MessageInfo.set("Search Result \"{sch}\" ->  {alb} / {trk} / {cds} / {siz} / {dur} <-".format(sch = (txt_search if len(txt_search)>0 else 'all'),
																						alb = DisplayCounters(counter, 'Album'),
																						cds =  DisplayCounters(cpt_cds, 'CD'),
																						trk = DisplayCounters(cpt_trk, 'Track'),
																						siz = txt_siz,
																						dur = txt_dur))
		else:
			self.MessageInfo.set("Search Result ({sch}) = nothing".format(sch = self.style_value.get()))
		if self.tree.get_children():
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
				self.Id_CD = curLign['values'][A_POSITIO['ID_CD']]
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
				tracks = SelectTOTab(self.con, req)
				for track in tracks:
					# SEARCH IN TRACKS
					if self.searchtracks.get() == 1 and (self.var_texte.get().lower() in track[A_POSITIO['Category']].lower() or self.var_texte.get().lower() in track[A_POSITIO['Family']].lower()):
						tag = '2'
					else:
						tag = str(counter%2)
					self.treealb.insert("", counter, iid='Row_%s'%counter, values = track, tag = tag)
					counter += 1
					cpt_len += sum(int(x) * 60 ** i for i,x in enumerate(reversed(track[3].split(":"))))
				# MAJ SCORE TRACK
				if counter > 0:
					# first line by defaut
					self.CurentTrack = 'Row_0'
					#self.treealb.selection_set(self.CurentTrack)
				else:
					self.CurentTrack = None
				# MAJ ALBUM NAME
				txt_album = self.albumname[:100] + "\n{tracks} / {dur} / {cd}".format(tracks = DisplayCounters(counter, 'track'),
																					 dur = str(int(((cpt_len/60))*10)/10) + ' mins',
																					 cd = DisplayCounters(curLign['values'][A_POSITIO['Qty_CD']], 'CD'))
				self.stralbumname.set(txt_album)
				# MAJ COVERS
				monimage = BuildCover(self.con, self.pathcover, self.curalbmd5)
				monimage = monimage.resize((400, 400), Image.ANTIALIAS)
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
			monimage = monimage.resize((400, 400), Image.ANTIALIAS)
			photo = ImageTk.PhotoImage(monimage)
			self.labcover.configure(image = photo)
			self.labcover.image = photo
		# MAJ TRACK INFO
		self.GetInfosTrack(self.CurentTrack)
	
	def GetInfosTrack(self, curItem):
		if self.treealb.get_children():
			curLign = self.treealb.item(curItem)
			self.ScoreTrack = curLign['values'][T_POSITIO['Score']]
			self.Id_TRACK = curLign['values'][T_POSITIO['ID_TRACK']]
			self.CurentTrack = curItem
			# MAJ SCORE
			self.postrack_scale.set(self.ScoreTrack)
			self.ScoTracklb.set(DisplayStars(self.ScoreTrack, SCOR_TRACKS))
			self.postrack_scale.config(state='normal')
		else:
			self.ScoreTrack = 0
			self.Id_TRACK = None
			self.CurentTrack = None
			self.postrack_scale.set(self.ScoreTrack)
			self.ScoTracklb.set(DisplayStars(self.ScoreTrack, SCOR_TRACKS))
			self.postrack_scale.config(state='disabled')
		
	def GetFolder(self):
		"""Ouvre dossier album dans l'explorateur."""
		self.curLign = self.tree.item(self.CurentAlbum)
		openFolder(self.curLign['values'][A_POSITIO['Path']])
	
	def OpenTagScan(self):
		"""Ouvre TAGSCAN."""
		self.curLign = self.treealb.item(self.CurentTrack)
		OpenComand(TAGS_SCAN, self.AlbumPath)
	
	def playmedia(self):
		"""Player Audio thread pyQT5."""
		self.curLign = self.treealb.item(self.CurentTrack)
		# first exec
		if self.tplay == None:
			self.tplay = Thread(target = PlayerProcess, args = (self.curLign['values'][T_POSITIO['REP_Track']], 
																self.curLign['values'][T_POSITIO['FIL_Track']],
																self.winfo_x()+5, 
																self.winfo_y()+self.winfo_height()-45))
			self.tplay.daemon = True
			self.tplay.start()
		else:
			# only one player run
			if not self.tplay.isAlive():
				self.tplay = Thread(target = PlayerProcess, args = (self.curLign['values'][T_POSITIO['REP_Track']], 
																	self.curLign['values'][T_POSITIO['FIL_Track']],
																	self.winfo_x()+5, 
																	self.winfo_y()+self.winfo_height()-45))
				self.tplay.daemon = True
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
	
	def showloadingWin(self):
		"""Display stats base"""
		self.loadingWin.update()
		self.loadingWin.deiconify()
	
	def RefreshBase(self):
		"""Recharge environnement."""
		self.ConnectEnvt(True)
	
	def CreateLocalBase(self):
		"""Create base Sqlite."""
		filename = BASE_SQLI.format(envt=self.Envs)
		if path.isfile(filename):
			remove(filename)
		logname = datetime.now().strftime("%Y%m%d%H%M%S") + "_CopyDatabaseToSqlite_" + self.Envs + ".log"
		self.config(cursor="wait")
		CopyDatabaseInvent(self.con, filename, path.join(LOGS_PROG, logname))
		self.config(cursor="")
	
	def UpdateAlbum(self):
		"""Execute powershell Script update albums infos."""
		self.GUIUpdateAlbum = tk.Toplevel(self.master)
		#p = ExcecutePowershell(PWSH_SCRU, '-Album_IDCD', str(self.Id_CD), '-Envt', self.Envs, '-Logs', LOGS_PROG)
		eCommand = BuildCommandPowershell(PWSH_SCRU, '-Album_IDCD', str(self.Id_CD), '-Envt', self.Envs, '-Logs', LOGS_PROG)
		DisplaySubprocessGui(self.GUIUpdateAlbum, eCommand, 'Execution PowerShell : '+path.basename(PWSH_SCRU)+' -Album_IDCD '+str(self.Id_CD)+' -Envt "'+self.Envs+'"')
		self.ConnectEnvt(True)
	
	def BuildInvent(self):
		"""Execute powershell Script update all albums infos."""
		self.GUIBuildInvent = tk.Toplevel(self.master)
		if 'LOSSLESS' in self.Envs:
			filescript = PWSH_SCRI.format(mod='LOSSLESS')
		else:
			filescript = PWSH_SCRI.format(mod='MP3')
		#p = ExcecutePowershell(filescript, '-Envt', self.Envs)
		eCommand = BuildCommandPowershell(filescript, '-Envt', self.Envs)
		DisplaySubprocessGui(self.GUIBuildInvent, eCommand, 'Execution PowerShell : '+path.basename(filescript)+' -Envt "'+self.Envs+'"')
		self.ConnectEnvt(True)
	
	def ViewArtWorks(self):
		"""views covers storage."""
		self.coverWin = tk.Toplevel(self.master)
		CoversViewGui(self.coverWin, self.AlbumPath, self.albumname)
	
	def Extras(self):
		request = A_REQUEST
		Dict = SelectTODict(self.con, request)
		print (Dict)
		for x in Dict:
			x["Base"]="Invent"
			print (x["ID"], x["Category"], x["Name"], x["Base"])


###################################################################
# START
if __name__ == "__main__":
	#path.dirname(os.path.realpath(sys.argv[0]))
	#chdir(os.path.dirname(sys.argv[0]))
	path.realpath(path.dirname(sys.argv[0]))
	app = CoverMainGui(None)
	app.mainloop()
	