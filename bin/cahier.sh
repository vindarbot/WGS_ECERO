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


