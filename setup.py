#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cx_Freeze import setup, Executable

includefiles = ['DBAlbums-cd-blank.png','DBAlbums-cd-blank3d.png','DBAlbums-cd-blank-mini.jpg','DBAlbums-cd-blank-mini3d.jpg','DBAlbums-icone.ico','DBAlbums-icone.png']

# On appelle la fonction setup
setup(
	name = "DBAlbums",
	version = "1.34",
	author='doubsman',
	description = "DBAlbums doubsman 2017",
	options = {'build_exe': {'include_files':includefiles}}, 
	executables = [Executable("DBAlbums.pyw")],
)