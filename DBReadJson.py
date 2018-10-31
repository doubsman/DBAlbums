#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os import path
from json import load
from PyQt5.QtCore import QObject


class JsonParams(QObject):
	def __init__(self, file_json='DBAlbums.json'):
		"""Init invent, build list albums exists in database."""
		super(JsonParams, self).__init__()
		with open(file_json) as data_file:    
			self.data = load(data_file)

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

	def buildCategories(self,  envt):
		"""Build list category simple and double from json file."""
		racine =  self.data[envt]["raci"]
		category = self.data[envt]["cate"]
		list_pathcollection = []
		list_pathcollection = self.buildCategory(racine, category)
		return list_pathcollection

	def buildCategory(self,  racine, category):
		"""Build list for one category."""
		list_pathcollection = []
		listcate = self.data[category]
		for cate in listcate:
			if isinstance( listcate[cate], list):
				# array elements
				for souslistcate in listcate[cate]:
					family = souslistcate["family"]
					racate = souslistcate["name"]
					mode = souslistcate["mode"]
					racate = path.join(racine, racate)
					list_pathcollection.append([cate, mode, racate, family])
			else:
				# one element
				family = listcate[cate]["family"]
				racate = listcate[cate]["name"]
				mode = listcate[cate]["mode"]
				racate = path.join(racine, racate)
				list_pathcollection.append([cate, mode, racate, family])
		return list_pathcollection
