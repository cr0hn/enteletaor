#!/usr/bin/env python

#
# Fork of:
#
# https://github.com/UndergroundLabs/ripe-inetnum-search
#

import six
import json
import netaddr
import requests
import logging


# ----------------------------------------------------------------------
def get_inet_num(search_term):
	"""
	Get intetnums for a domain
	
	:param search_term: keywork without dots, no domains are allowed. domain.com -> invalid |---| domain -> valid
	:type search_term: str

	:return: iterable with IP/CIDR notation or None 
	:rtype: list(str) | None
	
	"""
	# Disable request logging
	requests_log = logging.getLogger("requests")
	requests_log.addHandler(logging.NullHandler())
	requests_log.propagate = False

	# Search the RIPE database
	# There is an issue with RIPE. When making a request and including
	# the type-filter inetnum, the JSON response also includes other types.
	request = requests.get('http://rest.db.ripe.net/search.json', params={
		'query-string': search_term,
		'type-filter': 'inetnum'
	})

	json_results = json.loads(request.text)

	try:
		# Filter any object that doesn't have the type 'inetnum'
		ranges = [x['primary-key']['attribute'][0]['value']
		          for x in json_results['objects']['object']
		          if x['type'] == 'inetnum']
	except KeyError:
		return None

	# Turn the IP range string into CIDR
	cidrs = []
	for _range in ranges:
		_range = _range.split(' - ');
		cidrs.append(netaddr.iprange_to_cidrs(_range[0], _range[1]))

	results = set()

	# Print the CIDR's
	for cidr in cidrs:
		results.add(str(cidr[0]))

	return results