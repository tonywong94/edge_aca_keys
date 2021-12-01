#!/usr/bin/env python

import os, sys, glob
pipedir = '/data2/wongt/aca_edge/phangs_imaging_scripts/'
sys.path.append(pipedir)
from phangsPipeline import scNoiseRoutines as scn

allimg = glob.glob('../imaging/*/*co21.fits')
print(allimg)
for this_base_infile in allimg:
    print("Noise native res for ", this_base_infile)
    scn.recipe_phangs_noise(
        incube=this_base_infile,
        outfile=this_base_infile.replace('.fits','_noise.fits.gz'),
        noise_kwargs={'bandpass_smooth_window':5},
        overwrite=True)

#        noise_kwargs={'bandpass_smooth_window':0,'spec_box':3},
