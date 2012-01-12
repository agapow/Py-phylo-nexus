#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class for reading trees in Nexus format.

This currently quite hacky and throws most of the work to the newick parser.
"""
# TODO: currently we read just the first tree.

__docformat__ = 'restructuredtext'


### IMPORTS

import re, cStringIO

from phylo.core import io
from phylo.core.tree import Tree

from phylo.newick import NewickReader


### CONSTANTS & DEFINES ###

_TREE_BLK_REGEX = re.compile (r"BEGIN TREES;\s+(.*)End;", 
	re.IGNORECASE + re.MULTILINE + re.DOTALL)
_TRANS_TABLE_REGEX = re.compile (r"TRANSLATE\s+([^;]*);", 
	re.IGNORECASE + re.MULTILINE + re.DOTALL)
FIRST_TREE_REGEX = re.compile (r"TREE\s+([^;]*;)", 
	re.IGNORECASE + re.MULTILINE + re.DOTALL)
TREE_STR_REGEX = re.compile (r"\s+(\([^;]*);", 
	re.IGNORECASE + re.MULTILINE + re.DOTALL)


### IMPLEMENTATION ###

class NexusReader (io.BaseReader):

	def __init__ (self, dialect={}, tree_kls=Tree):
		io.BaseReader.__init__ (self, dialect=dialect)
		self._newick_rdr = NewickReader (dialect=self.dialect, tree_kls=Tree)

	def _read (self, src):
		"""
		Read the passed tree and return a Phylotree structure.

		:Params:
			src
				An open file or file-like object.

		:Returns:
			A phylotree.

		"""
		## Preconditions & preparation:

		## Main:
		file_str = src.read()
		m = _TREE_BLK_REGEX.search (file_str)
		assert (m), "can't find tree block"
		blk_str = m.group(1)
		
		m = _TRANS_TABLE_REGEX.search (blk_str)
		if m:
			trans_str = m.group(1)
			lines = trans_str.split(',')
			prs = [x.strip().split(' ', 1) for x in lines]
			table = {}
			for p in prs:
				k = p[0]
				v = p[1]
				if v.startswith('\''):
					v = v[1:-1]
				table[k] = v
		else:
			table = {}
		
		m = FIRST_TREE_REGEX.search (blk_str)
		assert (m), "can't find tree entry in block"
		tree_line = m.group(1)
		
		m = TREE_STR_REGEX.search (tree_line)
		assert (m), "can't find newick tree in line"		
		tree_src = cStringIO.StringIO (m.group(1))
		t = self._newick_rdr.read (tree_src)

		if table:
			for n in t.iter_nodes():
				new_name = table.get(n.title, None)
				if new_name:
					n.title = new_name

		return t

### TEST & DEBUG ###

def _doctest ():
   import doctest
   doctest.testmod ()


### MAIN ###

if __name__ == '__main__':
   _doctest()


### END ######################################################################
