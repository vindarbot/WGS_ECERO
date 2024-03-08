import os
import sys
import subprocess 
from multiprocessing import Pool, cpu_count
import glob

def process_pair(file_number):
    input_directory = "fastp/"
    output_directory = "riboseed/"

    # Convert the file number to a string and add leading zeros if necessary
    file_number_str = str(file_number)

    if file_number_str == "96":
            file_number_str = "096"
    if file_number_str == "97":
            file_number_str = "097"
    if file_number_str == "98":
            file_number_str = "098"
    if file_number_str == "99":
            file_number_str = "099"

    # Use glob to find the appropriate files matching the pattern
    trimmed_forward_reads = glob.glob(f"{input_directory}{file_number}*R1_001_trimmed.fastq.gz")
    trimmed_reverse_reads = glob.glob(f"{input_directory}{file_number}*R2_001_trimmed.fastq.gz")

    # Ensure only one file is found for each pattern
    if len(trimmed_forward_reads) == 1 and len(trimmed_reverse_reads) == 1:
        forward_reads = trimmed_forward_reads[0]
        reverse_reads = trimmed_reverse_reads[0]

        output_directory += file_number_str

        subprocess.call(f"ribo run -r data/reference/e_cecor.fasta -c riboseed/config.file -F {forward_reads} -R {reverse_reads} -o {output_directory} -v 1 --cores 8 --memory 128", shell=True)
    else:
        print(f"Error: Multiple or no files found for file number {file_number}")

if __name__ == "__main__":
    # Assuming file numbers range from 96 to 140
    file_numbers = range(96, 141)

    num_processes = 45  # Nombre d'échantillons à réaliser en parallèle
    total_threads = cpu_count()

    # Distribute threads evenly among processes
    threads_per_process = total_threads // num_processes
    with Pool(num_processes) as pool:
        pool.map(process_pair, file_numbers, chunksize=threads_per_process)