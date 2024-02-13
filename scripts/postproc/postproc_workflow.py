import sys
from nipype import SelectFiles, Node, Workflow, IdentityInterface
from nipype.interfaces.ants.resampling import ApplyTransforms
from nipype.interfaces.utility import Function
from nipype.interfaces.io import DataSink
from niworkflows.interfaces.confounds import ExpandModel
#sys.path.insert(0, '/home/despo/dlurie/Projects/despolab_lesion/code/common-denoiser/denoiser/')
#from denoiser.denoiser import denoise

#import pdb

# Define the roi_damage function
def roi_damage(lesion_path, atlas_path):
    import nibabel as nib
    import numpy as np
    import pandas as pd
    import os, re

    # Atlas image must be in the same space and resolution as the lesion mask.
    atlas_img = nib.load(atlas_path)
    atlas_data = atlas_img.get_data()
    lesion_img = nib.load(lesion_path)
    lesion_data = lesion_img.get_data()

    coverage_data = lesion_data*atlas_data
    roi_labels = np.unique(atlas_data)

    roi_sizes = []
    for roi in roi_labels:
        roi_sizes.append(np.count_nonzero(atlas_data == roi))

    roi_coverage = []
    for roi in roi_labels:
        roi_coverage.append(np.count_nonzero(coverage_data == roi))

    df = pd.DataFrame.from_records(np.array([roi_sizes, roi_coverage]).T, columns=['roi_size', 'lesioned_vox'])
    df = df.set_index(roi_labels.astype('uint16'))
    df.loc[:,'pct_lesion'] = df['lesioned_vox']/df['roi_size']*100
    df.index.name = 'roi_label'
    atlas_fname = os.path.basename(atlas_path)
    out_prefix = atlas_fname.split('_label')[0]
    atlas_label = re.search('(?<=_label-)([a-zA-Z0-9]+)[_]', atlas_fname).groups()[0]
    out_fname = '{0}_atlas-{1}_ROIdamage.tsv'.format(out_prefix, atlas_label) 
    df.to_csv(out_fname, sep='\t')
    return os.path.abspath(out_fname)

def epi_coverage(brain_mask, atlas_path):
    import numpy as np
    import pandas as pd
    import nibabel as nib
    from nilearn import image
    import re, os

    atlas_img = nib.load(atlas_path)
    mask_img = nib.load(brain_mask)
    atlas_resample = image.resample_to_img(atlas_img, mask_img, interpolation='nearest')
    mask_data = mask_img.get_data()
    atlas_data = atlas_resample.get_data()
    coverage_data = mask_data*atlas_data
    roi_labels = np.unique(atlas_data)
    
    roi_sizes = []
    for roi in roi_labels:
        roi_sizes.append(np.count_nonzero(atlas_data == roi))
    
    roi_coverage = []
    for roi in roi_labels:
        roi_coverage.append(np.count_nonzero(coverage_data == roi))
    
    df = pd.DataFrame.from_records(np.array([roi_sizes, roi_coverage]).T, columns=['roi_size', 'roi_count'])
    df = df.set_index(roi_labels.astype('uint16')) 
    df.loc[:,'pct_cov'] = df['roi_count']/df['roi_size']*100
    df.index.name = 'roi_label'
    out_prefix = os.path.basename(brain_mask).split('_desc')[0] # For older versions of FMRIPREP, split should be on "_brainmask".
    atlas_fname = os.path.basename(atlas_path)
    atlas_label = re.search('(?<=_label-)([a-zA-Z0-9]+)[_]', atlas_fname).groups()[0]
    out_fname = '{0}_atlas-{1}_EPIcoverage.tsv'.format(out_prefix, atlas_label)        
    df.to_csv(out_fname, sep='\t')
    return os.path.abspath(out_fname)

def make_subnum(pid):
    return "sub-{0}".format(pid)

def lesion_mni_fname(lesion_path):
    import os
    res = os.path.basename(lesion_path).split('T1w')
    return res[0]+'space-MNI152NLin2009cAsym'+res[1]

def atlas_t1_helper(atlas_path, pid):
    import os, re
    atlas_fname = os.path.basename(atlas_path)
    atlas_label = re.search('(?<=_label-)([a-zA-Z0-9]+)[_]', atlas_fname).groups()[0]
    res = atlas_fname.split('.', maxsplit=1)
    norm_fname = 'sub-{0}_space-T1w_label-{1}_atlas.{2}'.format(pid, atlas_label, res[1])
    return atlas_path, norm_fname 

# Define GLOBALS
ATLAS_LIST = [
              '/home/despo/dlurie/Data/reference/bids/ref_space-MNI_variant-maxprob25_label-BNA_atlas.nii.gz']

BASE_CONFOUNDS = ["a_comp_cor_00",
                  "a_comp_cor_01",
                  "a_comp_cor_02",
                  "a_comp_cor_03",
                  "a_comp_cor_04",
                  "a_comp_cor_05",
                  "trans_x",
                  "trans_x_derivative1",
                  "trans_x_derivative1_power2",
                  "trans_x_power2",
                  "trans_y",
                  "trans_y_derivative1",
                  "trans_y_power2",
                  "trans_y_derivative1_power2",
                  "trans_z",
                  "trans_z_derivative1",
                  "trans_z_derivative1_power2",
                  "trans_z_power2",
                  "rot_x",
                  "rot_x_derivative1",
                  "rot_x_power2",
                  "rot_x_derivative1_power2",
                  "rot_y",
                  "rot_y_derivative1",
                  "rot_y_power2",
                  "rot_y_derivative1_power2",
                  "rot_z",
                  "rot_z_derivative1",
                  "rot_z_derivative1_power2",
                  "rot_z_power2"]

GSR_COLS = ["global_signal",
            "global_signal_derivative1",
            "global_signal_derivative1_power2",
            "global_signal_power2"]

NUISANCE_STRATEGIES = [('M24aCC', BASE_CONFOUNDS), ('M24aCCGSR4', BASE_CONFOUNDS+GSR_COLS)]

RUNS = ['1']


#pid = sys.argv[1]
SUBJECT_LIST = ['003']  # TESTING HARD CODE


# Initiatlize and configure an infosource to map over patients.
patientsource = Node(IdentityInterface(fields=['pid']),
                          name="patientsource")
patientsource.iterables = [('pid', SUBJECT_LIST)]

# Initiatlize and configure an infosource to map over runs.
runsource = Node(IdentityInterface(fields=['run_num']),
                          name="runsource")
runsource.iterables = [('run_num', RUNS)]


"""
### ANAT WORKFLOW ###
"""

# Initiatlize the anat_postproc workflow
anat_postproc_wf = Workflow(name='anat_postproc_wf', 
        base_dir='/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/fmriprep/work')

# Define SelectFiles templates for anatomical workflow input data.
anat_templates = {
        't1w_preproc': 'fmriprep/out/fmriprep/sub-{pid}/anat/sub-{pid}_desc-preproc_T1w.nii.gz',
        't1_2_mni_transform': 'fmriprep/out/fmriprep/sub-{pid}/anat/sub-{pid}_from-T1w_to-MNI152NLin2009cAsym_mode-image_xfm.h5',
        'mni_2_t1_transform': 'fmriprep/out/fmriprep/sub-{pid}/anat/sub-{pid}_from-MNI152NLin2009cAsym_to-T1w_mode-image_xfm.h5',
        }

raw_templates = {'lesion_mask': 'sub-{pid}/ses-04/anat/sub-{pid}_ses-04_T1w_label-lesion_roi.nii.gz'}

# Initialize and configure anatomical workflow SelectFiles nodes
sf_anat = Node(SelectFiles(anat_templates), name="selectfiles_anat")
sf_anat.inputs.base_directory = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/'

sf_raw = Node(SelectFiles(raw_templates), name="selectfiles_raw")
sf_raw.inputs.base_directory = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/'

# Connect inputs to anatomical SelectFiles nodes
anat_postproc_wf.connect(patientsource, 'pid', sf_anat, 'pid')
anat_postproc_wf.connect(patientsource, 'pid', sf_raw, 'pid')

# Initialize and configure the lesion_mni_fname node
gen_lesion_mni_fname = Node(Function(input_names=['lesion_path'], output_names=['fname'],
                                     function=lesion_mni_fname), name='gen_lesion_mni_fname')

# Connect input to gen_lesion_mni_fname node
anat_postproc_wf.connect(sf_raw, 'lesion_mask', gen_lesion_mni_fname, 'lesion_path')

# Initialize and configure lesion_to_mni node
lesion_to_mni = Node(ApplyTransforms(), name='lesion_to_mni')
lesion_to_mni.inputs.default_value = 0
lesion_to_mni.inputs.dimension = 3
lesion_to_mni.inputs.float = True # I think this is equivalent to --float 1 in the ants command  line.
lesion_to_mni.inputs.interpolation = 'NearestNeighbor'
lesion_to_mni.inputs.reference_image = '/home/despo/dlurie/Data/reference/mni_icbm152_nlin_asym_09c/mni_icbm152_t1_tal_nlin_asym_09c.nii' 

# Connect inputs to lesion_to_mni
anat_postproc_wf.connect(sf_raw, 'lesion_mask', lesion_to_mni, 'input_image')
anat_postproc_wf.connect(sf_anat, 't1_2_mni_transform', lesion_to_mni, 'transforms')
anat_postproc_wf.connect(gen_lesion_mni_fname, 'fname', lesion_to_mni, 'output_image')

# Initialize and configure the atlas_t1_helper node
run_atlas_t1_helper = Node(Function(input_names=['atlas_path', 'pid'], output_names=['orig_path', 'norm_fname'],
                                     function=atlas_t1_helper), name='run_atlas_t1_helper')
run_atlas_t1_helper.iterables = ('atlas_path', ATLAS_LIST)

# Connect inputs to run_atlas_t1_helper node
anat_postproc_wf.connect(patientsource, 'pid', run_atlas_t1_helper, 'pid')

# Initialize and configure reverse_normalize_atlas node
reverse_normalize_atlas = Node(ApplyTransforms(), name='reverse_normalize_atlas')
reverse_normalize_atlas.inputs.default_value = 0
reverse_normalize_atlas.inputs.dimension = 3
reverse_normalize_atlas.inputs.float = True
reverse_normalize_atlas.inputs.interpolation = 'NearestNeighbor'
#reverse_normalize_atlas.iterables = ('input_image', ATLAS_LIST)

# Connect inputs to reverse_normalize_atlas
anat_postproc_wf.connect(sf_anat, 't1w_preproc', reverse_normalize_atlas, 'reference_image')
anat_postproc_wf.connect(sf_anat, 'mni_2_t1_transform', reverse_normalize_atlas, 'transforms')
anat_postproc_wf.connect(run_atlas_t1_helper, 'orig_path', reverse_normalize_atlas, 'input_image')
anat_postproc_wf.connect(run_atlas_t1_helper, 'norm_fname', reverse_normalize_atlas, 'output_image')

# Initialize and configure the roi_damage node
calculate_roi_damage = Node(Function(input_names=['lesion_path', 'atlas_path'],
                           output_names=['out_path'],
                           function=roi_damage),
                       name='calculate_roi_damage')

# Connect inputs to calculate_roi_damage
anat_postproc_wf.connect(sf_raw, 'lesion_mask', calculate_roi_damage, 'lesion_path')
anat_postproc_wf.connect(reverse_normalize_atlas, 'output_image', calculate_roi_damage, 'atlas_path')

# Initialize and configure a helper node to construct pretty subject number  strings (for naming  output subdirectories)
subnum_helper = Node(Function(input_names=['pid'], output_names=['subnum'], function=make_subnum), name='subnum_helper')

# Connect inputs to subnum_helper
anat_postproc_wf.connect(patientsource, 'pid', subnum_helper, 'pid')

# Initialize and configure the anatomical DataSink
anat_sinker = Node(DataSink(parameterization=False), name='anat_sinker')
anat_sinker.inputs.base_directory = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/'

# Connect outputs to anat_sinker
anat_postproc_wf.connect(subnum_helper, 'subnum', anat_sinker, 'container')
anat_postproc_wf.connect(lesion_to_mni, 'output_image', anat_sinker, 'anat.@lesion_mask')
anat_postproc_wf.connect(reverse_normalize_atlas, 'output_image', anat_sinker, 'anat.@atlas_native')
anat_postproc_wf.connect(calculate_roi_damage, 'out_path', anat_sinker, 'anat.@ROIdamage')

# Run the anat_postproc workflow
#anat_postproc_wf.run()

"""
### FUNC WORKFLOW ###
"""

# Initiatlize the func_postproc workflow
func_postproc_wf = Workflow(name='func_postproc_wf', 
        base_dir='/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/fmriprep/work/')

# Define SelectFiles templates for anatomical workflow input data.
bold_templates = {
        'bold_preproc': 'fmriprep/out/fmriprep/sub-{pid}/ses-04/func/sub-{pid}_ses-04_task-rest_run-{run_num}_space-T1w_desc-preproc_bold.nii.gz',
        'bold_brain_mask': 'fmriprep/out/fmriprep/sub-{pid}/ses-04/func/sub-{pid}_ses-04_task-rest_run-{run_num}_space-T1w_desc-brain_mask.nii.gz',
        'confounds_tsv': 'fmriprep/out/fmriprep/sub-{pid}/ses-04/func/sub-{pid}_ses-04_task-rest_run-{run_num}_desc-confounds_regressors.tsv'
        }

# Initialize and configure anatomical workflow SelectFiles nodes.
sf_bold = Node(SelectFiles(bold_templates), name="selectfiles_bold")
sf_bold.inputs.base_directory = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/'

# Tell sf_bold (and thus the rest of the func_postproc workflow) to iterate over patients and runs.
func_postproc_wf.connect(anat_postproc_wf, 'patientsource.pid', sf_bold, 'pid')
func_postproc_wf.connect(runsource, 'run_num', sf_bold, 'run_num')

# Initialize and configure the confounds_expansion node
confounds_expansion = Node(ExpandModel(), name='confounds_expansion')
confounds_expansion.model_formula = '(dd1(rps + gsr))^^2 + others'

# Connect inputs to confounds_expansion
func_postproc_wf.connect(sf_bold, 'confounds_tsv', confounds_expansion, 'confounds_file')

# Initialize and configure the epi_coverage node
calculate_epi_coverage = Node(Function(input_names=['brain_mask', 'atlas_path'],
                           output_names=['out_path'],
                           function=epi_coverage),
                       name='calculate_epi_coverage')

# Connect inputs to calculate_epi_coverage
func_postproc_wf.connect(sf_bold, 'bold_brain_mask', calculate_epi_coverage, 'brain_mask')
func_postproc_wf.connect(anat_postproc_wf, 'reverse_normalize_atlas.output_image', calculate_epi_coverage, 'atlas_path')

# Initialize and configure the functional DataSink
func_sinker = Node(DataSink(parameterization=False), name='func_sinker')
func_sinker.inputs.base_directory = '/home/despo/ioannis/Berkeley_research1/stroke/data/rsfMRI_D/rs_fMRI_initial_batch/ioannis_stroke_fmriprep/derivatives/postproc/out/'

# Connect outputs to func_sinker
func_postproc_wf.connect(anat_postproc_wf, 'subnum_helper.subnum', func_sinker, 'container')
func_postproc_wf.connect(confounds_expansion, 'confounds_file', func_sinker, 'func.@expanded_confounds')
func_postproc_wf.connect(calculate_epi_coverage, 'out_path', func_sinker, 'func.@epi_coverage')

"""
# Initiatlize and configure the run_denoiser node
run_denoiser = Node(Function(input_names=['img_file', 'tsv_file', 'out_path', 'col_names',
                                          'hp_filter', 'lp_filter', 'fd_col_name', 'FD_thr',
                                          'bids', 'strategy_name', 'template_file', 'sink_link'],
                             output_names=['clean_img'],
                             function=denoise),
                    name='run_denoiser')
run_denoiser.inputs.hp_filter = 0.008
run_denoiser.inputs.lp_filter = 0.08
run_denoiser.inputs.fd_col_name = 'framewise_displacement'
run_denoiser.inputs.FD_thr = 0.3
run_denoiser.inputs.bids = True
run_denoiser.inputs.template_file = '/home/despoB/dlurie/Projects/despolab_lesion/code/common-denoiser/denoiser/report_template.html'

# Connect inputs to run_denoiser
func_postproc_wf.connect(func_sinker, 'out_file', run_denoiser, 'sink_link') # Dummy connection to delay denoiser
func_postproc_wf.connect(sf_bold, 'bold_preproc', run_denoiser, 'img_file')
func_postproc_wf.connect(confounds_expansion, 'confounds_file', run_denoiser, 'tsv_file')
# HARD CODED SETTINGS FOR TESTING (and until we automate their configuration)
run_denoiser.inputs.out_path = '/home/despoB/dlurie/Projects/despolab_lesion/data/patients/derivatives/postproc/out/func'
run_denoiser.inputs.col_names = NUISANCE_STRATEGIES[0][1]
run_denoiser.inputs.strategy_name = NUISANCE_STRATEGIES[0][0]
"""
func_postproc_wf.run()
func_postproc_wf.write_graph(graph2use='hierarchical')

