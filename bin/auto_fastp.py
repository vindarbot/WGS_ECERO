import os
import sys
import subprocess 
from multiprocessing import Pool

inputdirectory = sys.argv[1]

def process_pair(fileR1):
    dividing = fileR1.split(".")
    if "R1" in fileR1:
        fileR2 = fileR1.replace('R1', 'R2')
        if os.path.isfile(inputdirectory + fileR2):
            dividing1 = fileR2.split(".")
            log1 = dividing[0]
            output1 = dividing[0]
            output2 = dividing1[0]
            subprocess.call("fastp --thread 12 --in1 " +
                            inputdirectory + fileR1 + " --in2 " +
                            inputdirectory + fileR2 + " --out1 " +
                            output1 + "_trimmed.fastq.gz --out2 " +
                            output2 + "_trimmed.fastq.gz --unpaired1 " +
                            "output_forward_unpaired.fq.gz --unpaired2 " +
                            "output_reverse_unpaired.fq.gz", shell=True)

if __name__ == "__main__":
    inputdirectory = sys.argv[1]
    file_list = [file for file in os.listdir(inputdirectory) if "R1" in file]

    # Adjust the number of processes based on your system's capabilities
    num_processes = 45  # You can change this number as needed

    with Pool(num_processes) as pool:
        pool.map(process_pair, file_list)