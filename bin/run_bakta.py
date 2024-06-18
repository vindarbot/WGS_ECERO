import os
import sys
import subprocess
import argparse
import shutil
from multiprocessing import Pool, cpu_count

def process_contigs(sample_info):
    strain_identity = sample_info
    input_file = f"{strain_identity}_contigs.fasta"
    input_path = os.path.join(args.input_dir, input_file)
    output = f"{strain_identity}"

    
    output_basename = strain_identity.replace('-','')
    output_dir = os.path.join(args.output_dir, output_basename)
        
    if os.path.isfile(input_path):
        os.makedirs(output_dir , exist_ok=True)

        # Add strain and locus-tag options
        bakta_command = [
            "bakta",
            "--db", "/save/user/vdarbot/bakta/db-light/",
            "--output", output_dir,
            "--prefix", output_basename,  # Include standardized strain identity in prefix
            "--strain", output_basename,  # Add standardized strain identity
            "--locus-tag", f"EC{output_basename}",  # Add standardized locus tag
            "--genus", "Enterococcus",
            "--species", "cecorum",
            input_path,
            "--force",
            "--skip-plot",
            "--skip-cds",
            "--skip-sorf"
        ]
        subprocess.call(bakta_command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input_dir', required=True, type=str, help='Path to the input directory')
    parser.add_argument('-o', '--output_dir', default="", type=str, help='Path to the output directory')
    parser.add_argument('--num_threads', type=int, default=1, help='Number of processes to use')

    args = parser.parse_args()

    args.output_dir = args.output_dir + "/"

    # Get list of sample names and strain identities from input directory
    sample_names_and_strains = [filename.split("_contigs.fasta")[0]  for filename in os.listdir(args.input_dir) if filename.endswith("_contigs.fasta")]

    total_threads = cpu_count()

    # Ensure we don't use more processes than threads
    num_processes = min(args.num_threads, total_threads)

    # Distribute threads evenly among processes
    threads_per_process = total_threads // num_processes

    with Pool(num_processes) as pool:
        pool.map(process_contigs, sample_names_and_strains, chunksize=threads_per_process)
