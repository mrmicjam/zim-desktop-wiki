# -*- coding: utf-8 -*-
#
# plantumleditor.py
# (based on ditaaeditor.py)
#
# This is a plugin for Zim, to include PlantUML diagrams
#
# Author: Rolf Kleef <rolf@drostan.org>
# Original Author: Yao-Po Wang <blue119@gmail.com>
# Date: 2014-08-04
# Copyright (c) 2012, 2014, released under the GNU GPL v2 or higher
#
#
from zim.plugins import PluginClass
from zim.plugins.base.imagegenerator import ImageGeneratorClass, BackwardImageGeneratorObjectType
from zim.fs import File, TmpFile
from zim.config import data_file
from zim.applications import Application, ApplicationError


# TODO put these commands in preferences
dotcmd = ('plantuml')


class InsertPlantumlPlugin(PluginClass):

	plugin_info = {
		'name': _('Insert PlantUML'), # T: plugin name
		'description': _('''\
This plugin provides a diagram editor for zim based on PlantUML.
'''), # T: plugin description
        'help': 'Plugins:PlantUML Editor',
		'author': 'Adaptation by Rolf Kleef of Ditaa plugin by Yao-Po Wang',
	}

	@classmethod
	def check_dependencies(klass):
		has_dotcmd = Application(dotcmd).tryexec()
		return has_dotcmd, [("Plantuml", has_dotcmd, True)]


class BackwardDitaaImageObjectType(BackwardImageGeneratorObjectType):

	name = 'image+plantuml'
	label = _('PlantUML graph') # T: menu item
	syntax = None
	scriptname = 'plantuml.pu'
	imagefile_extension = '.png'



class PlantumlGenerator(ImageGeneratorClass):
	def __init__(self, plugin, notebook, page):
		ImageGeneratorClass.__init__(self, plugin, notebook, page)
		self.dotfile = TmpFile('plantuml.pu')
		self.dotfile.touch()
		self.pngfile = File(self.dotfile.path[:-3] + '.png') # len('.pu') == 3


	def generate_image(self, text):
		# Write to tmp file
		self.dotfile.write(text)

		# Call GraphViz
		try:
			dot = Application(dotcmd)
			dot.run((self.dotfile, ))
		except ApplicationError as e:
			print(e)
			return None, None # Sorry, no log
		else:
			return self.pngfile, None

	def cleanup(self):
		self.dotfile.remove()
		self.pngfile.remove()
