#!/usr/bin/python

"""
Calculate salient preference positions, by the order in which the various parties have certain key parties
"""

KEYPARTIES = set(['Australian Labor Party', 'Liberal Party', 'National Party', 'Greens', 'One Nation'])

import json

avgpref = json.load(open("avgprefs.json"))['given']

ordergroup = {}

for (party, prefs) in avgpref.iteritems():
	preflist = [ d for d in prefs if d['name'] in KEYPARTIES]
	preflist.sort(key=lambda (d):d['pref'])
	order = ','.join([d['name'] for d in preflist])
	ordergroup.setdefault(order, []).append(party)

for (order, parties) in ordergroup.iteritems():
	print "Parties preferencing in order %s:"%order
	for party in parties:
		print " ", party
