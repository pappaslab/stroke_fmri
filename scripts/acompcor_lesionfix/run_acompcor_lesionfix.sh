for sub_id in `cat /mnt/data/raw/ds-patient_subset-FD03_QC-pass_version-20190401_participants.txt`; do
    python /mnt/code/acompcor_lesionfix/acompcor_lesionfix_workflow.py $sub_id /mnt/data/derivatives
done
