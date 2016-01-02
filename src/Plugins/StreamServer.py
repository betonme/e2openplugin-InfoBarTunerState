# -*- coding: utf-8 -*-from
# by betonme @2015

import string
import sys

from time import time
from random import randint

from enigma import eServiceReference
from ServiceReference import ServiceReference

# Config
from Components.config import *

# Plugin internal
from Plugins.Extensions.InfoBarTunerState.__init__ import _
from Plugins.Extensions.InfoBarTunerState.PluginBase import PluginBase
from Plugins.Extensions.InfoBarTunerState.Helper import getTunerByPlayableService, getNumber, getChannel, getTunerByServiceReference, getClient, getEventName

HAS_STREAMSERVER = False
try:
	from Components.StreamServerControl import streamServerControl
	HAS_STREAMSERVER = True
except:
	StreamingWebScreen = None


def getStreamID(count, ip):
	if HAS_STREAMSERVER:
		try:
			return str(count) + str(ip) + str(randint(0,9))
		except:
			pass
	return ""


class StreamServer(PluginBase):
	def __init__(self):
		PluginBase.__init__(self)
		self.ids = []

	def getStream(self, id):
		for sid, ip, servicereference_string in self.ids:
			if sid == id:
				return sid, ip, servicereference_string
	
	def getRef(self, id):
		for sid, ip, servicereference_string in self.ids:
			if sid == id:
				return servicereference_string
	
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
			if HAS_STREAMSERVER:
				try:
					from Components.StreamServerControl import streamServerControl
				except:
					pass
				if streamServerControl:
					if self.onEventClientCountChanged not in streamServerControl.onRtspClientCountChanged:
						streamServerControl.onRtspClientCountChanged.append(self.onEventClientCountChanged)
					if self.onEventParametersChanged not in streamServerControl.onUriParametersChanged:
						streamServerControl.onUriParametersChanged.append(self.onEventParametersChanged)

	def removeEvent(self):
		if HAS_STREAMSERVER:
			try:
				from Components.StreamServerControl import streamServerControl
			except:
				pass
			if streamServerControl:
				if self.onEventClientCountChanged in streamServerControl.onRtspClientCountChanged:
					streamServerControl.onRtspClientCountChanged.remove(self.onEventClientCountChanged)
				if self.onEventParametersChanged in streamServerControl.onUriParametersChanged:
					streamServerControl.onUriParametersChanged.remove(self.onEventParametersChanged)

	def onInit(self):
		if HAS_STREAMSERVER:
			try:
				from Components.StreamServerControl import streamServerControl
				for stream in range(streamServerControl.rtspClientCount):
					self.onEventClientCountChanged(streamServerControl.rtspClientCount, "")
			except:
				pass

	def onEventClientCountChanged(self, count, client, force=False):
		if len(self.ids) < count:
			
			# Extract parameters
			ip = str(client)
			
			id = getStreamID(count, ip)
			print "IBTS Stream Event StreamServer Start " + id
			
			self.ids.append( (id, ip, None) )
			
			# We will add the entry later
			
			if force:
				client = getClient(ip)
				
				from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
				gInfoBarTunerState.addEntry(id, self.getPluginName(), self.getType(), self.getText(), "", "", "", "", "", time(), 0, True, "", client, ip, "")
			
		else:
			
			# Remove Finished Stream
			print "IBTS Stream Event StreamServer End", count, client
			
			# There is no way to find the correct stream, just remove the oldest
			if  self.ids:
				id, ip, servicereference_string = self.ids[0]
				del self.ids[0]
				
				from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
				gInfoBarTunerState.finishEntry(id)

	def onEventParametersChanged(self, params):
		try:
			if self.ids:
				id, ip, servicereference_string = self.ids[-1]
				print "IBTS Stream Event StreamServer Changed " + id
				
				if servicereference_string is None:
				
					servicereference_string = str(params.get(streamServerControl.URI_PARAM_REF, [""])[0])
					
					self.ids[-1] = (id, ip, servicereference_string)
					
					eservicereference = eServiceReference(servicereference_string)
					if eservicereference.valid():
						
						service_ref = ServiceReference(servicereference_string)
						
						tuner, tunertype, tunernumber = getTunerByServiceReference( service_ref ) 
						
						name = getEventName(eservicereference)
						
						number = getNumber(eservicereference)
						channel = getChannel(eservicereference)
						name = getEventName(eservicereference)
						
						client = getClient(ip)
						
						from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
						gInfoBarTunerState.addEntry(id, self.getPluginName(), self.getType(), self.getText(), tuner, tunertype, tunernumber, name, number, channel, time(), 0, True, "", client, ip)
		except Exception, e:
			print "IBTS exception " + str(e)
			import os, sys, traceback
			print str(sys.exc_info()[0])
			print str(traceback.format_exc())
			sys.exc_clear()

	def update(self, id, tunerstate):
		
		servicereference_string = self.getRef(id)
		
		eservicereference = ref and eServiceReference(servicereference_string)
		if eservicereference and eservicereference.valid():
			
			tunerstate.name = getEventName(eservicereference)
		
		return True
