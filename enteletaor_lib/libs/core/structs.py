# -*- coding: utf-8 -*-

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
			r.append("%s: %s" % (x, str(v)))

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
