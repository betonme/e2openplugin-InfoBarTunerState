# -*- coding: utf-8 -*-from
# by betonme @2015

from time import time

# Config
from Components.config import *

# Plugin internal
from Plugins.Extensions.InfoBarTunerState.__init__ import _
from Plugins.Extensions.InfoBarTunerState.PluginBase import PluginBase
from Plugins.Extensions.InfoBarTunerState.Helper import getTuner, getNumber

HAS_WEBIF = False
try:
	from Plugins.Extensions.WebInterface.WebScreens import StreamingWebScreen 
	HAS_WEBIF = True
except:
	StreamingWebScreen = None


def getStreamID(stream):
	if HAS_WEBIF:
		try:
			return str(stream.screenIndex) + str(stream.clientIP)
		except:
			pass
	return ""

def getStream(id):
	if HAS_WEBIF:
		try:
			from Plugins.Extensions.WebInterface.WebScreens import streamingScreens 
		except:
			streamingScreens = []
		for stream in streamingScreens:
			if stream:
				if getStreamID(stream) == id:
					return stream
	return None


class StreamWebIf(PluginBase):
	def __init__(self):
		PluginBase.__init__(self)

	################################################
	# To be implemented by subclass
	def getText(self):
		return "Stream"

	def getType(self):
		from Plugins.Extensions.InfoBarTunerState.InfoBarTunerState import INFO, RECORD, STREAM, FINISHED
		# Pixmap number to be displayed as icon
		return STREAM

	def appendEvent(self):
		if config.infobartunerstate.show_streams.value:
			if HAS_WEBIF:
				try:
					from Plugins.Extensions.WebInterface.WebScreens import streamingEvents
					if self.onEvent not in streamingEvents:
						streamingEvents.append(self.onEvent)
				except:
					pass

	def removeEvent(self):
		if HAS_WEBIF:
			try:
				from Plugins.Extensions.WebInterface.WebScreens import streamingEvents
				if self.onEvent in streamingEvents:
					streamingEvents.remove(self.onEvent)
			except:
				pass

	def updateEvent(self):
		if HAS_WEBIF:
			try:
				from Plugins.Extensions.WebInterface.WebScreens import streamingScreens
			except:
				streamingScreens = []
			#TODO file streaming actually not supported
			for stream in streamingScreens:
				# Check if screen exists
				if stream and stream.request and 'file' not in stream.request.args:
					self.onEvent(StreamingWebScreen.EVENT_START, stream)

	def onEvent(self, event, stream):
		if StreamingWebScreen and stream:
			if (event == StreamingWebScreen.EVENT_START):
				id = getStreamID(stream)
				print "IBTS Stream Event WebIf Start " + id
				
				tuner, tunertype = getTuner( stream.getRecordService() ) 
				ref = stream.getRecordServiceRef()
				
				# Extract parameters
				ip = str(stream.clientIP)
				if ip:
					if ':' in ip and '.' in ip:
						# Mixed style ::ffff:192.168.64.27
						ip = string.split(str(stream.clientIP), ':')[-1]
				
				
				# Delete references to avoid blocking tuners
				del stream
				
				print "IBTS ip ####################################" + str(ip)
				port, host, client = "", "", ""
				
				event = ref and self.epg and self.epg.lookupEventTime(ref, -1, 0)
				if event: 
					name = event.getEventName()
				else:
					name = ""
					#TODO check file streaming
				
				service_ref = ServiceReference(ref)
				filename = "" #TODO file streaming - read meta eit
				
				try:
					host = ip and socket.gethostbyaddr( ip )
					client = host and host[0].split('.')[0]
				except:
					ip = ''
					client = ''
				
				number = service_ref and getNumber(service_ref.ref)
				channel = service_ref and service_ref.getServiceName()
				channel = channel.replace('\xc2\x86', '').replace('\xc2\x87', '')
				
				from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
				gInfoBarTunerState.addEntry(id, self.getPluginName(), self.getType(), self.getText(), tuner, tunertype, name, number, channel, filename, client, ip, port)
				
			elif event == StreamingWebScreen.EVENT_END:
				
				# Remove Finished Stream
				id = getStreamID(stream)
				print "IBTS Stream Event WebIf End " + id
				
				# Delete references to avoid blocking tuners
				del stream
				
				from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
				gInfoBarTunerState.finishEntry(id)

	def update(self, id, begin, end, endless):
		if config.infobartunerstate.show_streams.value:
			#TODO Avolid blocking - avoid using getStream to update the current name
			stream = getStream( id )
			if stream:
			
				#ref = stream.getRecordServiceRef()
				#if not win.tuner or not win.tunertype:
				#	win.tuner, win.tunertype = getTuner(stream.getRecordService())
				
				del stream
				
				#event = ref and self.epg and self.epg.lookupEventTime(ref, -1, 0)
				#if event: 
				#	name = event.getEventName()
				#else:
				#	name = ""
				
				#service_ref = None
				#if not win.number:
				#	service_ref = ServiceReference(ref)
				#	win.number = service_ref and getNumber(service_ref.ref)
				#if not win.channel:
				#	service_ref = service_ref or ServiceReference(ref)
				#	win.channel = win.channel or service_ref and service_ref.getServiceName()
				
				#win.updateName( name )
				#win.updateTimes( begin, end, endless )
				#win.update()
				
				from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
				gInfoBarTunerState.updateEntry(id, self.getType(), begin, None, True)
				
			else:
				
				# Stream is not active anymore
				from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
				gInfoBarTunerState.finishEntry(id)
