#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os import path
from sys import platform
from re import match
from copy import deepcopy
from PyQt5.QtCore import QObject, QDateTime, pyqtSignal
from DBFunction import getListFiles, getListFolders, getFolderSize, getListFilesNoSubFolders
from DBTImpoCUE import CueParser
from DBTImpoTRK import CardTracks
from DBTImpoTAG import DBMediasTags
from DBReadJson import JsonParams


class CardAlbum(QObject):
	signaltxt = pyqtSignal(str, int)		# message / level display
	
	mask_artwork = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.bmp', '.tiff')	
	mask_acovers = ('cover.jpg','Cover.jpg','cover.jpeg','cover.png','front.jpg','folder.jpg','folder.jpeg')
	mask_amedias = ('.flac','.ape','.wma','.mp3','.wv','.aac','.mpc')
	DCardAlbum = 	{	'ID_CD': None,			# Base
						'CATEGORY': None,		# Params
						'FAMILY': None,			# Params
						'NAME': None,			# Path
						'ARTIST': None,			# Tag
						'PATHNAME': None,		# Path
						'POSITION': None,		# Path
						'SUBPOSITION': None,	# Path
						'POSITIONHDD': None, 	# Path
						'AUDIOTRACKS': 0,		# Files
						'TRACKS': 0,			# Files
						'CUE': 0,				# Files
						'COVER': None,			# Files / Tag
						'PIC': 0,				# Files
						'SIZE': 0,				# Files
						'CD': 0,				# Tag / Path / Files
						'YEAR': None,			# Path / Tag
						'ISRC': None,			# Path
						'LABEL': None,			# Path
						'TAGISRC': None,		# Tag
						'TAGLABEL': None,		# Tag
						'STYLE': None,			# Tag
						'COUNTRY': None,		# Tag
						'LENGTHSECONDS': 0,		# Tag
						'LENGTHDISPLAY': None,	# Tag / Calcul
						'TYPEMEDIA': None,		# Tag
						'SCORE': 0, 			# default value
						'TAGMETHOD': None,		# method tag album
						'ADD': None, 			# Calcul
						'MODIFIED': None		# Calcul
						}

	def __init__(self, parent=None):
		"""Init."""
		super(CardAlbum, self).__init__(parent)
		self.parent = parent
		self.PATH_PROG = path.dirname(path.abspath(__file__))
		self.FILE__INI = path.join(self.PATH_PROG, 'DBAlbums.json')
		Json_params = JsonParams(self.FILE__INI)
		group_dbalbums = Json_params.getMember('dbalbums')
		self.TEXT_NCO = group_dbalbums['text_nocov']

	def defineAlbum(self, pathalbum, category, family):
		"""Define Card Album."""
		cardalbum = deepcopy(self.DCardAlbum)
		listcardtrack = []
		cardalbum['NAME'] = path.basename(pathalbum).replace('_',' ').replace('-WEB','')
		list_tracksaudio = list(getListFiles(pathalbum, self.mask_amedias))
		cardalbum['AUDIOTRACKS'] = len(list_tracksaudio)
		if cardalbum['AUDIOTRACKS'] > 0:
			cardalbum['CATEGORY'] = category
			cardalbum['FAMILY'] = family
			cardalbum['PATHNAME'] = pathalbum
			cardalbum['PIC'] = len(list(getListFiles(pathalbum, self.mask_artwork)))
			cardalbum['SIZE'] = int(round(getFolderSize(pathalbum)/1024/1024, 0))
			if platform == "darwin" or platform == 'linux':
				carseparat = '/'
			else:
				carseparat = '\\'
			cardalbum['POSITION'] = pathalbum.split(carseparat)[-3]
			cardalbum['SUBPOSITION'] = pathalbum.split(carseparat)[-2]
			cardalbum['POSITIONHDD'] = pathalbum.split(carseparat)[-3] + carseparat + pathalbum.split(carseparat)[-2]
			
			# cover path
			coversfile = list(getListFilesNoSubFolders(pathalbum, self.mask_acovers, 'Exactly'))
			coversfile.sort()
			if len(coversfile) > 0:
				# get first
				cardalbum['COVER'] = coversfile[0]
			else:
				coversfile = list(getListFiles(pathalbum, self.mask_acovers, 'Exactly'))
				coversfile.sort()
				if len(coversfile) > 0:
					cardalbum['COVER'] = coversfile[0]
				else:
					# tag no picture
					cardalbum['COVER'] = self.TEXT_NCO
				
			# year path
			yearfind = match(r'.*([(][1-2][0-9]{3}[)])', cardalbum['NAME'])
			if yearfind:
				cardalbum['YEAR'] = yearfind.group(1)[1:-1]
				cardalbum['NAME'] = cardalbum['NAME'][:-6]
			
			# label path
			if 'LABEL' in family.upper():
				cardalbum['LABEL'] = cardalbum['SUBPOSITION'].upper()
				# isrc path
				if cardalbum['NAME'].startswith('['):
					cardalbum['ISRC'] = cardalbum['NAME'].split(']')[0].split('[')[1]
					cardalbum['NAME'] = cardalbum['NAME'][cardalbum['NAME'].find(']')+2:]
					
			# artist path
			if 'ARTIST' in family.upper():
				cardalbum['ARTIST'] = cardalbum['SUBPOSITION'].upper()
				
			# list valid CUEsheet file
			listfilescue = []
			filescue = list(getListFiles(pathalbum, ('.cue', )))
			for filecue in filescue:
				try:
					parser = CueParser(filecue)
					lastfile = parser.lastfiletrack
					pathmedia = path.join(path.dirname(filecue), lastfile)
					if pathmedia.upper().endswith('.WAV'):
						pathmedia = pathmedia[:-3] + list_tracksaudio[0].split('.')[-1]
					if path.exists(pathmedia):
						listfilescue.append(filecue)
				except:
					pass
			cardalbum['CUE'] = len(listfilescue)
			listfilescue.sort(reverse=False)
			
			# TAG file media method ? CUE or TAG
			if len(listfilescue) < cardalbum['AUDIOTRACKS']:
				cardalbum['TAGMETHOD'] = 'TAG'
				# album folder numbers of CD ?
				audioroot = list(getListFilesNoSubFolders(pathalbum,  self.mask_amedias))
				if len(audioroot) > 0:
					cardalbum['CD'] += 1
					albumcardtracks = CardTracks().defineListTracksFiles(pathalbum)
					for cardtrack in albumcardtracks:
						if cardtrack['TRACKNUMBER'] is not None:
							cardtrack['TRACKORDER'] = str(cardtrack['TRACKNUMBER'].split('/')[0]).zfill(2)
					listcardtrack += albumcardtracks
				elif len(audioroot) < cardalbum['AUDIOTRACKS']:
					albumfolders = getListFolders(pathalbum)
					albumfolders.sort(reverse=False)
					for albumfolder in albumfolders:
						fullalbumfolder = path.join(pathalbum, albumfolder)
						if len(list(getListFilesNoSubFolders(fullalbumfolder, self.mask_amedias))) > 0:
							cardalbum['CD'] += 1
							albumcardtracks = CardTracks().defineListTracksFiles(fullalbumfolder)
							counter = 1
							for cardtrack in albumcardtracks:
								cardtrack['DISC'] = cardalbum['CD']
								if cardtrack['TRACKNUMBER'] is None:
									cardtrack['TRACKORDER'] = str(cardalbum['CD']).zfill(2) + str(counter).zfill(2)
								else:
									cardtrack['TRACKORDER'] = str(cardalbum['CD']).zfill(2) + str(cardtrack['TRACKNUMBER'].split('/')[0]).zfill(2)
								counter += 1
							listcardtrack += albumcardtracks
							
			else:
				cardalbum['TAGMETHOD'] = 'CUE'
				for filecue in listfilescue:
					cardalbum['CD'] = cardalbum['CD'] + 1
					albumcardtracks = CardTracks().defineListTracksCUE(filecue, list_tracksaudio[0].split('.')[-1]	)
					for cardtrack in albumcardtracks:
						cardtrack['DISC'] = cardalbum['CD']
						if len(listfilescue) > 1:
							cardtrack['TRACKORDER'] = str(cardalbum['CD']).zfill(2) + str(cardtrack['TRACKNUMBER']).zfill(2)
						else:
							cardtrack['TRACKORDER'] = str(cardtrack['TRACKNUMBER']).zfill(2)
						if cardtrack['FILENAME'].upper().endswith('.WAV'):
							cardtrack['FILENAME'] = cardtrack['FILENAME'][:-3] + cardtrack['TYPEMEDIA'].split('/')[1]
					listcardtrack += albumcardtracks
			
			# numbers cds path
			if cardalbum['CD'] is None:
				numbercdfind = match(r'.*([1-9][C][D])', cardalbum['NAME'])
				if numbercdfind:
					cardalbum['CD'] = numbercdfind.group(1)[:-2]
			
			# tracks tag to album card
			if listcardtrack:
				cardtrack = listcardtrack[0]
				cardalbum['COUNTRY'] = cardtrack['COUNTRY']
				cardalbum['TYPEMEDIA'] = cardtrack['TYPEMEDIA']
				if cardtrack['ISRC'] is not None:
					cardalbum['TAGISRC'] = cardtrack['ISRC'].upper()
				if cardtrack['ORGANIZATION'] is not None:				
					cardalbum['TAGLABEL'] = cardtrack['ORGANIZATION'].upper()
				if 	cardalbum['TAGISRC'] is None:
					pass
					#cardalbum['TAGISRC'] = cardalbum['ISRC']
			
				# albumartist or artist tag
				if ' VA ' in cardalbum['NAME'] or cardalbum['NAME'].startswith('VA '):
					cardalbum['ARTIST'] = 'Various'
				else:
					cardalbum['ARTIST'] = cardtrack['ALBUMARTIST']
					if cardalbum['ARTIST'] is not None:
						cardalbum['ARTIST'] = cardalbum['ARTIST'].replace('VA', 'Various')
						cardalbum['ARTIST'] = cardalbum['ARTIST'].replace('Various Artists', 'Various')
					if cardalbum['ARTIST'] is None:
						cardalbum['ARTIST'] = cardtrack['ARTIST']
				
				# year tag
				if cardalbum['YEAR'] is None:
					cardalbum['YEAR'] = cardtrack['DATE']
				else:
					if cardtrack['DATE'] is not None:
						if cardalbum['YEAR'] != cardtrack['DATE'][:4]:
							self.signaltxt.emit('WARNING : year tag {tag} <> year path {pat}'.format(tag=cardtrack['DATE'], pat=cardalbum['YEAR'][:4]), 2)
			else:
				self.signaltxt.emit('ERROR : no tracks '+pathalbum, 3)
				
			# no year tag and no year path format
			if cardalbum['YEAR'] is None:
				yearfind = match(r'.*([1-2][0-9]{3})', cardalbum['NAME'])
				if yearfind:
					cardalbum['YEAR'] = yearfind.group(1)
			
			# cover if one image artwork
			if cardalbum['COVER'] == self.TEXT_NCO and cardalbum['PIC'] == 1:
				cardalbum['COVER'] = list(getListFiles(pathalbum, self.mask_artwork))[0]
			
			# cover tag
			if cardalbum['COVER'] == self.TEXT_NCO:
				cover = path.join(cardalbum['PATHNAME'], )
				if DBMediasTags().getImageFromTag(cover):
					cardalbum['COVER'] = cover
					cardalbum['PIC'] = 1
			
			# length tag & genres
			liststyles = []
			seconds = 0
			for cardtrack in listcardtrack:
				seconds += cardtrack['LENGTHSECONDS']
				if cardtrack['GENRE'] is not None:
					genres = cardtrack['GENRE']
					genres = genres.replace(';', '/').replace(',', '/').replace('"', '').replace('-', ' ').replace('  ', ' ')
					for genre in genres.split('/'):
						genre = genre.strip().title()
						if genre not in liststyles:
							liststyles.append(genre)
			cardalbum['STYLE'] = '/'.join(liststyles)

			minutes = seconds // 60	
			cardalbum['LENGTHSECONDS'] = seconds
			cardalbum['LENGTHDISPLAY'] = "%02d:%02d" % (minutes, seconds % 60)
			
			# number of tracks albums
			cardalbum['TRACKS'] = len(listcardtrack)
			
			# date
			cardalbum['ADD'] = QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mm:ss')
			cardalbum['MODIFIED'] = QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mm:ss')
			
			# clean album name
			cleanfind = match(r'.*([-][1-2][0-9]{3})', cardalbum['NAME'])
			if cleanfind:
				self.signaltxt.emit('WARNING : clean : ' + cardalbum['NAME'], 2)
				cardalbum['NAME'] = self.cleanfolderalbum(cardalbum['NAME'])
			if cardalbum['NAME'].endswith('-'):
				cardalbum['NAME'] = cardalbum['NAME'][:-1]
				
			# cover from multiple pics
			if cardalbum['COVER'] == self.TEXT_NCO and cardalbum['PIC'] > 1:
				listcovers = list(getListFiles(pathalbum, self.mask_artwork))
				for listcover in listcovers:
					if 'front' in listcover.lower():
						cardalbum['COVER'] = listcover
			
		return cardalbum, listcardtrack

	def displayCardAlbum(self, cardalbum):
		"""Display CardAlbum."""
		print('-', '______----ALBUM----______')
		for key, value in cardalbum.items():
			print(f'{key:<15} = {value}')

	def cleanfolderalbum(self, albumname):
		"""Clean folder album name WEB."""
		albumtempo = albumname.replace("-psy-music.ru","").replace("_"," ").replace("."," ").replace("--","-")
		yearfind = match(r'.*([-][1-2][0-9]{3})', albumtempo)
		albumtempo = yearfind.group(0)[:-5]
		if albumtempo.find(' - ') > 0:
			arrayalbum = albumtempo.split(' - ')
		else:
			arrayalbum = albumtempo.split('-')
		numbertirets = len(arrayalbum)
		if numbertirets == 1:
			albumtempo = arrayalbum[0].strip()
		else:
			albumtempo = arrayalbum[0].strip() + ' - ' + arrayalbum[1].strip()
		#if numbertirets == 2:
		#	albumtempo = arrayalbum[0].strip() + '-' + arrayalbum[1].strip() + "[" + arrayalbum[2].strip() + "]"
		return albumtempo
		
