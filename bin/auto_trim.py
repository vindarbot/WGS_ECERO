#! python
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
            subprocess.call("trimmomatic PE -threads 12 -phred33 " +
                            inputdirectory + fileR1 + " " +
                            inputdirectory + fileR2 + " " +
                            output1 + "_trimmed.fastq.gz " +
                            "output_forward_unpaired.fq.gz " +
                            output2 + "_trimmed.fastq.gz " +
                            "output_reverse_unpaired.fq.gz " +
                            " SLIDINGWINDOW:4:20  2>&1", shell=True)

if __name__ == "__main__":
    inputdirectory = sys.argv[1]
    file_list = [file for file in os.listdir(inputdirectory) if "R1" in file]

    num_processes = 45  # Nombre d'échantillons à réaliser en parallèle

    with Pool(num_processes) as pool:
        pool.map(process_pair, file_list)