import os
import subprocess
import argparse
from multiprocessing import Pool, cpu_count

def run_quast(contigs_files):
    quast_folder = args.output_dir
    quast_command = f"quast.py -o {quast_folder} " + contigs_files
    subprocess.call(quast_command, shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input_dir', required=True, type=str, help='Path to the input directory')
    parser.add_argument('-o', '--output_dir', required=True, type=str, help='Path to the output directory')

    args = parser.parse_args()

    contigs_files = args.input_dir + "/*contigs.fasta"

    run_quast(contigs_files)

