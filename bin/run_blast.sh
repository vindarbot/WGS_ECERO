#!/bin/bash
#SBATCH -p workq
#SBATCH --mem=64G
#SBATCH -J blastn
#SBATCH --array=1-163

# Load any necessary modules or activate your conda environment if needed
# Example: module load your_module

# Define the function to process each file
process_file() {
    local file="$1"
    local basename=$(echo "$file" | rev | cut -d'/' -f1 | rev | cut -f1-2 -d".")
    
    # Adjust the command based on your needs
    run_resfinder.py -ifa "$file" -db_res /save/user/vdarbot/databases/genomicepidemiology-resfinder_db-f46d8fce2860/ -t 0.90 -l 0.60 --acquired --point --species "Enterococcus faecium" -o "results/resfinder/$basename"
}

export -f process_file

# Run the function for the current SLURM array task ID
file=$(ls results/prokka/*fna | sed -n "${SLURM_ARRAY_TASK_ID}p")
process_file "$file"