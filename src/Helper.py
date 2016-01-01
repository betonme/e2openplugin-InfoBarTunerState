#######################################################################
#
#    InfoBar Tuner State for Enigma-2
#    Coded by betonme (c) 2011 <glaserfrank(at)gmail.com>
#    Support: http://www.i-have-a-dreambox.com/wbb2/thread.php?threadid=162629
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#######################################################################

import socket

# for localized messages
from . import _

# Config
from Components.config import *

# Screen
from Components.NimManager import nimmanager
from enigma import eServiceCenter, eServiceReference, iServiceInformation, eEPGCache
from ServiceReference import ServiceReference


#######################################################
# Global helper functions
def normTuner(data):
	if data:
		type = str(data.get("tuner_type", ""))
		number = data.get("slot_number", -1)
		if number is None or number < 0:
			number = data.get("tuner_number", -1)
		if number is not None and number > -1:
			try:
				name = str(nimmanager.getNimSlotInputName(number))
			except:
				name = None
			if not name:
				name = str(chr( int(number) + ord('A') ))
			return ( name, type )
		else:
			return ( "", type )
	return ( "", "" )

def getTunerByServiceReferenceOLD(eservice):
	# service must be an instance of eServiceReference
	#if isinstance(service, eServiceReference):
	if eservice:
		serviceHandler = eServiceCenter.getInstance()
		serviceInfo = serviceHandler.info(eservice)
		data = serviceInfo and serviceInfo.getInfoObject(eservice, iServiceInformation.sTransponderData)
		return normTuner(data)
	return ( "", "" )
def getTunerByServiceReference(service_ref):
	# service must be an instance of ServiceReference
	#if isinstance(service, ServiceReference):
	if service_ref:
		info = service_ref.info()
		data = info and info.getInfoObject(service_ref.ref, iServiceInformation.sTransponderData)
		return normTuner(data)
	return ( "", "" )

def getTunerByPlayableService(iservice):
	# service must be an instance of iPlayableService or iRecordableService
	#if isinstance(service, iRecordableService):
	feinfo = iservice and iservice.frontendInfo()
	data = feinfo and feinfo.getFrontendData()
	return normTuner(data)

def getNumber(service_ref):
	# service must be an instance of ServiceReference
	#if isinstance(service, ServiceReference):
	if service_ref:
		actservice = service_ref.ref
		
		# actservice must be an instance of eServiceReference
		from Screens.InfoBar import InfoBar
		Servicelist = None
		if InfoBar and InfoBar.instance:
			Servicelist = InfoBar.instance.servicelist
		
		mask = (eServiceReference.isMarker | eServiceReference.isDirectory)
		number = 0
		
		bouquets = Servicelist and Servicelist.getBouquetList()
		if bouquets:
			
			#TODO get alternative for actbouquet
			actbouquet = Servicelist.getRoot()
			serviceHandler = eServiceCenter.getInstance()
			for name, bouquet in bouquets:
				
				if not bouquet.valid(): #check end of list
					break
				
				if bouquet.flags & eServiceReference.isDirectory:
					
					servicelist = serviceHandler.list(bouquet)
					if not servicelist is None:
						
						while True:
							service = servicelist.getNext()
							if not service.valid(): #check end of list
								break
							playable = not (service.flags & mask)
							if playable:
								number += 1
							if actbouquet:
								if actbouquet == bouquet and actservice == service:
									return number
							else:
								if actservice == service:
									return number
	return None

def getChannel(service_ref):
	# service must be an instance of ServiceReference
	#if isinstance(service, ServiceReference):
	if service_ref:
		return service_ref.getServiceName().replace('\xc2\x86', '').replace('\xc2\x87', '')
	return ""

def getEventName(service):
	# service must be an instance of eServiceReference
	#if isinstance(service, eServiceReference):
	if service:
		epg = eEPGCache.getInstance()
		event = epg and epg.lookupEventTime(service, -1, 0)
		if event: 
			return event.getEventName()
	return ""

def getClient(ip):
	try:
		host = ip and socket.gethostbyaddr( ip )
		if host:
			return host[0].split('.')[0]
	except:
		pass
	return ""


#######################################################
# Not used yet
def readBouquetList(self):
	serviceHandler = eServiceCenter.getInstance()
	refstr = '1:134:1:0:0:0:0:0:0:0:FROM BOUQUET \"bouquets.tv\" ORDER BY bouquet'
	bouquetroot = eServiceReference(refstr)
	self.bouquetlist = {}
	list = serviceHandler.list(bouquetroot)
	if list is not None:
		self.bouquetlist = list.getContent("CN", True)

