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
from Components.config import config, ConfigSubsection, ConfigNothing, ConfigYesNo, ConfigSelectionNumber, ConfigSelection, ConfigEnableDisable, ConfigText

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
VERSION = "4.0.1"
SUPPORT = "http://bit.ly/ibtsihad"
DONATE = "http://bit.ly/ibtspaypal"
ABOUT = "\n  " + NAME + " " + VERSION + "\n\n" \
				+ _("  (C) 2012 by betonme @ IHAD \n\n") \
				+ _("  If You like this plugin and want to support it,\n") \
				+ _("  or if just want to say ''thanks'',\n") \
				+ _("  feel free to donate via PayPal. \n\n") \
				+ _("  Thanks a lot ! \n  PayPal: ") + DONATE + "\n" \
				+ _("  SUPPORT: ") + SUPPORT

infobar_choices = [	
									("False",							_("no")),
									("True",							_("yes")),
									("only_onkeypress",		_("only on keypress")),
								]

# Config choices
field_choices = [	
									("TypeIcon",								_("Type (Icon)")),
									("TypeText",								_("Type (Text)")),
									("Tuner",										_("Tuner")),
									("TunerType",								_("Tuner Type")),
									("Number",									_("Channel Number")),
									("Channel",									_("Channel Name")),
									("ChannelIcon",							_("Channel Icon")),
									("Name",										_("Name")),
									("TimeLeftDuration",				_("Time Left / Duration")),
									("TimeLeft",								_("Time Left")),
									("TimeElapsed",							_("Time Elapsed")),
									("Begin",										_("Begin")),
									("End",											_("End")),
									("BeginEnd",									_("Begin / End")),
									("Duration",								_("Duration")),
									("TimerProgressGraphical",	_("Timer Progress (Graphical)")),  #TODO howto do for file streams
									("TimerProgressText",				_("Timer Progress (Text)")),  #TODO howto do for file streams
									("TimerDestination",				_("Destination")),		#TODO howto do for file streams
									("StreamClient",						_("Stream Client")),
									("StreamClientPort",				_("Stream Client with Port")),
									("DestinationStreamClient",	_("Destination / Client")),
									#Throughput
									#Overall transfer
									("FileSize",								_("File Size")),
									("FreeSpace",								_("Free Space")),
									("None",									_("None")),
								]

date_choices = [	
									("%H:%M",				_("HH:MM")),
									("%d.%m %H:%M",			_("DD.MM HH:MM")),
									("%d.%m. %H:%M",		_("DD.MM. HH:MM")),
									("%m/%d %H:%M",			_("MM/DD HH:MM")),
									("%d.%m.%Y %H:%M",		_("DD.MM.YYYY HH:MM")),
									("%Y/%m/%d %H:%M",		_("YYYY/MM/DD HH:MM")),
									("%H:%M %d.%m",			_("HH:MM DD.MM")),
									("%H:%M %m/%d",			_("HH:MM MM/DD")),
									("%H:%M %d.%m.%Y",		_("HH:MM DD.MM.YYYY")),
									("%H:%M %Y/%m/%d",		_("HH:MM YYYY/MM/DD")),
									("%a %d.%m. %H:%M",		_("WD DD.MM. HH:MM")),
									("%a, %d.%m. %H:%M",	_("WD, DD.MM. HH:MM")),
									("%a %H:%M",            _("WD HH:MM")),
									("-    %H:%M",			_("-    HH:MM")),
									
								]

# Config options
config.infobartunerstate                           = ConfigSubsection()

config.infobartunerstate.about                     = ConfigNothing()
config.infobartunerstate.enabled                   = ConfigYesNo(default = True)
config.infobartunerstate.extensions_menu_show      = ConfigYesNo(default = True)
config.infobartunerstate.extensions_menu_setup     = ConfigYesNo(default = False)
#config.infobartunerstate.popup_time               = ConfigSelectionNumber(0, 10, 1, default = 5)
config.infobartunerstate.popups_error_timeout      = ConfigSelectionNumber(0, 10, 1, default = 5)

#config.infobartunerstate.show_withinfobar          = ConfigYesNo(default = True)
#config.infobartunerstate.show_withplayer           = ConfigYesNo(default = False)		# Show with MoviePlayer only is actually not possible
#config.infobartunerstate.show_onkeypress           = ConfigYesNo(default = False)

config.infobartunerstate.show_withinfobar          = ConfigSelection(default = "False", choices = infobar_choices)
config.infobartunerstate.show_withplayer           = ConfigSelection(default = "False", choices = infobar_choices)

config.infobartunerstate.time_format_begin         = ConfigSelection(default = "%H:%M", choices = date_choices)
config.infobartunerstate.time_format_end           = ConfigSelection(default = "%H:%M", choices = date_choices)

config.infobartunerstate.number_finished_entries   = ConfigSelectionNumber(0, 10, 1, default = 5)
config.infobartunerstate.timeout_finished_entries  = ConfigSelectionNumber(0, 600, 10, default = 60)

config.infobartunerstate.fields                    = ConfigSubsection()
config.infobartunerstate.fields.a                  = ConfigSelection(default = "TypeIcon", choices = field_choices)
config.infobartunerstate.fields.b                  = ConfigSelection(default = "Tuner", choices = field_choices)
config.infobartunerstate.fields.c                  = ConfigSelection(default = "Number", choices = field_choices)
config.infobartunerstate.fields.d                  = ConfigSelection(default = "Channel", choices = field_choices)
config.infobartunerstate.fields.e                  = ConfigSelection(default = "Name", choices = field_choices)
config.infobartunerstate.fields.f                  = ConfigSelection(default = "TimerProgressGraphical", choices = field_choices)
config.infobartunerstate.fields.g                  = ConfigSelection(default = "TimeLeftDuration", choices = field_choices)
config.infobartunerstate.fields.h                  = ConfigSelection(default = "StreamClient", choices = field_choices)
config.infobartunerstate.fields.i                  = ConfigSelection(default = "None", choices = field_choices)
config.infobartunerstate.fields.j                  = ConfigSelection(default = "None", choices = field_choices)

config.infobartunerstate.fieldswidth               = ConfigSubsection()
config.infobartunerstate.fieldswidth.a             = ConfigSelectionNumber(0, 1500, 1, default = 0)
config.infobartunerstate.fieldswidth.b             = ConfigSelectionNumber(0, 1500, 1, default = 0)
config.infobartunerstate.fieldswidth.c             = ConfigSelectionNumber(0, 1500, 1, default = 0)
config.infobartunerstate.fieldswidth.d             = ConfigSelectionNumber(0, 1500, 1, default = 0)
config.infobartunerstate.fieldswidth.e             = ConfigSelectionNumber(0, 1500, 1, default = 0)
config.infobartunerstate.fieldswidth.f             = ConfigSelectionNumber(0, 1500, 1, default = 0)
config.infobartunerstate.fieldswidth.g             = ConfigSelectionNumber(0, 1500, 1, default = 0)
config.infobartunerstate.fieldswidth.h             = ConfigSelectionNumber(0, 1500, 1, default = 0)
config.infobartunerstate.fieldswidth.i             = ConfigSelectionNumber(0, 1500, 1, default = 0)
config.infobartunerstate.fieldswidth.j             = ConfigSelectionNumber(0, 1500, 1, default = 0)

config.infobartunerstate.offset_horizontal         = ConfigSelectionNumber(-1000, 1000, 1, default = 0)
config.infobartunerstate.offset_vertical           = ConfigSelectionNumber(-1000, 1000, 1, default = 0)
config.infobartunerstate.offset_padding            = ConfigSelectionNumber(-1000, 1000, 1, default = 0)
config.infobartunerstate.offset_spacing            = ConfigSelectionNumber(-1000, 1000, 1, default = 0)
config.infobartunerstate.offset_rightside          = ConfigSelectionNumber(-1000, 1000, 1, default = 0)
config.infobartunerstate.placeholder_pogressbar    = ConfigYesNo(default = True)
config.infobartunerstate.variable_field_width      = ConfigYesNo(default = True)
#MAYBE provide different sorting types / options
config.infobartunerstate.list_goesup               = ConfigYesNo(default = False)

config.infobartunerstate.infobar_timeout           = ConfigSelectionNumber(0, 100, 1, default = 0)
config.infobartunerstate.wake_hdd                  = ConfigYesNo(default = False)
config.infobartunerstate.skip_mounts               = ConfigYesNo(default = True)
config.infobartunerstate.background_transparency   = ConfigYesNo(default = False)

config.infobartunerstate.log_shell                 = ConfigYesNo(default = False) 
config.infobartunerstate.log_write                 = ConfigYesNo(default = False) 
config.infobartunerstate.log_file                  = ConfigText(default = "/tmp/infobartunerstate.log", fixed_size = False) 

config.infobartunerstate.log_shell                 = ConfigEnableDisable(default = False) 
config.infobartunerstate.log_write                 = ConfigEnableDisable(default = False) 
config.infobartunerstate.log_file                  = ConfigText(default = "/tmp/pushservice.log", fixed_size = False) 

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

