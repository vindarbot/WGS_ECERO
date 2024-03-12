import os
import sys
import subprocess
import argparse
from multiprocessing import Pool, cpu_count

def run_prokka(sample_name):
    input_file = f"{sample_name}_contigs.fasta"
    input_path = os.path.join(args.input_dir, input_file)
    output_dir = args.output_dir
    
    # Run Prokka command
    prokka_output_prefix = os.path.join(output_dir, f"{sample_name}")
    prokka_command = [
        "prokka",
        input_path,
        "--outdir", output_dir,
        "--prefix", sample_name,
        "--force"
    ]
    subprocess.call(prokka_command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input_dir', required=True, type=str, help='Path to the input directory')
    parser.add_argument('-o', '--output_dir', required=True, type=str, help='Path to the output directory')
    parser.add_argument('--num_threads', type=int, default=1, help='Number of processes to use')

    args = parser.parse_args()


    sample_names = [filename.split("_contigs.fasta")[0] for filename in os.listdir(args.input_dir) if filename.endswith("_contigs.fasta")]

    total_threads = cpu_count()


    num_processes = min(args.num_threads, total_threads)

    with Pool(num_processes) as pool:
        pool.map(run_prokka, sample_names)