#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os import path, stat
from hashlib import md5
from datetime import datetime
from time import ctime
from PyQt5.QtCore import QObject, pyqtSignal, QSettings
from DBFunction import getListFolders, getListFiles, getFolderSize
from DBDatabase import buildlistcategory


class BuildInvent(QObject):
	# signal
	signalthunchgt = pyqtSignal(int, str)		# signal browse
	# global
	families =  {"Physique":"Colonne", "Label/Physique":"Labels", "Download":"Download" }
	mask_amedias = ('.flac','.ape','.wma','.mp3','.wv','.aac','.mpc')
	A_POSITIO = (	'Category', 'Family', 'Name', 'Label', 'ISRC',
					'Qty_Tracks', 'Qty_CD', 'Year', 'Length', 'Size',
					'Score', 'Qty_covers', 'Date_Insert', 'Date_Modifs', 'Position',
					'Typ_Tag', 'Path', 'Cover', 'MD5', 'ID_CD')
					
	def __init__(self, list_albums, list_category, typeupdate, modsql, envt):
		"""Init invent, build list albums exists in database."""
		super(BuildInvent, self).__init__()
		self.list_albums = list_albums
		self.list_catego = list_category
		self.totalalbums = len(self.list_albums)
		self.typeupdate = typeupdate
		self.modsql = modsql
		self.envt = envt
		self.list_invent = []
		self.list_finaly = []
		self.list_action = []
		self.apresent = 0
		self.alupdate = 0
		self.albumnew = 0
		self.aldelete = 0

	def inventDatabase(self):
		"""Browse Folders for update database."""
		self.numbers = 0
		self.signalthunchgt.emit(self.numbers, '{0:<35}'.format('1/2 Browsing folders'))
		# PRESENT / UPDATE / ADD
		for rowcategory in self.list_catego:
			category = rowcategory[0]
			typsubfo = rowcategory[1]
			cracines = rowcategory[2]
			position = rowcategory[3]
			print(rowcategory)
			# LOSSLESS invent
			if 'LOSSLESS' in self.envt:
				listsubfolders = list(getListFolders(cracines))
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
		self.signalthunchgt.emit(self.numbers, '{0:<35}'.format('2/2 Browsing database'))
		for albums in self.list_albums:
			if albums[self.A_POSITIO.index('ID_CD')] not in self.list_invent:
				self.numbers += 1
				self.emitLoadindInvent(self.numbers, '2/2 Browsing database ' +albums[self.A_POSITIO.index('Category')])
				self.aldelete += 1
				self.list_finaly.append([albums[self.A_POSITIO.index('Category')],
												self.numbers,
												'DELETE',
												albums[self.A_POSITIO.index('ID_CD')],
												albums[self.A_POSITIO.index('Name')]])
				self.list_action.append([albums[self.A_POSITIO.index('Category')],
												family,
												'DELETE',
												albums[self.A_POSITIO.index('ID_CD')],
												albums[self.A_POSITIO.index('Name')],
												albums[self.A_POSITIO.index('Path')]])
		self.signalthunchgt.emit(100, '{0:<35}'.format('2/2 Browsing database'))

	def analyseSubFolders(self, category, family, folder, typefolder):
		"""Browse sub folders or sub/sub folders"""
		if typefolder == 'S':
			listsubfolders = list(getListFolders(folder))
			for subfolder in listsubfolders:
				subfolder = path.join(folder, subfolder)
				self.numbers += 1
				self.emitLoadindInvent(self.numbers, '1/2 Browsing folders ' + category)
				self.testUpdateAlbum(category, family, subfolder)
		elif typefolder == 'D':
			# sub folders
			listsubfolders = list(getListFolders(folder))
			for subfolder in listsubfolders:
				subfolder = path.join(folder, subfolder)
				listsubsubfolders = list(getListFolders(subfolder))
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
		if number % int(self.totalalbums/(min(100, self.totalalbums))) == 0:
			self.signalthunchgt.emit(int((number/self.totalalbums)*100), '{0:<35}'.format(message))

	def testUpdateAlbum(self, category, family, folder):
		"""Test album for init statut NEW, UPDATE, PRESENT, DELETE."""
		nb_amedias = len(list(getListFiles(folder, self.mask_amedias)))
		if nb_amedias > 0:
			# exist in database ?
			testalbum = self.albumExist(folder)
			if testalbum:
				self.list_invent.append(testalbum[19])
				if self.typeupdate == 'UPDATE':
					# Compare size
					sizefolder = int(round(getFolderSize(folder)/1024/1024, 0))
					# Compare date
					modifydate = ctime(max(stat(root).st_mtime for root in list(getListFiles(folder))))
					modifydate = datetime.strptime(modifydate, "%a %b %d %H:%M:%S %Y")
					#datefolder = ctime(path.getmtime(folder))
					#datefolder = datetime.strptime(datefolder, "%a %b %d %H:%M:%S %Y")
					creationdate = ctime(max(stat(root).st_ctime for root in list(getListFiles(folder))))
					creationdate = datetime.strptime(creationdate, "%a %b %d %H:%M:%S %Y")
					recentdate = max(modifydate, creationdate)
					if sizefolder < testalbum[self.A_POSITIO.index('Size')] or recentdate > testalbum[self.A_POSITIO.index('Date_Modifs')].toPyDateTime():
						# UPDATE
						self.alupdate += 1
						self.list_finaly.append([category, self.numbers, 'UPDATE', testalbum[self.A_POSITIO.index('ID_CD')], path.basename(folder)])
						self.list_action.append([category, family, 'UPDATE', testalbum[self.A_POSITIO.index('ID_CD')], path.basename(folder), folder])
					else:
						# PRESENT
						self.apresent += 1
						self.list_finaly.append([category, self.numbers, 'PRESENT', testalbum[self.A_POSITIO.index('ID_CD')], path.basename(folder)])
				elif self.typeupdate == 'NEW':
					# PRESENT
					self.apresent += 1
					self.list_finaly.append([category, self.numbers, 'PRESENT', testalbum[self.A_POSITIO.index('ID_CD')], path.basename(folder)])
			else:
				# ADD
				self.albumnew += 1
				self.list_finaly.append([category, self.numbers, 'ADD', '?', path.basename(folder)])
				self.list_action.append([category, family, 'ADD', '?', path.basename(folder), folder])

	def albumExist(self, folder):
		"""Find Album by MD5."""
		albumMD5 = self.getAlbumMD5(folder)
		for albums in self.list_albums:
			if albums[self.A_POSITIO.index('MD5')] == albumMD5:
				return(albums)
		return None

	def getAlbumMD5(self, folder):
		"""Encode Album Name."""
		return md5(path.basename(folder).encode('utf-8')).hexdigest().upper()

	def getListIds(self):
		"""Action for update database."""
		list_iddelet = []
		list_idupdate = []
		list_pathadd = []
		for listalbum in self.list_action:
			if listalbum[2] == 'DELETE':
				list_iddelet.append([listalbum[0], listalbum[1], listalbum[2], str(listalbum[3])])
			elif listalbum[2] == 'UPDATE':
				list_idupdate.append([listalbum[0], listalbum[1], listalbum[2], str(listalbum[3])])
			elif listalbum[2] == 'ADD':
				list_pathadd.append([listalbum[0], listalbum[1], listalbum[2], listalbum[5]])
		return list_idupdate + list_pathadd + list_iddelet



class BuildActions(QObject):
	# signal
	signalthunchgt = pyqtSignal(int, str)		# signal action database
					
	def __init__(self, list_actions):
		"""Init invent, build list albums exists in database."""
		super(BuildActions, self).__init__()
		self.list_action = list_actions
		self.list_idupdate = []
		self.list_idadd = []
		self.executeActions()

	def executeActions(self):
		"""Action for update database."""
		for listalbum in self.list_action:
			if listalbum[2] == 'DELETE':
				self.deleteAlbum(listalbum[3])
			elif listalbum[2] == 'UPDATE':
				self.updateAlbum(listalbum[3])
			elif listalbum[2] == 'ADD':
				self.addAlbum(listalbum)

	def updateAlbum(self, category, family, folder):
		"""Build album card."""
		#mask_artwork = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.bmp', '.tiff')	
		#mask_acovers = ('cover.jpg','Cover.jpg','cover.jpeg','cover.png','front.jpg','folder.jpg','folder.jpeg')
		#mask_amedias = ('.flac','.ape','.wma','.mp3','.wv','.aac','.mpc')
		#nb_amedias = len(list(getListFiles(folder, mask_amedias)))
		#nb_acovers = len(list(getListFiles(folder, mask_acovers))) # ############
		#nb_artwork = len(list(getListFiles(folder, mask_artwork)))
		#print(' '*20, GetalbumMD5(folder), nb_amedias, nb_acovers, nb_artwork)
		pass
		
	def addAlbums(self, listalbum):
		"""Add New Album in database."""
		#updatealbum = self.albumExist(folder)
		pass
	
def deleteAlbum(self, idcd):
	"""Delete Album in database."""
	pass



# ########################################################
def testini(envt):
	"""Connect base MySQL/Sqlite."""
	FILE__INI = 'DBAlbums.ini'
	configini = QSettings(FILE__INI, QSettings.IniFormat)
	configini.beginGroup(envt)
	#MODE_SQLI = configini.value('typb')
	BASE_RAC = r'' + configini.value('raci')
	RACI_DOU = configini.value('cate')
	RACI_SIM = configini.value('cats')
	configini.endGroup()
	if RACI_DOU is not None:
		list_category = buildlistcategory(configini, RACI_DOU, BASE_RAC, 'D')
	if RACI_SIM is not None:
		list_category += buildlistcategory(configini, RACI_SIM, BASE_RAC, 'S')
	for row in list_category:
		print(row)


if __name__ == '__main__':
	PATH_PROG = path.dirname(path.abspath(__file__))
	envt = 'MP3'
	testini(envt)



