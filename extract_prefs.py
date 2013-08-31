#!/usr/bin/python

from bs4 import BeautifulSoup
import re
import urllib
import json

GTV_BASE_URL = "http://www.abc.net.au/news/federal-election-2013/guide/gtv/"
STATES = ["nsw", "vic", "qld", "wa", "sa", "tas", "act", "nt"]

PARTY_NAME = {
    'Australian Christian' : 'Australian Christians',
    'Australian Greens' : 'Greens',
    "Australian Labor Party (Northern Territory) Branch" : "Australian Labor Party",
    'Australian Motoring Enthusiast Party' : 'Australian Motoring Enthusiasts Party',
    'Australian Voice' : 'Australian Voice Party',
    "A.F.N.P.P." : "Australia First Party",
    'Building Australia' : 'Building Australia Party',
    'Bullet Train For Australia' : 'Bullet Train for Australia',
    'Christian Democratic Party (Fred Nile Group)' : 'Christian Democratic Party',
    'Country Liberals (NT)' : 'Country Liberals',
    'DLP Democratic Labour' : 'Democratic Labour Party',
    'Democratic Labour Party (DLP)' : 'Democratic Labour Party',
    'Drug Law Reform Australia' : 'Drug Law Reform',
    'Family First Party' : 'Family First',
    'Help End Marijuana Prohibition (HEMP) Party' : 'Help End Marijuana Prohibition',
    "Labor" : "Australian Labor Party",
    "Liberal" : "Liberal Party",
    'Liberal / The Nationals' : 'Liberal National Party',
    'Liberal National Party of Queensland' : 'Liberal National Party',
    'Liberal and Nationals' : 'Liberal National Party',
    "Liberal Democrats" : "Liberal Democratic Party",
    'Pirate Party Australia' : 'Pirate Party',
    'Republican Party Australia' : 'Australian Republicans',
    'Rise Up Australia Party' : 'Rise Up Australia',
    'Senator Online (Internet Voting Bills/Issues)' : 'Senator OnLine',
    'Sex Party' : 'Australian Sex Party',
    'Shooters and Fishers Party' : 'Shooters and Fishers',
    'Smokers Rights Party' : 'Smokers Rights',
    'Stop CSG Party' : 'Stop CSG',
    'Stop The Greens' : 'Outdoor Recreation Party (Stop the Greens)',
    'The Australian Republicans' : 'Australian Republicans',
    'The Greens' : 'Greens',
    'The Greens (WA)' : 'Greens',
    'The Nationals' : 'National Party',
    '-': '_'
}
def normalisePartyName(name):
    name = name.strip()
    return PARTY_NAME.get(name, name)

DUMP = False

re_grouphd = re.compile('Group ([A-Z]+): *(.*)$')
def readstate(state):
    result = {}
    soup = BeautifulSoup(urllib.urlopen(GTV_BASE_URL+state+"/").read())
    for h2 in soup.find_all('h2'):
        groupname = h2.text
        tbl = h2.find_next_sibling('table')
        if tbl:
            htmlrows = tbl.find('tbody').find_all('tr')
            drows = [ dict([(t['class'][0], (t['class'][0] == 'preference' and int(t.text) or (t['class'][0] == 'party' and normalisePartyName(t.text) or t.text))) for t in r.find_all('td')]) for r in htmlrows]
            result[groupname] = drows
    return result


re_multiticket = re.compile("(.*) \(Ticket (\d+) of \d+\)")
party_tickets = {}
party_states = {}
for state in STATES:
    statedata = readstate(state)
    print "State %s: %d groups"%(state,len(statedata))
    for (groupname,rows) in statedata.iteritems():
        (groupid, partyname) = re_grouphd.match(groupname).groups()
        m = re_multiticket.match(partyname)
        if m:
            partyname = m.group(1)
        partyname = normalisePartyName(partyname)
        party_tickets.setdefault(partyname, []).append(rows)
        party_states.setdefault(partyname, set()).add(state)

# now party_tickets  == party -> [  [  { 'preference': , 'candidate':, 'party':} ] ]
# and party_states   == party -> set([state, state, ...])

#print party_tickets.values()[0][0][0]

# now compute the each party's average preference per other party

# the outgoing preferences of parties
# party -> { party : average preference}
prefgive = {}

# the received preferences of parties
# party -> { party : avgpref }
prefrecv = {}

recvtally = {}  # recipient -> {  donor -> [ pref, ] }
for (party, papers) in party_tickets.iteritems():
    preftally = {}  # party -> [pref, ...]
    for paper in papers:
        for d in paper:
#            print d
            preftally.setdefault(d['party'], []).append(d['preference'])
            recvtally.setdefault(d['party'], {}).setdefault(party,[]).append(d['preference'])
    partyavgs = []
    for (p, tally) in preftally.iteritems():
        partyavgs.append(dict(name=p, pref=float(sum(tally))/len(tally)))
    partyavgs.sort(key=lambda d:d['pref'])
    prefgive[party] = partyavgs

for (r,ds) in recvtally.iteritems():
    prefrecv[r] = []
    # k = receiving party; v = { donor: [pref, ...]}
    for (d, tally) in ds.iteritems():
        prefrecv[r].append(dict(name=d, pref=float(sum(tally))/len(tally)))
    prefrecv[r].sort(key=lambda d:d['pref'])


with open('avgprefs.json', 'w') as fp:
    json.dump(dict(
        given=prefgive, 
        received=prefrecv,
        states=dict([(k, list(v)) for (k,v) in party_states.iteritems()])), 
    fp)


if DUMP:
    for (party, avgs) in avgpref.iteritems():
        print "Average preferences of %s"%party
        avgs.sort(key = lambda i:i['pref'])
        for avg in avgs:
            print "%2.1f %s"%(avg['pref'],avg['name'])
