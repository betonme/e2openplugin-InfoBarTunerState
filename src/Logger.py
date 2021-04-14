# -*- coding: utf-8 -*-
#######################################################################
#
#    Series Plugin for Enigma-2
#    Coded by betonme (c) 2012 &lt;glaserfrank(at)gmail.com&gt;
#    Support: http://www.i-have-a-dreambox.com/wbb2/thread.php?threadid=TBD
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

from . import _

import logging

import os
import sys
import traceback

from Components.config import config

from Tools.Notifications import AddPopup
from Screens.MessageBox import MessageBox

from threading import currentThread

log = None


class Logger(object):
	def __init__(self):
		self.instance = logging.getLogger("infobartunerstate")
		self.instance.setLevel(logging.DEBUG)
		
		self.reinit()
	
	def reinit(self):
		self.instance.handlers = [] 
		
		if not hasattr(config, "infobartunerstate"):
			return
		
		if config.infobartunerstate.log_shell.value:
			shandler = logging.StreamHandler(sys.stdout)
			shandler.setLevel(logging.DEBUG)

			sformatter = logging.Formatter('[%(name)s] %(levelname)s - %(message)s')
			shandler.setFormatter(sformatter)

			self.instance.addHandler(shandler)
			self.instance.setLevel(logging.DEBUG)
			
		if config.infobartunerstate.log_write.value:
			fhandler = logging.FileHandler(config.infobartunerstate.log_file.value)
			fhandler.setLevel(logging.DEBUG)

			fformatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
			fhandler.setFormatter(fformatter)

			self.instance.addHandler(fhandler)
			self.instance.setLevel(logging.DEBUG)

	def shutdown(self):
		if self.instance:
			self.instance.shutdown()

	def info(self, *args):
		strargs = " ".join( [ str(arg) for arg in args ] )
		
		if self.instance:
			self.instance.info(strargs)
		
		elif config.infobartunerstate.log_shell.value:
			print strargs

	def debug(self, *args):
		strargs = " ".join( [ str(arg) for arg in args ] )
		
		if self.instance:
			self.instance.debug(strargs)
		
		elif config.infobartunerstate.log_shell.value:
			print strargs
		
		if sys.exc_info()[0]:
			self.instance.debug( str(sys.exc_info()[0]) )
			self.instance.debug( str(traceback.format_exc()) )
			sys.exc_clear()

	def warning(self, *args):
		strargs = " ".join( [ str(arg) for arg in args ] )
		
		if self.instance:
			self.instance.warning(strargs)
		
		elif config.infobartunerstate.log_shell.value:
			print strargs
		
		if int(config.infobartunerstate.popups_warning_timeout.value) != 0:
			if currentThread().getName() == 'MainThread':
				AddPopup(
					strargs,
					MessageBox.TYPE_WARNING,
					int(config.infobartunerstate.popups_warning_timeout.value),
					'IBTS_PopUp_ID_Warning_'+strargs
				)

	def error(self, *args):
		strargs = " ".join( [ str(arg) for arg in args ] )
		
		if self.instance:
			self.instance.error(strargs)
		
		elif config.infobartunerstate.log_shell.value:
			print strargs

		if int(config.infobartunerstate.popups_error_timeout.value) != 0:
			if currentThread().getName() == 'MainThread':
				AddPopup(
					strargs,
					MessageBox.TYPE_ERROR,
					int(config.infobartunerstate.popups_error_timeout.value),
					'IBTS_PopUp_ID_Error_'+strargs
				)
		
	def exception(self, *args):
		strargs = " ".join( [ str(arg) for arg in args ] )
		
		if self.instance:
			self.instance.exception(strargs)
		
		elif config.infobartunerstate.log_shell.value:
			print strargs
		
		if int(config.infobartunerstate.popups_error_timeout.value) != 0:
			if currentThread().getName() == 'MainThread':
				AddPopup(
					strargs,
					MessageBox.TYPE_ERROR,
					int(config.infobartunerstate.popups_error_timeout.value),
					'IBTS_PopUp_ID_Exception_'+strargs
				)
		
		import os
		import sys
		import traceback
		if sys.exc_info()[0]:
			#exc_type, exc_value, exc_traceback = sys.exc_info()
			#traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
			self.debug( str(sys.exc_info()[0]) )
			self.debug( str(traceback.format_exc()) )
			sys.exc_clear()


log = Logger()

