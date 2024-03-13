# WGS_ECERO

# REQUIREMENTS

 - Les lectures brutes doivent se situer dans un répertoire avec être sous la forme  SAMPLE_NAME_R1.fastq.gz et SAMPLE_NAME_R2.fastq.gz

 - Pour le rapport multiQC, il est préférable d'avoir l'ensemble des résultats dans un même dossier. Pour chaque analyse, créer donc un sous-dossier dans ce dossier de résultats
 Exemple: results/trim results/assemblies etc

# ETAPES

mkdir results/



## FASTQC

 - Contrôle qualité des lectures : possibilité de lancer fastQC sur les données brutes pour voir les graphiques de qualité des lectures (on est sensé observer une courbe qui décroit en fin de lectures, bonne qualité de lecture au dessus de 20 (score PHRED) )

Pour ça:

mkdir -p results/fastqc/raw

module load bioinfo/FastQC/0.12.1

sbatch --mem=8g --wrap="fastqc -o results/fastqc/raw test/*"

## Trimming

mkdir results/trim/

1) Fastp

module load bioinfo/fastp/0.23.2

sbatch --mem=128g  --wrap="python3 bin/auto_fastp.py -i test/ -o results/trim/ --num_threads 4"

- lancer fastQC après fastp : Normalement on enlève la décroissance en fin de lecture. Si ce n'est pas le cas, être plus stricte sur le score PHRED de fastp.

mkdir results/fastqc/trim/ 

sbatch --mem=8g --wrap="fastqc -o results/fastqc/trim results/trim/*"

## Assemblage avec Spades ou Riboseed 

2.1) Spades

mkdir results/spades/

module load bioinfo/SPAdes/3.15.5_compil

sbatch --mem=128g  --wrap="python3 bin/auto_spades.py -i results/trim/ -o results/spades/ --num_threads 4"


2.2) Riboseed + Spades

https://github.com/nickp60/riboSeed

riboSeed is an supplemental assembly refinement method to try to address the issue of multiple ribosomal regions in a genome, as these create repeats unresolvable by short read sequencing. It takes advantage of the fact that while each region is identical, the regions flanking are unique, and therefore can potentially be used to seed an assembly in such a way that rDNA regions are bridged.

mkdir results/riboseed 

Besoin d'avoir un génome de référence de l'espèce bacrérienne en question

python3 bin/auto_ribo.py -i res/trim/ -o res/riboseed/ -r data/reference/e_cecor.fasta




## Contrôle qualité et métriques des assemblages

3.1) Quast

mkdir results/spades/

python3 bin/run_quast.py -i results/spades/ -o results/quast/

Rapport QUAST: 
- Bon assemblage == on a une courbe ascendante avec plateau (graphe taille cumulative en fonction du nombre de contigs)
- Y a t'il des échantillons qui ont moins bien marché ? --> Comparaison des N50 des différents échantillons.  == assemblage moins fragmenté == meilleure qualité.


3.2) CheckM

module load devel/Miniconda/Miniconda3

module load bioinfo/CheckM/1.2.2

Checkm avec données WGS: on utilise la commande taxonomy_wf pour spécifier le genre bactérien en question.

checkm taxonomy_wf -t 32 -f res/checkm/checkm_results.txt -x fasta genus Enterococcus res/assembl/ res/checkm/

Le fichier res/checkm/checkm_results.txt donne les résultats de complétudes , contamination des génomes

## Annotations fonctionnelles

4) Prokka

conda install -c bioconda prokka

mkdir results/prokka/

sbatch --mem=128g  --wrap="python3 bin/run_prokka.py -i results/spades/ -o results/prokka/ --num_threads 4"


## Bakta

Pour réaliser l'annotation fonctionnelles des génomes 

conda install -c conda-forge  -c bioconda bakta

Si la base de données n'est pas téléchargé on peut la télécharger comme suit:

bakta_db download --output <output-path> --type light

Sinon, elle est accessible à : /save/user/vdarbot/bakta/db-light/

ATTENTION : Ne pas créé le dossier de sortie désiré en amont (exemple results/bakta) , car bakta le fait de lui même

sbatch --mem=128gg --wrap="python3 bin/run_bakta.py -i res/assembl/ -o res/bakta --num_threads 4"


## Comparaisons des génomes entre eux 

5) Roary (détection du core et du pan-genome: https://github.com/sanger-pathogens/Roary)

--mafft permet à la suite de l'identification des cores-genes, de réaliser l'alignement de ces cores-genes avec MAFFT

res/roary/_1710237466/gene_presence_absence.csv

conda create --name roary_env roary

conda activate roary

mkdir results/roary/

sbatch --mem=128g --wrap="roary -e --mafft -p 128 results/prokka/*gff -f results/roary/"


Le résultat d'alignement se situe dans results/roary/core_gene_alignment.aln

## Reconstruction phylogénétique à partir du core genome

6) RAXML

module load mpi/openmpi/4.1.4

module load bioinfo/RAxML-NG/1.2.0-MPI

raxml-ng-mpi --all --msa  results/roary/core_gene_alignment.aln --model GTR+G --tree results/tree/core_gene_raxml.tre --bs-trees 100

## Rapport

7) MULTIQC

Toutes les analyses doivent se situer dans un même dossier, puis indiquer ce dossier à multiqc 

module load bioinfo/MultiQC/1.19

multiqc results/

Cela génère un rapport multiqc_report.html détaillé 