#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IO classes for reading and writing to Nexus format. 

Requires phylo.newick and phylo.core.

"""

__docformat__ = 'restructuredtext en'
__author__ = "P-M Agapow <pma@agapow.net>"
__version__ = "0.1"


### IMPORTS ###

from dialect import *
from reader import *
from writer import *


### TEST & DEBUG ###

def _doctest ():
   import doctest
   doctest.testmod ()


### MAIN ###

if __name__ == '__main__':
   _doctest()


### END ########################################################################
