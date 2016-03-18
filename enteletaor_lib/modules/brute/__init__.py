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

import logging

from .. import IModule

from ...libs.core.structs import CommonData
from ...libs.core.models import StringField, IntegerField, FloatField

from .cmd_brute_main import cmd_brute_main
from .cmd_list_wordlists import cmd_list_wordlists

log = logging.getLogger()


# ----------------------------------------------------------------------
class ModuleModel(CommonData):
	port = StringField(default="6379")
	target = StringField()
	wordlist = StringField(default="10_million_password_list_top_1000")
	user = StringField(label="user for login to (optional)")
	concurrency = IntegerField(label="maximum parallels scans", default=10)
	timeout = FloatField(label="timeout for socket connections", default=0.2)


# ----------------------------------------------------------------------
class BruteProcessModule(IModule):
	"""
	Try to extract information from remote processes
	"""
	__model__ = ModuleModel
	__submodules__ = {
		'password': dict(
			help="do password brute forcer discover over the brokers/MQ",
			action=cmd_brute_main
		),
		'wordlist': dict(
			help="list internal available wordlist",
			action=cmd_list_wordlists
		),
	}

	name = "brute"
	description = "try to discover valid passwords in remote brorkers/MQ"
