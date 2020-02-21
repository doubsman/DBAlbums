#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from PyQt5.QtCore import pyqtSignal, QSize, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QStyle, QPushButton, QDesktopWidget

class ThemeColors(QObject):
	def __init__(self, nametheme):
		"""init theme list"""
		super(ThemeColors, self).__init__()
		self.themes = ['blue', 'green', 'brown', 'grey', 'pink']
		self.curthe = self.themes.index(nametheme)
		self.selectTheme(nametheme)
	
	def selectTheme(self, nametheme):
		"""Select theme "http://www.rapidtables.com/web/color/html-color-codes.htm"."""
		if nametheme == self.themes[0]:
			self.listcolors = ['lightsteelblue', 'lavender', 'lightgray', 'silver', 'dodgerblue']
		elif nametheme == self.themes[1]:
			self.listcolors = ['darkseagreen', 'honeydew', 'lightgray', 'silver', 'mediumseagreen']
		elif nametheme == self.themes[2]:
			self.listcolors = ['tan', 'papayawhip', 'lightgray', 'silver', 'peru']
		elif nametheme == self.themes[3]:
			self.listcolors = ['darkgray', 'azure', 'lightgray', 'silver', 'dimgray']
		elif nametheme == self.themes[4]:
			self.listcolors = ['rosybrown', 'lavenderblush', 'lightgray', 'silver', 'sienna']
	
	def nextTheme(self):
		"""Next color theme."""
		self.curthe += 1 
		self.curthe = self.curthe % len(self.themes)
		nametheme = self.themes[self.curthe]
		self.selectTheme(nametheme)


class GuiThemeWidget(QWidget):
	"""Widget Thunbnails for main & artworks viewers."""

	def __init__(self, parent, nametheme, center = True):
		super(GuiThemeWidget, self).__init__(parent)
		self.parent = parent
		
		# center widget
		if center:
			qtrectangle = self.frameGeometry()
			centerPoint = QDesktopWidget().availableGeometry().center()
			qtrectangle.moveCenter(centerPoint)
			self.move(qtrectangle.topLeft())
	


