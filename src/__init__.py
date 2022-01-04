# -*- coding: utf-8 -*-
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from os import environ as os_environ
import gettext

from Components.config import config, ConfigSubsection, ConfigNothing, ConfigYesNo, ConfigSelectionNumber, ConfigSelection, ConfigEnableDisable, ConfigText


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
