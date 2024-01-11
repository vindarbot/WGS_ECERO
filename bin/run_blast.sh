#!/bin/bash
#SBATCH -p workq
#SBATCH --mem=64G
#SBATCH -J blastn
#SBATCH --array=1-30

# Get the filename for this instance of the job array
fi=$(ls prokka/*fna | sed -n ${SLURM_ARRAY_TASK_ID}p)

# Run Prokka for this file
basename=$(echo $fi | cut -f2 -d"/" | cut -f1 -d".")
# blastn -query $fi -db /save/vdarbot/databases/genomicepidemiology-resfinder_db-f46d8fce2860/all.fsa -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qcovs qcovhsp" -out blast/resistence/"$basename".tsv

# mkdir virulencefinder/"$basename" 
# virulencefinder.py -i $fi -p /save/vdarbot/databases/genomicepidemiology-virulencefinder_db-0b9675612265/ -o virulencefinder/"$basename" -x 

mkdir resfinder/"$basename" 
run_resfinder.py -ifa $fi -db_res /save/vdarbot/databases/genomicepidemiology-resfinder_db-f46d8fce2860/ -t 0.90 -l 0.60 -o resfinder/"$basename" --acquired --point --species "Escherichia coli"