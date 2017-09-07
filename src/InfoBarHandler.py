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

from enigma import eTimer

# Config
from Components.config import *

# Plugin internal
from ExtensionHandler import addExtension, removeExtension


# Globals
InfoBarShow = None
InfoBarHide = None
InfoBarToggle = None


#######################################################
# InfoBarShowHide for MoviePlayer integration
def overwriteInfoBar():
	from Screens.InfoBarGenerics import InfoBarShowHide
	global InfoBarShow, InfoBarHide, InfoBarToggle
	if InfoBarShow is None:
		# Backup original function
		InfoBarShow = InfoBarShowHide._InfoBarShowHide__onShow
		# Overwrite function
		InfoBarShowHide._InfoBarShowHide__onShow = InfoBarShowTunerState
	if InfoBarHide is None:
		# Backup original function
		InfoBarHide = InfoBarShowHide._InfoBarShowHide__onHide
		# Overwrite function
		InfoBarShowHide._InfoBarShowHide__onHide = InfoBarHideTunerState
	if InfoBarToggle is None:
		# Backup original function
		InfoBarToggle = InfoBarShowHide.toggleShow
		# Overwrite function
		InfoBarShowHide.toggleShow = InfoBarToggleTunerState

# InfoBar Events
def recoverInfoBar():
	from Screens.InfoBarGenerics import InfoBarShowHide
	global InfoBarShow, InfoBarHide, InfoBarToggle
	if InfoBarShow:
		InfoBarShowHide._InfoBarShowHide__onShow = InfoBarShow
		InfoBarShow = None
	if InfoBarHide:
		InfoBarShowHide._InfoBarShowHide__onHide = InfoBarHide
		InfoBarHide = None
	if InfoBarToggle:
		InfoBarShowHide.toggleShow = InfoBarToggle
		InfoBarToggle = None


def InfoBarShowTunerState(self):
	global InfoBarShow
	if InfoBarShow:
		InfoBarShow(self)
	
	show = False
	player = type(self).__name__ != "InfoBar"
		
	if player and config.infobartunerstate.show_withplayer.value == "True":
			show = True
	elif not player and config.infobartunerstate.show_withinfobar.value == "True":
			show = True
	
	if show:
		from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
		if gInfoBarTunerState:
			gInfoBarTunerState.show()

def InfoBarHideTunerState(self):
	from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
	global InfoBarHide
	if InfoBarHide:
		InfoBarHide(self)
	# Always hide
	if gInfoBarTunerState:
		gInfoBarTunerState.hide()

def InfoBarToggleTunerState(self):
	global InfoBarToggle
	if InfoBarToggle:
		InfoBarToggle(self)
	
	if self._InfoBarShowHide__state == self.STATE_HIDDEN:
		# Always hide
		from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
		if gInfoBarTunerState:
			gInfoBarTunerState.hide()
		
	elif self._InfoBarShowHide__state == self.STATE_SHOWN:
		
		show = False
		player = type(self).__name__ != "InfoBar"
		
		if player and config.infobartunerstate.show_withplayer.value == "only_onkeypress":
			show = True
		elif not player and config.infobartunerstate.show_withinfobar.value == "only_onkeypress":
			show = True
		
		if show:
			from Plugins.Extensions.InfoBarTunerState.plugin import gInfoBarTunerState
			if gInfoBarTunerState:
				gInfoBarTunerState.show()

class InfoBarHandler(object):
	def __init__(self):
		
		overwriteInfoBar()
		
		# Handle extension menu integration
		if config.infobartunerstate.extensions_menu_show.value or config.infobartunerstate.extensions_menu_setup.value:
			# Add to extension menu
			addExtension()
		else:
			# Remove from extension menu
			removeExtension()

	def undoHandler(self):
		recoverInfoBar()
		removeExtension()
