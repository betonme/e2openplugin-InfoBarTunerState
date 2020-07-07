from __future__ import absolute_import
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
from Components.config import *
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText

from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Setup import SetupSummary

# Plugin internal
from .InfoBarTunerState import InfoBarTunerState
from .InfoBarTunerStatePlugins import InfoBarTunerStatePlugins


#######################################################
# Configuration screen
class InfoBarTunerStateConfiguration(Screen, ConfigListScreen, InfoBarTunerStatePlugins):
	def __init__(self, session):
		Screen.__init__(self, session)
		InfoBarTunerStatePlugins.__init__(self)
		self.skinName = [ "InfoBarTunerStateConfiguration", "Setup" ]
		
		# Summary
		from Plugins.Extensions.InfoBarTunerState.plugin import NAME, VERSION
		self.setup_title = NAME + " " + _("Configuration") + " " + VERSION
		self.onChangedEntry = []
		
		# Buttons
		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("OK"))
		
		# Define Actions
		self["custom_actions"] = ActionMap(["SetupActions", "ChannelSelectBaseActions"],
		{
			"cancel":				self.keyCancel,
			"save":					self.keySave,
			"nextBouquet":	self.pageUp,
			"prevBouquet":	self.pageDown,
		}, -2) # higher priority
		
		# Initialize Configuration part
		self.list = []
		self.config = []
		self.onChanged = [ config.infobartunerstate.enabled, config.infobartunerstate.log_write ]
		
		for plugin in self.getPlugins():
			onChanged = plugin.getOnChanged()
			if onChanged:
				self.onChanged.extend(onChanged)
		
		self.buildConfig()
		ConfigListScreen.__init__(self, self.list, session = session, on_change = self.changed)
		self.changeConfig()
		
		# Trigger change
		self.changed()

		self.onLayoutFinish.append(self.layoutFinished)

	def buildConfig(self):
		
		separator = "".ljust(250, "-")
		separatorE2Usage = "- E2 "+_("Usage")+" "
		separatorE2Usage = separatorE2Usage.ljust(250-len(separatorE2Usage), "-")
		
#         _config list entry
#         _                                                     , config element
		self.config = [
			(  _("Enable InfoBarTunerState"), config.infobartunerstate.enabled ),
			(  separator, config.infobartunerstate.about ),
			(  _("Add Show to extension menu"), config.infobartunerstate.extensions_menu_show ),
			(  _("Add Setup to extension menu"), config.infobartunerstate.extensions_menu_setup ),
#			(  _("Pop-Up time in seconds")                            , config.infobartunerstate.popup_time ),
			(  _("Show with InfoBar (TV-mode)"), config.infobartunerstate.show_withinfobar ),
			(  _("Show with Infobar (MoviePlayer)"), config.infobartunerstate.show_withplayer ),
			(  _("Time format begin"), config.infobartunerstate.time_format_begin ),
			(  _("Time format end"), config.infobartunerstate.time_format_end ),
			(  _("Number of finished entries in list"), config.infobartunerstate.number_finished_entries ),
			(  _("Number of seconds for displaying finished entries"), config.infobartunerstate.timeout_finished_entries ),
			(  separator, config.infobartunerstate.about ),
		]
		
		for plugin in self.getPlugins():
			options = plugin.getOptions()
			if options:
				for text, element in options:
					self.config.extend( [
						(  text, element ),
					] )
		
		self.config.extend( [
			(  separator, config.infobartunerstate.about ),
		] )
		
		for i, configinfobartunerstatefield in enumerate( config.infobartunerstate.fields.dict().itervalues() ):
			self.config.append(
			(  _("Field %d content") % (i), configinfobartunerstatefield )
			)
		for i, configinfobartunerstatefieldwidth in enumerate( config.infobartunerstate.fieldswidth.dict().itervalues() ):
			self.config.append(
			(  _("Field %d width") % (i), configinfobartunerstatefieldwidth )
			)
		
		self.config.extend( [
			(  separator, config.infobartunerstate.about ),
			(  _("Horizontal offset left in pixel"), config.infobartunerstate.offset_horizontal ),
			(  _("Horizontal offset right in pixel"), config.infobartunerstate.offset_rightside ),
			(  _("Vertical offset in pixel"), config.infobartunerstate.offset_vertical ),
			(  _("Text padding offset in pixel"), config.infobartunerstate.offset_padding ),
			(  _("Text spacing offset in pixel"), config.infobartunerstate.offset_spacing ),
			(  _("Variable field width"), config.infobartunerstate.variable_field_width ),
			(  _("Placeholder for Progressbar"), config.infobartunerstate.placeholder_pogressbar ),
			(  _("List goes up"), config.infobartunerstate.list_goesup ),
			(  _("Background transparency"), config.infobartunerstate.background_transparency ),
			(  _("Overwrite Infobar timeout"), config.infobartunerstate.infobar_timeout ),
			(  _("Wake HDD for free space statistics"), config.infobartunerstate.wake_hdd ),
			(  _("Skip mounts for free space statistics"), config.infobartunerstate.skip_mounts ),
			(  separator, config.infobartunerstate.about ),
			(  _("Log debug prints to shell"), config.infobartunerstate.log_shell ),
			(  _("Log to file"), config.infobartunerstate.log_write ),
		] )
		
		if config.infobartunerstate.log_write.value:
			self.config.append(
				(  _("Log file path and name"), config.infobartunerstate.log_file )
				)
		
		self.config.extend( [
			(  separatorE2Usage, config.infobartunerstate.about ),
			(  _("Infobar timeout"), config.usage.infobar_timeout ),
			(  _("Show Message when Recording starts"), config.usage.show_message_when_recording_starts ),
		] )

	def changeConfig(self):
		list = []
		self.buildConfig()
		for conf in self.config:
			# 0 entry text
			# 1 variable
			list.append( getConfigListEntry( conf[0], conf[1]) )
			if not config.infobartunerstate.enabled.value:
				break
		self.list = list
		self["config"].setList(self.list)

	def layoutFinished(self):
		self.setTitle(self.setup_title)

	def changed(self):
		for x in self.onChangedEntry:
			x()
		current = self["config"].getCurrent()[1]
		if current in self.onChanged:
			self.changeConfig()
			return

	# Overwrite ConfigListScreen keyCancel function
	def keyCancel(self):
		if self["config"].isChanged():
			self.session.openWithCallback(self.cancelConfirm, MessageBox, _("Really close without saving settings?"))
		else:
			self.close()

	# Overwrite ConfigListScreen cancelConfirm function
	def cancelConfirm(self, result):
		if not result:
			return
		for x in self["config"].list:
			x[1].cancel()
		self.close()

	# Overwrite ConfigList functions
	def saveAll(self):
		for x in self["config"].list:
			if isinstance(x, ConfigSubsection):
				for y in x.content.items.values():
					y.save()
			x[1].save()
		configfile.save()	

	# Overwrite ConfigListScreen functions
	def keySave(self):
		# Check field configuration
		fieldname = []
		fieldicon = []
		fieldprogress = []
		text = ""
		for i, c in enumerate( config.infobartunerstate.fields.dict().itervalues() ):
			if c.value == "Name":
				fieldname.append( i )
			if c.value == "TypeIcon":
				fieldicon.append( i )
			if c.value == "TimerProgressGraphical":
				fieldprogress.append( i )
		
		if len(fieldname) > 1:
			text += _("Only one Name field allowed:") + "\n" \
							+ "\n".join(["Field " + (str(f)) for f in fieldname])
		
		if len(fieldicon) > 1:
			text += _("Only one Icon field allowed:") + "\n" \
							+ "\n".join(["Field " + (str(f)) for f in fieldicon])
		
		if len(fieldprogress) > 1:
			if text: text += "\n\n"
			text += _("Only one Graphical Progress field allowed:") + "\n" \
							+ "\n".join(["Field " + (str(f)) for f in fieldprogress])
		
		if text:
			self.session.open(MessageBox, text, MessageBox.TYPE_ERROR, 3)
			return
		
		# Now save all
		self.saveAll()
		
		# Overwrite Screen close function to handle new config
		
		# We need assign / "write" access import the plugin module
		# global won't work across module scope
		from . import plugin
		if config.infobartunerstate.enabled.value:
			# Plugin should be enabled
			if plugin.gInfoBarTunerState:
				
				# Plugin is active - close it
				plugin.gInfoBarTunerState.close()
				plugin.gInfoBarTunerState = None
			
			
			# Force new instance
			plugin.gInfoBarTunerState = InfoBarTunerState(self.session)
			
			if plugin.gInfoBarTunerState:
				
				# Check for actual events
				plugin.gInfoBarTunerState.onInit()
		else:
			
			# Plugin should be disabled
			if plugin.gInfoBarTunerState:
				
				# Plugin is active, disable it
				plugin.gInfoBarTunerState.close()

		self.close()
	
	# Overwrite Screen close function
	def close(self):
		from .plugin import ABOUT
		self.session.openWithCallback(self.closeConfirm, MessageBox, ABOUT, MessageBox.TYPE_INFO)

	def closeConfirm(self, dummy=None):
		# Call baseclass function
		Screen.close(self)

	def getCurrentEntry(self):
		return self["config"].getCurrent()[0]

	def getCurrentValue(self):
		return str(self["config"].getCurrent()[1].getText())

	def createSummary(self):
		return SetupSummary

	def pageUp(self):
		self["config"].instance.moveSelection(self["config"].instance.pageUp)

	def pageDown(self):
		self["config"].instance.moveSelection(self["config"].instance.pageDown)

