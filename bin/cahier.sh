# Etapes à réaliser:
# 1) read cleaning : fastp
# 2) assemblage avec riboseed pour avoir une attention particulière aux régions ribosomiques
#         les contigs de riboseed seront utilisés en trusted contigs dans spades / unicycler
#    
# 3) assemblage avec unicycler / spades (en donnant option trusted contigs avec contigs de ribo)
# 4) annotation des génomes avec Bakta (on met les options de genre et espece pour améliorer l'annotation

# 5) vérification des assemblages avec quast (référence de Laurentie NCTC12421) et checkm

# 6) Quality checking avec fastqc et multiqc

# 7) utilisation de drep afin de comparer les génomes entre eux


### ACTIVATE CONDA ENV 
conda activate wgs_ececo
conda install -c bioconda seqtk

# subsampling 2 samples for tests
 seqtk sample -s SEED data/096-2023-56-C_S1_L001_R1_001.fastq.gz 10000 > test/01_subsamp_R1.fastq
 seqtk sample -s SEED data/096-2023-56-C_S1_L001_R2_001.fastq.gz 10000 > test/01_subsamp_R2.fastq
 seqtk sample -s SEED data/097-2022-56-C_S2_L001_R2_001.fastq.gz 10000 > test/02_subsamp_R2.fastq
 seqtk sample -s SEED data/097-2022-56-C_S2_L001_R1_001.fastq.gz 10000 > test/02_subsamp_R1.fastq

 gzip test/*


module load bioinfo/SPAdes/3.15.5
python3 bin/auto_spades.py results/trim/



### Running riboseed before spades 
conda create pob skesa seqtk mash

module load bioinfo/Seqtk/1.3
module load bioinfo/Mash/2.3
python3 -m pip install plentyofbugs
module load containers/singularity/3.9.9

# Change the names of bakta gff files to be compatible with roray:
find results/bakta/ -type f -name "contigs.gff3" -exec bash -c 'mv "$0" "${0%/*}/$(basename "${0%/*}").gff3"' {} \;


# roary 
sbatch --mem=128g --wrap="roary -e --mafft -p 128 results/prokka/*gff -f roary_with_publicgenomes_output/"


# blast genes to search
makeblastdb -in data/genes_to_search/genes_to_search.fasta -dbtype nucl -out data/genes_to_search/genes_to_search

A FAIRE:
HEATMAP avec GENES DE RESISTANCES DONT ECHANTILLONS OU YA RIEN , (45 + GENOMES PUBLICS + 2 POOLES)

ROARY : ARBRE PHYLO SUR l'ENSEMBLE POUR VOIR OU SE SITUENT LES 45 SOUCHES 

ASSEMBLAGES: FAIRE MARCHE RIBOSEED POUR VOIR SI CA AMELIORE LASSEMBLAGE