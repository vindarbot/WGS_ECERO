#!/bin/bash
#SBATCH -p workq
#SBATCH --mem=64G
#SBATCH -J prokka
#SBATCH --array=1-118

# Get the filename for this instance of the job array
fi=$(ls results/assembly_spades/ncbi-genomes-2024-01-11/*fna| sed -n ${SLURM_ARRAY_TASK_ID}p)

# Run Prokka for this file
basename=$(echo $fi | cut -f4 -d"/" )
prokka $fi --outdir results/prokka/ --prefix $basename --force  

