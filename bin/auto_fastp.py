import os
import sys
import subprocess
import argparse
from multiprocessing import Pool

def process_pair(fileR1):
    dividing = fileR1.split(".")
    if "R1" in fileR1:
        fileR2 = fileR1.replace('R1', 'R2')
        if os.path.isfile(args.input_dir + fileR2):
            dividing1 = fileR2.split(".")
            log1 = dividing[0]
            output1 = args.output_dir + dividing[0]
            output2 = args.output_dir + dividing1[0]
            out_suffix = "_".join(output1.split('_')[:-1])
            subprocess.call("fastp --thread 12 --in1 " +
                            args.input_dir + fileR1 + " --in2 " +
                            args.input_dir + fileR2 + " --out1 " +
                            output1 + "_trimmed.fastq.gz --out2 " +
                            output2 + "_trimmed.fastq.gz --unpaired1 " +
                            output1 + "_unpaired.fastq.gz --unpaired2 " +
                            output2 + "_unpaired.fastq.gz --json " +
                            args.output_dir + out_suffix + "_trimmed.json --html " +
                            args.output_dir + out_suffix + "_trimmed.html  --qualified_quality_phred 33 --length_required 20", shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input_dir', required=True, type=str, help='Path to the input directory')
    parser.add_argument('-o', '--output_dir', default="", type=str, help='Path to the output directory')
    parser.add_argument('-t', '--num_threads', type=int, default=1, help='Number of processes to use')

    args = parser.parse_args()

    file_list = [file for file in os.listdir(args.input_dir) if "R1" in file]

    with Pool(args.num_threads) as pool:
        pool.map(process_pair, file_list)