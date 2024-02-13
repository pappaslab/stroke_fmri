import numpy as np
import os
import pdb
import csv


for sub in ['001','002','003','004','005','006','007','008','009','010','011','012']:
#for sub in ['001','002']:
	for ses in ['01','02','03','04']:
		print(sub)
		print(ses)

		
		path_ = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s' %(sub,ses)
		if os.path.isdir(path_):
			




    
			# Set file-path templates
			corrmat_fpt = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func//sub-%s_ses-%s_task-rest_run-1_bold_space-T1w_corrmat_atlas-BNA_motion24.npy' %(sub, ses, sub, ses)

			corrmat_z_fpt = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func//sub-%s_ses-%s_task-rest_run-1_bold_space-T1w_corrmat_atlas-BNA_motion24_corrmatZ.csv' %(sub, ses, sub, ses)

			corrmat_z_fpt_LH = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func//sub-%s_ses-%s_task-rest_run-1_bold_space-T1w_corrmat_atlas-BNA_motion24_corrmatZ_LH.csv' %(sub, ses, sub, ses)

			corrmat_z_fpt_RH = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func//sub-%s_ses-%s_task-rest_run-1_bold_space-T1w_corrmat_atlas-BNA_motion24_corrmatZ_RH.csv' %(sub, ses, sub, ses)

			corrmat_z_fpt_lang = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func//sub-%s_ses-%s_task-rest_run-1_bold_space-T1w_corrmat_atlas-BNA_motion24_corrmatZ_lang.csv' %(sub, ses, sub, ses)

			corrmat_z_fpt_lang_L = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func//sub-%s_ses-%s_task-rest_run-1_bold_space-T1w_corrmat_atlas-BNA_motion24_corrmatZ_lang_L.csv' %(sub, ses, sub, ses)

			corrmat_z_fpt_lang_R = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func//sub-%s_ses-%s_task-rest_run-1_bold_space-T1w_corrmat_atlas-BNA_motion24_corrmatZ_lang_R.csv' %(sub, ses, sub, ses)
			    
			out_prefix_fpt = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func/sub-%s_ses-%s_task-rest_run-1_bold_space-T1w_atlas-BNA_variant-motion24_thresh-none_alg-Louvain_gamma-1.0' %(sub, ses, sub, ses)

			damage_file= '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/anat/sub-%s_space-T1w_atlas-BNA_ROIdamage.tsv' %(sub, ses, sub)

			epi_file = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func/sub-%s_ses-%s_task-rest_run-1_space-T1w_atlas-BNA_EPIcoverage.tsv' %(sub, ses, sub, ses)

			#save indices as well
			brain_all_fpt = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func//sub-%s_ses-%s_brain_all.txt' %(sub, ses, sub, ses)
			brain_all_fpt_set_diff_RH = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func//sub-%s_ses-%s_set_diff_RH.txt' %(sub, ses, sub, ses)
			brain_all_fpt_set_diff_LH = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func//sub-%s_ses-%s_set_diff_LH.txt' %(sub, ses, sub, ses)

			lang_all_fpt = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func//sub-%s_ses-%s_set_diff_langall.txt' %(sub, ses, sub, ses)
			lang_all_fpt_set_diff_LH = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func//sub-%s_ses-%s_set_diff_lang_L.txt' %(sub, ses, sub, ses)
			lang_all_fpt_set_diff_RH = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func//sub-%s_ses-%s_set_diff_lang_R.txt' %(sub, ses, sub, ses)

			#lesion
			tsv_file = open(damage_file)
			dam = csv.reader(tsv_file, delimiter="\t")
			dam_array = list(dam)
			dam_score = []
			for i in range(2,len(dam_array)):
				elem_ = dam_array[i]
				dam_score.append(float(elem_[3]))

			dam_score=np.asarray(dam_score)
			ind_dam = np.where(dam_score>50) 
			ind_dam = ind_dam[0]
			#epi
			epi_file = open(epi_file)
			epi = csv.reader(epi_file, delimiter="\t")
			epi_array = list(epi)
			
			epi_score = []
			for i in range(2,len(epi_array)):
				elem_ = epi_array[i]
				epi_score.append(float(elem_[3]))

			epi_score=np.asarray(epi_score)
			ind_epi = np.where(epi_score<25)
			ind_epi = ind_epi[0]


			#matrix
			corrmat = np.load(corrmat_fpt)
			np.fill_diagonal(corrmat, 0)

			# Filter the matrix by hemi

			
			shap_ = corrmat.shape
			RH = []
			LH = []
			for num in range(0, shap_[0]):
      
			   
				if num % 2 != 0:
					RH.append(num)
				else:
					LH.append(num)

			
			LH = np.asarray(LH)
			RH = np.asarray(RH)
			# ..Or by network
			LL = [15, 17, 23, 25, 29, 31, 33, 35, 37, 39, 43, 51, 53, 61, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 121, 123, 135, 137, 139, 141, 143, 145, 171, 173]
			LL = [189, 191, 193, 195, 197, 199, 201, 203, 205, 207, 209]			
			#LL = [81, 82, 83, 84, 85, 86, 87, 88]
			LL=np.asarray(LL)
			LL = LL-1

			RL = [16, 18, 24, 26, 30, 32, 34, 36, 38, 40, 44, 52, 54, 62, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 122, 124, 136, 138, 140, 142, 144, 146, 172, 174]
			#RL = [29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]	
			RL = [190, 192, 194, 196, 198, 200, 202, 204, 206, 208, 210]		
			RL= np.asarray(RL)
			RL = RL-1

			if ind_dam.size != 0:
				set_diff_LH = np.setdiff1d(LH, ind_dam)
				set_diff_RH = np.setdiff1d(RH, ind_dam)
				set_lang_LH = np.setdiff1d(LL, ind_dam)
				set_lang_RH = np.setdiff1d(RL, ind_dam)
			else:	
				set_diff_LH = LH
				set_diff_RH = RH
				set_lang_LH = LL
				set_lang_RH= RL
			
			brain_all = np.concatenate([set_diff_LH, set_diff_RH])
			lang_all = np.concatenate([set_lang_LH,set_lang_RH])
			#pdb.set_trace()
			#all brain
			corrmat_filtered = corrmat[brain_all][:,brain_all]
			corrmat_filtered_z = np.arctanh(corrmat_filtered)
			np.savetxt(brain_all_fpt, brain_all);
			#all language
			corrmat_filtered = corrmat[lang_all][:,lang_all]
			corrmat_filtered_z_lang = np.arctanh(corrmat_filtered)
			np.savetxt(lang_all_fpt, lang_all);
			#left language
			corrmat_filtered = corrmat[set_lang_LH][:,set_lang_LH]
			corrmat_filtered_z_LL = np.arctanh(corrmat_filtered)
			np.savetxt(lang_all_fpt_set_diff_LH, set_lang_LH);
			#right language
			corrmat_filtered = corrmat[set_lang_RH][:,set_lang_RH]
			corrmat_filtered_z_RL = np.arctanh(corrmat_filtered)
			np.savetxt(lang_all_fpt_set_diff_RH, set_lang_RH);

			
			#right hemi 
			corrmat_filtered_RH = corrmat[set_diff_RH][:,set_diff_RH]
			corrmat_filtered_z_RH = np.arctanh(corrmat_filtered_RH)
			np.savetxt(brain_all_fpt_set_diff_RH, set_diff_RH);
			#left hemi 
			corrmat_filtered_LH = corrmat[set_diff_LH][:,set_diff_LH]
			corrmat_filtered_z_LH = np.arctanh(corrmat_filtered_LH)
			np.savetxt(brain_all_fpt_set_diff_LH, set_diff_LH);
			
			#  save matrix
			np.savetxt(corrmat_z_fpt, corrmat_filtered_z)
			np.savetxt(corrmat_z_fpt_LH, corrmat_filtered_z_LH)
			np.savetxt(corrmat_z_fpt_RH, corrmat_filtered_z_RH)

			np.savetxt(corrmat_z_fpt_lang, corrmat_filtered_z_lang)
			np.savetxt(corrmat_z_fpt_lang_L, corrmat_filtered_z_LL)
			np.savetxt(corrmat_z_fpt_lang_R, corrmat_filtered_z_RL)


			# Run graph-theory pipeline
			#see /home/despo/ioannis/Berkeley_research1/stroke/scripts2/analysis_pipeline/rsfMRI_D
		    
