#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for 'phylore.nexus.reader', using nose.

"""


### IMPORTS ###

from phylo.nexus.reader import NexusReader


## CONSTANTS & DEFINES ###

ANN_TREE_FILE = "tests/in/big.nex"


### TESTS ###

def test_annotated_tree():
	rdr = NexusReader({'node_annotations': True})
	t1 = rdr.read (ANN_TREE_FILE)
	t1._validate()
	t1._dump()

	

### END ####################################################################