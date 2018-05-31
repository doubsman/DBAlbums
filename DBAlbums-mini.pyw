#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GetExist Version 0.9
from sys import platform, stdout, argv, executable
from os import system, path, getcwd, name as osname, remove, walk, chdir
from configparser import ConfigParser
from pymysql import connect as connectmysql		#mysql
from tkinter import (Tk, Toplevel, Label, Button, Checkbutton, Entry, Canvas, Grid, 
					Frame, Scale, Menu, Text, StringVar, IntVar, FALSE, TRUE, 
					RIDGE, SUNKEN, SOLID, FLAT, N, S, W, E, X, Y, RIGHT, LEFT, 
					BOTH, TOP, END, BOTTOM, VERTICAL, HORIZONTAL, INSERT, ALL)
from tkinter.filedialog import asksaveasfile
from tkinter.ttk import Treeview, Combobox, Scrollbar, Separator, Style
from DBAlbums import (centerWindows, connectDatabase, getRequest, AutocompleteEntry,
					  buildTree, buildIco, buildTabFromRequest, buildListFromRequest)

###################################################################
# CONSTANTS
# path
if getattr(system, 'frozen', False):
	# frozen
	PATH_PROG = path.dirname(executable)
else:
	# unfrozen
	PATH_PROG = path.realpath(path.dirname(argv[0]))
chdir(PATH_PROG) # working directory

# Read File DBAlbums.ini
FILE__INI = 'DBAlbums.ini'
readIni = ConfigParser()
readIni.read(FILE__INI)
# GUI
VERS_PROG   = readIni.get('dbalbums', 'prog_build')
TITL_PROG   = "♫ DBAlbums v{v} (2017)".format(v=VERS_PROG+"mini")
WINS_ICO    = readIni.get('dbalbums', 'wins_icone')

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


# MAIN MINI GUI
class DBAlbumsMainMiniGui(Tk):
	"""Fenetre principale."""
	def __init__(self , parent):
		Tk.__init__(self , parent)
		self.parent = parent
		self.tk.call('encoding', 'system', 'utf-8')
		self.title(TITL_PROG)
		# dimensions
		self.resizable(width=True, height=False)
		self.geometry("{w}x{h}".format(w=640, h=300))
		self.minsize(width=640, height=300)
		centerWindows(self)
		buildIco(self)
		# style
		s=Style()
		s.theme_use('clam')
		# saisie
		cadre = Frame(self)
		cadre.pack(fill=BOTH)
		# Label
		labelDir=Label(cadre, text="Search ")
		labelDir.pack(side="left", padx=5, pady=5)
		# ligne de saisie
		self.var_searchtext_value = StringVar(None)
		ligne_texte = AutocompleteEntry(cadre, textvariable=self.var_searchtext_value, width=30)
		ligne_texte.bind("<Return>", self.SearchMySQL)
		ligne_texte.focus()
		ligne_texte.pack(side=LEFT, padx=5, pady=5)
		# Boutons
		btn_sear = Button(cadre, text='➜', width=2,command= self.SearchMySQL)
		btn_sear.pack(side=LEFT, padx=5, pady=5)
		# resultat
		cadreresult = Frame(self)
		cadreresult.pack(fill=BOTH)
		# Treeview 
		self.tree = buildTree(cadreresult,  A_COLNAME, A_C_WIDTH, 10, True)
		self.tree.pack(side=TOP, anchor=W, fill=BOTH, expand=True)
		# label resultat
		cadreresult = Frame(self)
		cadreresult.pack(fill=BOTH)
		self.Resultat = StringVar()
		labelRes=Label(cadreresult, textvariable=self.Resultat)
		labelRes.pack(side="left", padx=5, pady=5)
		# auto-completion
		self.con, self.MODE_SQLI, self.homeMedias = connectDatabase('LOSSLESS')
		completion_list = buildListFromRequest(self.con, getRequest('autocompletion', self.MODE_SQLI))
		ligne_texte.set_completion_list(completion_list)
		# fill list
		self.Tabs = buildTabFromRequest(self.con, getRequest('albumslist', self.MODE_SQLI))
		self.con.close()
		# go
		self.SearchMySQL()
	
	def SearchMySQL(self, event=None):
		for i in self.tree.get_children():
			self.tree.delete(i)
		counter = 0
		txt_search = self.var_searchtext_value.get()
		for row in self.Tabs:
			if  txt_search.lower() in row[A_POSITIO.index('Name')].lower() or txt_search.lower() in row[A_POSITIO.index('Label')].lower():
				self.tree.insert("", counter, iid=row[A_POSITIO.index('ID_CD')], values=row, tag = (counter%2))
				counter += 1
		self.Resultat.set('Résultat -> ' + str(counter) + ' Album(s) trouvé(s)    ')


###################################################################
# START
if __name__ == "__main__":
	app = DBAlbumsMainMiniGui(None)
	app.mainloop()