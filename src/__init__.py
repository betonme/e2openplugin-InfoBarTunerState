# -*- coding: utf-8 -*-
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from os import environ as os_environ
import gettext

def localeInit():
	lang = language.getLanguage()[:2] # getLanguage returns e.g. "fi_FI" for "language_country"
	os_environ["LANGUAGE"] = lang # Enigma doesn't set this (or LC_ALL, LC_MESSAGES, LANG). gettext needs it!
	gettext.bindtextdomain("InfoBarTunerState", resolveFilename(SCOPE_PLUGINS, "Extensions/InfoBarTunerState/locale"))

def _(txt):
	if txt:
		t = gettext.dgettext("InfoBarTunerState", txt)
		if t == txt:
			t = gettext.gettext(txt)
		return t 
	else:
		return ""

localeInit()
language.addCallback(localeInit)


from Components.config import config, ConfigSubsection, ConfigNothing, ConfigYesNo, ConfigSelectionNumber, ConfigSelection, ConfigEnableDisable, ConfigText

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
									("None",										_("None")),
								]

date_choices = [	
									("%H:%M",							_("HH:MM")),
									("%d.%m %H:%M",				_("DD.MM HH:MM")),
									("%d.%m. %H:%M",			_("DD.MM. HH:MM")),
									("%m/%d %H:%M",				_("MM/DD HH:MM")),
									("%d.%m.%Y %H:%M",		_("DD.MM.YYYY HH:MM")),
									("%Y/%m/%d %H:%M",		_("YYYY/MM/DD HH:MM")),
									("%H:%M %d.%m",				_("HH:MM DD.MM")),
									("%H:%M %m/%d",				_("HH:MM MM/DD")),
									("%H:%M %d.%m.%Y",		_("HH:MM DD.MM.YYYY")),
									("%H:%M %Y/%m/%d",		_("HH:MM YYYY/MM/DD")),
									("%a %d.%m. %H:%M",		_("WD DD.MM. HH:MM")),
									("%a, %d.%m. %H:%M",	_("WD, DD.MM. HH:MM")),
									("-    %H:%M",				_("-    HH:MM")),
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
config.infobartunerstate.fieldswidth.a             = ConfigSelectionNumber(0, 1000, 1, default = 0)
config.infobartunerstate.fieldswidth.b             = ConfigSelectionNumber(0, 1000, 1, default = 0)
config.infobartunerstate.fieldswidth.c             = ConfigSelectionNumber(0, 1000, 1, default = 0)
config.infobartunerstate.fieldswidth.d             = ConfigSelectionNumber(0, 1000, 1, default = 0)
config.infobartunerstate.fieldswidth.e             = ConfigSelectionNumber(0, 1000, 1, default = 0)
config.infobartunerstate.fieldswidth.f             = ConfigSelectionNumber(0, 1000, 1, default = 0)
config.infobartunerstate.fieldswidth.g             = ConfigSelectionNumber(0, 1000, 1, default = 0)
config.infobartunerstate.fieldswidth.h             = ConfigSelectionNumber(0, 1000, 1, default = 0)
config.infobartunerstate.fieldswidth.i             = ConfigSelectionNumber(0, 1000, 1, default = 0)
config.infobartunerstate.fieldswidth.j             = ConfigSelectionNumber(0, 1000, 1, default = 0)

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

