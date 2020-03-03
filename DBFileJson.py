#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path, rename
from sys import platform
from json import load, dumps
from PyQt5.QtCore import QObject, QDateTime


class JsonParams(QObject):
	def __init__(self, file_json='DBAlbums.json', parent=None):
		"""Init invent, build list albums exists in database."""
		super(JsonParams, self).__init__(parent)
		self.file_json = file_json
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

	def getMember(self, member):
		"""Return array infos member of json."""
		return(self.data[member])
	
	def getContentMember(self, group, member):
		"""Return array infos member member of json."""
		return self.data[group][member]

	def modJson(self, group, param, value):
		self.data[group][param] = value

	def modJsonEnvt(self, group, param, value):
		self.data['environments'][group][param] = value

	def modJsonCate(self, group, param, column, value):
		self.data['categories'][group][param][column] = value

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

	def buildListEnvt(self, curenvt):
		"""Build list environments."""
		list_envt = []
		listenvt = list(self.data['environments'].keys())
		for envt in listenvt:
			if envt == curenvt:
				Curt_Evt = len(list_envt)
			list_envt.append(envt)
		return list_envt, Curt_Evt
	
	def addEnvt(self, envt):
		# add new envt
		number = len(self.data['environments'].keys()) + 1
		virginline = (self.data['environments'][list(self.data['environments'].keys())[0]]).copy()
		for key in virginline:
			virginline[key] = None
		folder = 'envt' + format(number, '03d')
		self.data['environments'][envt] = virginline

	def delEnvt(self, envt):
		del self.data['environments'][envt]

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
			racate = self.convertUNC(racate)
			list_pathcollection.append([mstyle, mode, racate, family])
		return list_pathcollection

	def addCategory(self, namecate):
		"""Create new Category + add list."""
		self.addLineCategory(namecate)

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
		folder = 'folder' + format(number, '03d')
		rows = len(self.data['categories'][category])
		# renumeroration FOLDERxxx
		for row in range(number, rows + 1):
			folderdes = 'folder' + format(row, '03d')
			foldersrc = 'folder' + format(row + 1, '03d')
			if row == rows:
				del self.data['categories'][category][folderdes]
			else:
				self.data['categories'][category][folderdes] = self.data['categories'][category][foldersrc]

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
