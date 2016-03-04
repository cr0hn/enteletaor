# -*- coding: utf-8 -*-

from __future__ import absolute_import


# ----------------------------------------------------------------------
def load_config():
	"""
	Fill global structures with user params
	"""

	try:
		from config import __author__, __tool_name__, __site__, __version__
	except ImportError:
		__author__ = __tool_name__ = __site__ = __version__ = "unknown"

	from .structs import AppSettings

	AppSettings.author = __author__
	AppSettings.tool_name = __tool_name__
	AppSettings.project_site = __site__
	AppSettings.version = __version__
