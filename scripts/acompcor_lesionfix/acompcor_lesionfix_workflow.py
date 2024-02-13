import os
import sys
import nipype.interfaces.io as nio
import nipype.pipeline.engine as pe
from nipype import Node, Function
from niworkflows.engine.workflows import LiterateWorkflow as Workflow
from nipype.utils.filemanip import loadpkl
from niworkflows.interfaces.bids import BIDSDataGrabber
from niworkflows.utils.bids import collect_data
import pdb

def subtract_roi(in_mask, roi_file, out_dir):
    import numpy as np
    import nibabel as nb
    import os
    from nipype.utils.filemanip import fname_presuffix

    msk = nb.load(in_mask)
    mskdata = msk.get_data().astype(np.uint8)  
    roi = np.invert(nb.load(roi_file).get_data().astype(np.bool))
    mskdata = mskdata * roi
    msk.set_data_dtype(np.uint8)

    out = os.path.join(out_dir, fname_presuffix(os.path.basename(in_mask), suffix='_roimsk'))
    msk.__class__(mskdata, msk.affine, msk.header).to_filename(out)
    return out

sub_id, deriv_dir = sys.argv[1:3]

fmriprep_ss_work_dir = os.path.join(deriv_dir, 'fmriprep/work/fmriprep_wf',
        'single_subject_{0}_wf'.format(str(sub_id)))

# Create and configure a workflow
acompcor_lesionfix_wf = Workflow(name="acompcor_lesionfix_wf")
acompcor_lesionfix_wf.base_dir = os.path.join(deriv_dir,'acompcor_lesionfix/work')

# Load the bidssrc DataGrabber node from FMRIPREP
bidssrc_old = loadpkl(os.path.join(fmriprep_ss_work_dir,'bidssrc/_node.pklz'.format(sub_id)))
bidssrc_old_res = bidssrc_old.run()

# Loop through the functional scans found by bidssrc
for scan_path in bidssrc_old_res.outputs.bold:
    scan_suffix = scan_path.split('_',1)[1].split('_bold')[0].replace('-', '_')

    # Clone and reconfigure the bidssrc DataGrabber node from FMRIPREP
    bidssrc_lf = bidssrc_old.clone(name="bidssrc_lf")
    bidssrc_lf.base_dir = str(acompcor_lesionfix_wf.base_dir)
    bidssrc_lf._output_dir = os.path.join(str(acompcor_lesionfix_wf.base_dir),
            bidssrc_lf._output_dir.split('fmriprep_wf/',1)[1])

    # Load, clone and reconfigure the acc_tfm node from FMRIPREP
    acc_tfm_old = loadpkl(os.path.join(fmriprep_ss_work_dir,
        'func_preproc_{0}_wf'.format(scan_suffix),'bold_confounds_wf/acc_tfm/_node.pklz'))
    acc_tfm_lf = acc_tfm_old.clone(name='acc_tfm_lf')
    acc_tfm_lf.base_dir = str(acompcor_lesionfix_wf.base_dir)
    acc_tfm_lf._output_dir = os.path.join(str(acompcor_lesionfix_wf.base_dir),
            acc_tfm_lf._output_dir.split('fmriprep_wf/',1)[1])

    # Initialize and configure the subtract_roi node
    subtract_roi_node = Node(Function(input_names=["in_mask", "roi_file","out_dir"],
                       output_names=["refined_mask"],
                       function=subtract_roi),
                    name='subtract_roi')
    subtract_roi_node.base_dir = str(acompcor_lesionfix_wf.base_dir)
    subtract_roi_node._output_dir = os.path.join(str(acompcor_lesionfix_wf.base_dir),
            acc_tfm_lf.output_dir().rstrip('acc_tfm'),'subtract_roi')
    subtract_roi_node.inputs.out_dir = subtract_roi_node._output_dir

    # Load, clone and reconfigure the acompcor node from FMRIPREP
    acompcor_old = loadpkl(os.path.join(fmriprep_ss_work_dir,
        'func_preproc_{0}_wf'.format(scan_suffix),'bold_confounds_wf/acompcor/_node.pklz'))
    acompcor_lf = acompcor_old.clone(name="acompcor_lf")
    acompcor_lf.base_dir = str(acompcor_lesionfix_wf.base_dir)
    acompcor_lf._output_dir = os.path.join(str(acompcor_lesionfix_wf.base_dir),
            acompcor_lf._output_dir.split('fmriprep_wf/',1)[1])
    
    # Load, clone and reconfigure the concat node from FMRIPREP
    concat_old = loadpkl(os.path.join(fmriprep_ss_work_dir,
        'func_preproc_{0}_wf'.format(scan_suffix),'bold_confounds_wf/concat/_node.pklz'))
    concat_lf = concat_old.clone(name="concat_lf")
    concat_lf.base_dir = str(acompcor_lesionfix_wf.base_dir)
    concat_lf._output_dir = os.path.join(str(acompcor_lesionfix_wf.base_dir),
            concat_lf._output_dir.split('fmriprep_wf/',1)[1])

    # Load, clone and reconfigure the ds_confounds DataSink node from FMRIPREP
    ds_confounds_old = loadpkl(os.path.join(fmriprep_ss_work_dir,
        'func_preproc_{0}_wf'.format(scan_suffix),'func_derivatives_wf/ds_confounds/_node.pklz'))
    ds_confounds_lf = ds_confounds_old.clone(name="ds_confounds_lf")
    ds_confounds_lf.inputs.base_dir = os.path.join(deriv_dir,'acompcor_lesionfix/out')
    ds_confounds_lf.inputs.base_directory = os.path.join(deriv_dir,'acompcor_lesionfix/out')
    ds_confounds_lf._output_dir = os.path.join(str(acompcor_lesionfix_wf.base_dir),
            ds_confounds_lf._output_dir.split('fmriprep_wf/',1)[1])
    ds_confounds_lf.inputs.desc = 'confounds_variant-lesionfix'

    # Run bidssrc node
    bidssrc_lf.run()

    # Connect bidssrc.outputs.roi --> acc_tfm.inputs.input_image 
    acc_tfm_lf.inputs.input_image = bidssrc_lf.result.outputs.roi

    # Run acc_tfm node
    acc_tfm_lf.run()

    # Connect acc_tfm.outputs.output_image --> subtract_roi_node.inputs.roi_file
    subtract_roi_node.inputs.roi_file = acc_tfm_lf.result.outputs.output_image

    # Connect acompcor_lf.inputs.mask_files[0] --> subtract_roi_node.inputs.in_mask
    subtract_roi_node.inputs.in_mask = acompcor_lf.inputs.mask_files[0]

    # Run acc_msk node
    subtract_roi_node.run()

    # Connect subtract_roi_node.outputs.refined_mask --> acompcor.inputs.mask_files
    acompcor_lf.inputs.mask_files = subtract_roi_node.result.outputs.refined_mask

    # Run acompcor node
    acompcor_lf.run()

    # Connect acompcor.outputs.components_file --> concat.inputs.acompcor
    concat_lf.inputs.acompcor = acompcor_lf.result.outputs.components_file

    # Run concat node
    concat_lf.run()

    # Connect concat.outputs.confound_file --> ds_confounds.inputs.in_file
    ds_confounds_lf.inputs.in_file = concat_lf.result.outputs.confounds_file

    # Run ds_confounds node
    ds_confounds_lf.run()




