# -*- coding: utf-8 -*-
#
# Enteletaor - https://github.com/cr0hn/enteletaor
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


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
