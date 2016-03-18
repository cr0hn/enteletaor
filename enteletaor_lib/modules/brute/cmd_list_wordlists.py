# -*- coding: utf-8 -*-

import os
import logging


log = logging.getLogger()


# ----------------------------------------------------------------------
def cmd_list_wordlists(config):
	"""
	Get all internal wordlist
	"""
	base_wordlists = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "resources", "wordlist"))

	log.error("  - Available wordlists:")
	for w in os.listdir(base_wordlists):
		if "readme" not in w.lower():
			log.error("    > %s" % w[:w.find(".txt")])
