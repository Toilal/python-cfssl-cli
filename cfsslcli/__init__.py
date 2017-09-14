#!/usr/bin/python
# -*- coding: utf-8 -*-

import pkg_resources

__version__ = None
try:
    __version__ = pkg_resources.require('cfsslcli')[0].version
except pkg_resources.DistributionNotFound as e:
    pass
