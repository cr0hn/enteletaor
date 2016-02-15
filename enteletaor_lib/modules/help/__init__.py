# -*- coding: utf-8 -*-

from libs.core.structs import CommonData
from libs.core.models import FloatField
from .. import IModule


class ModuleModel(CommonData):
	start_execution = FloatField(default=1.0)
	end_execution = FloatField(default=1.2)


# ----------------------------------------------------------------------
class HelpModule(IModule):
	"""
	Long description of module
	"""

	__model__ = ModuleModel

	name = "help"
	description = "long description"

	# ----------------------------------------------------------------------
	def run(self, config):
		print("hoooola")

