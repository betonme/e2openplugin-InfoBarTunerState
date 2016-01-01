# -*- coding: utf-8 -*-from
# by betonme @2015

from time import time
from ServiceReference import ServiceReference

# Config
from Components.config import *

# Plugin internal
from Plugins.Extensions.InfoBarTunerState.__init__ import _
from Plugins.Extensions.InfoBarTunerState.PluginBase import PluginBase
from Plugins.Extensions.InfoBarTunerState.Helper import getTunerByPlayableService, getNumber, getChannel, getEventData


class Live(PluginBase):
	def __init__(self):
		PluginBase.__init__(self)

	################################################
	# To be implemented by subclass
	def getText(self):
		return "Live"

	def getType(self):
		from Plugins.Extensions.InfoBarTunerState.InfoBarTunerState import LIVE
		return LIVE

	def onInit(self):
		from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
		if gInfoBarTunerState:
			
			gInfoBarTunerState.addEntry("Live", self.getPluginName(), self.getType(), self.getText())

	def onShow(self, tunerstates):
		for id, tunerstate in tunerstates.items():
			if tunerstate.plugin == "Live":
				break
		else:
			self.onInit()

	def update(self, id, tunerstate):
		
		print "IBTS Live update ID", self.getType()
		
		from NavigationInstance import instance
		if instance:
			iplayableservice = instance.getCurrentService()
			
			tunerstate.tuner, tunerstate.tunertype = getTunerByPlayableService(iplayableservice)
			tunerstate.name, tunerstate.begin, tunerstate.end = getEventData(iplayableservice)
		
			eservicereference = instance.getCurrentlyPlayingServiceReference()
			tunerstate.number = getNumber(eservicereference)
			tunerstate.channel = getChannel(eservicereference)
		
		return True

