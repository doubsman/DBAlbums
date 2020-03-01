#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from sys import platform
from json import load, dumps
from PyQt5.QtCore import QObject


class JsonParams(QObject):
	def __init__(self, file_json='DBAlbums.json', parent=None):
		"""Init invent, build list albums exists in database."""
		super(JsonParams, self).__init__(parent)
		self.file_json = file_json
		data_file = open(self.file_json, 'r')
		self.data = load(data_file)
		data_file.close()
		#self.data = loads(self.data_file).read())

	def getMember(self, member):
		"""Return array infos member of json."""
		return(self.data[member])

	def buildListEnvt(self, curenvt):
		"""Build list environments."""
		list_envt = []
		listenvt = self.data["environments"]
		for envt in listenvt:
			if listenvt[envt]==curenvt:
				Curt_Evt = len(list_envt)
			list_envt.append(listenvt[envt])
		return list_envt, Curt_Evt

	def buildDictScore(self):
		"""Build list scoring."""
		dict_score = {}
		listescore = self.data["score"]
		for envt in listescore:
			dict_score.update({int(envt): listescore[envt]})
		return dict_score

	def buildListcategory(self, envt):
		"""Build list category simple and double from json file."""
		racine =  self.data[envt]["raci"]
		category = self.data[envt]["cate"]
		list_pathcollection = []
		listcate = self.data[category]
		for cate in listcate:
			# one element
			mstyle = listcate[cate]["style"]
			family = listcate[cate]["family"]
			racate = listcate[cate]["folder"]
			mode = listcate[cate]["mode"]
			racate = path.join(racine, racate)
			racate = self.convertUNC(racate)
			list_pathcollection.append([mstyle, mode, racate, family])
		return list_pathcollection

	def addLineCategory(self, category):
		try:
			number  = len(self.data[category]) + 1
		except:
			# new category
			number = 1
			self.data[category] = {}	
		virginline = { "style" : '', "mode" : '', "folder" : '', "family" : '' }
		folder = 'FOLDER' + format(number, '03d')
		self.data[category][folder] = virginline

	def delLineCategory(self, category, number):
		folder = 'FOLDER' + format(number, '03d')
		del(self.data[category][folder])

	def saveJson(self):
		"""Save Json file conofiguration."""
		data_file = open(self.file_json+'2', 'w+')
		data_file.write(dumps(self.data, indent=4))
		data_file.close()

	def convertUNC(self, path):
		""" convert path UNC to linux."""
		# open file unc from Linux (/HOMERSTATION/_lossLess)
		# open file unc windows 10 (\\HOMERSTATION\_lossLess)
		if (platform == "darwin" or platform == 'linux'):
			if path.startswith(r'\\'):
				path = r""+path.replace('\\\\', '/').replace('\\', '/')
		else:
			if path.startswith(r'/'):
				path = r""+path.replace('/', '\\\\').replace('/', '\\')
		return path	
