import os
import numpy as np
import pandas as pd
import nibabel as nib
from nilearn import input_data

for sub in ['002','003','004','005','006','007','008','009','010','011','012']:
#for sub in ['003']:
	for ses in ['01','02','03','04']:

		
		path_ = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s' %(sub,ses)
		if os.path.isdir(path_):
			

			# Set file path templates
			func_fpt = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func/sub-%s_ses-%s_task-rest_run-1_space-T1w_desc-residuals_variant-Motion24aCompCor6GSR4_bold_scrubbed.nii.gz' %(sub, ses, sub, ses)
			mask_fpt = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/fmriprep/out/fmriprep/sub-%s/ses-%s/func/sub-%s_ses-%s_task-rest_run-1_space-T1w_desc-brain_mask.nii.gz' %(sub, ses, sub, ses)
			atlas_fpt = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/anat/sub-%s_space-T1w_label-BNA_atlas.nii.gz' %(sub, ses, sub)
			#motion24_fpt = '/home/despoB/dlurie/Projects/despolab_lesion/derivatives/sub-{0}/func/sub-{0}_task-rest_acq-{1}_run-01_bold_confounds-motion24.csv'
			ts_fpt = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func/sub-%s_ses-%s_task-rest_run-1_bold_space-T1w_timeseries_atlas-BNA_motion24.npy' %(sub, ses, sub, ses)

			corrmat_fpt = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func//sub-%s_ses-%s_task-rest_run-1_bold_space-T1w_corrmat_atlas-BNA_motion24.npy' %(sub, ses, sub, ses)

			

			bold_T1w_preproc = func_fpt
			bold_T1w_brainmask = nib.load(mask_fpt)
			#atlas_T1w_BNA = atlas_fpt.format(pid)
			#confounds = motion24_fpt.format(pid,epi_acq)

			bna_img = nib.load(atlas_fpt)

			bna_masker = input_data.NiftiLabelsMasker(labels_img=bna_img, background_label=0, mask_img=bold_T1w_brainmask,
						                  standardize=False,
						                  resampling_target="data")

			#print("...extracting brainnetome timeseries for patient {0}...".format(pid))
			timeseries = bna_masker.fit_transform(bold_T1w_preproc)
			np.save(ts_fpt, timeseries)

			#print("...computing correlation matrix for patient {0}...".format(pid))
			corrmat = np.corrcoef(timeseries.T)
			np.save(corrmat_fpt, corrmat)



