# -*- coding: utf-8 -*-

"""
This file contains command line actions for argparser
"""


# ----------------------------------------------------------------------
def parser_proc_raw_dump(parser):
	parser.add_argument("--tail", action="store_true", dest="tail_mode", default=False,
	                    help="although all information be dumped do not stop")
	parser.add_argument("-I", dest="interval", type=float, default=4,
	                    help="timeout interval between tow connections")
