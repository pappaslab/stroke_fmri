import os, sys
import numpy as np
import pdb
      
        


# os.system('conda activate denoiser')

#sub = '001'
runs = ['sherlockPart1', 'sherlockPart2']
epi_space = 'MNI152NLin2009cAsym' # 'T1w'

for sub in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16']:
#for sub in [01, 1008, 1009, 1016, 1021, 1027, 1032, 1037, 1042, 1005, 1011, 1017, 1022, 1028, 1033, 1038, 1043, 1006, 1012, 1018, 1023, 1029, 1034, 1039, 1044, 1007, 1014, 1019, 1024, 1030, 1035, 1040, 1015, 1020, 1026, 1031, 1036, 1041]: #np.arange(1,73):
	#if sub in [8, 19, 56]:
	#	continue
	for run in runs:

		img_file_str = '/home/despoC/ycleong/Desktop/ISFC_Diff/Datasets/preproc/Sherlock/fmriprep/sub-%s/func/sub-%s_task-%s_bold_space-%s_preproc.nii.gz' %(sub, sub, run, epi_space)
		
		tsv_file_str = '/home/despoC/ycleong/Desktop/ISFC_Diff/Datasets/preproc/Sherlock/fmriprep/sub-%s/func/sub-%s_task-%s_bold_confounds.tsv' %(sub, sub, run)
		out_path = '/home/despoC/ioannis/Berkeley_research1/YC/data/derivatives_sherlock/aux_data/sub-%s/denoise/' %(sub)

		if not os.path.isdir(out_path):
			os.mkdir(out_path)

		hp_filter = 0.009
		lp_filter = 0.1
		BASE_CONFOUNDS = 'aCompCor00 aCompCor01 aCompCor02 aCompCor03 aCompCor04 aCompCor05 X Y Z RotX RotY RotZ'   #'a_comp_cor_00 a_comp_cor_01 a_comp_cor_02 a_comp_cor_03 a_comp_cor_04 a_comp_cor_05 trans_x trans_x_derivative1 trans_x_derivative1_power2 trans_x_power2 trans_y trans_y_derivative1 trans_y_power2 trans_y_derivative1_power2 trans_z trans_z_derivative1 trans_z_derivative1_power2 trans_z_power2 rot_x rot_x_derivative1 rot_x_power2 rot_x_derivative1_power2 rot_y rot_y_derivative1 rot_y_power2 rot_y_derivative1_power2 rot_z rot_z_derivative1 rot_z_derivative1_power2 rot_z_power2'




		GSR_COLS = 'GlobalSignal' #'global_signal global_signal_derivative1 global_signal_derivative1_power2 global_signal_power2'

		col_names_str = BASE_CONFOUNDS # + ' ' + GSR_COLS
		fd_col_name_str = 'FramewiseDisplacement' #'framewise_displacement'
		FD_thr = 0.3
		bids = True
		template_str = '/home/despoB/adameich/Experiments/nScout/scripts/denoiser/report_template.html'
		strategy_name_str = '24p_Acc6_009_1' # '24p_Acc6_009_1' '24p_Acc6_009_1_GSR4'

		system_call = 'python /home/despoC/ioannis/Berkeley_research1/stroke/scripts2/denoiser/run_denoiser_test.py %s %s %s --hp_filter %s --lp_filter %s --col_names %s --fd_col_name %s --FD_thr %s --bids %s --strategy_name %s --template_file %s' %(img_file_str, tsv_file_str, out_path, hp_filter, lp_filter, col_names_str, fd_col_name_str, FD_thr, bids, strategy_name_str, template_str)
		os.system(system_call)
		print(system_call)

		



