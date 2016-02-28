# -*- coding: utf-8 -*-

import logging

from .. import IModule

from ...libs.core.structs import CommonData
from ...libs.core.models import StringField, BoolField, IntegerField, FloatField

from .scan_main import action_scan_main

log = logging.getLogger()


# ----------------------------------------------------------------------
class ModuleModel(CommonData):
	ports = StringField(default="5672,6379,5555", label="comma separated ports")
	target = StringField(required=True)
	own_ips = BoolField(label="Try to find all IPs registered for this company")
	concurrency = IntegerField(label="maximum parallels scans", default=10)
	output = StringField(label="output file, in JSON format")
	timeout = FloatField(label="timeout for socket connections", default=0.2)


# ----------------------------------------------------------------------
class ScanProcessModule(IModule):
	"""
	Try to extract information from remote processes
	"""
	__model__ = ModuleModel
	__submodules__ = {
		'default': dict(
			action=action_scan_main
		)
	}

	name = "scan"
	description = "do a scans trying to find open brokers / MQ"
