#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os import path
from copy import deepcopy
from PyQt5.QtCore import QObject, qDebug
from DBFunction import getListFilesNoSubFolders
from DBTImpoCUE import CueParser
from DBTImpoTAG import DBMediasTags


class CardTracks(QObject):
	DCardTrack = 	{	'ID_TRACK': None,
						'ID_CD': None,
						'FILENAME': None,
						'PATHNAME': None,
						# TAG
						'LENGTHSECONDS': 0, 
						'LENGTHDISPLAY': None,
						'TYPEMEDIA': None,
						'TITLE': None, 
						'ARTIST': None,
						'ALBUM': None,
						'DATE': None,
						'GENRE': None,
						'TRACKNUMBER': None,
						'ALBUMARTIST': None,
						'COMPOSER': None,
						'DISCNUMBER': None,
						'DISC': None,
						'TRACKORDER': None,
						'ISRC': None,
						'ORGANIZATION': None,
						'COUNTRY': None,
						# CUE
						'INDEX': None,
						'POS_START_SAMPLES': None,
						'POS_END_SAMPLES': None, 
						'SCORE': 0}
	
	def __init__(self, parent=None):
		"""Init."""
		super(CardTracks, self).__init__(parent)
		self.parent = parent
	
	def defineListTracksCUE(self, cuefile,  extension):
		"""transfert Cue file to Card Tracks
			no tag ALBUMARTIST / DISCNUMBER / ISRC / ORGANIZATION / COUNTRY ."""
		# first pass, define last track file for calcul duration
		listcardtrack = []
		pathcue = path.dirname(cuefile)
		parser = CueParser(cuefile)
		lastfile = parser.lastfiletrack
		pathmedia = path.join(pathcue, lastfile)
		# modified media test WAV in CUE with true extension
		if pathmedia.upper().endswith('.WAV'):
			pathmedia = pathmedia[:-3] + extension
			qDebug('-*- Extension WAV in CUE modified')
		if path.exists(pathmedia):
			list_tagtrack = DBMediasTags().getTagMedia(pathmedia)
			totalseconds = int(list_tagtrack['LENGTHSECONDS'])
			# parser final
			parser = CueParser(cuefile, totalseconds)
			listtrackscue = parser.get_data_tracks()
			for track in listtrackscue:
				track['PATHNAME'] = pathcue
				track['TYPEMEDIA'] = list_tagtrack['TYPEMEDIA']
				listcardtrack.append(self.defineTrackCUE(track))
		return listcardtrack
	
	def defineTrackCUE(self, trackcue):
		"""transfert Card Cue to Card Track."""
		mycardtrack = deepcopy(self.DCardTrack)
		#print(mycardtrack.keys(), trackcue.keys())
		for key in trackcue.keys():
			if key in mycardtrack.keys():
				mycardtrack[key] = trackcue[key]
		# translate
		mycardtrack['FILENAME'] = trackcue['FILE']
		mycardtrack['ARTIST'] = trackcue['PERFORMER']
		mycardtrack['COMPOSER'] = trackcue['SONGWRITER']
		return mycardtrack
	
	def defineListTracksFiles(self, pathfile):
		"""transfert file media tags to Card Tracks, no sub folders."""
		mask_amedias = ('.flac','.ape','.wma','.mp3','.wv','.aac','.mpc')
		listcardtrack = []
		listtracksfile = list(getListFilesNoSubFolders(pathfile, mask_amedias))
		for track in listtracksfile:
			mycardtrack = deepcopy(self.DCardTrack)
			#print hex(id(mycardtrack))
			list_tagtrack = DBMediasTags().getTagMedia(track)
			if list_tagtrack:
				list_tagtrack['LENGTHSECONDS'] = int(list_tagtrack['LENGTHSECONDS'])
				for key in list_tagtrack.keys():
					if key.upper() in mycardtrack.keys():
						mycardtrack[key.upper()] = list_tagtrack[key]
				listcardtrack.append(mycardtrack)
		#print(mycardtrack.keys(), list_tagtrack.keys())
		return listcardtrack

	def displayCardTracks(self, listcardtrack):
		"""Display CardTrack."""
		counter = 1
		for cardtrack in listcardtrack:
			print("\nTRACK--{num}--______--------______--------______----".format(num=counter))
			for key in cardtrack.keys():
				print(key, '=', cardtrack[key])
			counter += 1


if __name__ == '__main__':
	# list album track CUE TAG OK
	cuefile = r'E:\Work\ZTest\TAG_bluid\TRANCE\Download\2017\[OVNICD089] Ovnimoon & Rigel - Omnipresent Technology (2014)\Ovnimoon & Rigel - Omnipresent Technology.cue'
	cardtracks = CardTracks().defineListTracksCUE(cuefile)
	CardTracks().displayCardTracks(cardtracks)
	# list album track TAG
	cardtracks = CardTracks().defineListTracksFiles(r'E:\Work\ZTest\TAG_bluid\TRANCE\Labels\YSE\VA - Uncharted Vol.1 [Dacru Records] (2015)')
	CardTracks().displayCardTracks(cardtracks)
	
	
