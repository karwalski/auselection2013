#!/usr/bin/python

"""
Process the average-preferences file into a force-directed graph structure of the sort D3 likes.
"""

import json
import math
import colorsys

PARTY_RGB = {
	'Greens' : (0.0,0.75,0.0),
	'Australian Labor Party' : (0.75, 0.0, 0.0),
	'Liberal Party' : (0.0, 0.0, 0.75),
	'National Party' : (0.333, 5.5/15.0, 1.0/15.0),
#	'Australia First Party' : (-0.1, -0.1, -0.2),
}

def partyAffinity(a,b):
	"""Returns the closeness between two parties, from epsilon (not close at all) to 1 (the same party)"""
	rows = [row for row in avgpref.get(a,[]) if row['name'] == b]
	if not rows: return 0.0001
	return 1.0/math.sqrt(rows[0]['pref'])

def partyColour(party):
	rgb = PARTY_RGB.get(party)
	if not rgb:
		# calculate the distance 
		r = g = b = 0.6
		for( pb, pbrgb) in PARTY_RGB.iteritems():
			aff = partyAffinity(party, pb)
			r += pbrgb[0]*aff*2
			g += pbrgb[1]*aff*2
			b += pbrgb[2]*aff*2
		nastiness = partyAffinity(party, "Australia First Party")+partyAffinity(party, "One Nation")
		(r,g,b) = [max(0.0, v) for v in (r,g,b)]
		scale = min(1.0, 1.0/max([r,g,b]))
		(h,s,v) = colorsys.rgb_to_hsv(r,g,b)
		if party.lower().find('socialist') > -1:
			h = (h*0.1)
		if party.lower().find('christian') > -1:
			h = 0.65 + (h*0.1)
		v *= (1.0-math.pow(partyAffinity(party, "Australia First Party"), 0.25))
		rgb = colorsys.hsv_to_rgb(h, 0.55+(s*0.1), (1.0-(nastiness*0.75))*max(0.2+(v*0.5), 0.9))
	return '#%02x%02x%02x'%(rgb[0]*255.0, rgb[1]*255.0, rgb[2]*255.0)

avgpref = json.load(open("avgprefs.json"))['given']

maxavg = max([ max([d['pref'] for d in l]) for l in avgpref.values() ])

parties = set(avgpref.keys())
for d in avgpref.values():
    parties.update([v['name'] for v in d])
parties = list(parties)
parties.sort()
print "parties = ", parties
partyIndex = dict([(v,k) for (k,v) in enumerate(parties)])

nodes = [ dict(name=p, colour=partyColour(p)) for p in parties]
links = []

for (pa, recipients) in avgpref.iteritems():
    for d in recipients:
        links.append(dict(source=partyIndex[pa], target=partyIndex[d['name']], value=1.0/d['pref']))

with open('fdg.json', 'w') as fp:
    json.dump(dict(nodes=nodes, links=links), fp)