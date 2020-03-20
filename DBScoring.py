#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QStyle, QPushButton


class ScoreWidget(QWidget):
	"""Widget Thunbnails for main & artworks viewers."""
	# signal
	signalscorenew = pyqtSignal(int)		# save new score

	def __init__(self, parent, scoredict, scoreinit = None):
		super(ScoreWidget, self).__init__(parent)
		self.PATH_PROG = path.dirname(path.abspath(__file__))
		self.RESS_ICOS = path.join(self.PATH_PROG, 'ICO')

		self.parent = parent
		self.scoreinit = scoreinit
		self.scorecure = scoreinit
		self.scoredict = scoredict
		self.nbbutton = 0
		
		self.setMaximumSize(QSize(100 , 30))
		self.layout = QHBoxLayout()
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(0)
		
		self.layoutsave = QGridLayout()
		self.btnsav = QPushButton(self)
		self.btnsav.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
		self.btnsav.setStyleSheet("border: none;")
		self.btnsav.setVisible(False)
		self.layoutscore = QGridLayout()
		self.layoutscore.setContentsMargins(0, 0, 0, 0)
		self.layoutscore.setSpacing(0)
		self.layoutsave.addWidget(self.btnsav)

		# Create buttons
		for key, value in scoredict.items():
			if key != 0:
				button = QPushButton(self)
				button.clicked.connect(lambda event, n=key: self.scorechange(n))
				button.setStyleSheet("border: none;")
				button.setToolTip(value)
				button.setIconSize(QSize(30, 30))
				button.setIcon(QIcon(path.join(self.RESS_ICOS, 'staroff.png')))
				self.layoutscore.addWidget(button, 0, int(key))
				self.nbbutton += 1
		
		self.layout.addLayout(self.layoutsave)
		self.layout.addLayout(self.layoutscore)
		self.setLayout(self.layout)
		self.btnsav.clicked.connect(self.scoresave)
	
	def scorereinit(self, score):
		self.scoreinit = score
		self.scorechange(score, True)

	def scorechange(self, newscore, init=False):
		"""Modify button funttion score."""
		self.btnsav.setToolTip('Save new score ' + str(newscore) + ' (' + self.scoredict[newscore] + ')')
		if newscore == 1 and self.scorecure == 1 and not init:
			newscore = 0
		if newscore != self.scorecure:
			for colbut in range(0, self.nbbutton):
				if self.layoutscore.itemAtPosition(0, colbut) != 0:
					layoutitem = self.layoutscore.takeAt(0)
					button = layoutitem.widget()
					self.layoutscore.removeWidget(button)
					if newscore > colbut:
						button.setIcon(QIcon(path.join(self.RESS_ICOS, 'staron.png')))
					else:
						button.setIcon(QIcon(path.join(self.RESS_ICOS, 'staroff.png')))
					self.layoutscore.addWidget(button, 0, colbut)
			if self.scoreinit is not None:
				self.btnsav.setVisible(True)
			self.scorecure = newscore
		if self.scoreinit == self.scorecure:
			self.btnsav.setVisible(False)

	def scoresave(self):
		"""Modify button funttion score."""
		self.signalscorenew.emit(self.scorecure)
		self.btnsav.setVisible(False)
