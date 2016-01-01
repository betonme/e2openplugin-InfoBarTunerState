# -*- coding: utf-8 -*-from
# by betonme @2015

from time import time

# Config
from Components.config import *

# Plugin internal
from Plugins.Extensions.InfoBarTunerState.__init__ import _
from Plugins.Extensions.InfoBarTunerState.PluginBase import PluginBase
from Plugins.Extensions.InfoBarTunerState.Helper import getTuner, getNumber


def getTimerID(timer):
	#return str( timer.name ) + str( timer.repeatedbegindate ) + str( timer.service_ref ) + str( timer.justplay )
	return str( timer )

def getTimer(id):
	from NavigationInstance import instance
	if instance is not None:
		for timer in instance.RecordTimer.timer_list + instance.RecordTimer.processed_timers:
			#print "timerlist:", getTimerID( timer )
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
		from Plugins.Extensions.InfoBarTunerState.InfoBarTunerState import INFO, RECORD, STREAM, FINISHED
		return RECORD

	def appendEvent(self):
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

	def updateEvent(self):
		from NavigationInstance import instance
		if instance is not None:
			for timer in instance.RecordTimer.timer_list:
				if timer.isRunning() and not timer.justplay:
					self.onEvent(timer)

	def onEvent(self, timer):
		if not timer.justplay:
			#print "IBTS Timer Event "+ str(timer.state) + ' ' + str(timer.repeated)
			#TODO
			# w.processRepeated()
			# w.state = TimerEntry.StateWaiting
			if timer.state == timer.StatePrepared:
				print "IBTS Records StatePrepared"
				pass
			
			elif timer.state == timer.StateRunning:
				id = getTimerID( timer )
				print "IBTS Records StateRunning ID " + id
				
				from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
				if gInfoBarTunerState and not gInfoBarTunerState.hasEntry(id):
					service = timer.record_service
					
					#TEST Bug Repeating timer blocking tuner and are not marked as finished
					#timer.timeChanged = self.__OnTimeChanged
					
					name = timer.name
					
					service_ref = timer.service_ref
					
					begin = timer.begin
					end = timer.end
					endless = timer.autoincrease
					
					# Is this really necessary?
					try: timer.Filename
					except: timer.calculateFilename()
					filename = timer.Filename
					
					# Delete references to avoid blocking tuners
					del timer
					
					tuner, tunertype = getTuner(service)
					
					if service_ref:
						number = getNumber(service_ref.ref)
						channel = service_ref.getServiceName().replace('\xc2\x86', '').replace('\xc2\x87', '')
					
					gInfoBarTunerState.addEntry(id, self.getPluginName(), self.getType(), self.getText(), tuner, tunertype, name, number, channel, begin, end, endless, filename)
			
			# Finished repeating timer will report the state StateEnded+1 or StateWaiting
			else:
				id = getTimerID( timer )
				print "IBTS Records StateEnded ID " + id
				
				# Delete references to avoid blocking tuners
				del timer
				
				from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
				gInfoBarTunerState.finishEntry(id)

	def update(self, id, tunerstate):
		
		print "IBTS Records update ID ", id
		
		#TODO Avolid blocking - avoid using getTimer to update the timer times use timer.time_changed if possible
		
		timer = getTimer( id )
		if timer:
			service = None
			if not tunerstate.tuner or not tunerstate.tunertype:
				service = timer.record_service
			
			tunerstate.name = timer.name
			
			service_ref = None
			if not tunerstate.channel or not tunerstate.number:
				service_ref = timer.service_ref
			
			tunerstate.begin = timer.begin
			tunerstate.end = timer.end
			tunerstate.endless = timer.autoincrease
			
			if not tunerstate.filename:
				# Is this really necessary?
				try: timer.Filename
				except: timer.calculateFilename()
				tunerstate.filename = timer.Filename
			
			# Delete references to avoid blocking tuners
			del timer
			
			if service:
				tunerstate.tuner, tunerstate.tunertype = getTuner(timer.record_service)
			
			if service_ref:
				if not tunerstate.number:
					tunerstate.number = getNumber(service_ref.ref)
				if not tunerstate.channel:
					tunerstate.channel = service_ref.getServiceName().replace('\xc2\x86', '').replace('\xc2\x87', '')
			
			return True
		
		else:
			# This can happen, if the time has been changed or if the timer does not exist anymore
			
			self.updateEvent()
			
			return None
