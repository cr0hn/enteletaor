# -*- coding: utf-8 -*-

"""
This file contains command line actions for argparser
"""


# ----------------------------------------------------------------------
def parser_proc_raw_dump(parser):
	gr = parser.add_argument_group("custom raw dump options")

	gr.add_argument("--streaming", action="store_true", dest="streaming_mode", default=False,
	                help="although all information be dumped do not stop")
	gr.add_argument("-I", dest="interval", type=float, default=4,
	                help="timeout interval between tow connections")
	gr.add_argument("--output", dest="output", help="store dumped information into file")


# ----------------------------------------------------------------------
def parser_proc_list_tasks(parser):
	parser.add_argument("-N", "--no-stream", dest="no_stream", action="store_true", default=False,
	                    help="force to not listen until message is received")

	gr = parser.add_argument_group("process exporting options")

	gr.add_argument("-T", "--make-template", dest="template", type=str,
	                help="export process as a JSON template format, ready to make injections")
	gr.add_argument("-F", "--function-name", dest="function_name", type=str,
	                help="only export this function name")


# ----------------------------------------------------------------------
def parser_taks_inject_process(parser):
	gr = parser.add_argument_group("process importing options")

	gr.add_argument("-f", "--function-file", dest="function_files", type=str, required=True,
	                help="import process info from JSON file")
