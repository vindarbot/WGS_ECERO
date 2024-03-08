#!/bin/bash
#SBATCH -p workq
#SBATCH --mem=400G
#SBATCH --cpus-per-task=8
#SBATCH -J bakta_parallel
#SBATCH --array=1-45

# Get the list of assembly directories
assembly_dir="spades/"

# Get the index for this instance of the job array
index=${SLURM_ARRAY_TASK_ID}

# Extracting the sample name from the contigs file
sample_name=$(ls "${assembly_dir}" | sed -n "${index}p" | cut -d'_' -f1)

# Run Bakta for the corresponding assembly directory
bakta --db /save/user/vdarbot/bakta/db-light/ \
      --threads 8 \
      --output "bakta/spades/${sample_name}" \
      --prefix "${sample_name}_contigs" \
      --genus Enterococcus \
      --species cecorum \
      "${assembly_dir}${sample_name}_contigs.fasta" --force --skip-plot