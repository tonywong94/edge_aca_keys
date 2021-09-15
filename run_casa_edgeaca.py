#!/usr/bin/env python
# 
# Run this script inside CASA!
# 

##############################################################################
# Load routines, initialize handlers
##############################################################################

import os, sys

# Locate the master key
key_file = '/data2/wongt/aca_edge/edge_aca_keys/master_key_adata.txt'

# Set directory for the pipeline and change to this directory
pipedir = '/home/wongt/casa/phangs_imaging_scripts/'

sys.path.append('/home/wongt/casa/analysis_scripts/')
os.chdir(pipedir)

# Make sure we are inside CASA (modify this to use the command line version)
sys.path.append(os.getcwd())
casa_enabled = (sys.argv[0].endswith('start_casa.py'))
if not casa_enabled:
    print('Please run this script inside CASA!')
    sys.exit()

# Set the logging
from phangsPipeline import phangsLogger as pl
reload(pl)
pl.setup_logger(level='DEBUG', logfile=None)

# Imports

#sys.path.insert(1, )
from phangsPipeline import handlerKeys as kh
from phangsPipeline import handlerVis as uvh
from phangsPipeline import handlerImaging as imh
from phangsPipeline import handlerPostprocess as pph
#import statsHandler as sth

# Reloads (for debugging, can remove this in a non-debugging session)
reload(kh)
reload(uvh)
reload(imh)
reload(pph)
#reload(sth)

# Initialize the handlers
this_kh = kh.KeyHandler(master_key = key_file)
this_uvh = uvh.VisHandler(key_handler = this_kh)
this_imh = imh.ImagingHandler(key_handler = this_kh)
this_pph = pph.PostProcessHandler(key_handler= this_kh)
#this_sth = sth.StatsHandler(key_handler= this_kh)

# Make missing directories (optional)
this_kh.make_missing_directories(imaging=True,derived=True,postprocess=True,release=True)

##############################################################################
# Set up what we do this run
##############################################################################

# Set things to ACA only (7m and 7m+tp) and specify any targets


gals = ['UGC11680NED02']
this_uvh.set_targets(only=gals)
this_uvh.set_interf_configs(only=['7m'])
this_uvh.set_line_products()
this_uvh.set_no_cont_products(True)
# ,'ngc1097_lin','ngc1097_lpc'
this_imh.set_targets(only=gals)
this_imh.set_interf_configs(only=['7m'])


# this_pph.set_targets(only=['ngc1097'])
# this_pph.set_interf_configs(only=['7m'])
# this_pph.set_feather_configs(only=['7m+tp'])

# Switches for what steps to run

do_staging = True
do_imaging = True
do_postprocess = True
do_stats = False

##############################################################################
# Run staging
##############################################################################

if do_staging:

    this_uvh.loop_stage_uvdata(do_copy=True, do_contsub=True, 
                               do_extract_line=False, do_extract_cont=False,
                               do_remove_staging=False, overwrite=True)
    
    this_uvh.loop_stage_uvdata(do_copy=False, do_contsub=False, 
                               do_extract_line=True, do_extract_cont=False,
                               do_remove_staging=False, overwrite=True)
    
    this_uvh.loop_stage_uvdata(do_copy=False, do_contsub=False, 
                               do_extract_line=False, do_extract_cont=True,
                               do_remove_staging=False, overwrite=True)
    
    this_uvh.loop_stage_uvdata(do_copy=False, do_contsub=False, 
                               do_extract_line=False, do_extract_cont=False,
                               do_remove_staging=True, overwrite=True)
    
##############################################################################
# Step through imaging
##############################################################################

# Needs to run in CASA 5.4.0

if do_imaging:

    this_imh.loop_imaging(do_all = True)

##############################################################################
# Step through postprocessing
##############################################################################

if do_postprocess:

    this_pph.loop_postprocess(do_prep = True, do_feather = False, 
                              do_mosaic = True, do_cleanup = True)

##############################################################################
# Run stats on the residual
##############################################################################

if do_stats:

    this_sth.set_targets()
    this_sth.set_interf_configs(only=['7m'])
    this_sth.set_no_cont_products(True)
    this_sth.set_line_products(only=['co21'])
    this_sth.go(
        outfile_singlescale='stats_singlesale_7m.json',
        outfile_multiscale='stats_multiscale_7m.json',
        )


