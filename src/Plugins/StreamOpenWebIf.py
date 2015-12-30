# -*- coding: utf-8 -*-from
# by betonme @2015

from time import time

# Config
from Components.config import *

# Plugin internal
from Plugins.Extensions.InfoBarTunerState.__init__ import _
from Plugins.Extensions.InfoBarTunerState.PluginBase import PluginBase
from Plugins.Extensions.InfoBarTunerState.Helper import getTuner, getNumber

HAS_OPENWEBIF = False
try:
	from Plugins.Extensions.OpenWebif.controllers.stream import StreamAdapter
	HAS_OPENWEBIF = True
except:
	StreamAdapter = None


def getStreamID(stream):
	if HAS_OPENWEBIF:		
		try:
			return str(stream.streamIndex) + str(stream.clientIP)
		except:
			pass
	return ""

def getStream(id):
	if HAS_OPENWEBIF:
		try:
			from Plugins.Extensions.OpenWebif.controllers.stream import streamList
		except:
			streamList = []
		for stream in streamList:
			if stream:
				if getStreamID(stream) == id:
					return stream
	return None


class StreamOpenWebIf(PluginBase):
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
			if HAS_OPENWEBIF:
				try:
					from Plugins.Extensions.OpenWebif.controllers.stream import streamStates
					if self.onEvent not in streamStates:
						streamStates.append(self.onEvent)
				except:
					pass

	def removeEvent(self):
		if HAS_OPENWEBIF:
			try:
				from Plugins.Extensions.OpenWebif.controllers.stream import streamStates
				if self.onEvent in streamStates:
					streamStates.remove(self.onEvent)
			except:
				pass

	def updateEvent(self):
		if HAS_OPENWEBIF:
			try:
				from Plugins.Extensions.WebInterface.WebScreens import streamList
			except:
				streamList = []
			#TODO file streaming actually not supported
			for stream in streamList:
				# Check if screen exists
				if stream and stream.request and 'file' not in stream.request.args:
					self.onEvent(StreamAdapter.EV_BEGIN, stream)

	def onEvent(self, event, stream):
		print "IBTS Stream Event OpenWebIf"
		if StreamAdapter and stream:
			if (event == StreamAdapter.EV_BEGIN):
				id = getStreamID(stream)
				print "IBTS Stream Event OpenWebIf Start " + id
				
				tuner, tunertype = getTuner( stream.getService() ) 
				ref = stream.ref
				
				# Extract parameters
				ip = stream.clientIP
				
				# Delete references to avoid blocking tuners
				del stream
				
				print "IBTS ip " + str(ip)
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
			
			elif event == StreamAdapter.EV_STOP:
				
				# Remove Finished Stream
				id = getStreamID(stream)
				print "IBTS Stream Event OpenWebIf End " + id
				
				# Delete references to avoid blocking tuners
				del stream
				
				from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
				gInfoBarTunerState.finishEntry(id)

	def update(self, id, begin, end, endless):
		if config.infobartunerstate.show_streams.value:
			#TODO Avolid blocking - avoid using getStream to update the current name
			stream = getStream( id )
			if stream:
			
				#ref = stream.ref
				#if not win.tuner or not win.tunertype:
				#	win.tuner, win.tunertype = getTuner(stream.getService())
				
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
