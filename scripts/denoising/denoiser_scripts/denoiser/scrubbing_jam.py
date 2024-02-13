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

sess = ['001','002','003','004','005','006','007','008','009','010','011','012','013','014','015','016','017','018','019','020','021','022','023','024']

runs = ['001','002','003']
subs= ['001']

epi_space ='T1w_desc'

for sub in subs:
	
	for ses in sess:
		if ses == '001':
			runs = ['001','002']
		else:
			runs =['001','002','003']

		
		for run in runs:

			#if not os.path.isdir(out_path):
			#	os.mkdir(out_path)
			try:
				if ses == '001':
					aux_img_path='/home/despo/ioannis/Berkeley_research1/scantrain/data/derivatives/sub-%s/ses-%s/run-%s/sub-%s_ses-%s_task-learning-criterion_run-%s_space-T1w_desc-residuals_variant-30p_Acc6_065_1_bold_figures' %(sub,ses,run,sub,ses,run)
					fd_ind = aux_img_path+'/fd_ind.npy'
					
					select = np.load(fd_ind)
					select_i = np.invert(select)
					select_i=np.squeeze(select_i)
					
					out_path_img = '/home/despo/ioannis/Berkeley_research1/scantrain/data/derivatives/sub-%s/ses-%s/run-%s/' %(sub,ses,run)
					tt = 'sub-%s_ses-%s_task-learning-criterion_run-%s_space-%s-residuals_variant-30p_Acc6_065_1_bold.nii.gz' %(sub, ses, run, epi_space)
					tt_s = 'sub-%s_ses-%s_task-learning-criterion_run-%s_space-%s-residuals_variant-30p_Acc6_065_1_bold_scrubbed.nii.gz' %(sub, ses, run, epi_space)
					datanifti = nib.load(out_path_img+tt)
					#pdb.set_trace()
					scrubbeddata = datanifti.get_data()[:,:,:,select_i]
					newNii = nib.Nifti1Pair(scrubbeddata,None,datanifti.get_header())
					nib.save(newNii,out_path_img+tt_s)

				elif ses == '002' or ses == '003' or ses =='004' or ses =='005' or ses == '006' or ses == '007' or ses == '008' or ses == '009' or ses == '010' or ses == '011' or ses == '012' or ses == '013' or ses == '014' or ses == '015' or ses == '016' or ses == '017':	


					
					aux_img_path='/home/despo/ioannis/Berkeley_research1/scantrain/data/derivatives/sub-%s/ses-%s/run-%s/sub-%s_ses-%s_task-learning-block_run-%s_space-T1w_desc-residuals_variant-30p_Acc6_065_1_bold_figures' %(sub,ses,run,sub,ses,run)
					fd_ind = aux_img_path+'/fd_ind.npy'
					
						
					select = np.load(fd_ind)
					select_i = np.invert(select)
					select_i=np.squeeze(select_i)
					out_path_img = '/home/despo/ioannis/Berkeley_research1/scantrain/data/derivatives/sub-%s/ses-%s/run-%s/' %(sub,ses,run)
					tt = 'sub-%s_ses-%s_task-learning-block_run-%s_space-%s-residuals_variant-30p_Acc6_065_1_bold.nii.gz' %(sub, ses, run, epi_space)
					tt_s = 'sub-%s_ses-%s_task-learning-block_run-%s_space-%s-residuals_variant-30p_Acc6_065_1_bold_scrubbed.nii.gz' %(sub, ses, run, epi_space)
					datanifti = nib.load(out_path_img+tt)
					scrubbeddata = datanifti.get_data()[:,:,:,select_i]
					newNii = nib.Nifti1Pair(scrubbeddata,None,datanifti.get_header())
					nib.save(newNii,out_path_img+tt_s)

				else:
					aux_img_path='/home/despo/ioannis/Berkeley_research1/scantrain/data/derivatives/sub-%s/ses-%s/run-%s/sub-%s_ses-%s_task-learning-blockSR_run-%s_space-T1w_desc-residuals_variant-30p_Acc6_065_1_bold_figures' %(sub,ses,run,sub,ses,run)
					fd_ind = aux_img_path+'/fd_ind.npy'
					
					select = np.load(fd_ind)
					select_i = np.invert(select)
					select_i=np.squeeze(select_i)
					out_path_img = '/home/despo/ioannis/Berkeley_research1/scantrain/data/derivatives/sub-%s/ses-%s/run-%s/' %(sub,ses,run)
					tt = 'sub-%s_ses-%s_task-learning-blockSR_run-%s_space-%s-residuals_variant-30p_Acc6_065_1_bold.nii.gz' %(sub, ses, run, epi_space)
					tt_s = 'sub-%s_ses-%s_task-learning-blockSR_run-%s_space-%s-residuals_variant-30p_Acc6_065_1_bold_scrubbed.nii.gz' %(sub, ses, run, epi_space)
					datanifti = nib.load(out_path_img+tt)
					scrubbeddata = datanifti.get_data()[:,:,:,select_i]
					newNii = nib.Nifti1Pair(scrubbeddata,None,datanifti.get_header())
					nib.save(newNii,out_path_img+tt_s)
			except:
					pass







			
