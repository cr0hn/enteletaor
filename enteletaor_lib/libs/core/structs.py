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
This module contains common data information
"""
import six

from argparse import Namespace

from .models import (BaseField, IntegerField, StringField,
                     FloatField, Model, validators,
                     IncrementalIntegerField)


# --------------------------------------------------------------------------
class CommonData(Model):
	"""Common settings for all projects"""

	# ----------------------------------------------------------------------
	@property
	def vars(self):
		"""
		Get class vars

		:return: dict as format dict(str: _BaseType)
		:rtype: dict(str:model._BaseType)

		"""
		return self._fields

	# ----------------------------------------------------------------------
	def __init__(self, **kwargs):
		"""
		Match inputs with vars
		"""
		super(CommonData, self).__init__(**kwargs)

		if self.validate() is False:
			raise TypeError("\n".join("'%s' <- %s" % (x, y) for x, y in six.iteritems(self.errors)))

		# Add extra vars from modules
		try:
			module_name = kwargs['module_name']
			fake_kwargs = dict(kwargs)

			# Add metavars: action / subactions
			self.action = fake_kwargs.pop('module_name')
			self.sub_action = None

			# Is a sub-action selected
			for x, y in six.iteritems(fake_kwargs):
				if x.startswith("module_"):
					self.sub_action = fake_kwargs.pop(x)
					break

			module_model = getattr(AppSettings.modules[module_name], "__model__", None)

			if module_model is not None:
				# Load module model to check parameters
				module_model(**fake_kwargs)

				# If not errors, set vars and values
				for x, v in six.iteritems(fake_kwargs):
					if x not in self.vars:
						setattr(self, x, v)
		except KeyError:
			# No module name available -> not an error. Class must be loading from another locations
			pass

	# ----------------------------------------------------------------------
	@classmethod
	def from_argparser(cls, argparse_data):
		"""
		Load parameters from argparser
		"""

		if not isinstance(argparse_data, Namespace):
			raise TypeError("Expected Namespace, got '%s' instead" % type(argparse_data))

		return cls(**argparse_data.__dict__)

	# ----------------------------------------------------------------------
	def __repr__(self):
		r = []
		for x, v in six.iteritems(self.vars):
			try:
				r.append("%s: %s" % (x, str(v)))
			except TypeError:
				r.append("%s: %s" % (x, str(v.data)))

		return "\n".join(r)


# --------------------------------------------------------------------------
class CommonInputExecutionData(CommonData):
	"""Common information to run program"""

	verbosity = IncrementalIntegerField("global verbosity level of app (0-5).", default=1)


# --------------------------------------------------------------------------
class CommonResultsExecutionData(CommonData):
	"""Common information to run program"""

	start_execution = FloatField(default="0.0")
	end_execution = FloatField(default="0.0")
	end_execution_status = IntegerField(default=0)
	end_execution_message = StringField(default="Oks")


# --------------------------------------------------------------------------
class _AppSettings(CommonData):
	"""Global app settings"""

	tool_name = StringField(validators.length(max=80), default="")
	author = StringField(validators.length(max=200), default="")
	project_site = StringField(validators.length(max=255), default="")
	version = StringField(validators.length(max=20), default="")

	# Loaded dinamically
	hooks = None
	modules = None
	parallel_running = False

AppSettings = _AppSettings()
