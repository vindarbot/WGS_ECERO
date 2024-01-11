import os
import subprocess

# Path to the main folder containing the assembly subfolders
main_folder = "assembly"

# Iterate through each subfolder in the main folder
for subfolder in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder)

    # Check if the subfolder contains a contigs.fasta file
    contigs_path = os.path.join(subfolder_path, "contigs.fasta")
    if os.path.isfile(contigs_path):

        # Create a subfolder for QUAST results
        quast_folder = os.path.join("quast_spades", subfolder_path.split('/')[1])
        print(quast_folder)
        os.makedirs(quast_folder, exist_ok=True)

        # Run QUAST on the contigs.fasta file
        quast_command = f"quast.py -o {quast_folder} {contigs_path}"
        subprocess.run(quast_command, shell=True)

