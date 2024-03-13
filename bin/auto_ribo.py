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
            
            output = dividing[0].split('R1')[0].rstrip('_')
            

            subprocess.call("ribo run -r {} -c {}/config.file -F {} -R {} -o {}/{} -v 1 --memory 128 --cores 8".format(args.reference_file, args.output_dir, os.path.join(args.input_dir, fileR1), os.path.join(args.input_dir, fileR2), args.output_dir, output), shell=True)


            source_path = os.path.abspath(args.output_dir + "/" + output + "/seed/final_de_novo_assembly/contigs.fasta")

            destination_dir = os.path.abspath(args.output_dir)

            destination_file = os.path.join(destination_dir, output + "_" + os.path.basename(source_path))

            os.symlink(source_path, destination_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input_dir', required=True, type=str, help='Path to the input directory')
    parser.add_argument('-o', '--output_dir', default="", type=str, help='Path to the output directory')
    parser.add_argument('-r', '--reference_file', type=str, help='Path to the output directory')
    parser.add_argument('--num_threads', type=int, default=1, help='Number of processes to use')

    args = parser.parse_args()

    args.output_dir = args.output_dir + "/"
    file_list = [file for file in os.listdir(args.input_dir) if file.endswith("trimmed.fastq.gz") and "R1" in file]

    total_threads = cpu_count()


    num_processes = min(args.num_threads, total_threads)


    threads_per_process = total_threads // num_processes

    with Pool(num_processes) as pool:
        pool.map(process_pair, file_list, chunksize=threads_per_process)