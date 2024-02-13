import os, sys
import numpy as np
import pdb
      
        



# os.system('conda activate denoiser')

#sub = '001'
#runs = ['sherlockPart1', 'sherlockPart2']
epi_space = 'MNI152NLin2009cAsym' # 'T1w'

for sub in ['A00008326','A00032876','A00038642','A00040524','A00054621','A00062268','A00010893','A00033011','A00038718','A00040525','A00054895','A00062288','A00013809','A00033021','A00038731','A00040567','A00054897','A00062292','A00019903','A00033232']:
	for i in range(1):

		img_file_str = '/home/despoB/nki_rs/data/derivatives/fmriprep/sub-%s/ses-DS2/func/sub-%s_ses-DS2_task-rest_acq-645_bold_space-MNI152NLin2009cAsym_preproc.nii.gz' %(sub, sub)

		tsv_file_str = '/home/despoB/nki_rs/data/derivatives/fmriprep/sub-%s/ses-DS2/func/sub-%s_ses-DS2_task-rest_acq-645_bold_confounds.tsv' %(sub, sub)
		out_path = '/home/despoC/ioannis/Berkeley_research1/stroke/data/NKI/sub-%s' %(sub)

		if not os.path.isdir(out_path):
			os.mkdir(out_path)
		out_path = '/home/despoC/ioannis/Berkeley_research1/stroke/data/NKI/sub-%s/denoise/' %(sub)

		if not os.path.isdir(out_path):
			os.mkdir(out_path)

		hp_filter = 0.009
		lp_filter = 'Inf'
		BASE_CONFOUNDS = 'aCompCor00 aCompCor01 aCompCor02 aCompCor03 aCompCor04 aCompCor05 X Y Z RotX RotY RotZ'   #'a_comp_cor_00 a_comp_cor_01 a_comp_cor_02 a_comp_cor_03 a_comp_cor_04 a_comp_cor_05 trans_x trans_x_derivative1 trans_x_derivative1_power2 trans_x_power2 trans_y trans_y_derivative1 trans_y_power2 trans_y_derivative1_power2 trans_z trans_z_derivative1 trans_z_derivative1_power2 trans_z_power2 rot_x rot_x_derivative1 rot_x_power2 rot_x_derivative1_power2 rot_y rot_y_derivative1 rot_y_power2 rot_y_derivative1_power2 rot_z rot_z_derivative1 rot_z_derivative1_power2 rot_z_power2'




		GSR_COLS = '' #'GlobalSignal' #'global_signal global_signal_derivative1 global_signal_derivative1_power2 global_signal_power2'

		col_names_str = BASE_CONFOUNDS # + ' ' + GSR_COLS
		fd_col_name_str = ' '#'FramewiseDisplacement' #'framewise_displacement'
		FD_thr = 0.3
		bids = True
		template_str = '/home/despoB/adameich/Experiments/nScout/scripts/denoiser/report_template.html'
		strategy_name_str = '24p_Acc6_009_1' # '24p_Acc6_009_1' '24p_Acc6_009_1_GSR4'

		system_call = 'python /home/despoC/ioannis/Berkeley_research1/stroke/scripts2/denoiser/run_denoiser_test.py %s %s %s --hp_filter %s  --col_names %s  --bids %s --strategy_name %s --template_file %s' %(img_file_str, tsv_file_str, out_path, hp_filter,  col_names_str,  bids, strategy_name_str, template_str)
		os.system(system_call)
		print(system_call)

		



