#!/bin/bash
#SBATCH -p workq
#SBATCH --mem=64G
#SBATCH -J bakta_parallel
#SBATCH --array=1-45

# Get the list of assembly directories
assembly_dirs=($(ls -d results/assembly_spades/*/))

# Get the index for this instance of the job array
index=${SLURM_ARRAY_TASK_ID}

# Run Bakta for the corresponding assembly directory
current_dir=${assembly_dirs[$index - 1]}
sample_name=$(basename $current_dir)

bakta --db /usr/local/bioinfo/src/Bakta/bakta-v1.8.2/db/db/ \
      --output results/bakta/${sample_name} \
      --genus Enterococcus \
      --species cecorum \
      ${current_dir}contigs.fasta --force --skip-plot