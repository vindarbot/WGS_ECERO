import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the data from the tsv file
virulence_genes = pd.read_csv("results/resfinder/global_results_45_ECECO.tsv", sep="\t")
virulence_genes = pd.read_csv("results/resfinder/global_results_public_genomes.tsv", sep="\t")

# Create a binary column indicating the presence of each gene in each assembly
virulence_genes['Value'] = 1

# List of important genes
# important_genes = ["iroN", "iss", "hlyF", "iutA", "ompT"]

# Create a binary matrix indicating the presence/absence of important genes in each assembly
heatmap_data = virulence_genes.pivot_table(index='Assembly', columns='Gene', values='Value', fill_value=0)

# Save the heatmap data to a TSV file
heatmap_data.to_csv("results/resfinder/presence_absence_resistence_genes.tsv", sep="\t")
# Create the heatmap
plt.figure(figsize=(18, 40))
sns.heatmap(heatmap_data, cmap="YlGnBu", cbar=False)
plt.title("Resistances genes Presence/Absence Heatmap")
plt.xlabel("Genes")
plt.ylabel("Samples")
plt.xticks(rotation=90)


plt.savefig("heatmap.png")

plt.show()
