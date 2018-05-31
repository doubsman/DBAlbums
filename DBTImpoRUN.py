#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os import path
from sys import argv
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, QSettings, pyqtSignal, qDebug
from DBDatabase import DBFuncBase, connectDatabase
from DBTImpoALB import CardAlbum
from DBFunction import displayArrayDict


class ReleaseInvent(QObject):
	signalrun = pyqtSignal(int, str)		# percent / message
	signaltxt = pyqtSignal(str, int)		# message / level display
	signalend = pyqtSignal()
	signalmacroend = pyqtSignal()
		
	PATH_PROG = path.dirname(path.abspath(__file__))
	# Read File DBAlbums.ini
	qDebug('read ini file')
	FILE__INI = 'DBAlbums.ini'
	configini = QSettings(FILE__INI, QSettings.IniFormat)
	configini.beginGroup('dbalbums')
	WIDT_PICM = int(configini.value('thun_csize'))
	TEXT_NCO = configini.value('text_nocov')
	configini.endGroup()
					
	def __init__(self, list_actions):
		"""Init invent, build list albums exists in database."""
		super(ReleaseInvent, self).__init__()
		self.list_action = list_actions

	def executeActions(self):
		"""Action for update database.
			[CATEGORY, FAMILY, 'DELETE/UPDATE/ADD', ID_CD, 'NAME', 'PATHNAME']"""
		numbersactions = len(self.list_action)
		counter = 1
		for listalbum in self.list_action:
			self.signalrun.emit((counter / numbersactions) * 100, listalbum[2])
			message = "\n- {act} ({num}/{tot}) : {nam}".format(act = listalbum[2],
															num = counter,
															tot = numbersactions, 
															nam = listalbum[5])
			self.signaltxt.emit(message, 1)
			if listalbum[2] == 'DELETE':
				self.deleteAlbum(listalbum[3])
			elif listalbum[2] == 'UPDATE':
				#print('UPDATE', listalbum[0], listalbum[1], listalbum[5], listalbum[3])
				self.updateAlbum(listalbum[0], listalbum[1], listalbum[5], listalbum[3])
			elif listalbum[2] == 'ADD':
				#print('ADD', listalbum[0], listalbum[1], listalbum[5], listalbum[5])
				self.addAlbum(listalbum[0], listalbum[1], listalbum[5])
			else:
				self.signaltxt.emit('ERROR : Operation "' + listalbum[2] + '" error', 3)
			counter += 1 
		#QApplication.processEvents()
		self.signalrun.emit(100, 'Completed')
		self.signalend.emit()

	def emitDisplayCardAlbum(self, cardalbum, cardtracks):
		self.signaltxt.emit(displayArrayDict([cardalbum], ('ID_CD', 'CATEGORY', 'FAMILY', 'TAGMETHOD', 'POSITIONHDD', 'NAME')), 0)
		self.signaltxt.emit(displayArrayDict([cardalbum], ('AUDIOTRACKS', 'TRACKS', 'LENGTHDISPLAY', 'CUE', 'PIC', 'SIZE', 'CD', 'YEAR', 'ISRC', 'LABEL', 'TAGISRC', 'TAGLABEL', 'COUNTRY')), 0)
		self.signaltxt.emit(displayArrayDict(cardtracks, ('TRACKORDER', 'LENGTHDISPLAY', 'ARTIST', 'TITLE', 'TYPEMEDIA', 'DATE', 'GENRE', 'DISC', 'FILENAME')), 0)
		
	def updateAlbum(self, category, family, folder, idcd):
		"""Build album card."""
		# capture datas old
		oldcardalbum = DBFuncBase().sqlToArrayDict('ALBUMS', 'ID_CD', idcd)
		oldcardalbum = oldcardalbum[0]
		oldcardtracks = DBFuncBase().sqlToArrayDict('TRACKS', 'ID_CD', idcd)
		# delete old
		DBFuncBase().deleteTable("TRACKS", "ID_CD", idcd)
		DBFuncBase().deleteTable("COVERS", "ID_CD", idcd)
		# new
		analysealbum = CardAlbum()
		analysealbum.signaltxt.connect(self.infoAnalysealbum)
		cardalbum, cardtracks = analysealbum.defineAlbum(folder, category, family)
		# apply ID album
		for cardtrack in cardtracks:
			cardtrack['ID_CD'] = idcd
		# copy old datas  albums
		cardalbum['ID_CD'] = oldcardalbum['ID_CD']
		cardalbum['SCORE'] = oldcardalbum['SCORE']
		cardalbum['ADD'] = oldcardalbum['ADD']
		# copy score track
		for oldcardtrack in oldcardtracks:
			if oldcardtrack['SCORE'] > 0:
				print ("score")
				# copy score
				for cardtrack in cardtracks:
					if cardtrack['FILENAME'] == oldcardtrack['FILENAME'] and cardtrack['TRACKORDER'] == oldcardtrack['TRACKORDER']:
						cardtrack['SCORE'] = oldcardtrack['SCORE']
		# write album update
		DBFuncBase().arrayCardsToSql('UPDATE', cardalbum, 'ALBUMS', 'ID_CD')
		DBFuncBase().arrayCardsToSql('INSERT', cardtracks, 'TRACKS', 'ID_TRACK')
		if cardalbum['COVER'] != self.TEXT_NCO:
			DBFuncBase().imageToSql(cardalbum['COVER'], idcd, self.WIDT_PICM)
		# display consol
		self.emitDisplayCardAlbum(cardalbum, cardtracks)
		self.signalmacroend.emit()
		
	def addAlbum(self, category, family, folder):
		"""Add New Album in database."""
		analysealbum = CardAlbum()
		analysealbum.signaltxt.connect(self.infoAnalysealbum)
		cardalbum, cardtracks = analysealbum.defineAlbum(folder, category, family)
		DBFuncBase().arrayCardsToSql('INSERT', cardalbum, 'ALBUMS', 'ID_CD')
		# last id for cardtracks
		request = "SELECT LAST_INSERT_ID() as lastid;"
		idcd = DBFuncBase().sqlToArray(request)[0]
		for cardtrack in cardtracks:
			cardtrack['ID_CD'] = idcd
		DBFuncBase().arrayCardsToSql('INSERT', cardtracks, 'TRACKS', 'ID_TRACK')
		if cardalbum['COVER'] != self.TEXT_NCO:
			DBFuncBase().imageToSql(cardalbum['COVER'], idcd, self.WIDT_PICM)
		# display consol
		self.emitDisplayCardAlbum(cardalbum, cardtracks)
		self.signalmacroend.emit()
	
	def deleteAlbum(self, idcd):
		"""Delete Album in database."""
		DBFuncBase().deleteTable("ALBUMS", "ID_CD", idcd)
		DBFuncBase().deleteTable("TRACKS", "ID_CD", idcd)
		DBFuncBase().deleteTable("COVERS", "ID_CD", idcd)
		self.signalmacroend.emit()
	
	def infoAnalysealbum(self, text, level):
		self.signaltxt.emit(text, level)

if __name__ == '__main__':
	app = QApplication(argv)
	# debug
	envt = 'LOSSLESS_TEST'
	boolconnect, dbbase, modsql, rootDk, listcategory = connectDatabase(envt)
	
	# ADD
	#ReleaseInvent().addAlbums('TRANCE', 'Download', r'E:\Work\ZTest\TAG_bluid\TRANCE\Download\2017\[OVNICD089] Ovnimoon & Rigel - Omnipresent Technology (2014)')
	
	# UPDATE
	#cardalbum['ID_CD'] = 1
	#cardalbum['NAME'] = 'le petit lapin'
	#print(DBFuncBase().arrayCardsToSql('UPDATE', cardalbum, 'ALBUMS', 'ID_CD'))
	
	# INSERT
	#DBFuncBase().arrayCardsToSql('INSERT', cardalbum, 'ALBUMS', 'ID_CD')
	#for cardtrack in cardtracks:
	#	cardtrack['ID_CD'] = 2
	#DBFuncBase().arrayCardsToSql('INSERT', cardtracks, 'TRACKS', 'ID_TRACK')
	#CardAlbum().displayCardAlbum(cardalbum)
	#DBFuncBase().imageToSql(pathimage, idcd, minisize)

	# READ
	#print(DBFuncBase().sqllToArrayDict('ALBUMS', 'ID_CD', 1))
	#print(DBFuncBase().sqllToArrayDict('TRACKS', 'ID_CD', 2))	

	oldcardtracks = DBFuncBase().sqlToArrayDict('TRACKS', 'ID_CD', 23)
	print(oldcardtracks)


#	cardalbum, cardtracks = CardAlbum().defineAlbum(r'\\HOMERSTATION\_LossLess\TECHNO\Labels\Kompakt\[KOMPAKT CD 132] VA - Kompakt Total 16 (2016)', 'TECHNO', "Labels")
#	print(displayArrayDict([cardalbum], ('ID_CD', 'CATEGORY', 'FAMILY', 'TAGMETHOD', 'POSITIONHDD', 'NAME', 'COVER')))
#	print(displayArrayDict([cardalbum], ('AUDIOTRACKS', 'TRACKS', 'LENGTHDISPLAY', 'CUE', 'PIC', 'SIZE', 'CD', 'YEAR', 'ISRC', 'LABEL', 'TAGISRC', 'TAGLABEL', 'COUNTRY')))
#	print(displayArrayDict(cardtracks, ('TRACKORDER', 'LENGTHDISPLAY', 'ARTIST', 'TITLE', 'TYPEMEDIA', 'DATE', 'GENRE', 'DISC', 'FILENAME')))


	
