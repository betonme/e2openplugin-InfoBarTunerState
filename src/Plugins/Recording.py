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

def getNextPendingRecordTimers():
	from NavigationInstance import instance
	timer_list = []
	if instance is not None:
		now = time()
		for timer in instance.RecordTimer.timer_list:
			next_act = timer.getNextActivation()
			if timer.justplay or (timer.isRunning() and not timer.repeated) or next_act < now:
				continue
			if timer.begin:
				if not timer.isRunning():
					begin = timer.begin
					end = timer.end
				else:
					begin, end = processRepeated(timer)
				timer_list.append( (timer, begin, end) )
	return sorted( timer_list, key=lambda x: (x[1]) )

# Adapted from TimerEntry
def processRepeated(timer, findRunningEvent = False):
	print "ProcessRepeated"
	
	def addOneDay(timedatestruct):
		oldHour = timedatestruct.tm_hour
		newdate =  (datetime(timedatestruct.tm_year, timedatestruct.tm_mon, timedatestruct.tm_mday, timedatestruct.tm_hour, timedatestruct.tm_min, timedatestruct.tm_sec) + timedelta(days=1)).timetuple()
		if localtime(mktime(newdate)).tm_hour != oldHour:
			return (datetime(timedatestruct.tm_year, timedatestruct.tm_mon, timedatestruct.tm_mday, timedatestruct.tm_hour, timedatestruct.tm_min, timedatestruct.tm_sec) + timedelta(days=2)).timetuple()
		return newdate
	
	begin = timer.begin
	end = timer.end
		
	if (timer.repeated != 0):
		now = int(time()) + 1

		#to avoid problems with daylight saving, we need to calculate with localtime, in struct_time representation
		localrepeatedbegindate = localtime(timer.repeatedbegindate)
		localbegin = localtime(begin)
		localend = localtime(end)
		localnow = localtime(now)

		print "localrepeatedbegindate:", strftime("%c", localrepeatedbegindate)
		print "localbegin:", strftime("%c", localbegin)
		print "localend:", strftime("%c", localend)
		print "localnow:", strftime("%c", localnow)

		day = []
		flags = timer.repeated
		for x in (0, 1, 2, 3, 4, 5, 6):
			if (flags & 1 == 1):
				day.append(0)
				print "Day: " + str(x)
			else:
				day.append(1)
			flags = flags >> 1

		# if day is NOT in the list of repeated days
		# OR if the day IS in the list of the repeated days, check, if event is currently running... then if findRunningEvent is false, go to the next event
		while ((day[localbegin.tm_wday] != 0) or (mktime(localrepeatedbegindate) > mktime(localbegin))  or
			((day[localbegin.tm_wday] == 0) and ((findRunningEvent and localend < localnow) or ((not findRunningEvent) and localbegin < localnow)))):
			localbegin = addOneDay(localbegin)
			localend = addOneDay(localend)
			print "localbegin after addOneDay:", strftime("%c", localbegin)
			print "localend after addOneDay:", strftime("%c", localend)
			
		#we now have a struct_time representation of begin and end in localtime, but we have to calculate back to (gmt) seconds since epoch
		begin = int(mktime(localbegin))
		end = int(mktime(localend))
		if begin == end:
			end += 1
		
		print "ProcessRepeated result"
		print strftime("%c", localtime(begin))
		print strftime("%c", localtime(end))
	
	return begin, end


class Recording(PluginBase):
	def __init__(self):
		PluginBase.__init__(self)
		self.nextids = []

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
				print "IBTS Timer StatePrepared"
				pass
			
			elif timer.state == timer.StateRunning:
				id = getTimerID( timer )
				print "IBTS Timer StateRunning ID " + id
				
				from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
				if gInfoBarTunerState and not gInfoBarTunerState.hasEntry(id):
					tuner, tunertype = getTuner(timer.record_service)
					
					#TEST Bug Repeating timer blocking tuner and are not marked as finished
					#timer.timeChanged = self.__OnTimeChanged
					
					name = timer.name
					service_ref = timer.service_ref
					
					# Is this really necessary?
					try: timer.Filename
					except: timer.calculateFilename()
					filename = timer.Filename
					
					# Delete references to avoid blocking tuners
					del timer
					
					number = service_ref and getNumber(service_ref.ref)
					channel = service_ref and service_ref.getServiceName().replace('\xc2\x86', '').replace('\xc2\x87', '')
					
					gInfoBarTunerState.addEntry(id, self.getPluginName(), self.getType(), self.getText(), tuner, tunertype, name, number, channel, filename)
			
			# Finished repeating timer will report the state StateEnded+1 or StateWaiting
			else:
				id = getTimerID( timer )
				print "IBTS Timer StateEnded ID " + id
				
				# The id of a finished repeated timer can be changed
				#RecordTimerEntry(name=How I Met Your Mother, begin=Wed Jul 18 11:37:00 2012, serviceref=1:0:19:EF75:3F9:1:C00000:0:0:0:, justplay=False)
				#RecordTimerEntry(name=How I Met Your Mother, begin=Thu Jul 19 11:37:00 2012, serviceref=1:0:19:EF75:3F9:1:C00000:0:0:0:, justplay=False)
				#print "IBTS Timer finished ID", id, id in self.entries
				
				#begin = timer.begin
				#end = timer.end
				#endless = timer.autoincrease
				
				# Delete references to avoid blocking tuners
				del timer
				
				from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
				gInfoBarTunerState.finishEntry(id)

	def update(self, id, begin, end, endless):
		
		print "IBTS Timer update ID ", id
		
		#TODO Avolid blocking - avoid using getTimer to update the timer times use timer.time_changed if possible
		timer = getTimer( id )
		#print id, timer
		if timer:
			#tuner, tunertype = getTuner(timer.record_service)
			
			#name = timer.name
			#service_ref = timer.service_ref
			
			# Is this really necessary?
			#try: timer.Filename
			#except: timer.calculateFilename()
			#filename = timer.Filename
			
			del timer
			
			#number = service_ref and getNumber(service_ref.ref)
			#channel = service_ref and service_ref.getServiceName().replace('\xc2\x86', '').replace('\xc2\x87', '')
			#channel = channel
			
			from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
			gInfoBarTunerState.updateEntry(id, self.getType(), begin, end, endless)
		
		else:
			# This can happen, if the time has been changed or if the timer does not exist anymore
			from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
			gInfoBarTunerState.finishEntry(id)
			
			self.updateEvent()

	def upcomingEvents(self):
		
		from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
		from Plugins.Extensions.InfoBarTunerState.InfoBarTunerState import INFO
		
		number_pending_records = int( config.infobartunerstate.number_pending_records.value )
		print "IBTS upcomingEvents", number_pending_records
		
		toremove = self.nextids[:]
		
		if number_pending_records:
			pending_seconds = int( config.infobartunerstate.pending_hours.value ) * 3600
			pending_limit = (time() + pending_seconds) if pending_seconds else 0
			
			timer_list = getNextPendingRecordTimers()[:number_pending_records]
			
			if timer_list:
				timer_list.reverse()
				
				for i, (timer, begin, end) in enumerate(timer_list):
					id = 'next'+str(i)
					if timer:
						name = timer.name
						service_ref = timer.service_ref
						
						# Is this really necessary?
						try: timer.Filename
						except: timer.calculateFilename()
						
						try: filename = timer.Filename
						except: filename = timer.name
						
						endless = timer.autoincrease
						
						# Delete references to avoid blocking tuners
						del timer
						
						if pending_limit and pending_limit < begin:
							# Skip timer
							continue
						
						number = service_ref and getNumber(service_ref.ref)
						channel = service_ref and service_ref.getServiceName()
						
						# Only add timer if not recording
						if gInfoBarTunerState and gInfoBarTunerState.hasEntry(id):
							if id in toremove:
								toremove.remove(id)
							gInfoBarTunerState.updateName(id, name)
							gInfoBarTunerState.updateNumberChannel(id, number, channel)
							gInfoBarTunerState.updateFilename(id, filename)
						else:
							gInfoBarTunerState.addEntry(id, self.getPluginName(), INFO, self.getText(), '', '', name, number, channel, filename)
						gInfoBarTunerState.updateEntry(id, INFO, begin, end, endless)
						self.nextids.append(id)
			
			# Close all not touched next timers
			if toremove:
				for id in toremove:
					if id in self.nextids:
						self.nextids.remove(id)
					gInfoBarTunerState.removeEntry(id)
