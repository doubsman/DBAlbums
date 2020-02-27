#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os import path, stat
from datetime import datetime
from time import ctime
from PyQt5.QtCore import QThread, pyqtSignal
# general Libs
from LIBFilesProc import FilesProcessing


class ThreadAnalyseInvent(QThread, FilesProcessing):
	# signals
	signalchgt = pyqtSignal(int, str)		# signal browse
	signaltext = pyqtSignal(str, int)

	# global
	families =  {	"Physique"			: "Colonne", 
					"Label/Physique"	: "Labels", 
					"Download"			: "Download", 
					"Artists"			: "Artists"}
	mask_amedias = ('.flac','.ape','.wma','.mp3','.wv','.aac','.mpc')

	def __init__(self, list_albums, list_columns, list_category, typeupdate, envt):
		super(ThreadAnalyseInvent, self).__init__()
		self.boolstop = False				# stop analyse
		self.boolexec = False				# analyse in progress
		self.list_albums = list_albums
		self.list_catego = list_category
		self.list_columns = list_columns
		self.totalalbums = len(self.list_albums)
		self.typeupdate = typeupdate
		self.envt = envt
		self.list_invent = []
		self.list_finaly = []
		self.list_action = []
		self.apresent = 0
		self.alupdate = 0
		self.albumnew = 0
		self.aldelete = 0

	def __del__(self):
		self.wait()

	def stopAnalyse(self):
		self.boolstop = True
		while self.boolexec:
			wait = 1

	def run(self):
		"""Browse Folders for update database."""
		self.boolexec = True
		self.numbers = 0
		self.signalchgt.emit(self.numbers, '{0:<35}'.format('1/2 Browsing folders'))
		# PRESENT / UPDATE / ADD
		for rowcategory in self.list_catego:
			if self.boolstop:
				break
			category = rowcategory[0]
			typsubfo = rowcategory[1]
			cracines = rowcategory[2]
			position = rowcategory[3]
			self.signaltext.emit('ANALYSE FOLDERS: ' + '.'.join(item for item in rowcategory if item), 1)
			# LOSSLESS invent
			if 'LOSSLESS' in self.envt:
				listsubfolders = self.folder_list_folders(cracines)
				for fposition in listsubfolders:
					# define family
					boolfami, family = self.convertPositionFamily(fposition)
					folder = path.join(cracines, fposition)
					if boolfami:
						# no sub folders for folder LOSSLESS Download if no TRANCE
						if family == 'Download' and category != 'TRANCE':
							self.analyseSubFolders(category, family, folder, 'S')
						else:
							self.analyseSubFolders(category, family, folder, typsubfo)
			else:
				# MP3 invent
				# define family
				boolfami, family = self.convertPositionFamily(position)
				if boolfami:
					self.analyseSubFolders(category, family, cracines, typsubfo)
		# DELETE
		self.numbers = 0
		self.signalchgt.emit(self.numbers, '{0:<35}'.format('2/2 Browsing database'))
		for albums in self.list_albums:
			if albums[self.list_columns.index('ID_CD')] not in self.list_invent:
				self.numbers += 1
				self.emitLoadindInvent(self.numbers, '2/2 Browsing database ' +albums[self.list_columns.index('CATEGORY')])
				self.aldelete += 1
				self.list_finaly.append([albums[self.list_columns.index('CATEGORY')],
												self.numbers,
												'DELETE',
												albums[self.list_columns.index('ID_CD')],
												albums[self.list_columns.index('NAME')]])
				self.list_action.append([albums[self.list_columns.index('CATEGORY')],
												family,
												'DELETE',
												albums[self.list_columns.index('ID_CD')],
												albums[self.list_columns.index('NAME')],
												albums[self.list_columns.index('PATHNAME')]])
		self.signalchgt.emit(100, '{0:<35}'.format('2/2 Browsing database'))
		self.boolexec = False

	def analyseSubFolders(self, category, family, folder, typefolder):
		"""Browse sub folders or sub/sub folders"""
		if typefolder == 'S':
			listsubfolders = self.folder_list_folders(folder)
			for subfolder in listsubfolders:
				if self.boolstop:
					break
				subfolder = path.join(folder, subfolder)
				self.numbers += 1
				self.emitLoadindInvent(self.numbers, '1/2 Browsing folders ' + category)
				self.testUpdateAlbum(category, family, subfolder)
		elif typefolder == 'D':
			# sub folders
			listsubfolders = self.folder_list_folders(folder)
			for subfolder in listsubfolders:
				if self.boolstop:
					break
				subfolder = path.join(folder, subfolder)
				self.signaltext.emit('ANALYSE SUBFOLDERS: ' + subfolder, 1)
				listsubsubfolders = self.folder_list_folders(subfolder)
				for subsubfolder in listsubsubfolders:
					subsubfolder = path.join(subfolder, subsubfolder)
					self.numbers += 1
					self.emitLoadindInvent(self.numbers, '1/2 Browsing folders ' + category)
					self.testUpdateAlbum(category, family, subsubfolder)		
		
	def convertPositionFamily(self, position):
		"""Convert position to family via dict."""
		family = ''
		boolfami = False
		for fam, pos in self.families.items():
			if pos in position or position in pos:
				family = fam
				boolfami = True
				break
		return boolfami, family
	
	def emitLoadindInvent(self, number,  message = ''):
		"""Browsing folders in progress."""
		if self.totalalbums > 0:
			if number % int(self.totalalbums/(min(100, self.totalalbums))) == 0:
				self.signalchgt.emit(int((number/self.totalalbums)*100), '{0:<35}'.format(message))

	def testUpdateAlbum(self, category, family, folder):
		"""Test album for init statut NEW, UPDATE, PRESENT, DELETE."""
		nb_amedias = len(self.folder_list_files(folder, True, self.mask_amedias))
		if nb_amedias > 0:
			# exist in database ?
			testalbum = self.albumExist(folder)
			if testalbum:
				self.list_invent.append(testalbum[self.list_columns.index('ID_CD')])
				if self.typeupdate == 'UPDATE':
					# Compare size
					sizefolder = int(round(self.folder_size(folder)/1024/1024, 0))
					# Compare date
					modifydate = ctime(max(stat(root).st_mtime for root in self.folder_list_files(folder)))
					modifydate = datetime.strptime(modifydate, "%a %b %d %H:%M:%S %Y")
					#datefolder = ctime(path.getmtime(folder))
					#datefolder = datetime.strptime(datefolder, "%a %b %d %H:%M:%S %Y")
					creationdate = ctime(max(stat(root).st_ctime for root in self.folder_list_files(folder)))
					creationdate = datetime.strptime(creationdate, "%a %b %d %H:%M:%S %Y")
					recentdate = max(modifydate, creationdate)
					if isinstance(testalbum[self.list_columns.index('MODIFIED')], str):
						if 'T' in testalbum[self.list_columns.index('MODIFIED')]:
							date_format = "%Y-%m-%dT%H:%M:%S.%f"
						else:
							date_format = "%Y-%m-%d %H:%M:%S"
						datebase = datetime.strptime(testalbum[self.list_columns.index('MODIFIED')], date_format)
					else:
						datebase = testalbum[self.list_columns.index('MODIFIED')].toPyDateTime()
					if sizefolder < testalbum[self.list_columns.index('SIZE')] or recentdate > datebase or  testalbum[self.list_columns.index('PATHNAME')] != folder:
						# UPDATE
						self.alupdate += 1
						self.list_finaly.append([category, self.numbers, 'UPDATE', testalbum[self.list_columns.index('ID_CD')], path.basename(folder)])
						self.list_action.append([category, family, 'UPDATE', testalbum[self.list_columns.index('ID_CD')], path.basename(folder), folder])
					else:
						# PRESENT
						self.apresent += 1
						self.list_finaly.append([category, self.numbers, 'PRESENT', testalbum[self.list_columns.index('ID_CD')], path.basename(folder)])
				elif self.typeupdate == 'NEW':
					# PRESENT
					self.apresent += 1
					self.list_finaly.append([category, self.numbers, 'PRESENT', testalbum[self.list_columns.index('ID_CD')], path.basename(folder)])
			else:
				# ADD
				self.albumnew += 1
				self.list_finaly.append([category, self.numbers, 'ADD', '?', path.basename(folder)])
				self.list_action.append([category, family, 'ADD', '?', path.basename(folder), folder])

	def albumExist(self, folder):
		"""Find Album by ID_CD."""
		albumfind = None
		for albums in self.list_albums:
			if albums[self.list_columns.index('PATHNAME')] == folder:
				# exist
				albumfind = albums
				break
			elif path.basename(folder) == path.basename(albums[self.list_columns.index('PATHNAME')]):
				if not path.exists(albums[self.list_columns.index('PATHNAME')]):
					# album move
					albumfind = albums
					break
				else:
					# add doublon
					self.signaltext.emit('WARNING: Doublons Albums :' + folder, 3)
		# no exist
		return albumfind



