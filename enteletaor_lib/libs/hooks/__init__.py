# -*- coding: utf-8 -*-


"""
This file contains utils for handle decorators
"""

import logging
import functools

from collections import defaultdict

log = logging.getLogger()


# --------------------------------------------------------------------------
# Config decorators
# --------------------------------------------------------------------------
def on_config_loaded(func):
	"""
	This decorator mark a function or method as hook to run when:

	Running config is loaded
	"""
	@functools.wraps(func)
	def func_wrapper(*args, **kwargs):
		return func(*args, **kwargs)

	func_wrapper.hook_type = "config"

	return func_wrapper


# --------------------------------------------------------------------------
# Find hooks
# --------------------------------------------------------------------------
def find_hooks():
	"""
	Find all hooks and return pointers to functions categorized by hook type.

	:return: dict with hooks and type as format: dict(hook_type: function_pointer)
	:rtype: dict(str: function)

	"""
	import os
	import os.path
	import inspect

	base_dir = os.path.abspath(os.path.dirname(__file__))

	# Modules found
	results = defaultdict(list)

	for root, dirs, files in os.walk(base_dir):
		# Check if folder is a package
		if "__init__.py" not in files:
			continue
		# Remove files or path that starts with "_"
		if any(True for x in root.split("/") if x.startswith("_")):
			continue

		for filename in files:
			if filename.endswith(".py") and \
				not filename.startswith("celery") and \
				not filename.startswith("test_"):

				if filename.startswith("_"):
					if filename != "__init__.py":
						continue

				# loop_file = os.path.join(root, filename)
				loop_file = os.path.join(root, filename) \
					.replace(base_dir, '') \
					.replace(os.path.sep, '.') \
					.replace('.py', '')

				loop_file = loop_file[1:] if loop_file.startswith(".") else loop_file

				# Load module info
				try:
					classes = __import__("%s.%s" % (__package__, loop_file), globals=globals(), locals=locals(), level=loop_file.count("."))
				except ImportError:
					classes = __import__(loop_file, globals=globals(), locals=locals(), level=loop_file.count("."))

				# Get Modules instances
				for m in dir(classes):
					_loaded_module = getattr(classes, m)

					if inspect.isfunction(_loaded_module) and hasattr(_loaded_module, "hook_type"):
						log.debug("Loading hook: %s" % _loaded_module.__name__)
						results[_loaded_module.hook_type].append(_loaded_module)

	return results
