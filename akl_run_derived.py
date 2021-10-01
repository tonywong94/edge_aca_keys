#!/usr/bin/env python
# 
# Run this script inside pure python
# 

##############################################################################
# Load routines, initialize handlers
##############################################################################

import os, sys
import importlib

# Locate the master key
key_file = '/data/tycho/0/leroy.42/reduction/alma/edge_aca_keys/akl_edgeaca_keys/akl_master_key.txt'

# Set directory for the pipeline and change to this directory
pipedir = '/data/tycho/0/leroy.42/reduction/alma/phangs_imaging_scripts/'
os.chdir(pipedir)

# Set the logging
from phangsPipeline import phangsLogger as pl
importlib.reload(pl)
pl.setup_logger(level='DEBUG', logfile=None)

# Imports

#sys.path.insert(1, )
from phangsPipeline import handlerKeys as kh
from phangsPipeline import handlerDerived as der

# Reloads for debugging
importlib.reload(kh)
importlib.reload(der)

# Initialize key handler

this_kh = kh.KeyHandler(master_key = key_file)
this_der = der.DerivedHandler(key_handler= this_kh)

# Make missing directories

this_kh.make_missing_directories(imaging=True,derived=True,postprocess=True,release=True)

# ACA only

this_der.set_targets()
this_der.set_no_cont_products(True)
this_der.set_interf_configs(only=['7m'])
this_der.set_feather_configs()
this_der.set_line_products(only=['co21'])

do_convolve = True
do_noise = True
do_strictmask = True
do_broadmask = True
do_moments = True
do_secondary = True

##############################################################################
# Step through derived product creation
##############################################################################

if do_convolve:
    this_der.loop_derive_products(do_convolve = True, do_noise = False, 
                                  do_strictmask = False, do_broadmask = False,
                                  do_moments = False, do_secondary = False)

if do_noise:
    this_der.loop_derive_products(do_convolve = False, do_noise = True, 
                                  do_strictmask = False, do_broadmask = False,
                                  do_moments = False, do_secondary = False)

if do_strictmask:
    this_der.loop_derive_products(do_convolve = False, do_noise = False, 
                                  do_strictmask = True, do_broadmask = False,
                                  do_moments = False, do_secondary = False)

if do_broadmask:
    this_der.loop_derive_products(do_convolve = False, do_noise = False, 
                                  do_strictmask = False, do_broadmask = True,
                                  do_moments = False, do_secondary = False)

if do_moments:
    this_der.loop_derive_products(do_convolve = False, do_noise = False, 
                                  do_strictmask = False, do_broadmask = False,
                                  do_moments = True, do_secondary = False)

if do_secondary:
    this_der.loop_derive_products(do_convolve = False, do_noise = False, 
                                  do_strictmask = False, do_broadmask = False,
                                  do_moments = False, do_secondary = True)
