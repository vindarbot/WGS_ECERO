library('tidyverse')
library('ggplot2')
setwd("~/Bureau/ecoli_genomes/")
library('readr')
library('dplyr')
library('tidyr')
library("ggtree")
library('ape')

virulence_genes = read_tsv("stats/acquired_res_gene_to_assembly.tsv")

virulence_genes_tide <- virulence_genes %>% mutate(Value = 1)

important_genes <- c("iroN", "iss", "hlyF", "iutA", "ompT")
all_genes <- unique(virulence_genes_tide$Gene)

# Identify the columns associated with important genes
important_cols <- unique(virulence_genes_tide$Assembly[virulence_genes_tide$Gene %in% important_genes])

ggplot(virulence_genes_tide, aes(x = Gene, y = Assembly)) +
  geom_tile(aes(fill = Value), color = "white") +
  scale_fill_gradient(low = "white", high = "dark red", na.value = "white") +
  theme_minimal() +
  labs(title = "Virulence genes Presence/Absence Heatmap") +
  labs(x = "Genes", y = "Samples") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5)) + 
  guides(fill= "none") 

spread(virulence_genes_tide, key = Gene, value = Value)

# 11 genes : iroN, iss, hlyF, iutA, ompT. La souche est considéré comme pathogène si elle contient 4 de ces 5 gènes.


## Imoort SNP tree
# Read in the Newick file as a phylogenetic tree object
tree <- read.tree("alignment/core_alignment_20_coli_fasttree.tre")

# Plot the tree with ggtree
g <- ggtree(tree)

# add labels to the nodes
g <- g + geom_text2(aes(subset=isTip, label=label), hjust=0, size=4.5)

# add branch lengths
g <- g + geom_treescale(width=0.02, offset=0.5, fontsize=4, color='grey')
g


# Créer une inset pour un cercle de couleur
circle_inset <- inset(ggplot(), 
                      width = 0.1, 
                      height = 0.1, 
                      xmin = -Inf, 
                      xmax = Inf, 
                      ymin = -Inf, 
                      ymax = Inf, 
                      align = TRUE, 
                      hjust = 1.1, 
                      vjust = 1.1) + 
  geom_circle(aes(x = 0, y = 0, r = 0.5, fill = "red"))

# Créer une inset pour un texte
text_inset <- inset(ggplot(), 
                    width = 0.1, 
                    height = 0.1, 
                    xmin = -Inf, 
                    xmax = Inf, 
                    ymin = -Inf, 
                    ymax = Inf, 
                    align = TRUE, 
                    hjust = -0.1, 
                    vjust = 1.1) + 
  annotate("text", x = 0, y = 0, label = "Inset Text")

# Ajouter les insets à l'objet ggtree
ggtree_obj <- ggtree_obj + 
  insets(list(circle_inset, text_inset))

# Afficher le tracé avec les insets
ggtree_obj

final_plot <- virulence_genes_tide +
  inset(g, width = 0.5, height = 0.5, hjust = 0, vjust = 1)





wide_table <- virulence_genes_tide %>%
  pivot_wider(names_from = Assembly, values_from = Value, values_fill = 0)

write_tsv(wide_table, "stats/virulence_gene_to_assembly_wide_table.tsv")
