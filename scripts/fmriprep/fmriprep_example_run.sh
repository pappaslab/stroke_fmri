#!/bin/bash
# Job name:
#SBATCH --job-name=patient_fmriprep_array
#
# Account:
#SBATCH --account=fc_despolab
#
# Partition:
#SBATCH --partition=savio
#
# QoS:
#SBATCH --qos=savio_normal
#
# Processors per task:
#SBATCH --cpus-per-task=18
#
# Memory:
#SBATCH --mem-per-cpu=2560M
#
#
# Wall clock limit:
#SBATCH --time=2-00:00:00
#
# Mail type:
#SBATCH --mail-type=all
#
# Mail user:
#SBATCH --mail-user=ioannis@berkeley.edu
#
## Command(s) to run (example):
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK; 

SUB_ID=$(cat /global/scratch/users/ioannis/lesion_study_2019/data/participants.txt | sed -n ${SLURM_ARRAY_TASK_ID}p);

singularity run -B /global/scratch/users/ioannis/lesion_study_2019/:/mnt /global/scratch/users/ioannis/scripts/fmriprep-1.3.2.simg \
    /mnt/data/raw/bids \
    /mnt/data/preprocessed/ participant \
    --participant-label $SUB_ID \
    --nthreads 18 \
    --omp-nthreads 6 \
    --mem_mb 25600 \
    --output-space T1w template \
    --fs-license-file /global/scratch/users/ioannis/scripts/license.txt \
    --fs-no-reconall \
    --work-dir /mnt/data/work/ ;

echo "Finished FMRIPREP run attempt for subject $SUB_ID."