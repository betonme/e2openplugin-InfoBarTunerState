# -*- coding: utf-8 -*-from
# by betonme @2015

from time import time

# Config
from Components.config import *

from enigma import eEPGCache

# Plugin internal
from Plugins.Extensions.InfoBarTunerState.__init__ import _
from Plugins.Extensions.InfoBarTunerState.PluginBase import PluginBase
from Plugins.Extensions.InfoBarTunerState.Helper import getTunerByPlayableService, getNumber, getChannel
from Plugins.Extensions.InfoBarTunerState.Logger import log


# Config options
event_choices = [	
					( "start",		_("Start record")),
					( "end",		_("End record")),
					( "startend",	_("Start / End record"))
				]
config.infobartunerstate.plugin_records             = ConfigSubsection()
config.infobartunerstate.plugin_records.enabled     = ConfigYesNo(default = True)
config.infobartunerstate.plugin_records.show_events = ConfigSelection(default = "startend", choices = event_choices)


def getTimerID(timer):
	#return str( timer.name ) + str( timer.repeatedbegindate ) + str( timer.service_ref ) + str( timer.justplay )
	#return str( timer )
	#return '<%s instance at %x name=%s %s>' % (self.__class__.__name__, id(self), self.name, hasattr(self,"Filename") and self.Filename or "")
	return 'record %x %s %x' % ( id(timer), timer.name, int(timer.eit or 0) )

def getTimer(id):
	from NavigationInstance import instance
	if instance is not None:
		for timer in instance.RecordTimer.timer_list:
			#log.debug( "timerlist:", getTimerID( timer ) )
			if getTimerID( timer ) == id:
				return timer
	return None

def getProcessedTimer(id):
	from NavigationInstance import instance
	if instance is not None:
		for timer in instance.RecordTimer.processed_timers:
			#log.debug( "timerlist:", getTimerID( timer ) )
			if getTimerID( timer ) == id:
				return timer
	return None

class Records(PluginBase):
	def __init__(self):
		PluginBase.__init__(self)

	################################################
	# To be implemented by subclass
	def getText(self):
		return "Record"

	def getType(self):
		from Plugins.Extensions.InfoBarTunerState.InfoBarTunerState import RECORD
		return RECORD

	def getPixmapNum(self):
		return 0

	def getOptions(self):
		return [(_("Show record(s)"), config.infobartunerstate.plugin_records.enabled),]

	def appendEvent(self):
		if config.infobartunerstate.plugin_records.enabled.value:
			from NavigationInstance import instance
			if instance is not None:
				# Recording Events
				# If we append our function, we will never see the timer state StateEnded for repeating timer
				if self.onEvent not in instance.RecordTimer.on_state_change:
					instance.RecordTimer.on_state_change.insert(0, self.onEvent)

	def removeEvent(self):
		from NavigationInstance import instance
		if instance is not None:
			# Recording Events
			# If we append our function, we will never see the timer state StateEnded for repeating timer
			if self.onEvent in instance.RecordTimer.on_state_change:
				instance.RecordTimer.on_state_change.remove(self.onEvent)

	def onInit(self):
		if config.infobartunerstate.plugin_records.enabled.value:
			from NavigationInstance import instance
			if instance is not None:
				for timer in instance.RecordTimer.timer_list:
					if timer.isRunning() and not timer.justplay:
						self.onEvent(timer)

	def onEvent(self, timer):
		if timer.justplay:
			return
		
		elif timer.state == timer.StatePrepared:
			log.debug( "IBTS Records StatePrepared" )
			return
		
		elif timer.state == timer.StateRunning:
			id = getTimerID( timer )
			log.debug( "IBTS Records StateRunning ID " + id )
			
			from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
			if gInfoBarTunerState and not gInfoBarTunerState.hasEntry(id):
				
				#TEST Bug Repeating timer blocking tuner and are not marked as finished
				#timer.timeChanged = self.__OnTimeChanged
				
				name = timer.name
				
				begin = timer.begin
				end = timer.end
				endless = timer.autoincrease
				
				# Is this really necessary?
				try: timer.Filename
				except: timer.calculateFilename()
				
				try: filename = timer.Filename
				except: filename = timer.name
				
				irecordservice = timer.record_service
				servicereference = timer.service_ref
				
				# Delete references to avoid blocking tuners
				del timer
				
				tuner, tunertype, tunernumber = getTunerByPlayableService(irecordservice)
				
				number = getNumber(servicereference.ref)
				channel = getChannel(servicereference.ref)
				reference = str(servicereference.ref)
					
				gInfoBarTunerState.addEntry(id, self.getPluginName(), self.getType(), self.getText(), tuner, tunertype, tunernumber, name, number, channel, reference, begin, end, endless, filename)
				if config.infobartunerstate.plugin_records.show_events.value == "start" or config.infobartunerstate.plugin_records.show_events.value == "startend":
					gInfoBarTunerState.onEvent()
		
		# Finished repeating timer will report the state StateEnded+1 or StateWaiting
		else:
			id = getTimerID( timer )
			log.debug( "IBTS Records StateEnded ID " + id )
			
			# Delete references to avoid blocking tuners
			del timer
			
			from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
			if gInfoBarTunerState:
				gInfoBarTunerState.finishEntry(id)
				if config.infobartunerstate.plugin_records.show_events.value == "startend" or config.infobartunerstate.plugin_records.show_events.value == "end":
					gInfoBarTunerState.onEvent()

	def update(self, id, tunerstate):
		
		#TODO Avolid blocking - avoid using getTimer to update the timer times use timer.time_changed if possible
		
		timer = getTimer( id )
		if timer:
			tunerstate.name = timer.name
			
			tunerstate.begin = timer.begin
			tunerstate.end = timer.end
			
			if hasattr(timer, 'vpsplugin_enabled') and timer.vpsplugin_enabled:
			#and hasattr(timer, 'vpsplugin_overwrite') and timer.vpsplugin_overwrite:
				tunerstate.endless = False
				epgcache = eEPGCache.getInstance()
				
				if timer.eit:
					log.debug( "IBTS Records event by lookupEventId" )
					event = epgcache.lookupEventId(timer.service_ref.ref, timer.eit)
				
				if not event:
					log.debug( "IBTS Records event by lookupEventTime" )
					event = epgcache.lookupEventTime( timer.service_ref.ref, timer.begin + 5 );
				
				if event:
					log.debug( "IBTS Records event" )
					begin = event.getBeginTime() or 0
					duration = event.getDuration() or 0
					tunerstate.end  = begin + duration
					
					if not tunerstate.end:
						log.debug( "IBTS Records no end" )
						tunerstate.endless = True
				else:
					tunerstate.endless = timer.autoincrease
			else:
				tunerstate.endless = timer.autoincrease
			
			irecordservice = timer.record_service
			servicereference = timer.service_ref
			
			# Delete references to avoid blocking tuners
			del timer
			
			if not tunerstate.tuner or not tunerstate.tunertype or not tunerstate.tunernumber:
				tunerstate.tuner, tunerstate.tunertype, tunerstate.tunernumber = getTunerByPlayableService(irecordservice)
			
			if not tunerstate.number:
				tunerstate.number = getNumber(servicereference.ref)
			if not tunerstate.channel:
				tunerstate.channel = getChannel(servicereference.ref)
			if not tunerstate.reference:
				tunerstate.reference = str(servicereference.ref)
			
			return True
		
		else:
			# This can happen, if the time has been changed or if the timer does not exist anymore
			
			self.onInit()
			
			return False
