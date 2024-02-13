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
import pdb


for sub in ['001','002','003','004','005','006','007','008','009','010','011','012']:
#for sub in ['003']:
	
	for ses in ['01','02','03','04']:
		

		path_ = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s' %(sub,ses)
		if os.path.isdir(path_):


			aux_img_path='/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func/sub-%s_ses-%s_task-rest_run-1_space-T1w_desc-residuals_variant-Motion24aCompCor6GSR4_bold_figures' %(sub,ses,sub,ses)
			fd_ind = aux_img_path+'/fd_ind.npy'
			#pdb.set_trace()
			
			print(sub)
			print(ses)
			select = np.load(fd_ind)
			select_i = np.invert(select)
			
			out_path_img = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func/' %(sub,ses)
			tt = 'sub-%s_ses-%s_task-rest_run-1_space-T1w_desc-residuals_variant-Motion24aCompCor6GSR4_bold.nii.gz' %(sub, ses)
			tt_s = 'sub-%s_ses-%s_task-rest_run-1_space-T1w_desc-residuals_variant-Motion24aCompCor6GSR4_bold_scrubbed.nii.gz' %(sub, ses)
			datanifti = nib.load(out_path_img+tt)
			#pdb.set_trace()
			select_i=np.squeeze(select_i)
			scrubbeddata = datanifti.get_data()[:,:,:,select_i]
			newNii = nib.Nifti1Pair(scrubbeddata,None,datanifti.get_header())
			nib.save(newNii,out_path_img+tt_s)
			
