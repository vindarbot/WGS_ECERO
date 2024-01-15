import sys 
import os
import glob
from collections import defaultdict

gene_to_assembly = defaultdict(list)

#"resfinder or virulencefinder"
folder = "results/resfinder/"

for fold in glob.glob(folder + "*fna"):
	basename = fold.split('/')[2]
	print(basename)
	with open(fold + "/ResFinder_results_tab.txt") as cur_fi:
		for li in cur_fi:
			if li.startswith('Resistance'):
				continue

			li = li.strip().split('\t')

			gene_to_assembly[li[7]].append(basename)

print("Gene\tAssembly")

for key, values in gene_to_assembly.items():
	for value in values:
		print(key + "\t" + value)


