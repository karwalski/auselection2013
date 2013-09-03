WikiLeaks Party as Default
==========================

Note. this fork is for the WikiLeaks Party to be selected by default, styling adjustments otherwise overall functioning remains similar.

Task, to have the preferences for WikiLeaks Party opened on loading of the page. All other functionality to remain the same.



Original - auselection2013 
==========================

This repository contains code I have written for data analysis and visualisations relating to the Australian federal election of 2013. This includes a [D3](http://d3js.org)-based visualisation of Senate preference affinity (affinity.html) and scripts for fetching and preparing the data for it, as well as a bonus script for categorising parties according to how they order a basket of other parties in their preferences.


Running the visualisation
=========================

To get the visualisation working, you will need to do the following in the directory where the files are:

1)  Run the extract_prefs.py script; this will fetch the preferences from [the ABC's group voting ticket site](http://www.abc.net.au/news/federal-election-2013/guide/gtv/) and process them to generate a file named `avgprefs.json`.
    python extract_prefs.py

2) Run the makefdg.py script to produce `fdg.json`, which contains data for the force-directed graph component of the visualisation and the political party colours:
    python makefdg.json

3) To serve the visualisation locally, start a local HTTP server using Python by running the following command in the code directory:
    python -m SimpleHTTPServer 8000

4) Then go to `http://localhost:8000/affinity.html`, and voilà.

Notes
=====

Note that the code has not been refactored and is probably a lot uglier than it otherwise would be.

Optional extras
===============

- salient1.py

This script processes the contents of `avgprefs.json`, categorises parties by which order they favour a basket of marker parties and prints the list to standard output. It was written for the purpose of writing [this blog post](http://dev.null.org/blog/item/201308240207_australian_election_). The basket of parties is hardcoded to the major parties, the Greens and One Nation (i.e., the ones people are likely to have strong opinions about), but this can be changed fairly easily.
