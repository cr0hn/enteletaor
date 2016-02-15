# -*- coding: utf-8 -*-


def boot_loader():
	"""
    Load app
    """
	# --------------------------------------------------------------------------
	# Local import to avoid locks
	# --------------------------------------------------------------------------
	from ...modules import find_modules
	from ..hooks import find_hooks
	from .config import load_config
	from .structs import AppSettings
	from .logger import setup_logging
	from .cmd import setup_cmd

	# Load config
	load_config()

	# Config logging
	setup_logging()

	# Config command line
	setup_cmd()

	# Load hooks
	AppSettings.hooks = find_hooks()

	# Load modules
	AppSettings.modules = find_modules()

	# Check imports

	# Load libraries

	# Load modules
