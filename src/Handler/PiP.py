# -*- coding: utf-8 -*-from
# by betonme @2015

from time import time
from ServiceReference import ServiceReference
from enigma import eDVBResourceManager, eServiceReference

# Config
from Components.config import config, ConfigSubsection, ConfigYesNo

# Plugin internal
from Plugins.Extensions.InfoBarTunerState.__init__ import _
from Plugins.Extensions.InfoBarTunerState.PluginBase import PluginBase
from Plugins.Extensions.InfoBarTunerState.Helper import getTunerByPlayableService, getNumber, getChannel, getEventData, getTunerName
from Plugins.Extensions.InfoBarTunerState.Logger import log

# Config options
config.infobartunerstate.plugin_pip         = ConfigSubsection()
config.infobartunerstate.plugin_pip.enabled = ConfigYesNo(default = False)


class PiP(PluginBase):
	def __init__(self):
		PluginBase.__init__(self)
		self.tunerstate = None
		self.eservicereference_string = None

	################################################
	# To be implemented by subclass
	def getText(self):
		return "PiP"

	def getType(self):
		from Plugins.Extensions.InfoBarTunerState.InfoBarTunerState import PIP
		return PIP

	def getPixmapNum(self):
		return 7

	def getOptions(self):
		return [(_("Show PiP service(s)"), config.infobartunerstate.plugin_pip.enabled),]

	def appendEvent(self):
		pass

	def removeEvent(self):
		pass

	def checkPiP(self):
		log.debug( "IBTS PiP check" )
		from Screens.InfoBar import InfoBar
		if InfoBar.instance and InfoBar.instance.session and hasattr(InfoBar.instance.session, "pip"):
			if hasattr(InfoBar.instance.session.pip, "currentService") and InfoBar.instance.session.pip.currentService is not None: 
				from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
				if gInfoBarTunerState:
					log.debug( "IBTS PiP check add" )
					return gInfoBarTunerState.addEntry("PiP", self.getPluginName(), self.getType(), self.getText())
		return None

	def onInit(self):
		if config.infobartunerstate.plugin_pip.enabled.value:
			if not self.tunerstate:
				self.tunerstate = self.checkPiP()

	def onEvent(self, mask):
		pass

	def onShow(self, tunerstates):
		if config.infobartunerstate.plugin_pip.enabled.value:
			if not self.tunerstate:
				self.tunerstate = self.checkPiP()
			else:
				from Screens.InfoBar import InfoBar
				if InfoBar.instance and InfoBar.instance.session and hasattr(InfoBar.instance.session, "pip")==False:
					from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
					if gInfoBarTunerState:
						gInfoBarTunerState.finishEntry("PiP")

	def update(self, id, tunerstate):
		if config.infobartunerstate.plugin_pip.enabled.value:
			
			remove = True
			
			if tunerstate:
				
				from Screens.InfoBar import InfoBar
				if InfoBar.instance and InfoBar.instance.session:

					if hasattr(InfoBar.instance.session, "pip"):
					
						pip = InfoBar.instance.session.pip
						
						eservicereference = None
						if hasattr(pip, "currentService"): 
							eservicereference = pip.currentService
						
						if eservicereference:
							log.debug( "IBTS PiP update service" )
							
							remove = False
							changed = False
							
							eservicereference_string = str(eservicereference)
							
							# Avoid recalculations
							if self.eservicereference_string != eservicereference_string:
								tunerstate.number = None
								tunerstate.channel = ""
								tunerstate.reference = ""
								
								tunerstate.tuner, tunerstate.tunertype, tunerstate.tunernumber = "", "", None
								tunerstate.name, tunerstate.begin, tunerstate.end = "", 0, 0
								
								self.eservicereference_string = eservicereference_string
								
							if not tunerstate.number:
								tunerstate.number = getNumber(eservicereference)
								changed = True
							if not tunerstate.channel:
								tunerstate.channel = getChannel(eservicereference)
								changed = True
							if not tunerstate.reference:
								tunerstate.reference = eservicereference_string
								changed = True
							
							iplayableservice = None
							if hasattr(pip, "pipservice"):
								iplayableservice = pip.pipservice
							#if hasattr(pip, "getCurrentServiceReference"):
							#	iplayableservice = pip.getCurrentServiceReference()
							
							log.debug( "IBTS PiP update iPlay", str(iplayableservice) )
							if iplayableservice:
								if not tunerstate.tuner or not tunerstate.tunertype or not tunerstate.tunernumber:
									tunerstate.tuner, tunerstate.tunertype, tunerstate.tunernumber = getTunerByPlayableService(iplayableservice)
									changed = True
								
								if not tunerstate.name or not tunerstate.begin or not tunerstate.end:
									tunerstate.name, tunerstate.begin, tunerstate.end = getEventData(iplayableservice)
									changed = True
								
							if changed:
								from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
								if gInfoBarTunerState:
									gInfoBarTunerState.updateMetrics()
					
			if remove:
				
				from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
				if gInfoBarTunerState:
					gInfoBarTunerState.finishEntry(id)
				return False
				
			else:
				return True
