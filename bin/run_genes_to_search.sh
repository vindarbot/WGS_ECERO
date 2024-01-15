#!/bin/bash
#SBATCH --job-name=blastn_search
#SBATCH --output=blastn_search_%A_%a.out
#SBATCH --error=blastn_search_%A_%a.err
#SBATCH --array=1-163

# Load any necessary modules or activate your conda environment if needed
# Example: module load your_module

# Set the directory to store blast results
output_dir="blast_results"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Define the function to perform makeblastdb and blastn
perform_blastn() {
    local file="$1"
    local basename=$(basename "$file" .fna)
    local db_name="data/genes_to_search/genes_to_search"

    # Step 2: Run blastn
    blastn -query "$file" -db "$db_name" -out "$output_dir/${basename}_blastn_results.tsv" -outfmt 6
}

export -f perform_blastn

# Run the function for the current SLURM array task ID
file=$(ls results/prokka/*fna | sed -n "${SLURM_ARRAY_TASK_ID}p")
perform_blastn "$file"
