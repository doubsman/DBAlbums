#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtCore import QObject, pyqtSignal
from DBTImpoALB import CardAlbum
from DBFunction import displayArrayDict

class ReleaseInvent(QObject):
	signalrun = pyqtSignal(int, str)		# percent / message
	signaltxt = pyqtSignal(str, int)		# message / level display
	signalend = pyqtSignal()
	signalmacroend = pyqtSignal()
		
	def __init__(self, parent, list_actions):
		"""Init invent, build list albums exists in database."""
		super(ReleaseInvent, self).__init__()
		self.parent = parent
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
		oldcardalbum = self.parent.CnxConnect.sqlToArrayDict('ALBUMS', 'ID_CD', idcd)
		oldcardalbum = oldcardalbum[0]
		oldcardtracks = self.parent.CnxConnect.sqlToArrayDict('TRACKS', 'ID_CD', idcd)
		# delete old
		self.parent.CnxConnect.deleteLineTable("TRACKS", "ID_CD", idcd)
		self.parent.CnxConnect.deleteLineTable("COVERS", "ID_CD", idcd)
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
				# copy score
				for cardtrack in cardtracks:
					if cardtrack['FILENAME'] == oldcardtrack['FILENAME'] and cardtrack['TRACKORDER'] == oldcardtrack['TRACKORDER']:
						cardtrack['SCORE'] = oldcardtrack['SCORE']
		# write album update
		self.parent.CnxConnect.arrayCardsToSql('UPDATE', cardalbum, 'ALBUMS', 'ID_CD')
		self.parent.CnxConnect.arrayCardsToSql('INSERT', cardtracks, 'TRACKS', 'ID_TRACK')
		if cardalbum['COVER'] != self.parent.TEXT_NCO:
			self.parent.CnxConnect.imagesToSql(cardalbum['COVER'], idcd, self.parent.WIDT_PICM)
		# display consol
		self.emitDisplayCardAlbum(cardalbum, cardtracks)
		self.signalmacroend.emit()
		
	def addAlbum(self, category, family, folder):
		"""Add New Album in database."""
		analysealbum = CardAlbum()
		analysealbum.signaltxt.connect(self.infoAnalysealbum)
		cardalbum, cardtracks = analysealbum.defineAlbum(folder, category, family)
		self.parent.CnxConnect.arrayCardsToSql('INSERT', cardalbum, 'ALBUMS', 'ID_CD')
		# last id for cardtracks
		#request = "SELECT LAST_INSERT_ID() as lastid;"
		request = self.parent.CnxConnect.getrequest('lastid')
		idcd = self.parent.CnxConnect.sqlToArray(request)[0]
		for cardtrack in cardtracks:
			cardtrack['ID_CD'] = idcd
		self.parent.CnxConnect.arrayCardsToSql('INSERT', cardtracks, 'TRACKS', 'ID_TRACK')
		if cardalbum['COVER'] != self.parent.TEXT_NCO:
			self.parent.CnxConnect.imagesToSql(cardalbum['COVER'], idcd, self.parent.WIDT_PICM)
		# display consol
		self.emitDisplayCardAlbum(cardalbum, cardtracks)
		self.signalmacroend.emit()
	
	def deleteAlbum(self, idcd):
		"""Delete Album in database."""
		self.parent.CnxConnect.deleteLineTable("ALBUMS", "ID_CD", idcd)
		self.parent.CnxConnect.deleteLineTable("TRACKS", "ID_CD", idcd)
		self.parent.CnxConnect.deleteLineTable("COVERS", "ID_CD", idcd)
		self.signalmacroend.emit()
	
	def infoAnalysealbum(self, text, level):
		self.signaltxt.emit(text, level)


