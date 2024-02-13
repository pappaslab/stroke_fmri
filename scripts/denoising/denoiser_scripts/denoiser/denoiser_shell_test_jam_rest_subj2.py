import os, sys
import numpy as np
import pdb
      
        


# os.system('conda activate denoiser')


sess = ['001','002','003','004','005','006','007','008','009','010','011','012','013','014','015','016','017','018','019','020','021','022','023','024']

runs = ['001','002']
subs= ['002']
#sess =['002']

epi_space ='T1w_desc'
for sub in subs:
	out_path = '/home/despo/ioannis/Berkeley_research1/scantrain/data/derivatives_rest/sub-%s' %(sub)

	if not os.path.isdir(out_path):
		os.mkdir(out_path)
	for ses in sess:

		out_path = '/home/despo/ioannis/Berkeley_research1/scantrain/data/derivatives_rest/sub-%s/ses-%s' %(sub,ses)

		if not os.path.isdir(out_path):
			os.mkdir(out_path)
		for run in runs:
		        
			img_file_str = '/home/despoB/jam124/ScanTrain/data/derivatives/fmriprep/sub-%s/ses-%s/func/sub-%s_ses-%s_task-rest_run-%s_space-%s-preproc_bold.nii.gz' %(sub, ses, sub, ses, run, epi_space)
				
			tsv_file_str = '/home/despoB/jam124/ScanTrain/data/derivatives/fmriprep/sub-%s/ses-%s/func/sub-%s_ses-%s_task-rest_run-%s_desc-confounds_regressors.tsv' %(sub, ses, sub, ses, run)
			
			
			

			out_path = '/home/despo/ioannis/Berkeley_research1/scantrain/data/derivatives_rest/sub-%s/ses-%s/run-%s' %(sub,ses,run)

			if not os.path.isdir(out_path):
				os.mkdir(out_path)

			#pdb.set_trace()
			

			

			hp_filter = 0.009
			lp_filter = 0.065
			BASE_CONFOUNDS = 'a_comp_cor_00 a_comp_cor_01 a_comp_cor_02 a_comp_cor_03 a_comp_cor_04 a_comp_cor_05 trans_x trans_x_derivative1 trans_x_derivative1_power2 trans_x_power2 trans_y trans_y_derivative1 trans_y_power2 trans_y_derivative1_power2 trans_z trans_z_derivative1 trans_z_derivative1_power2 trans_z_power2 rot_x rot_x_derivative1 rot_x_power2 rot_x_derivative1_power2 rot_y rot_y_derivative1 rot_y_power2 rot_y_derivative1_power2 rot_z rot_z_derivative1 rot_z_derivative1_power2 rot_z_power2'




			GSR_COLS = 'GlobalSignal' #'global_signal global_signal_derivative1 global_signal_derivative1_power2 global_signal_power2'

			col_names_str = BASE_CONFOUNDS # + ' ' + GSR_COLS
			fd_col_name_str = 'framewise_displacement'
			FD_thr = 0.21 #0.3
			bids = True
			template_str = '/home/despo/ioannis/Berkeley_research1/stroke/scripts2/denoiser/report_template.html'
			strategy_name_str = '30p_Acc6_065_1' # '24p_Acc6_009_1' '24p_Acc6_009_1_GSR4'

			system_call = 'python /home/despo/ioannis/Berkeley_research1/stroke/scripts2/denoiser/run_denoiser_test.py %s %s %s --hp_filter %s --lp_filter %s --col_names %s --fd_col_name %s --FD_thr %s --bids %s --strategy_name %s --template_file %s' %(img_file_str, tsv_file_str, out_path, hp_filter, lp_filter, col_names_str, fd_col_name_str, FD_thr, bids, strategy_name_str, template_str)
			os.system(system_call)
			print(system_call)

		



