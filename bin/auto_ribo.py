import os
import sys
import subprocess 
from multiprocessing import Pool, cpu_count
import glob

def process_pair(file_number):
    input_directory = "fastp/"
    output_directory = "riboseed/"
    contigs_directory = "assembly_spades/"

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
    contigs_files = glob.glob(f"{contigs_directory}{file_number}*/contigs.fasta")
    trimmed_forward_reads = glob.glob(f"{input_directory}{file_number}*R1_001_trimmed.fastq.gz")
    trimmed_reverse_reads = glob.glob(f"{input_directory}{file_number}*R2_001_trimmed.fastq.gz")

    # Ensure only one file is found for each pattern
    if len(contigs_files) == 1 and len(trimmed_forward_reads) == 1 and len(trimmed_reverse_reads) == 1:
        contigs_file = contigs_files[0]
        forward_reads = trimmed_forward_reads[0]
        reverse_reads = trimmed_reverse_reads[0]

        output_directory += file_number_str

        subprocess.call(f"ribo run -r {contigs_file} -c riboseed/config.file -F {forward_reads} -R {reverse_reads} -o {output_directory} -v 1", shell=True)
    else:
        print(f"Error: Multiple or no files found for file number {file_number}")

if __name__ == "__main__":
    # Assuming file numbers range from 96 to 140
    file_numbers = range(96, 141)

    # Adjust the number of processes based on your system's capabilities
    num_processes = 45  # You can change this number as needed
    total_threads = cpu_count()

    # Distribute threads evenly among processes
    threads_per_process = total_threads // num_processes
    print(file_numbers)
    with Pool(num_processes) as pool:
        pool.map(process_pair, file_numbers, chunksize=threads_per_process)