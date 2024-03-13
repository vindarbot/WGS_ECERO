import os
import sys
import subprocess
import argparse
import shutil
from multiprocessing import Pool, cpu_count

def process_pair(fileR1):
    dividing = fileR1.split(".")
    if "R1" in fileR1:
        fileR2 = fileR1.replace('R1', 'R2')
        if os.path.isfile(os.path.join(args.input_dir, fileR2)):
            dividing1 = fileR2.split(".")
            log1 = dividing[0]
            output = dividing[0].split('R1')[0].rstrip('_')
            output2 = dividing1[0]
            subprocess.call("spades.py -o " + args.output_dir + output + " --pe-1 1 " +
                            os.path.join(args.input_dir, fileR1) + " --pe-2 1 " +
                            os.path.join(args.input_dir, fileR2) +
                            " --pe-or 1 fr --cov-cutoff auto --isolate 2>&1", shell=True)
            

            ### Pour 
            source_path = os.path.abspath(args.output_dir + output + "/contigs.fasta")
            parent_folder = os.path.basename(os.path.dirname(source_path))

            destination_dir = os.path.join(os.path.dirname(source_path), "..")

            destination_file = os.path.join(destination_dir, parent_folder + "_" + os.path.basename(source_path))

            os.symlink(source_path, destination_file)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input_dir', required=True, type=str, help='Path to the input directory')
    parser.add_argument('-o', '--output_dir', default="", type=str, help='Path to the output directory')
    parser.add_argument('--num_threads', type=int, default=1, help='Number of processes to use')

    args = parser.parse_args()

    args.output_dir = args.output_dir + "/"
    file_list = [file for file in os.listdir(args.input_dir) if file.endswith("trimmed.fastq.gz") and "R1" in file]

    total_threads = cpu_count()


    num_processes = min(args.num_threads, total_threads)


    threads_per_process = total_threads // num_processes

    with Pool(num_processes) as pool:
        pool.map(process_pair, file_list, chunksize=threads_per_process)