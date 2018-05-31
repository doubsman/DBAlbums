#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sys import argv
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings
from DBDatabase import connectDatabase
from DBFunction import buildlistcategory
from DBTImpoTAG import DBMediasTags


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
	app = QApplication(argv)
	# debug
	envt = 'LOSSLESS_TEST'
	boolconnect, dbbase, modsql, rootDk, listcategory = connectDatabase(envt)

	list_infostrack = DBMediasTags().getTagMediaAPE('E:\\Work\\ZTest\\Hexstatic.ape')
	#coveral = DBMediasTags().getImageFromTagAPE('E:\\Work\\ZTest\\01 - Orb - Valley.ape', 'E:\\Work\\ZTest\\', 'APEkkxxyy')
	#print(list_infostrack)
	cb = QApplication.clipboard()
	cb.clear(mode=cb.Clipboard )
	cb.setText("Clipboard Text", mode=cb.Clipboard)
	
	
	#E:\Work\ZTest\TAG_bluid\TECHNO\Download\Caia - The Magic Dragon (2003)\01-caia--the_magic_dragon-csa.ape
	#timeduration = DBMediasTime('E:\\Work\\ZTest\\Hexstatic.ape').totalduration
	#timeduration = processfindduration.getLengthMedia()
	#print('koala', timeduration)

	rc = app.exec_()
	exit(rc)

