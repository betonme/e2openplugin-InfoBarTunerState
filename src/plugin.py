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

# for localized messages
from . import _

# Config
from Components.config import config

# Plugin
from Plugins.Plugin import PluginDescriptor

# MessageBox
from Screens.MessageBox import MessageBox

# Plugin internal
from IBTSConfiguration import InfoBarTunerStateConfiguration
from InfoBarTunerState import InfoBarTunerState, TunerStateInfo
from Logger import log

# Contants
NAME = _("InfoBarTunerState")
IBTSSHOW = _("Show InfoBarTunerState")
IBTSSETUP = _("InfoBarTunerState Setup")
VERSION = "3.2.5"
SUPPORT = "http://bit.ly/ibtsihad"
DONATE = "http://bit.ly/ibtspaypal"
ABOUT = "\n  " + NAME + " " + VERSION + "\n\n" \
				+ _("  (C) 2012 by betonme @ IHAD \n\n") \
				+ _("  If You like this plugin and want to support it,\n") \
				+ _("  or if just want to say ''thanks'',\n") \
				+ _("  feel free to donate via PayPal. \n\n") \
				+ _("  Thanks a lot ! \n  PayPal: ") + DONATE + "\n" \
				+ _("  SUPPORT: ") + SUPPORT

# Globals
gInfoBarTunerState = None

# Temporary if we do not import the modules the config will not be loaded
from Plugins.Extensions.InfoBarTunerState.Handler import *


#######################################################
# Plugin main function
def Plugins(**kwargs):
	descriptors = []
	
	if config.infobartunerstate.enabled.value:
		# SessionStart
		descriptors.append( PluginDescriptor(where = PluginDescriptor.WHERE_SESSIONSTART, fnc = start, needsRestart = False) )
		if config.infobartunerstate.extensions_menu_show.value:
			descriptors.append( PluginDescriptor(name = IBTSSHOW, description = IBTSSHOW, where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc = show, needsRestart = False) )
		if config.infobartunerstate.extensions_menu_setup.value:
			descriptors.append( PluginDescriptor(name = IBTSSETUP, description = IBTSSETUP, where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc = setup, needsRestart = False) )
	
	descriptors.append( PluginDescriptor(name = NAME, description = NAME + " " +_("configuration"), where = PluginDescriptor.WHERE_PLUGINMENU, fnc = setup, needsRestart = False, icon = "plugin.png") )

	return descriptors


#######################################################
# Plugin # Plugin configuration
def setup(session, **kwargs):
	log.info( "InfoBarTunerState setup" )
	#TODO config
	# Overwrite Skin Position
	# Show Live TV Tuners PiP LiveStream FileStream
	# alltime permanent display, needs an dynamic update service
	# Always display at least Nothing running
	# show free tuner with dvb-type
	# Used disk size
	# Event popup timeout
	# Feldbreitenbegrenzung fuer Namen ...
	# Streaming amount of data
	# Display next x timers also if deactivated
	try:
		session.open(InfoBarTunerStateConfiguration)
	except Exception, e:
		log.exception( "InfoBarTunerStateMenu exception " + str(e) )


#######################################################
# Sessionstart
def start(reason, **kwargs):
	log.info( "InfoBarTunerState start" )
	if reason == 0: # start
		if kwargs.has_key("session"):
			if config.infobartunerstate.enabled.value:
				global gInfoBarTunerState
				session = kwargs["session"]
				try:
					gInfoBarTunerState = InfoBarTunerState(session)
					gInfoBarTunerState.onInit()
				except Exception, e:
					log.exception( "InfoBarTunerState start exception " + str(e) )
	# Do not cleanup on session shutdown, it will break the movie player integration


#######################################################
# Extension Menu
def show(session, **kwargs):
	log.info( "InfoBarTunerState show" )
	if gInfoBarTunerState:
		try:
			gInfoBarTunerState.show(True, forceshow=True)
		except Exception, e:
			log.exception( "InfoBarTunerState show exception " + str(e) )
	else:
		# No InfoBarTunerState Instance running
		log.info( "InfoBarTunerState disabled" )
		session.open(MessageBox, _("InfoBarTunerState is disabled"), MessageBox.TYPE_INFO, 3)

