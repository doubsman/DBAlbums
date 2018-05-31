#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Python v3
from PyQt5.QtGui import QIcon
from PyQt5 import QtDesigner

# https://pyqt.developpez.com/tutoriels/widgets-qtdesigner/
# ===== à adapter selon le widget! ==========================================
# nom (str) du fichier du widget sans extension
FICHIERWIDGET = "QLabeldnd"
# nom (str) de la classe du widget importé
NOMCLASSEWIDGET = "QLabeldnd"
# nom (str) de l'instance crée dans Designer
NOMWIDGET = "QLabeldnd"
# groupe (str) de widgets pour Designer
GROUPEWIDGET = "Mes widgets perso"
# texte (str) pour le toolTip dans Designer
TEXTETOOLTIP = "QLabel with drag & Drop picture"
# texte (str) pour le whatsThis dans Designer
TEXTEWHATSTHIS = "QLabel with drag & Drop picture"
# icone (rien ou QPixmap) pour présenter le widget dans Designer
ICONEWIDGET = QIcon()  # sans pixmap, l'icone par défaut est celui de Qt
# ===========================================================================
 
# importation de la classe du widget
modulewidget = __import__(FICHIERWIDGET, fromlist=[NOMCLASSEWIDGET])
CLASSEWIDGET = getattr(modulewidget, NOMCLASSEWIDGET)
 
#############################################################################
class GeoLocationPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):
    """classe pour renseigner Designer sur le widget
       nom de classe à renommer selon le widget
    """
  #========================================================================
    def __init__(self, parent=None):
        super(GeoLocationPlugin, self).__init__(parent)
        self.initialized = False
    #========================================================================
    def initialize(self, core):
        if self.initialized:
            return
        self.initialized = True
     #========================================================================
    def isInitialized(self):
        return self.initialized
    #========================================================================
    def createWidget(self, parent):
        """retourne une instance de la classe qui définit le nouveau widget
        """
        return CLASSEWIDGET(parent)
    #========================================================================
    def name(self):
        """définit le nom du widget dans QtDesigner
        """
        return NOMCLASSEWIDGET
     #========================================================================
    def group(self):
        """définit le nom du groupe de widgets dans QtDesigner
        """
        return GROUPEWIDGET
    #========================================================================
    def icon(self):
        """retourne l'icone qui represente le widget dans Designer
           => un QIcon() ou un QIcon(imagepixmap)
        """
        return ICONEWIDGET
    #========================================================================
    def toolTip(self):
        """retourne une courte description du widget comme tooltip
        """
        return TEXTETOOLTIP
     #========================================================================
    def whatsThis(self):
        """retourne une courte description du widget pour le "What's this?"
        """
        return TEXTEWHATSTHIS
     #========================================================================
    def isContainer(self):
        """dit si le nouveau widget est un conteneur ou pas
        """
        return False
     #========================================================================
    def domXml(self):
        """donne des propriétés du widget pour utilisation dans Designer
        """
        return ('<widget class="{}" name="{}">\n' \
               ' <property name="toolTip" >\n' \
               '  <string>{}</string>\n' \
               ' </property>\n' \
               ' <property name="whatsThis" >\n' \
               '  <string>{}</string>\n' \
               ' </property>\n' \
               '</widget>\n'\
               ).format(NOMCLASSEWIDGET, NOMWIDGET, TEXTETOOLTIP, TEXTEWHATSTHIS)
     #========================================================================
    def includeFile(self):
        """retourne le nom du fichier (str sans extension) du widget
        """
        return FICHIERWIDGET
