# WGS_ECERO

# REQUIREMENTS

Les lectures brutes doivent se situer dans un répertoire avec être sous la forme  SAMPLE_NAME_R1.fastq.gz et SAMPLE_NAME_R2.fastq.gz

# ETAPES
mkdir -r results/trim/

1) Trimming
module load bioinfo/fastp/0.23.2
sbatch --mem=128g  --wrap="python3 bin/auto_fastp.py -i test/ -o results/trim/ --num_threads 45"

2) Assembly with SPADES or RIBOSEED

2.1) Spades
mkdir results/spades/

module load bioinfo/SPAdes/3.15.5_compil
sbatch --mem=128g  --wrap="python3 bin/auto_spades.py -i results/trim/ -o results/spades/ --num_threads 45"


2.2) Riboseed + Spades
https://github.com/nickp60/riboSeed
riboSeed is an supplemental assembly refinement method to try to address the issue of multiple ribosomal regions in a genome, as these create repeats unresolvable by short read sequencing. It takes advantage of the fact that while each region is identical, the regions flanking are unique, and therefore can potentially be used to seed an assembly in such a way that rDNA regions are bridged.

mkdir results/riboseed 

# Besoin d'avoir un génome de référence de l'espèce vacrérienne en question





# Contrôle qualité et métriques des assemblages:
3) Quast
mkdir results/spades/

python3 bin/run_quast.py -i results/spades/ -o results/quast/


# Annotations fonctionnelles
4) Prokka
conda install -c bioconda prokka

mkdir results/prokka/

sbatch --mem=128g  --wrap="python3 bin/run_prokka.py -i results/spades/ -o results/prokka/ --num_threads 45"


# Comparaisons des génomes entre eux 
5) Roary (détection du core et du pan-genome: https://github.com/sanger-pathogens/Roary)
--mafft permet à la suite de l'identification des cores-genes, de réaliser l'alignement de ces cores-genes avec MAFFT


conda create --name roary_env roary
conda activate roary

mkdir results/roary/

sbatch --mem=128g --wrap="roary -e --mafft -p 128 results/prokka/*gff -f results/roary/"


Le résultat d'alignement se situe dans output_dir/core_gene_alignment.aln


6) Reconstruction phyloégéntique à partir du core genome
module load mpi/openmpi/4.1.4
module load bioinfo/RAxML-NG/1.2.0-MPI

raxml-ng-mpi --all --msa  results/roary/core_gene_alignment.aln --model GTR+G --tree results/tree/core_gene_raxml.tre --bs-trees 100

7) MULTIQC

Toutes les analyses doivent se situer dans un même dossier, puis indiquer ce dossier à multiqc 

module load bioinfo/MultiQC/1.19

multiqc results/

Cela génère un rapport multiqc_report.html détaillé 