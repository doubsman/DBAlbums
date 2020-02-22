#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QDesktopWidget


class GuiThemeWidget(QWidget):
	"""Widget Thunbnails for main & artworks viewers."""

	def __init__(self, center = True):
		super(GuiThemeWidget, self).__init__()
		self.jsondatathemes = None	# data theme json file
		self.themes = []			# list themes
		self.listcolors = []		# list colors
		self.curthe = 0				# current theme

		# center widget
	def centerWidget(self, widget):
		qtrectangle = widget.frameGeometry()
		centerPoint = QDesktopWidget().availableGeometry().center()
		qtrectangle.moveCenter(centerPoint)
		widget.move(qtrectangle.topLeft())
	
	def defineThemes(self, nametheme, jsondatathemes):
		self.jsondatathemes = jsondatathemes
		self.themes = []
		for key, value in self.jsondatathemes.items():
			self.themes.append(key)
			#print(key, value)
		self.curthe = self.themes.index(nametheme)
		self.selectTheme(nametheme)

	def selectTheme(self, nametheme):
		"""Select theme "http://www.rapidtables.com/web/color/html-color-codes.htm"."""
		self.listcolors = self.jsondatathemes[nametheme]
	
	def nextTheme(self):
		"""Next color theme."""
		self.curthe += 1 
		self.curthe = self.curthe % len(self.themes)
		nametheme = self.themes[self.curthe]
		self.selectTheme(nametheme)
