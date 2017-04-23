# -*- coding: utf-8 -*-
# by betonme @2012

# Plugin internal
from Plugins.Extensions.PushService.Logger import log

# Internal

class PluginBase(object):
	def __init__(self):
		pass
	
	################################################
	# Base classmethod functions
	@classmethod
	def getClass(cls):
		# Return the Class
		return cls.__name__

	################################################
	# Base functions
	def getPluginName(self):
		# Return the Class Name
		return self.__class__.__name__

	def getValue(self, key):
		if key in self.options:
			return self.options[key][0].value
		else:
			return None

	def setValue(self, key, value):
		self.options[key][0].value = value

	def getOption(self, key):
		if key in self.options:
			return self.options[key]
		else:
			return None

	def setOption(self, key, option, description):
		self.options[key] = ( option, description )

	def setOptions(self, options):
		# Parse a list of key-value string tuples
		# [ (key, value) , ]
		# If something is missing, the last/default value is used
		for key, value in options:
			try:
				default = self.getValue(key)
				if type(default) is str:
					self.setValue(key, value)
				elif type(default) is bool:
					self.setValue(key, eval(value))
				elif type(default) is int:
					self.setValue(key, int(value))
			except:
				log.debug( ("Skipping config option:") + str(key) + " " + str(value) )
				continue

	################################################
	# To be implemented by subclass
	def getText(self):
		# Short text to be displayed in GUI
		pass

	def getType(self):
		from Plugins.Extensions.InfoBarTunerState.InfoBarTunerState import INFO
		# Pixmap number to be displayed as icon
		return INFO

	def getPixmapNum(self):
		from Plugins.Extensions.InfoBarTunerState.InfoBarTunerState import INFO
		# Pixmap number to be displayed as icon
		return INFO

	def appendEvent(self):
		pass

	def removeEvent(self):
		pass

	def onInit(self):
		pass

	def onEvent(self):
		pass

	def onShow(self, tunerstates):
		pass

	def update(self, id, tunerstate):
		# Return true if entry is still valid
		return True
