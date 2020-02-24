#! /usr/bin/python
# coding: utf-8

__author__ = "doubsman"
__copyright__ = "Copyright 2020, Files Project"
__credits__ = ["doubsman"]
__license__ = "GPL"
__version__ = "1.00"
__maintainer__ = "doubsman"
__email__ = "doubsman@doubsman.fr"
__status__ = "Production"


from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, qDebug, QDateTime, QProcess
from os import walk, rename, path, mkdir, remove, rmdir, startfile, listdir
from sys import argv,platform
from glob import glob
from shutil import move, rmtree
from codecs import open


class FilesProcessing(QObject):
	"""build list folders name, search youtube and download first video find format mp4."""
						
	def __init__(self, parent=None):
		"""Init."""
		super(FilesProcessing, self).__init__(parent)
		self.parent = parent
		self.blacklist = ['desktop.ini', 'Thumbs.db']
		self.listfolders = None
		self.listfiles = None
		self.sizefolder = None

	def folder_list_files(self, folderPath, boolsubfolders=True, masks=None, exact=None):
		"""Build files list."""
		self.listfiles = []
		for folderName, subfolders, filenames in walk(folderPath):
			if subfolders and subfolders:
				for subfolder in subfolders:
					self.folder_list_files(subfolder, boolsubfolders, masks, exact)
			for filename in filenames:
				if masks is None:
					# no mask
					if filename not in self.blacklist:
						self.listfiles.append(path.join(folderName, filename))
				else:
					# same
					if exact:
						if filename.lower() in masks:
							if filename not in self.blacklist:
									self.listfiles.append(path.join(folderName, filename))
					else:
						# mask joker *.
						for xmask in masks:
							if filename[-len(xmask):].lower() in xmask:
								if filename not in self.blacklist:
									self.listfiles.append(path.join(folderName, filename))
			if not boolsubfolders:
				break
		return self.listfiles

	def folder_list_folders(self, folderPath):
		"""Build folders list."""
		self.listfolders = [d for d in listdir(folderPath) if path.isdir(path.join(folderPath, d))]
		return self.listfolders

	def folder_size(self, folderPath, boolsubfolders=True):
		"""Calcul folder size."""
		total_size = path.getsize(folderPath)
		for item in listdir(folderPath):
			itempath = path.join(folderPath, item)
			if path.isfile(itempath):
				total_size += path.getsize(itempath)
			elif path.isdir(itempath) and boolsubfolders:
				total_size += self.folder_size(itempath)
		self.sizefolder = total_size
		return total_size

	def folder_move(self, srcDir, dstDir):
		"""Move files and folders command."""
		# Check if both the are directories
		if path.isdir(srcDir) and path.isdir(dstDir) :
			# Iterate over all the files in source directory
			for filePath in glob(srcDir.replace('[', '[[]') + '\*'): #, recursive=True):
				# Move each file to destination Directory
				move(filePath, dstDir)

	def folder_delete(self, pathFolder):
		"""Delete folder with the content."""
		if path.exists(pathFolder):
			rmtree(pathFolder)

	def folder_delete_old(pathFolder):
		"""Delete folder with the content."""
		deleteFiles = []
		deleteDirs = []
		for root, dirs, files in walk(pathFolder):
			for f in files:
				deleteFiles.append(path.join(root, f))
			for d in dirs:
				deleteDirs.append(path.join(root, d))
		for f in deleteFiles:
			remove(f)
		for d in deleteDirs:
			rmdir(d)
		rmdir(pathFolder)

	def folder_open(self, folderPath):
		"""Open File Explorer."""
		if platform == "win32":
			self.execute_command('explorer', folderPath)
		elif platform == "darwin":
			self.execute_command('open', folderPath)
		elif platform == 'linux':
			self.execute_command('xdg-open', folderPath)

	def file_open(self, filePath):
		"""Open programme association with file."""
		startfile(filePath)

	def file_delete(self, filePath):
		"""File delete."""
		if path.exists(filePath):
			remove(filePath)

	def execute_command(self, prog, *argv):
		"""Execute a program no wait, no link."""
		argums = []
		for arg in argv:
			argums += (arg,)
		p = QProcess()
		p.startDetached(prog, argums)

	def convertUNC(self, folderPath):
		""" convert path UNC to linux."""
		# open file unc from Linux (mount \HOMERSTATION\_lossLess)
		if (platform == "darwin" or platform == 'linux') and path.startswith(r'\\'):
			folderPath = r""+folderPath.replace('\\\\', '/').replace('\\', '/')
		return folderPath


if __name__ == '__main__':
	app = QApplication(argv)
	if len(argv)>1:
		# prod
		myfolder = argv[1]
	else:
		# test envt
		myfolder = r"D:\WorkDev\DBAlbumsTEST\TECHNO\Download"
	# class
	#BuildProcess = FilesProcessing()
	#listfolders = BuildProcess.folder_list_folders(myfolder)
	#variable CLASS BuildProcess.listfolders
	#listfiles = BuildProcess.folder_list_files(myfolder, False)
	#variable CLASS BuildProcess.listfiles
	#listfiles = BuildProcess.folder_list_files(myfolder)
	#foldersize = BuildProcess.folder_size(myfolder)
	#BuildProcess.folder_open(myfolder)
	#BuildProcess.file_open(r'D:\WorkDev\DBAlbumsTEST\TECHNO\Download\Nouveau document RTF.nfo')
	


