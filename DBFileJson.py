#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path, rename
from json import load, dumps
from PyQt5.QtCore import QObject, QDateTime
# general Libs
from LIBFilesProc import FilesProcessing


class JsonParams(QObject):
	def __init__(self, file_json='DBAlbums.json', parent=None):
		"""Init invent, build list albums exists in database."""
		super(JsonParams, self).__init__(parent)
		self.file_json = file_json
		self.file_gest = FilesProcessing()
		self.loadJson()

	def loadJson(self):
		"""Load Json file configuration."""
		data_file = open(self.file_json, 'r')
		self.data = load(data_file)
		data_file.close()
		#self.data = loads(self.data_file).read())
		self.jsonlistcategories = list(self.data['categories'].keys())
		self.jsonlistenvironments = list(self.data['environments'].keys())

	def reloadJson(self, filejson):
		"""Change file Json configuration."""
		self.file_json = filejson
		self.loadJson()

	def saveJson(self):
		"""Save Json file conofiguration."""
		# rename old
		oldname = None
		if path.exists(self.file_json):
			oldname = self.file_json.replace('.json','') + QDateTime.currentDateTime().toString('yyMMddhhmmss') + ".json"
			rename(self.file_json, oldname)
			print(oldname)
		data_file = open(self.file_json, 'w+')
		data_file.write(dumps(self.data, indent=4))
		data_file.close()
		return oldname, self.file_json

	def getMember(self, member):
		"""Return array infos member of json."""
		return(self.data[member])
	
	def getContentMember(self, group, member):
		"""Return array infos member member of json."""
		return self.data[group][member]

	def buildDictScore(self):
		"""Build list scoring."""
		dict_score = {}
		listescore = self.data["score"]
		for envt in listescore:
			dict_score.update({int(envt): listescore[envt]})
		return dict_score

	def buildListcategory(self, envt):
		"""Build list category simple and double from json file."""
		racine =  self.data['environments'][envt]["raci"]
		category = self.data['environments'][envt]["cate"]
		list_pathcollection = []
		listcate = self.data['categories'][category]
		for cate in listcate:
			# one element
			mstyle = listcate[cate]["style"]
			family = listcate[cate]["family"]
			racate = listcate[cate]["folder"]
			mode = listcate[cate]["mode"]
			racate = path.join(racine, racate)
			racate = self.file_gest.convertUNC(racate)
			list_pathcollection.append([mstyle, mode, racate, family])
		return list_pathcollection

	def buildListEnvt(self, curenvt):
		"""Build list environments."""
		list_envt = []
		listenvt = list(self.data['environments'].keys())
		for envt in listenvt:
			if envt == curenvt:
				Curt_Evt = len(list_envt)
			list_envt.append(envt)
		return list_envt, Curt_Evt
	
	def modJsonGeneral(self, group, param, value):
		self.data[group][param] = value

	def addEnvt(self, envt):
		# add new envt
		virginline = (self.data['environments'][list(self.data['environments'].keys())[0]]).copy()
		for key in virginline:
			virginline[key] = None
		self.data['environments'][envt] = virginline

	def modJsonEnvt(self, group, param, value):
		self.data['environments'][group][param] = value

	def delEnvt(self, envt):
		del self.data['environments'][envt]

	def addFami(self, key):
		self.data['families'][key] = '<folder name>'

	def modJsonFami(self, row, col, value, oldvalue):
		currow = 0
		for key, val in self.data['family'].items():
			if currow == row:
				if col == 0:
					# rename keys
					self.data['families'][value] = val
					del self.data['families'][oldvalue]
				else:
					# change value
					self.data['families'][key] = value
				break
			currow += 1

	def delFami(self, key):
		del self.data['families'][key]

	def addCategory(self, namecate):
		"""Create new Category + add list."""
		self.addLineCategory(namecate)

	def modJsonCate(self, group, param, column, value):
		self.data['categories'][group][param][column] = value

	def delCategory(self, namecate):
		"""Delete Category + del list."""
		del self.data['categories'][namecate]

	def addLineCategory(self, category):
		"""Creation category if new line and no exist."""
		try:
			number  = len(self.data['categories'][category]) + 1
		except:
			# new category
			number = 1
			self.data['categories'][category] = {}
		virginline = (self.data['categories'][list(self.data['categories'].keys())[0]]['folder001']).copy()
		for key in virginline:
			virginline[key] = ''
		#virginline = { "style" : '', "mode" : '', "folder" : '', "family" : '' }
		folder = 'folder' + format(number, '03d')
		self.data['categories'][category][folder] = virginline

	def delLineCategory(self, category, number):
		rows = len(self.data['categories'][category])
		# renumeroration FOLDERxxx
		for row in range(number, rows + 1):
			folderdes = 'folder' + format(row, '03d')
			foldersrc = 'folder' + format(row + 1, '03d')
			if row == rows:
				del self.data['categories'][category][folderdes]
			else:
				self.data['categories'][category][folderdes] = self.data['categories'][category][foldersrc]



