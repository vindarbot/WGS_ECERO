import sys
import os
# Specify the path to the directory containing blast result files
directory_path = 'results/blast_results/'

# Output file path
output_file_path = 'results/blast_results/filtered_genes_output.txt'



# Open the output file for writing
with open(output_file_path, 'w') as output_file:

    # Iterate through each file in the specified directory
    for file_name in os.listdir(directory_path):

        # Build the full path to the current file
        file_path = os.path.join(directory_path, file_name)

        # Open the blast output file for reading
        with open(file_path, 'r') as file:
            # Dictionary to keep track of seen genes
            seen_genes = {}
            if file_path.split('/')[-1].startswith("GCA"):
                assembly_name = file_path.split("/")[-1].replace("_assembly_genomic.fna_blastn_results.tsv", "")
            else:
                assembly_name = file_path.split("/")[-1].split('-')[0].replace("_assembly_genomic.fna_blastn_results.tsv", "")
            # Iterate through each line in the file
            for line in file:

                # Split the line into fields
                fields = line.split()

                # Check if the p-value is less than 0.05
                if float(fields[10]) < 0.05:

                    # Check if the gene has been seen before
                    if fields[1] not in seen_genes:

                        # Add the gene to the dictionary and write to the output file
                        seen_genes[fields[1]] = assembly_name
                        output_file.write(f"{fields[1]}\t{assembly_name}\n")