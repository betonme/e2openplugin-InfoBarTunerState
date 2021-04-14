# -*- coding: utf-8 -*-from
# by betonme @2015

from time import strftime, time, localtime, mktime
from datetime import datetime, timedelta

# Config
from Components.config import config, ConfigSubsection, ConfigYesNo, ConfigSelectionNumber

# Plugin internal
from Plugins.Extensions.InfoBarTunerState.__init__ import _
from Plugins.Extensions.InfoBarTunerState.PluginBase import PluginBase
from Plugins.Extensions.InfoBarTunerState.Helper import getTunerByPlayableService, getNumber, getChannel
from Plugins.Extensions.InfoBarTunerState.Logger import log


# Config options
config.infobartunerstate.plugin_timers                           = ConfigSubsection()
config.infobartunerstate.plugin_timers.enabled                   = ConfigYesNo(default=True)
config.infobartunerstate.plugin_timers.number_pending_timers     = ConfigSelectionNumber(0, 10, 1, default=1)
config.infobartunerstate.plugin_timers.pending_hours             = ConfigSelectionNumber(0, 1000, 1, default=0)
config.infobartunerstate.plugin_timers.show_energy_timers        = ConfigYesNo(default=True)


def getTimer(id):
	from NavigationInstance import instance
	if instance is not None:
		for timer in instance.RecordTimer.timer_list + instance.RecordTimer.processed_timers:
			#log.debug( "IBTS timerlist:", getTimerID( timer ) )
			if getTimerID(timer) == id:
				return timer
		#else:
		#	log.debug( "IBTS getTimer for else" )
	return None

def getTimerID(timer):
	return 'timer %x %s %x' % (id(timer), timer.name, int(timer.eit or 0))

def getNextPendingRecordTimers(pending_limit):
	from NavigationInstance import instance
	timer_list = []
	if instance is not None:
		now = time()
		for timer in instance.RecordTimer.timer_list:
			next_act = timer.getNextActivation()
			if timer.justplay:
				continue
			if timer.isRunning():
				continue
			if next_act < now:
				continue
			if pending_limit and pending_limit < timer.begin:
				continue
			if timer.begin:
				if not timer.isRunning():
					begin = timer.begin
					end = timer.end
				else:
					begin, end = processRepeated(timer)
				timer_list.append(timer)
	return sorted(timer_list, key=lambda x: (x.begin))

# Adapted from TimerEntry
def addOneDay(timedatestruct):
	oldHour = timedatestruct.tm_hour
	newdate =  (datetime(timedatestruct.tm_year, timedatestruct.tm_mon, timedatestruct.tm_mday, timedatestruct.tm_hour, timedatestruct.tm_min, timedatestruct.tm_sec) + timedelta(days=1)).timetuple()
	if localtime(mktime(newdate)).tm_hour != oldHour:
		return (datetime(timedatestruct.tm_year, timedatestruct.tm_mon, timedatestruct.tm_mday, timedatestruct.tm_hour, timedatestruct.tm_min, timedatestruct.tm_sec) + timedelta(days=2)).timetuple()
	return newdate

def processRepeated(timer, findRunningEvent=False):
	begin = timer.begin
	end = timer.end
		
	if (timer.repeated != 0):
		now = int(time()) + 1

		#to avoid problems with daylight saving, we need to calculate with localtime, in struct_time representation
		localrepeatedbegindate = localtime(timer.repeatedbegindate)
		localbegin = localtime(begin)
		localend = localtime(end)
		localnow = localtime(now)

		day = []
		flags = timer.repeated
		for x in (0, 1, 2, 3, 4, 5, 6):
			if (flags & 1 == 1):
				day.append(0)
				#log.debug( "Day: " + str(x) )
			else:
				day.append(1)
			flags = flags >> 1

		# if day is NOT in the list of repeated days
		# OR if the day IS in the list of the repeated days, check, if event is currently running... then if findRunningEvent is false, go to the next event
		while ((day[localbegin.tm_wday] != 0) or (mktime(localrepeatedbegindate) > mktime(localbegin))  or
			((day[localbegin.tm_wday] == 0) and ((findRunningEvent and localend < localnow) or ((not findRunningEvent) and localbegin < localnow)))):
			localbegin = addOneDay(localbegin)
			localend = addOneDay(localend)
			
		#we now have a struct_time representation of begin and end in localtime, but we have to calculate back to (gmt) seconds since epoch
		begin = int(mktime(localbegin))
		end = int(mktime(localend))
		if begin == end:
			end += 1
	
	return begin, end


class Timers(PluginBase):
	def __init__(self):
		PluginBase.__init__(self)
		self.nextids = []

	################################################
	# To be implemented by subclass
	def getText(self):
		return "Timer"

	def getType(self):
		from Plugins.Extensions.InfoBarTunerState.InfoBarTunerState import TIMER
		return TIMER

	def getPixmapNum(self):
		return 6

	def getOnChanged(self):
		return [config.infobartunerstate.plugin_timers.enabled]

	def getOptions(self):
		options = []
		options.append((_("Show pending timer(s)"), config.infobartunerstate.plugin_timers.enabled))
		
		if config.infobartunerstate.plugin_timers.enabled.value:
			options.append((_("   Number of pending timer(s)"),                 config.infobartunerstate.plugin_timers.number_pending_timers))
			options.append((_("   Show pending records only within x hour(s)"), config.infobartunerstate.plugin_timers.pending_hours))
			options.append((_("   Show Energy shedule timers"),                 config.infobartunerstate.plugin_timers.show_energy_timers))
		
		return options

	def onShow(self, tunerstates):
		if config.infobartunerstate.plugin_timers.enabled.value:
			number_pending_timers = int(config.infobartunerstate.plugin_timers.number_pending_timers.value)
			#log.debug( "IBTS number_pending_timers", number_pending_timers )
			
			toremove = self.nextids[:]
			
			if number_pending_timers:
				pending_seconds = int(config.infobartunerstate.plugin_timers.pending_hours.value) * 3600
				pending_limit = (time() + pending_seconds) if pending_seconds else 0
				#log.debug( "IBTS pending_limit", pending_limit )
				timer_end = 0
				timer_list = getNextPendingRecordTimers(pending_limit)[:]
				#pprint.pprint(timer_list)
				
				if timer_list:
					
					#timer_list.reverse()
					
					for i, timer in enumerate(timer_list):
						if i>=number_pending_timers+timer_end:
							break
						if timer:
							
							id = getTimerID(timer)
							#log.debug( "IBTS toadd", id )
							
							if id in toremove:
								toremove.remove(id)
							
							# Only add timer if not recording
							from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
							if gInfoBarTunerState:
								if gInfoBarTunerState.hasEntry(id):
									
									# Delete references to avoid blocking tuners
									del timer
									
								else:
								
									name = timer.name
									servicereference = timer.service_ref
									
									# if ((name=="Ausschalten")or(name=="Einschalten")or(name=="Standby"))and(config.infobartunerstate.plugin_timers.show_energy_timers.value==False):
									# isset zapbeforerecord="0" justremind="0" wakeup_t="0" shutdown_t="0" notify_t="0" standby_t="1"
									
									if (str(servicereference)[0]=="-")and(config.infobartunerstate.plugin_timers.show_energy_timers.value==False):
										timer_end+=1
										
									else:
										# Is this really necessary?
										try:
											timer.Filename
										except:
											timer.calculateFilename()
										
										try:
											filename = timer.Filename
										except:
											filename = timer.name
										
										begin = timer.begin
										end = timer.end
										endless = timer.autoincrease
										
										# Delete references to avoid blocking tuners
										del timer
										
										number = getNumber(servicereference.ref)
										channel = getChannel(servicereference.ref)
										reference = str(servicereference)
										
										self.nextids.append(id)
										gInfoBarTunerState.addEntry(id, self.getPluginName(), self.getType(), self.getText(), "", "", None, name, number, channel, reference, begin, end, endless, filename)

				# Close all not touched next timers
				if toremove:
					from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
					if gInfoBarTunerState:
						log.debug("IBTS toremove")
						#pprint.pprint(toremove)
						for id in toremove:
							log.debug("IBTS timers toremove", id)
							if id in self.nextids:
								self.nextids.remove(id)
							gInfoBarTunerState.removeEntry(id)

	def update(self, id, tunerstate):
		
		log.debug("IBTS Timers update ID", id)
		if id in self.nextids:
			
			timer = getTimer(id)
			if timer:
				
				tunerstate.name = timer.name
				
				tunerstate.begin = timer.begin
				tunerstate.end = timer.end
				tunerstate.endless = timer.autoincrease
				
				servicereference = timer.service_ref
				
				del timer
				
				if not tunerstate.number:
					tunerstate.number = getNumber(servicereference.ref)
				if not tunerstate.channel:
					tunerstate.channel = getChannel(servicereference.ref)
				if not tunerstate.reference:
					tunerstate.reference = str(servicereference.ref)
				
				return True
			else:
				log.debug("IBTS timers update FINISHED no timer", id)
				return None
		else:
			log.debug("IBTS timers update FINISHED not in ids", id)
			return None
