import numpy as np
import numpy.ma
import nibabel as nib
from nipype.interfaces import afni
from nipype.algorithms import confounds
import os, sys, subprocess
import string, random
import re
import logging
import math
import argparse
from argparse import ArgumentParser
from nilearn import plotting
import os.path
import matplotlib as plt
import shutil

sess = ['001','002','003','004','005','006','007','008','009','010','011','012','013','014','015','016','017','018','019','020','021','022','023','024']

runs = ['001','002']
subs= ['001']

epi_space ='T1w_desc'

for sub in subs:
	
	for ses in sess:

		
		for run in runs:

			#if not os.path.isdir(out_path):
			#	os.mkdir(out_path)
			aux_img_path='/home/despo/ioannis/Berkeley_research1/scantrain/data/derivatives_rest/sub-%s/ses-%s/run-%s/sub-%s_ses-%s_task-rest_run-%s_space-T1w_desc-residuals_variant-30p_Acc6_065_1_bold_figures' %(sub,ses,run,sub,ses,run)
			fd_ind = aux_img_path+'/fd_ind.npy'
			try:
				select = np.load(fd_ind)
				select_i = np.invert(select)
				select_i=np.squeeze(select_i)
				out_path_img = '/home/despo/ioannis/Berkeley_research1/scantrain/data/derivatives_rest/sub-%s/ses-%s/run-%s/' %(sub,ses,run)
				tt = 'sub-%s_ses-%s_task-rest_run-%s_space-%s-residuals_variant-30p_Acc6_065_1_bold.nii.gz' %(sub, ses, run, epi_space)
				tt_s = 'sub-%s_ses-%s_task-rest_run-%s_space-%s-residuals_variant-30p_Acc6_065_1_bold_scrubbed.nii.gz' %(sub, ses, run, epi_space)
				datanifti = nib.load(out_path_img+tt)
				scrubbeddata = datanifti.get_data()[:,:,:,select_i]
				newNii = nib.Nifti1Pair(scrubbeddata,None,datanifti.get_header())
				nib.save(newNii,out_path_img+tt_s)
			except:
				pass
