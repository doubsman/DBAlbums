#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sys import argv
from os import path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings
#from DBDatabase import connectDatabase
from DBFunction import buildlistcategory
#from DBTImpoTAG import DBMediasTags
from json import load
from PyQt5.QtCore import QObject

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


class JsonParams(QObject):
	def __init__(self, file_json='DBAlbums.json'):
		"""Init invent, build list albums exists in database."""
		super(JsonParams, self).__init__()
		with open(file_json) as data_file:    
			self.data = load(data_file)

	def buildCategories(self,  envt):
		"""Build list category simple and double from json file."""
		racine =  self.data[envt]["raci"]
		category = self.data[envt]["cate"]
		list_category = []
		list_category += self.buildCategory(racine, category)
		return list_category

	def defineDbalbum(self):
		return(self.data['dbalbums'])

	def defineProgExt(self):
		return(self.data['programs'])

	def defineEnvt(self,  envt):
		return(self.data[envt])
	
	def buildCategory(self,  racine, category):
		"""Build list for one category."""
		list_category = []
		listcate = self.data[category]
		for cate in listcate:
			family = None
			if isinstance( listcate[cate], list) or isinstance( listcate[cate], dict):
				if isinstance( listcate[cate], list) :
					for souslistcate in listcate[cate]:
						if isinstance( souslistcate, dict):
							family = souslistcate["family"]
							racate = souslistcate["name"]
							mode = souslistcate["mode"]
							racate = path.join(racine, racate)
							list_category.append([cate, mode, racate, family])
						else:
							family =  None
							racate =  listcate[cate]
							mode= 'D'
							racate = path.join(racine, racate)
							list_category.append([cate, mode, racate, family])
				else:
					family = listcate[cate]["family"]
					racate = listcate[cate]["name"]
					mode = listcate[cate]["mode"]
					racate = path.join(racine, racate)
					list_category.append([cate, mode, racate, family])
			else:
				family =  None
				racate =  listcate[cate]
				mode= 'D'
				racate = path.join(racine, racate)
				list_category.append([cate, mode, racate, family])
			
			
		return list_category
	
	def buildListEnvt(self):
		"""Build list environments."""
		list_envt = []
		listenvt = self.data["environments"]
		for envt in listenvt:
			list_envt.append(listenvt[envt])
		return list_envt

	def buildListScore(self):
		"""Build list scoring."""
		dict_score = {}
		listescore = self.data["score"]
		for envt in listescore:
			dict_score.update({int(envt): listescore[envt]})
		return dict_score


 

if __name__ == '__main__':
	app = QApplication(argv)
	# debug
	#envt = 'LOSSLESS_TEST'
	#boolconnect, dbbase, modsql, rootDk, listcategory = connectDatabase(envt)
	testini('MP3')
	print("---")
	
	params = JsonParams()
	mylist = params.buildCategories('MP3')
	for row in mylist:
		print(row)
	#for key in mylist:
	#	print(key + " = " + str(mylist[key]))
	
	#list_infostrack = DBMediasTags().getTagMediaAPE('E:\\Work\\ZTest\\Hexstatic.ape')
	#coveral = DBMediasTags().getImageFromTagAPE('E:\\Work\\ZTest\\01 - Orb - Valley.ape', 'E:\\Work\\ZTest\\', 'APEkkxxyy')
	#print(list_infostrack)
	#cb = QApplication.clipboard()
	#cb.clear(mode=cb.Clipboard )
	#cb.setText("Clipboard Text", mode=cb.Clipboard)
	
	
	#E:\Work\ZTest\TAG_bluid\TECHNO\Download\Caia - The Magic Dragon (2003)\01-caia--the_magic_dragon-csa.ape
	#timeduration = DBMediasTime('E:\\Work\\ZTest\\Hexstatic.ape').totalduration
	#timeduration = processfindduration.getLengthMedia()
	#print('koala', timeduration)

	rc = app.exec_()
	exit(rc)

