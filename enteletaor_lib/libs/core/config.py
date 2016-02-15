# -*- coding: utf-8 -*-


# ----------------------------------------------------------------------
def get_user_config_path():
	"""

	"""


# ----------------------------------------------------------------------
def get_project_config_path():
	"""

	"""


# ----------------------------------------------------------------------
def load_config():
	"""
	Fill global structures with user params
	"""

	try:
		from config import __author__, __name__, __site__, __version__
	except ImportError:
		__author__ = __name__ = __site__ = __version__ = "unknown"

	from .structs import AppSettings

	AppSettings.author = __author__
	AppSettings.tool_name = __name__
	AppSettings.project_site = __site__
	AppSettings.version = __version__
