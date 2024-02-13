import sys
import os
#conda activate denoiser
#unset PYTHONPATH

for sub in ['001','002','003','004','005','006','007','008','009','010','011','012']:
#for sub in ['003']:
	for ses in ['01','02','03','04']:

		path_ = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s' %(sub,ses)
		if os.path.isdir(path_):
			

			input_img_file='/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/fmriprep/out/fmriprep/sub-%s/ses-%s/func/sub-%s_ses-%s_task-rest_run-1_space-T1w_desc-preproc_bold.nii.gz'%(sub, ses, sub, ses)
			input_tsv_file='/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func/sub-%s_ses-%s_task-rest_run-1_desc-confounds_regressors_expansion.tsv'%(sub, ses, sub, ses)




			

			input_out_path='/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/sub-%s/ses-%s/func/'%(sub, ses)


			command_ = 'python /home/despoC/ioannis/Berkeley_research1/stroke/scripts2/denoiser/run_denoiser_test.py  ' + input_img_file + ' ' + input_tsv_file + ' ' + input_out_path + ' ' + '--col_names global_signal global_signal_derivative1 global_signal_derivative1_power2 global_signal_power2 trans_x trans_x_derivative1 trans_x_derivative1_power2 trans_x_power2 trans_y trans_y_derivative1 trans_y_derivative1_power2 trans_y_power2 trans_z trans_z_derivative1 trans_z_derivative1_power2 trans_z_power2 rot_x rot_x_derivative1 rot_x_power2 rot_x_derivative1_power2 rot_y rot_y_derivative1 rot_y_derivative1_power2 rot_y_power2 rot_z rot_z_derivative1 rot_z_derivative1_power2 rot_z_power2 a_comp_cor_00 a_comp_cor_01 a_comp_cor_02 a_comp_cor_03 a_comp_cor_04 a_comp_cor_05 --hp_filter 0.009 --lp_filter 0.1 --fd_col_name framewise_displacement --FD_thr 0.4 --bids True --strategy_name Motion24aCompCor6GSR4 --template_file /home/despo/ioannis/Berkeley_research1/stroke/scripts2/denoiser/report_template.html'

			os.system(command_)

